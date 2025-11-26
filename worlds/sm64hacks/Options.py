from dataclasses import dataclass
from Options import Toggle, Range, Choice, FreeText, PerGameCommonOptions, DeathLink

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
    """Enables checks for grabbing troll stars, if the JSON supports it. But beware! Every new check created by troll stars adds one trap to the pool!
    In asyncs, traps received while you are not playing will not be received all immediately but will activate randomly while you are playing the game
    Note: Each world has 1 check shared among all its troll stars, not one check per troll star.
    
    Off - Troll stars are not randomized
    
    On - Troll stars are randomized and traps are added to the pool
    
    On (no traps) - Troll stars are randomized and traps are not added into the pool. Instead singular coins will be added"""
    option_off = 0
    option_on = 1
    option_on_no_traps = 2
    display_name = "Troll Stars"

class RandomizeMoat(Toggle):
    """Shuffles the moat as a check in logic. If off, the moat will instead be placed in the vanilla location."""

class FillerTrapPercentage(Range):
    """Decides what percent chance of filler items should be traps, compared to coins. This only matters if some items need to be created outside of the APWorld (for example, due to item_links), not for internal junk (i.e. Troll Stars)
    
    0 - All filler is coins
    
    100 - All filler is traps"""

    display_name = "Filler Trap Percentage"
    range_start = 0
    default = 30
    range_end = 100


@dataclass
class SM64HackOptions(PerGameCommonOptions):
    progressive_keys: ProgressiveKeys
    troll_stars: TrollStars
    json_file: JsonFile
    randomize_moat: RandomizeMoat
    death_link: DeathLink
    filler_trap_percentage: FillerTrapPercentage
