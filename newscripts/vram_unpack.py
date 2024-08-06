import struct
import os, sys
import numpy as np

from typing import List, Tuple, Dict, Optional

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3DCollection

import xml.etree.ElementTree as ET

from uber_unpack import UberPointerManager 

class Block:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

class VertexBlock(Block):
    def __init__(self, start: int, end: int, offset: int):
        super().__init__(start, end)
        self.offset = offset

class ModelParser:
    SHORT_SIZE = 2
    MAX_SHORT_POSITIVE  = 0x7FFF
    MAX_USHORT_POSITIVE = 0xFFFF

    def __init__(self, file_path: str):
        self.file_path = file_path

    def parse_buffers_blocks_offsets(self) -> Tuple[List[VertexBlock], List[Block]]:
        def find_next_ending(data: bytes, start: int) -> int:
            return data.find(b'\xFF\x7F', start)

        vertex_blocks: List[VertexBlock] = []
        index_blocks: List[Block] = []

        with open(self.file_path, 'rb') as file:
            data = file.read()

        pos = 0
        while True:
            first_ff7f = find_next_ending(data, pos)
            if first_ff7f == -1:
                break

            second_ff7f = find_next_ending(data, first_ff7f + 2)
            if second_ff7f == -1:
                break

            vertex_offset = second_ff7f - first_ff7f
            third_ff7f = second_ff7f + vertex_offset

            if data[third_ff7f:third_ff7f+2] == b'\xFF\x7F':
                vertex_block_start = first_ff7f - 6
                vertex_block = VertexBlock(vertex_block_start, 0, vertex_offset)

                current_pos = third_ff7f
                while data[current_pos:current_pos+2] == b'\xFF\x7F':
                    current_pos += vertex_offset

                vertex_block.end = current_pos - 6
                vertex_blocks.append(vertex_block)

                index_block_start = vertex_block.end
                next_ff7f = find_next_ending(data, index_block_start)

                if next_ff7f != -1:
                    index_block_end = next_ff7f - 6
                    index_blocks.append(Block(index_block_start, index_block_end))
                    pos = next_ff7f
                else:
                    index_blocks.append(Block(index_block_start, len(data)))
                    break
            else:
                pos = second_ff7f + 2

        return vertex_blocks, index_blocks

    def read_vertex_data(self, start_address: int, 
                         end_address: int, 
                         struct_size: int = 24, 
                         pos_multiplier: Tuple[float, float, float] = (1.0, 1.0, 1.0), 
                         vertex_offset: int = 0) -> List[Tuple[float, float, float]]:
        vertices: List[Tuple[float, float, float]] = []
        with open(self.file_path, 'rb') as f:
            f.seek(start_address)
            data = f.read(end_address - start_address)
        fmt = '<h'
       
        for i in range(0, len(data), struct_size):
            if i + self.SHORT_SIZE * 3 > len(data):
                break

            x = struct.unpack(fmt, data[i+vertex_offset+self.SHORT_SIZE*0:i+vertex_offset+self.SHORT_SIZE*1])[0]
            y = struct.unpack(fmt, data[i+vertex_offset+self.SHORT_SIZE*1:i+vertex_offset+self.SHORT_SIZE*2])[0]
            z = struct.unpack(fmt, data[i+vertex_offset+self.SHORT_SIZE*2:i+vertex_offset+self.SHORT_SIZE*3])[0]

            # Normalisation
            x = x / 32767.0
            y = y / 32767.0
            z = z / 32767.0

            x *= pos_multiplier[0]
            y *= pos_multiplier[1] # TO CHANGE
            z *= pos_multiplier[2]

            vertices.append((x, y, z))

        return vertices

    def read_index_buffer(self, start_address: int, end_address: int) -> List[int]:
        indices: List[int] = []
        with open(self.file_path, 'rb') as f:
            f.seek(start_address)
            data = f.read(end_address - start_address)
        fmt = '<H'
        for i in range(0, len(data), 2):
            if i + 2 > len(data):
                break
            index = struct.unpack(fmt, data[i:i+2])[0]
            indices.append(index)
        return indices

    def read_normals(self, start_address: int, end_address: int, struct_size: int = 24, normal_offset: int = 8) -> List[Tuple[float, float, float]]:
        normals: List[Tuple[float, float, float]] = []
        with open(self.file_path, 'rb') as f:
            f.seek(start_address)
            data = f.read(end_address - start_address)
        fmt = '<h'
        
        for i in range(0, len(data), struct_size):
            if i + self.SHORT_SIZE * 3 + 8 > len(data):
                break

            nx = struct.unpack(fmt, data[i+normal_offset+self.SHORT_SIZE*0:i+normal_offset+self.SHORT_SIZE*1])[0] # 8 = xyz + additional bytes
            ny = struct.unpack(fmt, data[i+normal_offset+self.SHORT_SIZE*1:i+normal_offset+self.SHORT_SIZE*2])[0]
            nz = struct.unpack(fmt, data[i+normal_offset+self.SHORT_SIZE*2:i+normal_offset+self.SHORT_SIZE*3])[0]
            
            # Normalisation
            nx = nx / 32767.0
            ny = ny / 32767.0
            nz = nz / 32767.0

            normals.append((nx, ny, nz))

        return normals

    def read_uvs(self, start_address: int, end_address: int, struct_size: int = 24, uv_offset: int = 0) -> List[Tuple[float, float]]:
        uvs: List[Tuple[float, float]] = []
        with open(self.file_path, 'rb') as f:
            f.seek(start_address)
            data = f.read(end_address - start_address)
        fmt = '<H'
        
        for i in range(0, len(data), struct_size):
            if i + struct_size > len(data):
                break

            u = struct.unpack(fmt, data[i+struct_size-4:i+struct_size-2])[0] # -4 bytes from end of structure
            v = struct.unpack(fmt, data[i+struct_size-2:i+struct_size])[0]

            '''
            print(f"uu: {u/32767.0}, uv: {v/32767.0} \
                  \nsu: {u/65535.0}, sv: {v/65535.0}\n")
            '''

            # Normalisation
            u = u / 65535.0 #32767.0 #
            v = v / 65535.0 #32767.0 #

            uvs.append((u, v))

        return uvs

