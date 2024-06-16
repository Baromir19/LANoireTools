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

    # SPAWN CONTROLLER
    b'\x05\xD8\xF0\x04': 'SpawnController',
    b'\x21\xAC\x82\x8E': 'SpawnImmediatly',                 # Spawn directly all the vehicles and actors.
    b'\xF8\x5C\xDA\xFC': 'DisableAfterSpawning',            # Disable the controller once it has spawned the vehicles and actors.
    b'\xBF\x07\x76\x9A': 'DespawnCreatedObjectOnDisable',   # Destroy all created objects on disable
    b'\x87\xE5\x23\x01': 'ForceDespawn',                    # Force despawning all created objects on disable
    b'\x8F\xE9\xC1\x22': 'CaseVehiclesToSpawn',             # The list of vehicle to spawn.
    b'\x72\x7F\x7B\xC8': 'CaseActorsToSpawn',               # The list of actors to spawn.
    b'\xBA\xC7\x29\xDE': 'PlayerPositionWrapper',           # An optional transform for the player
    b'\x68\xD9\x67\x13': 'PartnerPositionWrapper',          # An optional transform for the partner

    # VEHICLE TO SPAWN
    b'\xDC\x0D\x89\xCE': 'PositionWrapper',         # An optional updated spawn transform
    b'\xE3\x59\x2C\x68': 'TeleportIfAlreadySpawn',  # Teleport the vehicle if it was already spawned
    b'\xDD\xC5\x08\xCD': 'UpateSpawnTransform',     # Update the spawn transform of the case vehicle

    # ONEVENTTRIGGER :: TRIGGER
    b'\x15\xCD\xF3\x55': 'OnEventTrigger',
    b'\x8F\x94\xAD\xD4': 'InitiallyEnabled',    # Start enabled or not?
    b'\x87\x5A\x85\x3E': 'ExecutionCount',      # Number of times the trigger will execute (-1 for infinite)
    b'\x43\x88\xD6\xBD': 'Condition',           # The condition to evaluate
    b'\x92\x8C\xCC\x47': 'Action',              # Action which will be executed if the condition is true

    # TOGGLETRIGGER :: TRIGGER
    b'\x17\x33\x70\xC0': 'ToggleTrigger',
    b'\x16\xA4\xB2\xBE': 'ExitAction',              # Action which will be executed when the condition is not true anymore
    b'\xFB\xA6\x1C\x72': 'FireExitActionOnDisable', # Execute the exit condition if the trigger was entered when you disable the trigger

    # VEHICLE INFO SHOWROOM
    b'\xA6\x96\xF8\x47': 'VehicleShowRoomInfo', 
    b'\xF7\x2A\x0B\xBE': 'NameElement',                 # String to display vehicle name
    b'\x42\x49\x8B\xF1': 'SubNameElement',              # String to display vehicle sub-name
    b'\xE3\x90\x67\xA0': 'YearElement',                 # String to display vehicle year
    b'\xC5\x68\x8B\xAC': 'PowerElement',                # String to display vehicle power
    b'\x5D\xDE\x0F\x3F': 'TopSpeedElement',             # String to display vehicle speed
    b'\xEA\x11\xEA\xF5': 'PriceElement',                # String to display vehicle price
    b'\xC1\x73\x9B\xB7': 'CategoryElement',             # String to display vehicle category
    b'\x1E\x6B\x40\x39': 'Curtains',                    # Curtains to change tint with category
    b'\xD4\xC6\xCB\x56': 'CategoryTwoDoorStringID',     # StringID for category '2 door'
    b'\xB1\xF4\x9B\x97': 'CategoryFourDoorStringID',    # StringID for category '4 door'
    b'\x86\xC7\x7F\x06': 'CategorySportsStringID',      # StringID for category 'sports'
    b'\xBD\x81\x36\x63': 'CategoryServiceStringID',     # StringID for category 'service'
    b'\x32\xFC\x90\xEF': 'CategoryMotorbikeStringID',   # StringID for category 'motorbike'
    b'\xA0\x64\xCC\xE0': 'CategoryBonusStringID',       # StringID for category 'bonus'
    b'\xA7\xA1\x88\x09': 'CategoryPoliceStringID',      # StringID for category 'police'
    b'\x4F\x9D\x05\x8A': 'ShowTransition',              # Transition to use when showing this screen
    b'\x4F\x9A\x11\xF9': 'HideTransition',              # Transition to use when leaving this screen
    b'\x7C\x50\xA4\x97': 'ShowUnlockedTransition',      # Transition when switching to an unlocked vehicle
    b'\x60\xB4\x36\x74': 'HideUnlockedTransition',      # Transition when switching from an unlocked vehicle
    b'\x76\xF2\x31\x8D': 'ShowLockedTransition',        # Transition when switching to a locked vehicle
    b'\xA7\x38\xDD\xB6': 'HideLockedTransition',        # Transition when switching from a locked vehicle

    # AMBIENT ZONE
    b'\x1A\x31\x78\x05': 'AmbientZone', # editorui/interesting_location.dae
    b'\x84\xBB\xF9\x50': 'Enabled',             # Is this ambient zone active?
    b'\x2F\x45\x1A\x8C': 'Width',               # Width of the box.     (metres)
    b'\x0F\xE5\x4D\xF5': 'Height',              # Height of the box.    (metres)
    b'\x69\x1C\xA3\xFA': 'Depth',               # Depth of the box.     (metres)
    b'\x27\xDC\xA6\x62': 'Priority',            # Priority used to control zones when more than one overlaps.  100 = high, 50 = normal, 0 = low"
    b'\x27\x13\x8B\xED': 'VolumeLevel',         # Volume level
    b'\x1A\x03\xB6\xFE': 'MinFadeTime',         # Minimum fade time
    b'\x19\xB5\x3F\xC5': 'AmbientStream',       # Stream to play        (audio/ambience, mp3)
    b'\x14\xF5\x29\xFB': 'NightAmbientStream',  # Night stream to play  (audio/ambience, mp3)
    b'\xA1\xC8\x0F\x57': 'RainAmbientStream',   # Rain stream to play   (audio/ambience, mp3)
    b'\x90\x2B\x0C\x6E': 'ReverbName',          # Reverb name
    b'\xF3\x6C\x4D\x98': 'ReverbMinLevel',      # Room parameter value at the distance = FadeOffDistance. Fading in would be calculated between this value and Room parameter in corresponding Reverb
    
    # b'\x90\x50\x87\xF2': '', PlanarReflectionLocator / ReflectiveMaterialLocator 
    
    # HOSTAGE MINIGAME PREPZONE
    b'\xAD\xD1\xB8\xC6': 'HostageMinigamePrepZone',
    b'\xD8\x23\x34\x41': 'HostageTaker',        # The actor that will be the hostage taker in the hostage minigame situation
    b'\xDE\xCD\x9A\xB9': 'Volume',              # Start preparing for the hostage minigame when the player is in this zone.

    # ACTOR EVENTS
    b'\x42\x50\x3B\xFD': 'ActorEvents',
    b'\xAB\x33\xA6\xA8': 'OnShotToDeathEvent',                  # The triggers to evaluate when the actor is shot till death
    b'\x01\x6E\x29\xBD': 'OnDeadEvent',                         # The triggers to evaluate when the actor is dead
    b'\xAE\x2D\x64\xBD': 'OnShotEvent',                         # The triggers to evaluate when the actor is shot
    b'\x3E\x06\x1A\x59': 'OnFireEvent',                         # The triggers to evaluate when the actor is shooting
    b'\x23\x70\xB9\x62': 'OnFireAndHitEvent',                   # The triggers to evaluate when the actor has hit someone with his gun
    b'\x13\xC7\xF2\x60': 'OnStruckEvent',                       # The triggers to evaluate when the actor is strucked
    b'\x60\xCC\x03\x42': 'OnStrikeEvent',                       # The triggers to evaluate when the actor is striking
    b'\x8E\xFC\x86\x96': 'OnTackleEvent',                       # The triggers to evaluate when the actor is tackling
    b'\xCF\xA1\x34\x9D': 'OnTackledEvent',                      # The triggers to evaluate when the actor is tackled
    b'\x0F\x70\x3F\x95': 'OnPulledFromClimbableEvent',          # The triggers to evaluate when the actor is pulled from a climbable
    b'\x45\x65\xB4\x8D': 'OnKickingOnClimbableEvent',           # The triggers to evaluate when the actor kicks an actor below them on a climbable
    b'\x17\xC9\x20\x33': 'OnCarJackEvent',                      # The triggers to evaluate when the actor is car jacked
    b'\x5F\x58\x91\x3E': 'OnSurrenderEvent',                    # The triggers to evaluate when the actor is surrending
    b'\x1A\xAA\x83\xB3': 'OnFleeEvent',                         # The triggers to evaluate when the actor is fleeing
    b'\xA6\xA3\x43\x36': 'OnPanicEvent',                        # The triggers to evaluate when the actor is panicking
    b'\x4F\x34\x93\xFF': 'OnApprehendedEvent',                  # The triggers to evaluate when the actor is apprehended
    b'\x2B\x44\x00\xD0': 'OnPreApprehendedEvent',               # The triggers to evaluate when the actor is going to be apprehended
    b'\x21\xCE\xB0\x7A': 'OnGotAwayDuringChase',                # The triggers to evaluate when this actor gets away during a chase
    b'\xC8\x96\xC3\x30': 'OnFleeMinigameComplete',              # The triggers to evaluate when this actor is successfully targeted using the minigame and sequence has finished
    b'\xC1\x49\x85\x0D': 'OnFleeMinigameChaseComplete',         # The triggers to evaluate when this actor is successfully targetd using the minigame before the sequence plays. If no sequence is to play, fires at same time as OnFleeMinigameComplete
    b'\x5F\xE7\xCB\x38': 'OnStartBrawlingEvent',                # The triggers to evaluate when the actor is entering brawling
    b'\xE7\x13\x09\x87': 'OnEnterBrawlLockEvent',               # The triggers to evaluate when the actor is entering brawling lock on.
    b'\x4A\xCB\xA8\xC1': 'OnStartFinisherEvent',                # The triggers to evaluate when the actor is starts a finishing move.
    b'\x7F\x9A\x5C\x58': 'OnEndBrawlingEvent',                  # The triggers to evaluate when the actor exits brawling.
    b'\x32\xD4\x5F\xE5': 'OnSwayingEvent',                      # The triggers to evaluate when the actor is swaying.
    b'\x94\xDB\x7E\x3A': 'OnGrapplingEvent',                    # The triggers to evaluate when the actor is grappled.
    b'\x27\xC3\xB2\x0F': 'OnWeaponGrappledEvent',               # The triggers to evaluate when the actor is grappled.
    b'\xF2\x33\x7F\xAF': 'OnKnockedDownEvent',                  # The triggers to evaluate when the actor is knocked down
    b'\x7B\x97\x98\x57': 'OnKnockedOutEvent',                   # The triggers to evaluate when the actor is knocked out
    b'\x9B\xB3\x5D\xDD': 'OnKnockedOutFinisher',                # The triggers to evaluate when the actor is knocked out due to a finisher
    b'\xD1\x62\x36\x32': 'OnKnockedOutNonFinisher',             # The triggers to evaluate when the actor is knocked out from a non finisher
    b'\x5B\xEF\xA4\x1E': 'OnBlockedEvent',                      # The triggers to evaluate when the actor is knocked out
    b'\x9A\xB6\x13\x37': 'OnEnterIncognitoEvent',               # The triggers to evaluate when the actor enters incognito mode. NOTE: this will only affect the player as he is the only one who can enter incognito
    b'\xF4\xB3\x79\x74': 'OnExitIncognitoEvent',                # The triggers to evaluate when the actor exits incognito events. NOTE: this will only affect the player as he is the only one who can enter incognito
    b'\x07\xE3\x1B\x35': 'OnStartAmbushEvent',                  # The triggers to evaluate when the actor starts an ambush.
    b'\x76\xD6\xAF\xC4': 'OnEndAmbushEvent',                    # The triggers to evaluate when the actor ends an ambush.
    b'\x39\xA0\xFE\xA6': 'OnStartWalkingAmbushEvent',           # The triggers to evaluate when the actor starts a walking ambush.
    b'\xAE\x32\xCB\x63': 'OnEndWalkingAmbushEvent',             # The triggers to evaluate when the actor ends a walking ambush.
    b'\x0D\x27\x15\x62': 'OnBargedEvent',                       # The triggers to evaluate when the actor is barged.
    b'\xB8\x63\x6E\x32': 'OnGetOutOfTheWayEvent',               # The triggers to evaluate when the actor gets out of the way of someone.
    b'\x16\x55\x5C\x6B': 'OnHostageShotByHostageTakerEvent',    # The triggers to evaluate when the hostage-taker shoots a hostage in a hostage situation.
    b'\xB3\xCA\x2B\x3E': 'OnHostageShotByPlayerEvent',          # The triggers to evaluate when the player shoots a hostage in a hostage situation.
    b'\xBA\x41\x81\xDD': 'OnHostageKilledByPlayerEvent',        # The triggers to evaluate when the player kills a hostage in a hostage situation.
    b'\x02\xAD\xC1\xE6': 'OnHostageTakerShotByPlayerEvent',     # The triggers to evaluate when the player shoots a hostage-taker in a hostage situation.
    b'\x81\x01\x5A\x85': 'OnHostageTakerWoundedByPlayerEvent',  # The triggers to evaluate when the player wounds a hostage-taker in a hostage situation.
    b'\x5A\x8C\xD6\xE7': 'OnHostageTakenByHostageTakerEvent',   # The triggers to evaluate if this actor takes a hostage (this could be before the sequence as we wait for the player).
    b'\x74\x82\x0A\xF6': 'OnHostageMinigameStartedEvent',       # The triggers to evaluate when the hostage minigame begins (when the sequence is about to play).
    b'\x20\x73\xBD\x98': 'OnStruckByVehicleEvent',              # The triggers to evaluate when the actor has hit someone with his gun

    # CINEMATIC TODO:
    b'\x14\xB8\xB7\x1E': 'Cinematic',
}

