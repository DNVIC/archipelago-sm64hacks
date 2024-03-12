from BaseClasses import Location
from typing import List
from .Data import sm64hack_items, Data

class SM64HackLocation(Location):
    game = "SM64 Romhack"

    # override constructor to automatically mark event locations as such
    def __init__(self, player: int, name = "", code = None, parent = None):
        super(SM64HackLocation, self).__init__(player, name, code, parent)
        self.event = code is None


def location_names(data = Data()) -> List[str]:
    output: List[str] = []
    for course, info in data.locations.items():
        
        if(course == "Other"):
            for itemId in range(5):
                if info["Stars"][itemId]["exists"]:
                    output.append(sm64hack_items[itemId])
            continue
        for star in range(7): #generates locations for each star in the level
            if info["Stars"][star]["exists"]:
                output.append(f"{course} Star {star + 1}")
    

    return output