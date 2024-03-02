from BaseClasses import Item
from .Locations import location_names

class SM64HackItem(Item):
    game = "SM64 Romhack" 

def star_count():
    return len(["Star" for location in location_names() if "Star" in location])

