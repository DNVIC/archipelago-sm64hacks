import settings
from worlds.AutoWorld import World
from worlds.generic.Rules import add_rule
from typing import Union, Tuple, List, Dict, Set, ClassVar
from .Options import SM64HackOptions
from .Items import SM64HackItem, star_count
from .Locations import SM64HackLocation, location_names
from .Data import sm64hack_items, Data
from BaseClasses import Region, Location, Entrance, Item, ItemClassification

class SM64HackSettings(settings.Group):
    pass
    #class RomFile(settings.HackRomPath):
    #    """Insert help text for host.yaml here"""
    #rom_file: RomFile = RomFile("SM64Hack.z64")

class SM64HackWorld(World):
    game = "SM64 Romhack"
    options_dataclass = SM64HackOptions
    options: SM64HackOptions
    settings: ClassVar[SM64HackSettings]
    topology_present = True

    base_id = 40693

    Data.import_json()

    item_name_to_id = {name: id for
                       id, name in enumerate(sm64hack_items, base_id)}

    location_name_to_id = {name: id for
                       id, name in enumerate(location_names(), base_id)}

    def create_item(self, item: str) -> SM64HackItem:
        if item == "Star":
            classification = ItemClassification.progression_skip_balancing
        else:
            classification = ItemClassification.progression
        return SM64HackItem(item, classification, self.item_name_to_id[item], self.player)

    def create_event(self, event: str):
        return SM64HackItem(event, ItemClassification.progression, None, self.player)

    def create_items(self) -> None:
        # Add items to the Multiworld.
        # If there are two of the same item, the item has to be twice in the pool.
        # Which items are added to the pool may depend on player settings,
        # e.g. custom win condition like triforce hunt.
        # Having an item in the start inventory won't remove it from the pool.
        # If an item can't have duplicates it has to be excluded manually.

        # List of items to exclude, as a copy since it will be destroyed below
        #exclude = [item for item in self.multiworld.precollected_items[self.player]]

        #for item in map(self.create_item, sm64hack_items):
        #    if item in exclude:
        #        exclude.remove(item)  # this is destructive. create unique list above
        #        self.multiworld.itempool.append(self.create_item("nothing"))
        #    else:
        #        self.multiworld.itempool.append(item)
        
        #add stars
        self.multiworld.itempool += [self.create_item("Star") for _ in range(star_count())]
        if self.options.progressive_keys:
            for Key in range(2):
                if Data.locations["Other"]["Stars"][Key]["exists"]:
                    self.multiworld.itempool += [self.create_item("Progressive Key")]
        else:
            for Key in range(2):
                if Data.locations["Other"]["Stars"][Key]["exists"]:
                    self.multiworld.itempool += [self.create_item(sm64hack_items[Key])]
        
        for item in range(2,5):
            if Data.locations["Other"]["Stars"][item]["exists"]:
                self.multiworld.itempool += [self.create_item(sm64hack_items[item])]
        #print("TEST" + str(len(self.multiworld.itempool)))

        

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        for course, data in Data.locations.items():
            course_region = Region(course, self.player, self.multiworld)
            
            if course != "Other":
                course_region.add_locations(
                    dict(filter(lambda location: location[0].startswith(course + ' '), self.location_name_to_id.items())),
                    SM64HackLocation
                )
            else:
                course_region.add_locations(
                    dict(filter(lambda location: location[0] in sm64hack_items, self.location_name_to_id.items())),
                    SM64HackLocation
                )
            
            if course == "Course 15": #add Victory in bowser 3, even if it isn't in bowser 3.
                course_region.add_locations(
                    dict({"Victory Location": None}),
                    SM64HackLocation
                )
            self.multiworld.regions.append(course_region)
            star_requirement = data.get("StarRequirement")
            if(not star_requirement):
                star_requirement = 0
            menu_region.connect(
                course_region, 
                f"{course} Connection", 
                lambda state, star_requirement = int(star_requirement): state.has("Star", self.player, star_requirement)
            )
    def check_conditional_requirements(self, state, course_conditional_requirements):
        for requirement in course_conditional_requirements:
            star_requirement = requirement["StarRequirement"]
            if not star_requirement:
                star_requirement = 0
            if state.has("Star", self.player, star_requirement):
                course_requirements = requirement["Requirements"]
                if(not course_requirements):
                    return True

                if(self.options.progressive_keys):
                    flag = True
                    for requirement in course_requirements:
                        if(requirement.startswith("Key")):
                            if not state.has("Progressive Key", self.player, int(requirement[-1])):
                                flag = False
                                break
                        elif not state.has(requirement, self.player):
                            flag = False
                            break
                    if(flag):
                        return True
                        
                elif(state.has_all(course_requirements, self.player)):
                    return True

        return False
    
    def set_rules(self) -> None:
        print(len(self.multiworld.regions.location_cache[1]))
        for course in Data.locations:
            if course == "Other":
                for item in range(5):
                    star_requirement = Data.locations[course]["Stars"][item].get("StarRequirement")
                    if(star_requirement):
                        add_rule(self.multiworld.get_location(sm64hack_items[item], self.player),
                        lambda state, star_requirement = int(star_requirement): state.has("Star", self.player, star_requirement))
                continue
            course_requirements = Data.locations[course].get("Requirements")
            if course_requirements:
                if(self.options.progressive_keys):
                    for requirement in course_requirements:
                        if(requirement.startswith("Key")):
                            add_rule(self.multiworld.get_entrance(f"{course} Connection", self.player), 
                            lambda state, requirement = requirement: state.has("Progressive Key", self.player, int(requirement[-1])))
                        else:
                            add_rule(self.multiworld.get_entrance(f"{course} Connection", self.player), 
                            lambda state, requirement = requirement: state.has(requirement, self.player))
                else:
                    add_rule(self.multiworld.get_entrance(f"{course} Connection", self.player), 
                    lambda state, course_requirements = course_requirements: state.has_all(course_requirements, self.player))
            course_conditional_requirements = Data.locations[course].get("ConditionalRequirements")
            if course_conditional_requirements:
                add_rule(self.multiworld.get_entrance(f"{course} Connection", self.player), 
                lambda state, course_conditional_requirements = course_conditional_requirements: self.check_conditional_requirements(state, course_conditional_requirements))
                

            for star in range(7):
                star_requirement = Data.locations[course]["Stars"][star].get("StarRequirement")
                if(star_requirement):
                    add_rule(self.multiworld.get_location(f"{course} Star {star + 1}", self.player),
                    lambda state, star_requirement = int(star_requirement): state.has("Star", self.player, star_requirement))
                other_requirements = Data.locations[course]["Stars"][star].get("Requirements")
                if(other_requirements):
                    for requirement in other_requirements:
                        if requirement == "Key 1" and self.options.progressive_keys:
                            add_rule(self.multiworld.get_location(f"{course} Star {star + 1}", self.player),
                            lambda state: state.has("Progressive Key", self.player, 1))
                        elif requirement == "Key 2" and self.options.progressive_keys :
                            add_rule(self.multiworld.get_location(f"{course} Star {star + 1}", self.player),
                            lambda state: state.has("Progressive Key", self.player, 2))
                        else:
                            add_rule(self.multiworld.get_location(f"{course} Star {star + 1}", self.player),
                            lambda state, requirement = requirement: state.has(requirement, self.player))
                star_conditional_requirements = Data.locations[course]["Stars"][star].get("ConditionalRequirements")
                if star_conditional_requirements:
                    add_rule(self.multiworld.get_entrance(f"{course} Connection", self.player), 
                    lambda state, star_conditional_requirements = star_conditional_requirements: self.check_conditional_requirements(state, star_conditional_requirements))
                
    
    def generate_basic(self) -> None:
        self.multiworld.get_location("Victory Location", self.player).place_locked_item(self.create_event("Victory"))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
