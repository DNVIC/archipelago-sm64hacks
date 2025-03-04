from BaseClasses import Item
from .Locations import location_names
from .Data import Data


class SM64HackItem(Item):
    game = "SM64 Romhack" 

def star_count(data):
    return len(["Star" for location in location_names(data) if "Star" in location])

def item_is_important(item_name, data = Data()):
    datastring = str(data.locations)
    if("Cap" in item_name):
        return datastring.count(item_name) > 1 #since each cap is also the name of a stage
    if item_name == "Progressive Key":
        return item_is_important("Key 1", data) or item_is_important("Key 2", data)
    return item_name in datastring