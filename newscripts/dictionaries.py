SIZE_DICT = {
    1: 0x4, 
    2: 0x4, 
    3: 0x4,
    4: 0x1, 
    5: 0xC, 
    6: 0x8, 
    7: 0x40, 
    8: 0x2, 
    9: 0x8, 
    10: 0x10, 
    11: 0x2,
    30: 0x4, 
    40: 0x2, 
    50: 0x8, 
    60: 0x0, 
    70: 0x4 
}

TYPE_DICT = {
    1: 'int32',
    2: 'uint32', 
    3: 'float', 
    4: 'bool', 
    5: 'Vec3', 
    6: 'Vec2', 
    7: 'Mat4',
    8: 'AString', 
    9: 'uint64',
    10: 'Vec4',
    11: 'UString', 
    30: 'PolyPtr', 
    40: 'Link', # weak referenced value, Link * 8 + 4 + Weak ref ptr. WeakRef<ExposedObject>. Pointer (Unscoped) to type -> %s
    50: 'Bitfield', # %u,%u format
    60: 'Array', 
    70: 'Structure'
}

IS_SIZE_PTR_DICT = {
    1: 0, 
    2: 0,
    3: 0,
    4: 0,
    5: 0, 
    6: 0,
    7: 0, 
    8: 0, 
    8: 1,
    10: 0,
    11: 1,
    30: 0, 
    40: 0,
    50: 0,
    60: 0,
    70: 0
}

BASE_TYPE_DICT = { # used as baseType tag for objects
    0x1: 'Object',
    0x2: 'Structure',
    0x4: 'Collection',
    0x8: 'MetaData',
    0x10: 'PolymorphicStructure'
}

