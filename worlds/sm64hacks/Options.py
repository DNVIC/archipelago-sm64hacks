from dataclasses import dataclass
from Options import Toggle, Range, Choice, FreeText, PerGameCommonOptions, DeathLink, OptionSet, OptionGroup, Visibility, StartInventoryPool

class JsonFile(FreeText):
    """Name of the json file which the hack information.
    Must be placed in sm64hack_jsons folder upon world generation, if using a custom json file"""
    display_name = "Json File"
    default = "superMario64.json"

class ProgressiveKeys(Choice):
    """Makes the keys progressive items

    Off - Keys are not progressive items

    On - Keys are progressive items, you get Key 1 first and then Key 2
    May make generation impossible if there's only Key 2
    
    Reverse - Keys are progressive items, you get Key 2 first, and then Key 1
    May make generation impossible if there's only Key 1
    
    JSON - Go with the recommended value for the hack you are playing in the JSON
    Will only work with newer JSONs"""
    display_name = "Make keys progressive"
    option_off = 0
    option_on = 1
    option_reverse = 2
    option_json = 3
    default = 3

class TrollStars(Choice):
    """Enables checks for grabbing troll stars, if the JSON supports it.
    Note: Each world has 1 check shared among all its troll stars, not one check per troll star.
    
    Off - Troll stars are not randomized
    
    On - Troll stars are randomized"""
    option_off = 0
    option_on = 1
    display_name = "Troll Stars"

class RandomizeMoat(Toggle):
    """Shuffles the moat as a check in logic. If off, the moat will instead be placed in the vanilla location."""

class FillerUsefulWeight(Range):
    """Decides what percent chance of filler items should be somewhat useful items, compared to other filler.
    
    0 - No junk can be generated as useful items
    
    100 - Maximum Weight"""

    display_name = "Filler Useful Weight"
    range_start = 0
    default = 20
    range_end = 100

class FillerJunkWeight(Range):
    """Decides what percent chance of filler items should be junk items, compared to other filler.
    
    0 - No junk can be generated as filler
    
    100 - Maximum Weight"""

    display_name = "Filler Junk Weight"
    range_start = 0
    default = 50
    range_end = 100

class FillerTrapWeight(Range):
    """Decides what percent chance of filler items should be traps, compared to other filler. 
    In asyncs, traps received while you are not playing will not be received all immediately but will activate randomly while you are playing the game
    
    0 - No traps can be generated as filler
    
    100 - Maximum Weight"""

    display_name = "Filler Trap Weight"
    range_start = 0
    default = 30
    range_end = 100

class TurnOffTraps(OptionSet):
    """Turns off specific traps from generating. Has no effect if filler_trap_weight is set to 0."""
    valid_keys = ["Green Demon Trap", "Heave-ho Trap", "Mario Choir", "Squish Trap", "Spin Trap", "Tempo Trap"]
class SignRandomization(Toggle):
    """There is 1 check per level (not per sign) for reading a sign inside it. If you are generating a solo game and it fails, the logic might be too restrictive; enabling this will ease up the logic a bit since there is usually a sign right next to the start"""

class LevelTickets(Toggle):
    """Generate level tickets for each level, excluding the overworlds and usually course 1. There is logic to account for the scenario of going through a different level to access a level."""

class MoveRandomization(Toggle):
    """Moves are now items and you will need them in order to use mario's moveset. 
    The moves randomized are 3 progressive jumps (single, double, triple), long jumps, backflips, sideflips, wallkicks, dives, ground pounding, kicking, punching, slidekicking, and riding a shell
    You will always start with a random choice of either one of the 3 jumps, long jumps, backflips, or sideflips, since otherwise you can easily run into generation issues. 
    If you put one of those in your starting items, however, you will always start with it."""

class ForceMoveRandomization(Toggle):
    """Moves will be randomized even if the hack you are playing does not have logic for it. Use at your own risk, depending on the hack and your starting jump option it can very likely lead to impossible seeds"""
    visibility = Visibility(0b0101)

class StartingJump(Choice):
    """Decides what jumps you start (or dont start) with.

    Jumps (default) - Start with a random jump (single jump, long jump, sideflip, and backflip), weighted towards single jump
    
    Single Jump - Always start with a single jump
    
    Rollout - Start with either slidekicks or dives to allow you to rollout from the start.

    Nothing - You will not start with a random jump. This may lead to significant generation issues with solo generations, especially with hacks with no levels you can enter without jumping, and if you're playing in a large multiworld, be prepared to do nothing for a long time. 
    Expect logic to be a little unintuitive without jumping.
    """
    option_jumps = 0
    option_single_jump = 1
    option_rollout = 2
    option_nothing = 3
    default = 0

