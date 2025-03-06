from BaseClasses import Location
from typing import List
from .Data import sm64hack_items, Data, badges

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
    

    return output

def location_names_that_exist (data = Data()) -> List[str]:
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
        

    

    return output