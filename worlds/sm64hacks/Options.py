from dataclasses import dataclass
from Options import Toggle, Range, Choice, PerGameCommonOptions


class ProgressiveKeys(Toggle):
    """Makes the keys progressive items
    May make generation impossible if there's only Key 2"""
    display_name = "Make keys progressive"
    
@dataclass
class SM64HackOptions(PerGameCommonOptions):
    progressive_keys: ProgressiveKeys


