from dataclasses import dataclass
from Options import Toggle, Range, Choice, FreeText, PerGameCommonOptions, DeathLink


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

class JsonFile(FreeText):
    """Name of the json file which the hack information.
    Must be placed in base folder upon world generation.
    If using a preset, ignore this."""
    display_name = "Json File"
    default = "superMario64.json"
    
@dataclass
class SM64HackOptions(PerGameCommonOptions):
    progressive_keys: ProgressiveKeys
    troll_stars: TrollStars
    json_file: JsonFile
    death_link: DeathLink

