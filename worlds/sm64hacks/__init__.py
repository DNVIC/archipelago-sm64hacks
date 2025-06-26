import settings
from random import choice
from worlds.AutoWorld import World
from worlds.generic.Rules import add_rule
from typing import Union, Tuple, List, Dict, Set, ClassVar, Mapping, Any
from .Options import SM64HackOptions
from .Items import SM64HackItem, item_is_important
from .Locations import SM64HackLocation, location_names, location_names_that_exist
from .Data import sm64hack_items, star_like, traps, badges, sr6_25_locations, Data
from .client import SM64HackClient
from BaseClasses import Region, Location, Entrance, Item, ItemClassification, CollectionState

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
    stars_created = 0

    item_name_to_id = {name: id for
                       id, name in enumerate(sm64hack_items, base_id)}

    location_name_to_id = {name: id for
                       id, name in enumerate(location_names(), base_id)}
    
    required_client_version: Tuple[int, int, int] = (0, 4, 0)

    def __init__(self,multiworld, player: int):
        super().__init__(multiworld, player)
        self.data = Data()
        
    def generate_early(self):
        self.data.import_json(self.options.json_file.value)
        self.progressive_keys = self.options.progressive_keys
        if isinstance(self.data.locations["Other"]["Settings"], list):
            raise ValueError("JSON is too old. \
                            \nPlease reimport the JSON into the website (https://dnvic.com/ArchipelagoGenerator), \
                              and export with a new progressive key setting at the bottom, and try again")
        if self.progressive_keys == 3:
            try:
                self.progressive_keys = self.data.locations["Other"]["Settings"]["prog_key"]
            except TypeError:
                raise ValueError("JSON is too old and does not have a default for progressive keys")


    def create_item(self, item: str) -> SM64HackItem:
        if item == "Power Star":
            if self.stars_created < self.data.maxstarcount: #only create progression stars up to the max starcount for the hack
                classification = ItemClassification.progression_skip_balancing
                self.stars_created += 1
            else:
                classification = ItemClassification.useful
        elif item in traps:
            classification = ItemClassification.trap
        elif item == "Coin":
            classification = ItemClassification.filler
        elif item.endswith("Star"): # cannon stars in sr6.25
            classification = ItemClassification.progression
            self.stars_created += 1
        else:
            classification = ItemClassification.progression if item_is_important(item, self.data) else ItemClassification.useful
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
        junk = 0
        for course in self.data.locations:
            if(course == "Other"):
                continue
            if(self.data.locations[course]["Cannon"]["exists"]):
                self.multiworld.itempool += [self.create_item(f"{course} Cannon")]
            if(self.data.locations[course]["Troll Star"]["exists"]):
                junk += 1
            for i in range(8):
                if self.data.locations[course]["Stars"][i]["exists"]:
                    if "sr6.25" not in self.data.locations["Other"]["Settings"] or (i != 7 or (course != "Course 1" and course != "Bowser 3")): #cannon star nonsense
                        self.multiworld.itempool += [self.create_item("Power Star")]
        if self.progressive_keys > 0:
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
        
        if("sr7" in self.data.locations["Other"]["Settings"]):
            for item in range(5):
                if item < 2:
                    if self.data.locations["Other"]["Stars"][item + 7]["exists"]:
                        self.multiworld.itempool += [self.create_item("Progressive Stomp Badge")]
                else:
                    if self.data.locations["Other"]["Stars"][item + 7]["exists"]:
                        self.multiworld.itempool += [self.create_item(sm64hack_items[item + 32])]

        if("sr6.25" in self.data.locations["Other"]["Settings"]):
            self.multiworld.itempool += [self.create_item("Yellow Switch")]
            self.multiworld.itempool += [self.create_item("Overworld Cannon Star")]
            self.multiworld.itempool += [self.create_item("Bowser 2 Cannon Star")]
        
        if("sr3.5" in self.data.locations["Other"]["Settings"]):
            self.multiworld.itempool += [self.create_item("Black Switch")]
        #print("TEST" + str(len(self.multiworld.itempool)))

        if self.options.troll_stars == 1:
            self.multiworld.itempool += [self.create_item(choice(traps)) for _ in range(junk)]
        elif self.options.troll_stars == 2:
            self.multiworld.itempool += [self.create_item("Coin") for _ in range(junk)]



    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)
        existing_location_names = location_names_that_exist(self.data, self.options.troll_stars)
        location_names_that_exist_to_id = dict(filter(lambda location: location[0] in existing_location_names, self.location_name_to_id.items()))

        for course, data in self.data.locations.items():
            course_region = Region(course, self.player, self.multiworld)
            match course:
                case "Other":
                    course_region.add_locations(
                        dict(filter(lambda location: location[0] in sm64hack_items[:5], location_names_that_exist_to_id.items())),
                        SM64HackLocation
                    )
                    course_region.add_locations(
                        dict({"Victory Location": None}),
                        SM64HackLocation
                    )
                    if("sr7" in self.data.locations["Other"]["Settings"]):
                        #print(dict(filter(lambda location: location[0] in badges, location_names_that_exist_to_id.items())))
                        course_region.add_locations(
                            dict(filter(lambda location: location[0] in badges, location_names_that_exist_to_id.items())),
                            SM64HackLocation
                        )
                    if("sr3.5" in self.data.locations["Other"]["Settings"]):
                        course_region.add_locations(
                            {"Black Switch": location_names_that_exist_to_id["Black Switch"]}
                        )
                case "Extra": #EX only exists in sr6.25 (at least right now)
                    course_region.add_locations(
                        dict(filter(lambda location: location[0] in sr6_25_locations, location_names_that_exist_to_id.items())),
                        SM64HackLocation
                    )
                case _:          
                    course_region.add_locations(
                        dict(filter(lambda location: location[0].startswith(course + ' '), location_names_that_exist_to_id.items())),
                        SM64HackLocation
                    )
                
                
            self.multiworld.regions.append(course_region)
            star_requirement = data.get("StarRequirement")
            if(not star_requirement):
                star_requirement = 0
            menu_region.connect(
                course_region, 
                f"{course} Connection", 
                lambda state, star_requirement = int(star_requirement): state.has_from_list(star_like, self.player, int(star_requirement))
            )
    def check_conditional_requirements(self, state, course_conditional_requirements):
        for requirement in course_conditional_requirements:
            star_requirement = requirement.get("StarRequirement")
            if not star_requirement:
                star_requirement = 0
            if state.has_from_list(star_like, self.player, int(star_requirement)):
                course_requirements = requirement.get("Requirements")
                if(not course_requirements):
                    return True

                flag = True
                for requirement in course_requirements:
                    if(requirement.startswith("Key") and self.progressive_keys > 0):
                        num = int(requirement[-1])
                        if(self.progressive_keys == 2):
                            num = 2 if num == 1 else 1
                        if not state.has("Progressive Key", self.player, num):
                            flag = False
                            break
                    elif requirement == "Super Badge":
                        if not state.has("Progressive Stomp Badge", self.player, 1):
                            flag = False
                            break
                    elif requirement == "Ultra Badge":
                        if not state.has("Progressive Stomp Badge", self.player, 2):
                            flag = False
                            break
                    elif not state.has(requirement, self.player):
                        flag = False
                        break
                if(flag):
                    return True

        return False
    
    def can_access_location(self, state, star_data: dict, actflag=False, course=None, star=None):
        star_requirement = star_data.get("StarRequirement")
        if(star_requirement):
            if(not state.has_from_list(star_like, self.player, int(star_requirement))):
                return False
        other_requirements = star_data.get("Requirements")
        if(other_requirements):
            stomp_level = 0
            if "Super Badge" in other_requirements: stomp_level = 1
            if "Ultra Badge" in other_requirements: stomp_level = 2

            if(not state.has("Progressive Stomp Badge", self.player, stomp_level)):
                return False

            other_requirements = [req for req in other_requirements if req not in ["Super Badge", "Ultra Badge", "actspecific"]] 
            #SB and UB are handled above, actspecific seems a bit computationally expensive so it should only be checked if the location would be reachable otherwise, since otherwise its wasted effort
            
            for requirement in other_requirements:
                if requirement.startswith("Key") and self.progressive_keys > 0:
                    num = int(requirement[-1])
                    if(self.progressive_keys == 2):
                        num = 2 if num == 1 else 1
                    if not state.has("Progressive Key", self.player, num):
                        return False
                else:
                    if(not state.has(requirement, self.player)):
                        return False
        star_conditional_requirements = star_data.get("ConditionalRequirements")
        if star_conditional_requirements:
            if not self.check_conditional_requirements(state, star_conditional_requirements):
                return False
        
        other_requirements = star_data.get("Requirements")
        if(other_requirements):
            if "actspecific" in other_requirements and actflag: #actflag is to prevent act specific stars checking act specific stars which check other act specific stars, exponentially increasing stuff
                for i in range(star): #this might be computationally expensive but its the best idea i can think of...
                    if not self.can_access_location(state, self.data.locations[course]["Stars"][i]):
                        return False
        return True

    
    def set_rules(self) -> None:
        for course in self.data.locations:
            if course == "Other":
                for item in range(5):
                    star_data = self.data.locations[course]["Stars"][item]
                    if(star_data.get("exists")):
                        add_rule(self.multiworld.get_location(sm64hack_items[item], self.player),
                            lambda state, star_data=self.data.locations[course]["Stars"][item]: self.can_access_location(state, star_data))
                    
                
                if("sr7" in self.data.locations["Other"]["Settings"]):
                    for item in range(5):
                        stardata = self.data.locations[course]["Stars"][item + 7]
                        if(stardata.get("exists")):
                            print(self.multiworld.get_location(badges[item], self.player))
                            add_rule(self.multiworld.get_location(badges[item], self.player),
                                lambda state, star_data=self.data.locations[course]["Stars"][item + 7]: self.can_access_location(state, star_data))
                
                if("sr6.25" in self.data.locations["Other"]["Settings"]):
                    add_rule(self.multiworld.get_location("Yellow Switch", self.player),
                             lambda state, star_data=self.data.locations[course]["Stars"][5]: self.can_access_location(state, star_data))
                
                if("sr3.5" in self.data.locations["Other"]["Settings"]):
                    add_rule(self.multiworld.get_location("Black Switch", self.player),
                             lambda state, star_data=self.data.locations[course]["Stars"][5]: self.can_access_location(state, star_data))

                star_data = self.data.locations[course]["Stars"][6]
                add_rule(self.multiworld.get_location("Victory Location", self.player),
                    lambda state, star_data=self.data.locations[course]["Stars"][6]: self.can_access_location(state, star_data))
                continue
            if course == "Extra":
                for star in range(8):
                    star_data = self.data.locations[course]["Stars"][star]
                    if(star_data.get("exists")):
                        add_rule(self.multiworld.get_location(sr6_25_locations[star + 1], self.player),
                            lambda state, course=course, star=star, star_data=self.data.locations[course]["Stars"][star]: self.can_access_location(state, star_data, True, course, star))
                continue
                    
                
            
            course_data = self.data.locations[course]
            add_rule(self.multiworld.get_entrance(f"{course} Connection", self.player),
                lambda state, course_data=self.data.locations[course]: self.can_access_location(state, course_data))
            
            star_data = self.data.locations[course]["Cannon"]
            if(star_data.get("exists")):
                add_rule(self.multiworld.get_location(f"{course} Cannon", self.player),
                    lambda state, star_data=self.data.locations[course]["Cannon"]: self.can_access_location(state, star_data))
                    
            star_data = self.data.locations[course]["Troll Star"]
            if(star_data.get("exists")):
                add_rule(self.multiworld.get_location(f"{course} Troll Star", self.player),
                    lambda state, star_data=self.data.locations[course]["Troll Star"]: self.can_access_location(state, star_data))

            for star in range(8):
                star_data = self.data.locations[course]["Stars"][star]
                if(star_data.get("exists")):
                    add_rule(self.multiworld.get_location(f"{course} Star {star + 1}", self.player),
                        lambda state, course=course, star=star, star_data=self.data.locations[course]["Stars"][star]: self.can_access_location(state, star_data, True, course, star))
                
    
    def generate_basic(self) -> None:
        self.multiworld.get_location("Victory Location", self.player).place_locked_item(self.create_event("Victory"))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def fill_slot_data(self) -> Mapping[str, Any]:
        return {
            "Cannons": self.data.locations["Other"]["Settings"]["cannons"],
            "ProgressiveKeys": self.progressive_keys,
            "DeathLink": self.options.death_link.value == True, # == True so it turns it into a boolean value
            "Badges": "sr7" in self.data.locations["Other"]["Settings"],
            "sr6.25": "sr6.25" in self.data.locations["Other"]["Settings"],
            "sr3.5": "sr3.5" in self.data.locations["Other"]["Settings"]
        }