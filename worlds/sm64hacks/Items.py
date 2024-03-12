from BaseClasses import Item
from .Locations import location_names

class SM64HackItem(Item):
    game = "SM64 Romhack" 

def star_count(data):
    return len(["Star" for location in location_names(data) if "Star" in location])

