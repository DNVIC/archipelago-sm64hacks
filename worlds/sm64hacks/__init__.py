import settings
from worlds.AutoWorld import World
from worlds.generic.Rules import add_rule
from typing import Union, Tuple, List, Dict, Set, ClassVar, Mapping, Any
from .Options import SM64HackOptions
from .Items import SM64HackItem, star_count
from .Locations import SM64HackLocation, location_names, location_names_that_exist
from .Data import sm64hack_items, Data
from BaseClasses import Region, Location, Entrance, Item, ItemClassification

#class SM64HackSettings(settings.Group):
#    pass
    #class RomFile(settings.HackRomPath):
    #    """Insert help text for host.yaml here"""
    #rom_file: RomFile = RomFile("SM64Hack.z64")



class SM64HackWorld(World):
    game = "SM64 Romhack"
    options_dataclass = SM64HackOptions
    options: SM64HackOptions
#    settings: ClassVar[SM64HackSettings]
    topology_present = True
    data: Data

    base_id = 40693


    item_name_to_id = {name: id for
                       id, name in enumerate(sm64hack_items, base_id)}

    location_name_to_id = {name: id for
                       id, name in enumerate(location_names(), base_id)}
    
    required_client_version: Tuple[int, int, int] = (0, 2, 0)

    def __init__(self,multiworld, player: int):
        super().__init__(multiworld, player)
        self.data = Data()
        
    def generate_early(self):
        self.data.import_json(self.options.json_file.value)


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
        
        for course in self.data.locations:
            if(course == "Other"):
                continue
            if(self.data.locations[course]["Cannon"]["exists"]):
                self.multiworld.itempool += [self.create_item(f"{course} Cannon")]
            for i in range(8):
                if self.data.locations[course]["Stars"][i]["exists"]:
                    self.multiworld.itempool += [self.create_item("Star")]
        if self.options.progressive_keys:
            for Key in range(2):
                if self.data.locations["Other"]["Stars"][Key]["exists"]:
                    self.multiworld.itempool += [self.create_item("Progressive Key")]
        else:
            for Key in range(2):
                if self.data.locations["Other"]["Stars"][Key]["exists"]:
                    self.multiworld.itempool += [self.create_item(sm64hack_items[Key])]
        
        for item in range(2,5):
            if self.data.locations["Other"]["Stars"][item]["exists"]:
                self.multiworld.itempool += [self.create_item(sm64hack_items[item])]
        #print("TEST" + str(len(self.multiworld.itempool)))


    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)
        existing_location_names = location_names_that_exist(self.data)
        location_names_that_exist_to_id = dict(filter(lambda location: location[0] in existing_location_names, self.location_name_to_id.items()))

        for course, data in self.data.locations.items():
            course_region = Region(course, self.player, self.multiworld)
            if course != "Other":
                
                course_region.add_locations(
                    dict(filter(lambda location: location[0].startswith(course + ' '), location_names_that_exist_to_id.items())),
                    SM64HackLocation
                )
            else:
                course_region.add_locations(
                    dict(filter(lambda location: location[0] in sm64hack_items[:5], location_names_that_exist_to_id.items())),
                    SM64HackLocation
                )
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
            if state.has("Star", self.player, int(star_requirement)):
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
        for course in self.data.locations:
            if course == "Other":
                for item in range(5):
                    if(not self.data.locations[course]["Stars"][item].get("exists")):
                        continue
                    star_requirement = self.data.locations[course]["Stars"][item].get("StarRequirement")
                    if(star_requirement):
                        add_rule(self.multiworld.get_location(sm64hack_items[item], self.player),
                        lambda state, star_requirement = int(star_requirement): state.has("Star", self.player, star_requirement))
                    other_requirements = self.data.locations[course]["Stars"][item].get("Requirements")
                    if(self.options.progressive_keys):
                        for requirement in other_requirements:
                            if(requirement.startswith("Key")):
                                add_rule(self.multiworld.get_entrance(f"{course} Connection", self.player), 
                                lambda state, requirement = requirement: state.has("Progressive Key", self.player, int(requirement[-1])))
                            else:
                                add_rule(self.multiworld.get_entrance(f"{course} Connection", self.player), 
                                lambda state, requirement = requirement: state.has(requirement, self.player))
                    else:
                        add_rule(self.multiworld.get_entrance(f"{course} Connection", self.player), 
                        lambda state, course_requirements = other_requirements: state.has_all(course_requirements, self.player))
                    star_conditional_requirements = self.data.locations[course]["Stars"][item].get("ConditionalRequirements")
                    if star_conditional_requirements:
                        add_rule(self.multiworld.get_location(sm64hack_items[item], self.player), 
                        lambda state, star_conditional_requirements = star_conditional_requirements: self.check_conditional_requirements(state, star_conditional_requirements))
                
                
                star_requirement = self.data.locations[course]["Stars"][6].get("StarRequirement")
                star_conditional_requirements = self.data.locations[course]["Stars"][6].get("ConditionalRequirements")
                other_requirements = self.data.locations[course]["Stars"][6].get("Requirements")
                if(self.options.progressive_keys and other_requirements is not None):
                    for requirement in other_requirements:
                        if(requirement.startswith("Key")):
                            add_rule(self.multiworld.get_entrance(f"{course} Connection", self.player), 
                            lambda state, requirement = requirement: state.has("Progressive Key", self.player, int(requirement[-1])))
                        else:
                            add_rule(self.multiworld.get_entrance(f"{course} Connection", self.player), 
                            lambda state, requirement = requirement: state.has(requirement, self.player))
                elif other_requirements is not None:
                    add_rule(self.multiworld.get_entrance(f"{course} Connection", self.player), 
                    lambda state, course_requirements = other_requirements: state.has_all(course_requirements, self.player))
                if star_conditional_requirements:
                    add_rule(self.multiworld.get_location("Victory Location", self.player), 
                    lambda state, star_conditional_requirements = star_conditional_requirements: self.check_conditional_requirements(state, star_conditional_requirements))
                if(star_requirement):
                    add_rule(self.multiworld.get_location("Victory Location", self.player),
                    lambda state, star_requirement = int(star_requirement): state.has("Star", self.player, star_requirement))
                continue
            course_requirements = self.data.locations[course].get("Requirements")
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
            course_conditional_requirements = self.data.locations[course].get("ConditionalRequirements")
            if course_conditional_requirements:
                add_rule(self.multiworld.get_entrance(f"{course} Connection", self.player), 
                lambda state, course_conditional_requirements = course_conditional_requirements: self.check_conditional_requirements(state, course_conditional_requirements))
            
            if(self.data.locations[course]["Cannon"].get("exists")):
                star_requirement = self.data.locations[course]["Cannon"].get("StarRequirement")
                if(star_requirement):
                    add_rule(self.multiworld.get_location(f"{course} Cannon", self.player),
                    lambda state, star_requirement = int(star_requirement): state.has("Star", self.player, star_requirement))
                other_requirements = self.data.locations[course]["Cannon"].get("Requirements")
                if(other_requirements):
                    for requirement in other_requirements:
                        if requirement == "Key 1" and self.options.progressive_keys:
                            add_rule(self.multiworld.get_location(f"{course} Cannon", self.player),
                            lambda state: state.has("Progressive Key", self.player, 1))
                        elif requirement == "Key 2" and self.options.progressive_keys :
                            add_rule(self.multiworld.get_location(f"{course} Cannon", self.player),
                            lambda state: state.has("Progressive Key", self.player, 2))
                        else:
                            add_rule(self.multiworld.get_location(f"{course} Cannon", self.player),
                            lambda state, requirement = requirement: state.has(requirement, self.player))
                star_conditional_requirements = self.data.locations[course]["Cannon"].get("ConditionalRequirements")
                if star_conditional_requirements:
                    add_rule(self.multiworld.get_location(f"{course} Cannon", self.player), 
                    lambda state, star_conditional_requirements = star_conditional_requirements: self.check_conditional_requirements(state, star_conditional_requirements))
                    
            for star in range(8):
                if(not self.data.locations[course]["Stars"][star].get("exists")):
                    continue
                star_requirement = self.data.locations[course]["Stars"][star].get("StarRequirement")
                if(star_requirement):
                    add_rule(self.multiworld.get_location(f"{course} Star {star + 1}", self.player),
                    lambda state, star_requirement = int(star_requirement): state.has("Star", self.player, star_requirement))
                other_requirements = self.data.locations[course]["Stars"][star].get("Requirements")
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
                star_conditional_requirements = self.data.locations[course]["Stars"][star].get("ConditionalRequirements")
                if star_conditional_requirements:
                    add_rule(self.multiworld.get_location(f"{course} Star {star + 1}", self.player), 
                    lambda state, star_conditional_requirements = star_conditional_requirements: self.check_conditional_requirements(state, star_conditional_requirements))
                
    
    def generate_basic(self) -> None:
        self.multiworld.get_location("Victory Location", self.player).place_locked_item(self.create_event("Victory"))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def fill_slot_data(self) -> Mapping[str, Any]:
        return {
            "Cannons": "cannons" in self.data.locations["Other"]["Settings"],
            "DeathLink": self.options.death_link.value == True # == True so it turns it into a boolean value
        }