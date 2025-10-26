from BaseClasses import Location
from typing import List
from .Data import sm64hack_items, Data, badges, sr6_25_locations

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
                output.append(sm64hack_items[itemId])
                output.append(badges[itemId])
            continue
        for star in range(8): #generates locations for each possible star in each level
            output.append(f"{course} Star {star + 1}")
        output.append(f"{course} Cannon")
        output.append(f"{course} Troll Star")
    
    output.append("Black Switch") #star revenge 3.5
    output.extend(sr6_25_locations)
    output.append("Castle Moat")

    return output

def location_names_that_exist(data: Data, troll_stars: int) -> List[str]:
    output: List[str] = []
    for course, info in data.locations.items():
        
        if(course == "Other"):
            for itemId in range(5):
                if info["Stars"][itemId].get("exists"):
                    output.append(sm64hack_items[itemId])
            if "sr7" in data.locations["Other"]["Settings"]:
                for itemId in range(5):
                    if(info["Stars"][itemId + 7].get("exists")):
                        output.append(badges[itemId])
            continue
        for star in range(8): #generates locations for each possible star in each level
            try:
                if info["Stars"][star].get("exists"):
                    #print(f"{course} Star {star + 1}")
                    output.append(f"{course} Star {star + 1}")
            except IndexError:
                data.locations[course]["Stars"].append({"exists": False}) #so i dont need to do this try except block later
        if(info["Cannon"].get("exists")):
            output.append(f"{course} Cannon")
        if info.get("Troll Star") is None:
            info["Troll Star"] = {"exists": False}
        if(info["Troll Star"].get("exists") and troll_stars > 0):
            output.append(f"{course} Troll Star")
        
    if "sr3.5" in data.locations["Other"]["Settings"]:
        output.append("Black Switch")
    elif "sr6.25" in data.locations["Other"]["Settings"]:
        output.extend(sr6_25_locations)
    elif data.locations["Other"]["Stars"][5].get("exists"):
        output.append("Castle Moat") #at the end for now to avoid client troubles
    

    return output