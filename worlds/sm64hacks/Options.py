from dataclasses import dataclass
from Options import Toggle, Range, Choice, FreeText, PerGameCommonOptions


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
    json_file: JsonFile