FILE_EXTENSIONS_DICTIONARY = { 
    b'\x41\x54\x42\x04': 'atb',                 # attribute
    b'\x46\x45\x56\x31': 'fev',                 # unknown format, for music, version 1
    b'\x46\x53\x42\x34': 'fsb',                 # compressed music, fsbank (4)
    b'\xFF\xFB\x94\x04': 'mp3',                 # MPEG file without ID3 header
    b'\x4F\x67\x67\x53': 'ogv',                 # Theora video format
    b'\x42\x49\x4B\x69': 'bik',                 # Bink video format
    b'\x44\x47\x41\x44': 'bin',                 # unknown (dgad) format
    b'\x42\x4D\x46\x03': 'fnt',                 # bmf font format
    b'\x44\x44\x53\x20': 'dds',                 # dds image format
    b'\x74\x72\x4D\x23': 'pack',                # unknown trM# format, archive?
    b'\x74\x72\x4D\x23': 'trunk',               # also trM#
    b'\x54\x52\x4C\x41': 'ids',                 # TRLA, for always loaded textures? uknown file extension
    b'\x23\x4D\x70\x70': 'bin.dx9',             # unknown format
    b'\xC5\x3C\x00\x00': 'vfp.dx11',            # unknown format
    b'\xDE\x3C\x00\x00': 'vfp.dx9',             # unknown format
    b'\x70\x74\x4D\x23': 'packedragdoll',       # ptM# format, uses Havok serialization?
    b'\x70\x74\x4D\x23': 'packedskeleton',      # ptM# format too
    b'\x70\x74\x4D\x23': 'uber',                # ptM# format too. or with roadnavnetwork.
    b'\x43\x42\x46\x31': 'contents',            # CBF1, is this where the naming of all files is located?
    b'\x52\x4E\x4D\x23': 'roadnavdata',         # RNM#
}