class StartingTickets(Range):
    """If you have level tickets enabled, decides what percent of level tickets are given as starting items. Intended to ease up logic generation, especially in linear games"""
    range_start = 0
    default = 25
    range_end = 100
    

class LogicDifficulty(Choice):
    """Decides what the difficulty of the logic (compared to the hack itself) should be.
    
    Strict - Everything that could be considered the intended requirements will be required. This will require certain items even if its more likely that a casual would skip said items than actually use them to get the star, since the skip is either easier to find or easier to perform than the intended path.
    
    Reasonable - Every skip that a casual could reasonably find in normal gameplay is considered in logic, assuming it is not significantly more difficult than expected for the hack it is in.
    
    Obscure - Skips that may be hard to find on your own but not necessarily difficult to perform, compared to the hack's average difficulty, are considered in logic
    
    Hard - Any skips that are relatively hard to perform (and usually hard to find as a result), compared to the average difficulty of the hack, are considered in logic"""

    option_strict = 0
    option_reasonable = 1
    option_obscure = 2
    option_hard = 3
    default = 1

class LogicGlitches(OptionSet):
    """Decides what common glitches are considered in logic.
    Glitches considered: "Bomb Clips", "BLJs", "Chuckya Clips", "Bomb Walking", "Framewalks"
    Does nothing if logic is on strict (after all, using a glitch is almost certainly unintended)
    If in the rare instance a glitch is actually intended for a certain star in the hack you're playing, it will always be considered in-logic and this option won't matter."""
    valid_keys = ["Bomb Clips", "BLJs", "Chuckya Clips", "Bomb Walking", "Framewalks"]

class MajorSkips(Toggle):
    """If this is enabled, major skips (obviously unintended skips which may unlock one or more stages) will be considered in-logic"""

class HackSpecificOptions(OptionSet):
    """Any options specific to the hack you are playing should be put here. Check the wiki page (https://wiki.dnvic.com) for the hack you are playing to see which options exist in the hack you are playing"""

class StarBundles(Range):
    """Decides what percent of stars will be converted into star bundles, worth 2 stars each. 
    
    If there are more items than locations (from move/tickets) the generator will automatically convert Stars to Star Bundles to lower the number of items, regardless of this setting, but if you want there to be more filler items/traps this option will free up item slots for junk.
    Also, if there is an odd number of stars in the hack, it will still create 1 normal star, even at 100% star bundles, so that the star count remains the same."""
    range_start = 0
    default = 0
    range_end = 100

class RingLink(Choice):
    """
    Whether your coin counter is linked to other players.

    On - Normal RingLink. You only send coins to other players and can receive any amount of coins from other players.

    Hard RingLink (Not recommended) - Same as on, but allows the client to send negative rings upon leaving a level.
    """
    display_name = "Ring Link"
    option_off = 0
    option_on = 1
    option_hard_ringlink = 2


option_groups = [
    OptionGroup("Main Options", [
        JsonFile,
        ProgressiveKeys
    ]),
    OptionGroup("Extra Randomization", [
        TrollStars,
        SignRandomization,
        RandomizeMoat,
        LevelTickets,
        MoveRandomization
    ]),
    OptionGroup("Item Settings", [
        StartingJump,
        StartingTickets,
        StarBundles,
        FillerUsefulWeight,
        FillerJunkWeight,
        FillerTrapWeight,
        TurnOffTraps
    ]),
    OptionGroup("Logic Options", [
        LogicDifficulty,
        LogicGlitches,
        MajorSkips,
        HackSpecificOptions,
        ForceMoveRandomization
    ]),
    OptionGroup("Misc Options", [
        DeathLink,
        RingLink
    ])
]
@dataclass
class SM64HackOptions(PerGameCommonOptions):
    json_file: JsonFile
    progressive_keys: ProgressiveKeys
    troll_stars: TrollStars
    sign_randomization: SignRandomization
    randomize_moat: RandomizeMoat
    level_tickets: LevelTickets
    starting_tickets: StartingTickets
    star_bundles: StarBundles
    move_randomization: MoveRandomization
    force_move_randomization: ForceMoveRandomization
    starting_jump: StartingJump
    filler_trap_weight: FillerTrapWeight
    filler_junk_weight: FillerJunkWeight
    filler_useful_weight: FillerUsefulWeight
    turn_off_traps: TurnOffTraps
    logic_difficulty: LogicDifficulty
    glitches_in_logic: LogicGlitches
    major_skips: MajorSkips
    hack_specific_options: HackSpecificOptions
    death_link: DeathLink
    start_inventory_from_pool: StartInventoryPool
    ring_link: RingLink