class ModelPlotter:
    @staticmethod
    def plot_model(vertices: List[Tuple[int, int, int]], indices: List[int], selected_vertices: bool = False, aspect_ratio: Optional[List[Tuple[int, int]]] = None) -> None:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        vertices_np = np.array(vertices)
        xs, ys, zs = vertices_np[:, 0], vertices_np[:, 1], vertices_np[:, 2]

        if selected_vertices:
            ax.scatter(xs, ys, zs, c='r', marker='o')

        edges: List[List[Tuple[int, int, int]]] = []

        for i in range(0, len(indices), 2):
            if i + 1 < len(indices):
                start = indices[i]
                end = indices[i+1]
                if start < len(vertices) and end < len(vertices):
                    edges.append([vertices[start], vertices[end]])

        edge_collection = Line3DCollection(edges, colors='b')
        ax.add_collection3d(edge_collection)

        if aspect_ratio is None:
            max_range = np.array([xs.max()-xs.min(), ys.max()-ys.min(), zs.max()-zs.min()]).max() / 2.0
            mid_x = (xs.max()+xs.min()) * 0.5
            mid_y = (ys.max()+ys.min()) * 0.5
            mid_z = (zs.max()+zs.min()) * 0.5

            ax.set_xlim(mid_x - max_range, mid_x + max_range)
            ax.set_ylim(mid_y - max_range, mid_y + max_range)
            ax.set_zlim(mid_z - max_range, mid_z + max_range)
        else:
            ax.set_xlim(aspect_ratio[0])
            ax.set_ylim(aspect_ratio[1])
            ax.set_zlim(aspect_ratio[2])

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Object')

        plt.show()