OBJECT_TYPES_DICTIONARY = { # I think the values is hashed in 4 bytes
    b'\xB6\x64\xC1\x76': "ExposedCollection",

    # FOR CASE ACTOR
    b'\x51\xFC\x48\x98': 'CaseActor',
    # b'\xA7\x47\xA5\x6C': '', # unknown bool
    # b'\x91\x3E\x32\xD7': '', # uknown float 
    b'\xF9\x56\x75\x44': 'Actor',                               # The Actor to include in this case
    b'\x1E\x3E\xCB\xE2': 'SpawnedWhenOnTheNavmesh',             # Should this case actor be spawned all the time or only when he is in an area with navmesh ?
    b'\xBB\xDF\xCE\x04': 'DefaultExpression',                   # The default expression (overrides the Actor's default expression).
    b'\x9B\x08\x3D\xD5': 'CorrespondingNotebookEntry',          # The notebook entry associated with this CaseActor.
    b'\x49\x3F\x58\x03': 'NotebookConstraints',                 # The initial notebook constraints
    b'\x7D\x9D\xCB\x81': 'InitialTransform',                    # Where we will spawn this Actor if they are not already.
    b'\x53\x2D\x3C\x8D': 'InitiallySpawned',                    # If true, when a case/act containing this CaseActor is loaded the CaseActor will be spawned.
    b'\x94\xCF\xE0\x7C': 'CanBeBarged',                         # This actor can be barged into and react. NB. Reaction anims can cause actors to move.
    b'\x0A\x16\xE9\xF6': 'CanGetOutOfWay',                      # This actor can get out of way.
    b'\xA5\x5D\x83\xE8': 'CanOnlyBeArrestedInBrawling',         # This actor can only be arrested in brawling.
    b'\x8F\xE7\x9A\xC9': 'CanPlayFeatureAnimations',            # Can this actor play feature animations?
    b'\xED\x57\x7C\x6E': 'OverrideMapLabelStringID',            # Name of the actor to use on the map
    b'\x7F\xA3\xFA\x74': 'IsDieInteresting',                    # Is this actor interesting when dying
    b'\x87\xA4\x97\xC3': 'IgnoreGunIfOtherOpponentsAvailable',  # Should this actor force brawling auto-lock to be turned off when holding a gun whilst other brawlers are available?.
    b'\x37\x47\xCB\xBD': 'FailCaseIfKilled',                    # Should we fail the case if this actor is killed?
    b'\x1D\x42\x36\x8D': 'FailCaseIfLeftBehindSurrendering',    # Should we fail the case if this actor is left behing while surrendering ?
    b'\x4F\xAC\x2A\x66': 'SubmitInsteadOfDazed',                # This actor should submit instead of going dazed.  This should be used for important actors that should be interrogated or arrested.
    b'\x1D\xBE\x97\xBB': 'CanBeArrestedByPartner',              # Can this actor be arrested by the partner ?
    b'\x1D\x74\xD0\x34': 'BossCharacter',                       # This actor is a boss character and will have special handing (i.e. will not play heavy hit reactions, only flinches ).
    b'\x28\x98\xA6\x28': 'StateTargetOverrideDisabled',         # This actor will not use any state specific targetting overrides - this will default to targetting at the chest
    b'\x40\x91\x28\xE0': 'UpdateBehaviorsOnCinematicBlendOut',  # When blending out a cinematic force this actors behaviors to be updated when blending out, this can be used to ensure that an actor will be in the correct behavior when the cinematic completes.
    b'\x27\x4B\x69\x73': 'PlayFallingScreamWhenUnconscious',    # This case actor will play a falling scream when unconscious.
    b'\x8E\xC4\x72\x40': 'UseAlternateInterpolatedSmoothing',   # only for programmer
    b'\xEF\xBA\x45\x79': 'SaveHealth',                          # If true, this case actors health will be maintained by soft saves. NOTE: Only works if you enable "UseCaseActorSettings"
    b'\x30\xC9\x15\x4C': 'AllowCustomDeaths',                   # Allows the actor to use custom deaths when he dies ( NOTE: he wont always play a custom death if this is enabled ).
    b'\x0C\x2F\x87\x48': 'ForceCustomDeath',                    # Set this to a custom death to force the actor to play this custom death when he dies.Warning, be careful when using this as the death will not be validated against the environment for space
    b'\xDF\x88\xB1\x27': 'UseCaseActorSettings',                # Do you want to override the settings of the actor by these ones ?
    b'\xE0\xE7\x6A\xDD': 'CaseActorSettings',                   # Overloaded settings for the actor
    b'\x7B\xC4\xEF\x32': 'DisableGenericUtterances',            # Stop the case actor from using generic utterances.
    b'\x7D\xE6\x47\x2B': 'AllowAmbientUtterances',              # Allow the actor to say ambient lines?
    b'\xC8\xC9\x7B\xC1': 'IgnoreInterestingEvents',             # Should the case actor ignore interesting events
    b'\x98\x08\x91\x63': 'IgnoreScaryEvents',                   # Should the case actor ignore scary events
    b'\x90\x8B\x04\x83': 'Faction',                             # If set, overrides the actor's faction for the length of the case.
    b'\x69\x0D\x93\xBA': 'Profession',                          # Profession
    b'\x7D\x46\x55\x90': 'BrawlingProfile',                     # Defines the way this actor brawls, if not set the default will be used.
    b'\x01\x96\x02\x32': 'Outfit',                              # The outfit to use this actor
    b'\xCA\xDA\x4C\x49': 'NewHat',                              # The hat to use for this actor.
    b'\x11\x56\x8E\x3D': 'ShootingProfile',                     # Defines the way this actor shoots
    b'\x4E\xB5\x0A\x82': 'GunCombatProfile',                    # Defines the way this actor behaves in gunfights
    b'\xE5\x73\xE0\xD7': 'CombatProfile',                       # Defines the way this actor fights
    b'\xA1\x49\xB0\x36': 'SoundAwarenessZone',                  # A zone that limits where the actor can hear sounds from.
    b'\x2C\x16\xF9\x8A': 'FleeProfile',                         # Defines the way the actor acts when fleeing in a chase
    b'\x27\x47\x64\xC7': 'PursuerProfile',                      # Defines the way the actor acts when pursuing an actor in a chase
    b'\x9F\x55\x9E\x6B': 'DamageProfile',                       # Defines the way this actor is damaged
    b'\x16\x11\x58\x1C': 'CaseBehaviorPlan',                    # The default case behaviour plan of the actor
    # b'': 'EditorModel', AString
    b'\x6A\x8A\x69\x57': 'Role',                                # The role of this actor
    b'\x70\xA1\x82\xB4': 'ActorUtterances',                     # Overloaded utterances for the actor

    # FOR CONVERSATION TEMPLATE
    b'\xF4\xF0\x7E\x78': 'ConversationTemplate',
    b'\x0E\x41\x29\x3A': 'Characters',                          # Layout of Characters
    b'\x21\xDE\x18\xB2': 'DefaultLine',                         # Default Camera Line
    b'\x6A\x27\x5F\x6B': 'Cameras',
    b'\x8D\x4B\x13\xBC': 'NotebookAngles',
    # --- start ConversationTemplate_NotebookAngle - 0xb9cc4636
    b'\x02\x69\x2D\xAC': 'InitiatorPosition',                   # Position in the template of the initiator
    b'\x11\xCA\xD2\xC8': 'FocusPosition',                       # Position in the template of the focus
    b'\x4A\x1B\xA7\x5B': 'Mirror',                              # Does this angle work if we swap the initiator and focus?
    b'\x60\x55\x80\x6B': 'StandCameraAngles',                   # Camera angles when Notebook user is standing
    b'\x97\xEF\xEB\x74': 'SitCameraAngles',                     # Camera angles when Notebook user sitting
    # --- end
    b'\x7C\x58\x69\x42': 'SunShadows',                          # DEPRECATED Optional override of sun shadows.

    # FOR NOTEBOOK CONSTRAINTS
    b'\x49\x3F\x58\x03': 'NotebookConstraints',
    b'\xB5\x16\x84\x48': 'Constraints',                         # The specific set of constraints to use
    b'\x24\x8D\xB0\x0C': 'StandCameraOverride',                 # Override the standing camera angle
    b'\xA7\xBF\xF9\x7C': 'SitCameraOverride',                   # Override the sitting camera angle
    b'\x7C\x58\x69\x42': 'SunShadows',                          # DEPRECATED Optional override of sun shadows.
    b'\xA1\xA1\xB7\x6F': 'IncompleteNotebookSessionEvents',     # The triggers to evaluate when the player has finished a notebook session but no exit conversation fired

    # FOR FLEE PROFILE
    b'\x2C\x16\xF9\x8A': 'FleeProfile',
    b'\x0B\x8E\x0A\x7C': 'UseWeaponInChase',                    # Use a weapon in chase
    b'\x87\x07\xD9\x88': 'TimeToCheckForPursuer',               # Minimum and maximum inspection time to check for a persuer
    b'\x50\x27\x6E\x6F': 'MiniMapDisplayDuration',              # Duration to draw the actor on the mini map
    b'\xBF\x29\x45\xC2': 'MiniMapBlinkingDisplayDuration',      # Duration to draw the actor blinking on the mini map
    b'\xB1\x15\x01\xBD': 'MiniMapHidingDisplayDuration',        # Duration to draw the zone around the last position of the actor on the mini map
    b'\xD0\x4F\x58\x7C': 'OutOfSightDistanceOnFoot',            # The distance at which an actor is considered out of sight even if he is visible ( when fleeing on foot ).
    b'\x27\x37\x94\x7B': 'OutOfSightDistanceInVehicle',         # The distance at which an actor is considered out of sight even if he is visible ( when fleeing in a vehicle ).
    b'\x97\x0D\x25\x56': 'NextFleeProfile',                     # The next flee profile
    b'\x6B\xF7\x83\x62': 'FleeOnFootControls',                  # Chase controls when on foot
    b'\x9E\x01\xB0\x1E': 'FleeMiniGameSettings',                # Settings for the fleeing actor minigame (for actors with this profile set)
    b'\xAE\x9F\x3C\xB1': 'HostageMiniGameSettings',             # Settings for the hostage minigame (for actors with this profile set)

    # FOR ACTOR (GLOBAL)
    b'\xF9\x56\x75\x44': 'Actor',
    # b'\xA7\x47\xA5\x6C': '', # uknown first byte, init just "| = 1u"
    b'\x7B\x46\xB4\x9B': 'LogNameStringID',                     # Name of Actor to use in Log
    b'\x61\x1D\x0F\xBE': 'MovementSettings',                    # Movement settings for the actor
    b'\xD2\x11\xF8\xB3': 'ActorSettings',                       # Actor settings that will influence his behaviour
    b'\x8C\xBC\x1E\x59': 'AnimationGroups',                     # The animation groups to use for this actor.
    b'\x89\xF5\x55\x17': 'ActorHead',                           # Head to use for this actor.
    b'\xCA\xDA\x4C\x49': 'NewHat',                              # The hat to use for this actor.
    b'\x01\x96\x02\x32': 'Outfit',                              # The outfit to use this actor
    b'\x4F\xE4\x79\x30': 'SpecularColorSkin',                   # Specular color for skin.
    b'\x57\x8D\x15\x30': 'SpecularCoefficientSkin',             # Specular coefficient for skin.
    b'\xF3\x08\x70\xFA': 'SpecularRollOffSkin',                 # Roll off value for the skin's fresnel reflectance.
    b'\xF0\xC0\xCB\x2B': 'ObjectToAttach',                      # Attached object
    b'\x42\x0A\x47\xC7': 'Gender',                              # The gender of the actor
    b'\xBB\xDF\xCE\x04': 'DefaultExpression',                   # The default expression
    b'\x74\x1F\x2D\x0A': 'DefaultWeapon',                       # The weapon that this actor starts with by default.
    b'\x1C\x9E\xB1\xFF': 'SecondaryWeapon',                     # The actor will also start with this weapon.
    b'\x7D\x46\x55\x90': 'BrawlingProfile',                     # Defines the way this actor brawls, if not set the default will be used.
    b'\x11\x56\x8E\x3D': 'ShootingProfile',                     # Defines the way this actor shoots
    b'\x4E\xB5\x0A\x82': 'GunCombatProfile',                    # Defines the way this actor behaves in gunfights
    b'\xE5\x73\xE0\xD7': 'CombatProfile',                       # Defines the way this actor fights
    b'\x2C\x16\xF9\x8A': 'FleeProfile',                         # Defines the way the actor acts when fleeing in a chase
    b'\x27\x47\x64\xC7': 'PursuerProfile',                      # Defines the way the actor acts when pursuing an actor in a chase
    b'\x9F\x55\x9E\x6B': 'DamageProfile',                       # Defines the way this actor is damaged
    b'\x81\xC4\xA8\xE5': 'BehaviorPlan',                        # Defines the behavior plan of this actor
    b'\xD7\xDC\x38\x50': 'IsPartOfLAPD',                        # Is the actor part of the LAPD
    b'\x94\xCF\xE0\x7C': 'CanBeBarged',                         # This actor can be barged into
    b'\x0A\x16\xE9\xF6': 'CanGetOutOfWay',                      # This actor can use the get out of way move
    b'\xA5\x5D\x83\xE8': 'CanOnlyBeArrestedInBrawling',         # This actor can only be arrested in brawling
    b'\x36\xA4\x43\xFA': 'ArrestAutomation',                    # How can you arrest this actor ?
    b'\xB0\xF9\xDE\x19': 'RequiresAngryIdle',                   # This actor requires an angry idle.
    b'\xF3\xDB\x06\x31': 'UsesBrawlingIdleWhenBrawling',        # This actor requires a brawling idle to use when brawling.
    b'\x27\x4B\x69\x73': 'PlayFallingScreamWhenUnconscious',    # This actor will play a falling scream when unconscious
    b'\x69\x0D\x93\xBA': 'Profession',                          # Profession
    b'\xEE\xA3\xF6\x9F': 'HomeLocation',                        # A point inside the home location of the actor
    b'\x90\x8B\x04\x83': 'Faction',                             # The faction that this actor is in, e.g. a particular gang or the LAPD.
    b'\xA0\x59\xE3\xF0': 'GodMode',                             # If true, this actor cannot be harmed.
    b'\x6A\x8A\x69\x57': 'Role',                                # The role of this actor.
    b'\x2A\x28\xC4\xF2': 'BrawlingSounds',                      # Link to brawling sound events
    b'\x84\xAF\x9D\xEE': 'ImpactSounds',                        # Link to impact sound events
    b'\x3E\xEA\x7D\x0C': 'TalkingCaptureSessionOverride',       # The capture session override to use for talking idles.

    # FOR VEHICLE
    b'\xAC\x44\x5D\x4B': 'CaseVehicle', 
    b'\x15\x97\xE1\x5B': 'VehicleType',       
    b'\x53\x2D\x3C\x8D': 'InitiallySpawned',
    b'\xB2\x34\x97\xE6': 'ForceSpawn',
    b'\x7D\x9D\xCB\x81': 'InitialTransform',
    b'\x9D\x6E\x8A\xC1': 'LicencePlate',
    b'\x32\x2F\xE4\xDF': 'SecondaryId',
    b'\x1C\x3E\x69\x0E': 'GenericActorType',
    b'\x57\x28\x62\xF2': 'GenericDriver',
    b'\x91\x50\x42\xFA': 'GenericActorBehaviorPlan',
    b'\x72\x81\x45\x96': 'UsePaintColors',
    b'\x23\x9F\x7A\xF5': 'PaintColors',
    b'\x84\xCD\x90\xE0': 'SwapTexture',    
    b'\xE4\x83\xA1\x7F': 'Unbreakable',
    b'\x58\x1C\xF8\x6A': 'Undriveable',
    b'\x9F\xCB\x56\xCD': 'Immobile',
    b'\x5C\x3C\xFE\x94': 'HeadlightsOn',
    b'\x1C\xDE\xF9\x7A': 'EngineOn',
    b'\xCC\xF0\xF3\xC5': 'FrontLeftDoorOpen',
    b'\x3C\x64\x19\x7A': 'FrontRightDoorOpen',
    b'\xF1\x52\x31\xA8': 'DoorOpenAngle', # in degrees
    b'\x62\x5B\x06\x3A': 'BootDestroyed',
    b'\x9B\xE3\xD6\xFA': 'BootOpen',
    b'\x8C\x30\x04\xF4': 'CanOpenBoot',
    b'\x46\x02\xC1\x28': 'SmokeOnlyWhenCrashed',
    b'\x84\x1A\x59\x8B': 'BurningPersists',
    b'\x4E\xF7\x8E\xB6': 'PhysicsLodHighOnCreation',
    b'\x69\xB3\xD0\x55': 'CanKillPeds',
    b'\xC5\xBC\x19\x5D': 'Deformable',
    b'\x05\xA2\x36\x58': 'AllowPlayerCoverInAllLods',
    b'\x20\x87\x4A\x90': 'ExtraDamagingFactor',
    b'\x88\x41\x9C\x07': 'SoundAmplification',
    b'\xE4\xD5\x6C\xCE': 'RadioEnabled',
    b'\xB9\xA8\xC5\xA5': 'OnSpawnedAction',
    b'\x61\x73\x8E\xB1': 'OnSpawnedEvents',
    b'\x84\x68\x56\x6D': 'HardPoints',
    b'\xBA\x2F\x8B\xE5': 'SpectacularSettingsOverride',

    # FOR CASE CLUE
    b'\xFF\xCA\x2D\xCD': 'CaseClue',
    # b'\xB6\x64\xC1\x76': 'NotClue',
    b'\x8E\x5A\x6F\x1F': 'PropType',            # The prop type of this clue.
    b'\x04\x5F\x20\x14': 'ClueNotebookEntry',   # The clue notebook entry that refers to this clue.
    b'\x6F\x49\x6A\xD9': 'InventoryParams',     # Exposes options relating to how this case clue is treated by the inventory system.
    b'\xD7\x52\x89\x9E': 'RedHerring',          # Is this clue a Red Herring?  (affects Trophy unlocking)

    # FOR STRING TABLE
    b'\x3E\x80\x67\x1C': 'StringTable', 
    b'\xF5\x6A\x9A\xB4': 'Strings',             # Strings to be localized
    b'\xEE\x2C\x93\xE5': 'StringID',            # Globally unique StringID for referencing this string
    b'\x00\x02\x83\x2C': 'English',             # Languages... without Unicode
    b'\x5E\xCE\x75\xAF': 'French',
    b'\xA1\x40\x34\xA2': 'German',
    b'\xCF\x69\xB9\x57': 'Italian',
    b'\x6E\x41\x97\x0A': 'Japanese',
    b'\x75\xF1\x66\xEB': 'Russian',
    b'\x34\xF5\x18\x34': 'Spanish', 
    # TODO: also ImportCRC-languages 

    # PROPS
    b'\xAD\x81\xB2\x77': 'Transform',
    # conversation base
}
