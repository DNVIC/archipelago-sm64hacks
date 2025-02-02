from dataclasses import dataclass
from Options import Toggle, Range, Choice, FreeText, PerGameCommonOptions, DeathLink


class ProgressiveKeys(Toggle):
    """Makes the keys progressive items
    May make generation impossible if there's only Key 2"""
    display_name = "Make keys progressive"

class JsonFile(FreeText):
    """Name of the json file which the hack information.
    Must be placed in base folder upon world generation.
    If using a preset, ignore this."""
    display_name = "Json File"
    default = "superMario64.json"
    
@dataclass
class SM64HackOptions(PerGameCommonOptions):
    progressive_keys: ProgressiveKeys
    death_link: DeathLink
    json_file: JsonFile