def create_dae_file(vertices: List[Tuple[float, float, float]],
                    normals: List[Tuple[float, float, float]],
                    uvs: List[Tuple[float, float]],
                    indices: List[int],
                    output_file: str = "output.dae"):
    
    # root element
    root = ET.Element("COLLADA", xmlns="http://www.collada.org/2005/11/COLLADASchema", version="1.4.1")

    # asset section
    asset = ET.SubElement(root, "asset")
    ET.SubElement(asset, "contributor")
    ET.SubElement(asset, "created").text = "2019-08-19T00:00:00"
    ET.SubElement(asset, "modified").text = "2019-08-19T00:00:00"
    ET.SubElement(asset, "unit", name="meter", meter="1")
    ET.SubElement(asset, "up_axis").text = "Y_UP"

    library_geometries = ET.SubElement(root, "library_geometries")
    geometry = ET.SubElement(library_geometries, "geometry", id="Mesh")
    mesh = ET.SubElement(geometry, "mesh")

    # vertices
    source_positions = ET.SubElement(mesh, "source", id="Mesh-positions")
    float_array_positions = ET.SubElement(source_positions, "float_array", id="Mesh-positions-array", count=str(len(vertices) * 3))
    float_array_positions.text = " ".join(map(lambda v: f"{v[0]:.6f} {v[1]:.6f} {v[2]:.6f}", vertices))
    technique_common_positions = ET.SubElement(source_positions, "technique_common")
    accessor_positions = ET.SubElement(technique_common_positions, "accessor", source="#Mesh-positions-array", count=str(len(vertices)), stride="3")
    ET.SubElement(accessor_positions, "param", name="X", type="float")
    ET.SubElement(accessor_positions, "param", name="Y", type="float")
    ET.SubElement(accessor_positions, "param", name="Z", type="float")

    # normals
    source_normals = ET.SubElement(mesh, "source", id="Mesh-normals")
    float_array_normals = ET.SubElement(source_normals, "float_array", id="Mesh-normals-array", count=str(len(normals) * 3))
    float_array_normals.text = " ".join(map(lambda n: f"{n[0]:.6f} {n[1]:.6f} {n[2]:.6f}", normals))
    technique_common_normals = ET.SubElement(source_normals, "technique_common")
    accessor_normals = ET.SubElement(technique_common_normals, "accessor", source="#Mesh-normals-array", count=str(len(normals)), stride="3")
    ET.SubElement(accessor_normals, "param", name="X", type="float")
    ET.SubElement(accessor_normals, "param", name="Y", type="float")
    ET.SubElement(accessor_normals, "param", name="Z", type="float")

    # uv
    source_uvs = ET.SubElement(mesh, "source", id="Mesh-uv")
    float_array_uvs = ET.SubElement(source_uvs, "float_array", id="Mesh-uv-array", count=str(len(uvs) * 2))
    float_array_uvs.text = " ".join(map(lambda uv: f"{uv[0]:.6f} {uv[1]:.6f}", uvs))
    technique_common_uvs = ET.SubElement(source_uvs, "technique_common")
    accessor_uvs = ET.SubElement(technique_common_uvs, "accessor", source="#Mesh-uv-array", count=str(len(uvs)), stride="2")
    ET.SubElement(accessor_uvs, "param", name="S", type="float")
    ET.SubElement(accessor_uvs, "param", name="T", type="float")

    vertices_element = ET.SubElement(mesh, "vertices", id="Mesh-vertices")
    ET.SubElement(vertices_element, "input", semantic="POSITION", source="#Mesh-positions")

    triangles = ET.SubElement(mesh, "triangles", count=str(len(indices) // 3))
    ET.SubElement(triangles, "input", semantic="VERTEX", source="#Mesh-vertices", offset="0")
    ET.SubElement(triangles, "input", semantic="NORMAL", source="#Mesh-normals", offset="1")
    ET.SubElement(triangles, "input", semantic="TEXCOORD", source="#Mesh-uv", offset="2")
    p = ET.SubElement(triangles, "p")
    p.text = " ".join(map(str, [f"{i} {i} {i}" for i in indices]))

    library_visual_scenes = ET.SubElement(root, "library_visual_scenes")
    visual_scene = ET.SubElement(library_visual_scenes, "visual_scene", id="Scene")
    node = ET.SubElement(visual_scene, "node", id="Mesh")
    instance_geometry = ET.SubElement(node, "instance_geometry", url="#Mesh")

    # scene
    scene = ET.SubElement(root, "scene")
    instance_visual_scene = ET.SubElement(scene, "instance_visual_scene", url="#Scene")

    # to save
    tree = ET.ElementTree(root)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)

def create_full_dae_file(all_vertices: List[List[Tuple[float, float, float]]],
                    all_normals: List[List[Tuple[float, float, float]]],
                    all_uvs: List[List[Tuple[float, float]]],
                    all_indices: List[List[int]],
                    output_file: str = "output.dae"):
    
    # root element
    root = ET.Element("COLLADA", xmlns="http://www.collada.org/2005/11/COLLADASchema", version="1.4.1")

    # asset section
    asset = ET.SubElement(root, "asset")
    ET.SubElement(asset, "contributor")
    ET.SubElement(asset, "created").text = "2019-08-19T00:00:00"
    ET.SubElement(asset, "modified").text = "2019-08-19T00:00:00"
    ET.SubElement(asset, "unit", name="meter", meter="1")
    ET.SubElement(asset, "up_axis").text = "Y_UP"

    library_geometries = ET.SubElement(root, "library_geometries")

    for i, (vertices, normals, uvs, indices) in enumerate(zip(all_vertices, all_normals, all_uvs, all_indices)):
        geometry = ET.SubElement(library_geometries, "geometry", id=f"Mesh_{i}")
        mesh = ET.SubElement(geometry, "mesh")

        # vertices
        source_positions = ET.SubElement(mesh, "source", id=f"Mesh_{i}-positions")
        float_array_positions = ET.SubElement(source_positions, "float_array", id=f"Mesh_{i}-positions-array", count=str(len(vertices) * 3))
        float_array_positions.text = " ".join(map(lambda v: f"{v[0]:.6f} {v[1]:.6f} {v[2]:.6f}", vertices))
        technique_common_positions = ET.SubElement(source_positions, "technique_common")
        accessor_positions = ET.SubElement(technique_common_positions, "accessor", source=f"#Mesh_{i}-positions-array", count=str(len(vertices)), stride="3")
        ET.SubElement(accessor_positions, "param", name="X", type="float")
        ET.SubElement(accessor_positions, "param", name="Y", type="float")
        ET.SubElement(accessor_positions, "param", name="Z", type="float")

        # normals
        source_normals = ET.SubElement(mesh, "source", id=f"Mesh_{i}-normals")
        float_array_normals = ET.SubElement(source_normals, "float_array", id=f"Mesh_{i}-normals-array", count=str(len(normals) * 3))
        float_array_normals.text = " ".join(map(lambda n: f"{n[0]:.6f} {n[1]:.6f} {n[2]:.6f}", normals))
        technique_common_normals = ET.SubElement(source_normals, "technique_common")
        accessor_normals = ET.SubElement(technique_common_normals, "accessor", source=f"#Mesh_{i}-normals-array", count=str(len(normals)), stride="3")
        ET.SubElement(accessor_normals, "param", name="X", type="float")
        ET.SubElement(accessor_normals, "param", name="Y", type="float")
        ET.SubElement(accessor_normals, "param", name="Z", type="float")

        # uv
        source_uvs = ET.SubElement(mesh, "source", id=f"Mesh_{i}-uv")
        float_array_uvs = ET.SubElement(source_uvs, "float_array", id=f"Mesh_{i}-uv-array", count=str(len(uvs) * 2))
        float_array_uvs.text = " ".join(map(lambda uv: f"{uv[0]:.6f} {uv[1]:.6f}", uvs))
        technique_common_uvs = ET.SubElement(source_uvs, "technique_common")
        accessor_uvs = ET.SubElement(technique_common_uvs, "accessor", source=f"#Mesh_{i}-uv-array", count=str(len(uvs)), stride="2")
        ET.SubElement(accessor_uvs, "param", name="S", type="float")
        ET.SubElement(accessor_uvs, "param", name="T", type="float")

        vertices_element = ET.SubElement(mesh, "vertices", id=f"Mesh_{i}-vertices")
        ET.SubElement(vertices_element, "input", semantic="POSITION", source=f"#Mesh_{i}-positions")

        triangles = ET.SubElement(mesh, "triangles", count=str(len(indices) // 3))
        ET.SubElement(triangles, "input", semantic="VERTEX", source=f"#Mesh_{i}-vertices", offset="0")
        ET.SubElement(triangles, "input", semantic="NORMAL", source=f"#Mesh_{i}-normals", offset="1")
        ET.SubElement(triangles, "input", semantic="TEXCOORD", source=f"#Mesh_{i}-uv", offset="2")
        p = ET.SubElement(triangles, "p")
        p.text = " ".join(map(str, [f"{i} {i} {i}" for i in indices]))

    library_visual_scenes = ET.SubElement(root, "library_visual_scenes")
    visual_scene = ET.SubElement(library_visual_scenes, "visual_scene", id="Scene")
    for i in range(len(all_vertices)):
        node = ET.SubElement(visual_scene, "node", id=f"Mesh_{i}")
        instance_geometry = ET.SubElement(node, "instance_geometry", url=f"#Mesh_{i}")

    # scene
    scene = ET.SubElement(root, "scene")
    instance_visual_scene = ET.SubElement(scene, "instance_visual_scene", url="#Scene")

    # to save
    tree = ET.ElementTree(root)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)

def main() -> None:
    try:
        vram_file_path = sys.argv[1:][0]
        if not os.path.exists(vram_file_path):
            raise Exception('Path does not exist')
    except:
        vram_file_path = input('Path to file: ')
        if not os.path.exists(vram_file_path):
            raise Exception('Path does not exist')

    if not os.path.exists(vram_file_path):
        print(f"File not found: {vram_file_path}")
        return
    
    uber_file_path = sys.argv[2] if len(sys.argv) > 2 else None
    vram_dir = os.path.dirname(vram_file_path)
    vram_cutted_file_name = os.path.splitext(os.path.basename(vram_file_path))[0]
    vram_cutted_file_name = vram_cutted_file_name[:-4]

    if not uber_file_path or not os.path.exists(uber_file_path):
        potential_paths = [
            os.path.join(vram_dir, os.path.basename(uber_file_path)) if uber_file_path else None,
            os.path.join(vram_dir, vram_cutted_file_name + 'Main'),
            os.path.join(vram_dir, vram_cutted_file_name + 'Main.uber'),
            os.path.join(vram_dir, 'GraphicsMain'), # for exceptional case
            os.path.join(vram_dir, 'GraphicsMain.uber')
        ]
        for path in potential_paths:
            if path and os.path.exists(path):
                uber_file_path = path
                break
        else:
            raise Exception('Uber file not found')

    # variables
    directory_path = 'models'
    block_index = 0
    savename = 'null.dae'
    to_show_plot = False
    uber_unpacker = UberPointerManager(uber_file_path)
    pointers, pointers_addresses = uber_unpacker.get_pointer_by_block(1)
    multipliers = uber_unpacker.get_vertex_positions_multiplier(pointers, pointers_addresses)
    print(multipliers)

    parser = ModelParser(vram_file_path)
    vertex_blocks, index_blocks = parser.parse_buffers_blocks_offsets()

    print("Vertex blocks:")
    for i, block in enumerate(vertex_blocks):
        print(f"{i}: start={block.start}, end={block.end}, offset={block.offset}")

    print("\nIndex blocks:")
    for i, block in enumerate(index_blocks):
        print(f"{i}: start={block.start}, end={block.end}")

    block_index = int(input("\nSelect block number: "))

    path_elements = vram_file_path.split(os.sep)
    
    if len(path_elements) > 1:
        name = path_elements[-2]
    else:
        name = path_elements[-1]

    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    savename = f"{directory_path}/{name}{block_index}.dae"

    if 0 <= block_index < len(vertex_blocks):
        vertex_block = vertex_blocks[block_index]
        index_block = index_blocks[block_index]

        vertices = parser.read_vertex_data(vertex_block.start, vertex_block.end, vertex_block.offset, multipliers[block_index])
        normals = parser.read_normals(vertex_block.start, vertex_block.end, vertex_block.offset)
        uvs = parser.read_uvs(vertex_block.start, vertex_block.end, vertex_block.offset)

        indices = parser.read_index_buffer(index_block.start, index_block.end)

        create_dae_file(vertices, normals, uvs, indices, savename)

        #aspect_ratio = [(-80000, 80000), (-50000, 50000), (-35000, 35000)] # for your own model-ratio
        #ModelPlotter.plot_model(vertices, indices, True, aspect_ratio)
        if to_show_plot:
            ModelPlotter.plot_model(vertices, indices, True)

    elif block_index == -1:
        all_vertices = []
        all_normals = []
        all_uvs = []
        all_indices = []

        for block_index in range(len(vertex_blocks)):
            vertex_block = vertex_blocks[block_index]
            index_block = index_blocks[block_index]

            vertices = parser.read_vertex_data(vertex_block.start, vertex_block.end, vertex_block.offset, multipliers[block_index])
            normals = parser.read_normals(vertex_block.start, vertex_block.end, vertex_block.offset)
            uvs = parser.read_uvs(vertex_block.start, vertex_block.end, vertex_block.offset)

            indices = parser.read_index_buffer(index_block.start, index_block.end)

            all_vertices.append(vertices)
            all_normals.append(normals)
            all_uvs.append(uvs)
            all_indices.append(indices)

        create_full_dae_file(all_vertices, all_normals, all_uvs, all_indices, savename)

        '''
        max_index = 0
        all_vertices: List[Tuple[int, int, int]] = []
        all_indices: List[int] = []

        for block_index in range(len(vertex_blocks)):
            vertex_block = vertex_blocks[block_index]
            index_block = index_blocks[block_index]

            vertices = parser.read_vertex_data(vertex_block.start, vertex_block.end, vertex_block.offset)
            normals = parser.read_normals(vertex_block.start, vertex_block.end, vertex_block.offset)
            uvs = parser.read_uvs(vertex_block.start, vertex_block.end, vertex_block.offset)

            indices = parser.read_index_buffer(index_block.start, index_block.end)

            #if to_show_plot:
            indices = [index + max_index for index in indices]

            all_vertices.extend(vertices)
            all_indices.extend(indices)
            max_index += len(vertices)

        #aspect_ratio = [(-90000, 90000), (-40000, 40000), (-80000, 80000)]
        #ModelPlotter.plot_model(all_vertices, all_indices, True, aspect_ratio)
        if to_show_plot:
            ModelPlotter.plot_model(all_vertices, all_indices, True)

        '''
    else:
        print("Incorrect choice.")
        return

if __name__ == "__main__":
    main()

#print(f'vertex_blocks: {vertex_blocks}')
#print(f'index_blocks: {index_blocks}')