CRC32_KEY = [
    0x00000000, 0x77073096, 0xEE0E612C, 0x990951BA,
    0x076DC419, 0x706AF48F, 0xE963A535, 0x9E6495A3,
    0x0EDB8832, 0x79DCB8A4, 0xE0D5E91E, 0x97D2D988,
    0x09B64C2B, 0x7EB17CBD, 0xE7B82D07, 0x90BF1D91,
    0x1DB71064, 0x6AB020F2, 0xF3B97148, 0x84BE41DE,
    0x1ADAD47D, 0x6DDDE4EB, 0xF4D4B551, 0x83D385C7,
    0x136C9856, 0x646BA8C0, 0xFD62F97A, 0x8A65C9EC,
    0x14015C4F, 0x63066CD9, 0xFA0F3D63, 0x8D080DF5,
    0x3B6E20C8, 0x4C69105E, 0xD56041E4, 0xA2677172,
    0x3C03E4D1, 0x4B04D447, 0xD20D85FD, 0xA50AB56B,
    0x35B5A8FA, 0x42B2986C, 0xDBBBC9D6, 0xACBCF940,
    0x32D86CE3, 0x45DF5C75, 0xDCD60DCF, 0xABD13D59,
    0x26D930AC, 0x51DE003A, 0xC8D75180, 0xBFD06116,
    0x21B4F4B5, 0x56B3C423, 0xCFBA9599, 0xB8BDA50F,
    0x2802B89E, 0x5F058808, 0xC60CD9B2, 0xB10BE924,
    0x2F6F7C87, 0x58684C11, 0xC1611DAB, 0xB6662D3D,
    0x76DC4190, 0x01DB7106, 0x98D220BC, 0xEFD5102A,
    0x71B18589, 0x06B6B51F, 0x9FBFE4A5, 0xE8B8D433,
    0x7807C9A2, 0x0F00F934, 0x9609A88E, 0xE10E9818,
    0x7F6A0DBB, 0x086D3D2D, 0x91646C97, 0xE6635C01,
    0x6B6B51F4, 0x1C6C6162, 0x856530D8, 0xF262004E,
    0x6C0695ED, 0x1B01A57B, 0x8208F4C1, 0xF50FC457,
    0x65B0D9C6, 0x12B7E950, 0x8BBEB8EA, 0xFCB9887C,
    0x62DD1DDF, 0x15DA2D49, 0x8CD37CF3, 0xFBD44C65,
    0x4DB26158, 0x3AB551CE, 0xA3BC0074, 0xD4BB30E2,
    0x4ADFA541, 0x3DD895D7, 0xA4D1C46D, 0xD3D6F4FB,
    0x4369E96A, 0x346ED9FC, 0xAD678846, 0xDA60B8D0,
    0x44042D73, 0x33031DE5, 0xAA0A4C5F, 0xDD0D7CC9,
    0x5005713C, 0x270241AA, 0xBE0B1010, 0xC90C2086,
    0x5768B525, 0x206F85B3, 0xB966D409, 0xCE61E49F,
    0x5EDEF90E, 0x29D9C998, 0xB0D09822, 0xC7D7A8B4,
    0x59B33D17, 0x2EB40D81, 0xB7BD5C3B, 0xC0BA6CAD,
    0xEDB88320, 0x9ABFB3B6, 0x03B6E20C, 0x74B1D29A,
    0xEAD54739, 0x9DD277AF, 0x04DB2615, 0x73DC1683,
    0xE3630B12, 0x94643B84, 0x0D6D6A3E, 0x7A6A5AA8,
    0xE40ECF0B, 0x9309FF9D, 0x0A00AE27, 0x7D079EB1,
    0xF00F9344, 0x8708A3D2, 0x1E01F268, 0x6906C2FE,
    0xF762575D, 0x806567CB, 0x196C3671, 0x6E6B06E7,
    0xFED41B76, 0x89D32BE0, 0x10DA7A5A, 0x67DD4ACC,
    0xF9B9DF6F, 0x8EBEEFF9, 0x17B7BE43, 0x60B08ED5,
    0xD6D6A3E8, 0xA1D1937E, 0x38D8C2C4, 0x4FDFF252,
    0xD1BB67F1, 0xA6BC5767, 0x3FB506DD, 0x48B2364B,
    0xD80D2BDA, 0xAF0A1B4C, 0x36034AF6, 0x41047A60,
    0xDF60EFC3, 0xA867DF55, 0x316E8EEF, 0x4669BE79,
    0xCB61B38C, 0xBC66831A, 0x256FD2A0, 0x5268E236,
    0xCC0C7795, 0xBB0B4703, 0x220216B9, 0x5505262F,
    0xC5BA3BBE, 0xB2BD0B28, 0x2BB45A92, 0x5CB36A04,
    0xC2D7FFA7, 0xB5D0CF31, 0x2CD99E8B, 0x5BDEAE1D,
    0x9B64C2B0, 0xEC63F226, 0x756AA39C, 0x026D930A,
    0x9C0906A9, 0xEB0E363F, 0x72076785, 0x05005713,
    0x95BF4A82, 0xE2B87A14, 0x7BB12BAE, 0x0CB61B38,
    0x92D28E9B, 0xE5D5BE0D, 0x7CDCEFB7, 0x0BDBDF21,
    0x86D3D2D4, 0xF1D4E242, 0x68DDB3F8, 0x1FDA836E,
    0x81BE16CD, 0xF6B9265B, 0x6FB077E1, 0x18B74777,
    0x88085AE6, 0xFF0F6A70, 0x66063BCA, 0x11010B5C,
    0x8F659EFF, 0xF862AE69, 0x616BFFD3, 0x166CCF45,
    0xA00AE278, 0xD70DD2EE, 0x4E048354, 0x3903B3C2,
    0xA7672661, 0xD06016F7, 0x4969474D, 0x3E6E77DB,
    0xAED16A4A, 0xD9D65ADC, 0x40DF0B66, 0x37D83BF0,
    0xA9BCAE53, 0xDEBB9EC5, 0x47B2CF7F, 0x30B5FFE9,
    0xBDBDF21C, 0xCABAC28A, 0x53B39330, 0x24B4A3A6,
    0xBAD03605, 0xCDD70693, 0x54DE5729, 0x23D967BF,
    0xB3667A2E, 0xC4614AB8, 0x5D681B02, 0x2A6F2B94,
    0xB40BBE37, 0xC30C8EA1, 0x5A05DF1B, 0x2D02EF8D
]