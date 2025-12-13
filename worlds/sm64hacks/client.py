import worlds._bizhawk as bizhawk
import pkgutil
import random
from worlds._bizhawk.client import BizHawkClient
from .ClientData import *
from .Locations import location_names
from .Data import sm64hack_items, sr6_25_locations
from time import time
from struct import unpack
from NetUtils import ClientStatus
from Utils import get_unique_identifier

class SM64HackClient(BizHawkClient):
#Despite the fact this is a "BizHawkClient", this is not meant to use BizHawk
#Use Luna's Project64 with connector_pj64_generic.js
    game = "SM64 Romhack"
    system = "N64"

    base_id = 40693

    location_name_to_id = {name: id for
                    id, name in enumerate(location_names(), base_id)}
    
    items = ["Wing Cap", "Metal Cap", "Vanish Cap", "Key 1", "Key 2"] #order is seperate from items list in data

    def reset_data(self) -> None:
        self.file1Stars = None
        self.received_items = 0
        self.flags = [False, False, False, False, False]
        self.moat = 0
        self.cannons = {
            8:  False,
            12: False,
            13: False,
            14: False,
            15: False,
            16: False,
            17: False,
            18: False,
            19: False,
            20: False,
            21: False,
            22: False,
            23: False,
            24: False,
            25: False,
            26: False,
            27: False,
            28: False,
            29: False,
            30: False,
            31: False,
            32: False,
            33: False,
            34: False,
            35: False,
            36: False,
            37: False
        }
        self.death_flag = True
        self.death_time = 0
        self.last_death_link = None
        self.level = None
        self.choir_active = False
        self.choir_timer = 0
        self.choirs = 0
        self.area = None
        self.level_start_time = None
        self.flagPtr = None
        self.greenDemonPtr = None
        self.heaveHoPtr = None
        self.green_demon_data = None
        self.receive_items = False
        self.sent_get_requests = []
        self.loops = 0
        self.traps_received_this_game = []
        self.async_traps = []
        self.eeprom = ""
        self.receiving_ring = False
        self.receiving_ring_amount = 0
        self.supposed_ring_count = 0
    
    def __init__(self) -> None:
        super().__init__()
        self.reset_data()

    
    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            rom_magic = await bizhawk.read(ctx.bizhawk_ctx, [(0, 4, "ROM")])
            ram_magic = await bizhawk.read(ctx.bizhawk_ctx, [(0, 4, "RDRAM")])
            if(ram_magic[0] != bytes.fromhex("3C1A8032") or rom_magic[0] != bytes.fromhex("80371240")):
                return False #i cant just read the game name, romhacks have different names (surprisingly)
            
        except bizhawk.RequestFailedError:
            return False
        
        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.5
        return True
    
    #async def fix_star_count(count: int):
    #    pass
    
    def set_file_2_flags(self, file1data, file2data, ctx) -> None:
        file2data[9] = file1data[9] if not ctx.slot_data["sr6.25"] else file2data[9]
        if ctx.slot_data["sr3.5"] or ctx.slot_data["sr6.25"] or ctx.slot_data.get("moat"):
            file2data[10] = file1data[10] & 0b11111101
            file2data[10] |= self.moat << 1 #yellow/black switch is the same flag as moat
        else:
            file2data[10] = file1data[10]
        important_data = file1data[11]
        for i in range(5):
            if self.flags[i]:
                important_data |= (1 << (5 - i))
            else:
                important_data &= 0b11111111 ^ (1 << (5-i))
        file2data[11] = important_data
        return file2data

    async def check_death(self, read, ctx):
        if(int.from_bytes(read[4]) == 0):
            return 0
        gread = await bizhawk.guarded_read(ctx.bizhawk_ctx, [(int.from_bytes(read[6]) & 0x7FFFFFFF, 0x4, "RDRAM")], [(marioFloorPtr, read[6], "RDRAM")])
        if(gread is None):
            return 0
        
        hp = read[2]
        action = read[5].hex()
        ypos = unpack('>f', read[7])[0]
        floorheight = unpack('>f', read[8])[0]
        floor = gread[0]
        
        match action:
            case "00001302":
                return 0 #stargrab, to prevent fake deaths
            case "00001303":
                return 0 #stargrab, to prevent fake deaths
            case "00001307":
                return 0 #stargrab, to prevent fake deaths
            case "00001904":
                return 0 #stargrab, to prevent fake deaths
            case "00001320":
                return 0 #pulling door, to prevent fake deaths
            case "00001321":
                return 0 #pushing door, to prevent fake deaths
            case "00021312":
                return 1 #quicksand
            case "300222E3":
                return 2 #whirlpool
            case "00021317":
                return 3 #bubba
            case "00021314":
                return 4 #toxic gas
            case "300032C4":
                return 5 #drown
            case "00021313":
                return 6 #electrocution
        
        if(list(floor)[1] == 0x0A and ypos - floorheight < 2048):
            return 8 #death barrier
        if(list(floor)[1] == 0x38 and ypos - floorheight < 2048):
            return 9 #wind
        
        if(hp[0] == 0x00):
            if(action == "00020338"):
                return 0 #wait for electrocution
            if(action == "010208B7"):
                return 7 #lava
            return 10 #generic
        
        return 0

    async def get_level_badges(self, addresses, level, ctx):
        level_badges = []
        reads = []
        for address in addresses:
            reads.append((address + 0x74, 0x4, "RDRAM"))  #0, active flag
            reads.append((address + 0x20C, 0x4, "RDRAM")) #1, beh data
            reads.append((address + 0x147, 0x1, "RDRAM")) #2, bparam2
        
        gread = await bizhawk.guarded_read(ctx.bizhawk_ctx, reads, [(levelPtr, bytearray([level]), "RDRAM")])
        if gread is None:
            return ["Super Badge", "Ultra Badge", "Wall Badge", "Triple Badge", "Lava Badge"]
        for i in range(len(addresses)):
            active = int.from_bytes(gread[i * 3])
            if active != 0:
                behavior = gread[1 + i * 3]
                if behavior.hex().upper() == "800F06A8":
                    bparam = int.from_bytes(gread[2 + i * 3])
                    level_badges.append(badge_dict[bparam])


        return level_badges
    
    async def receive_junk_item(self, ctx, index, name, coins=None):
        #flag for if unimportant items have been received can't be stored in savedata both because it'd fuck with the async traps 
        #and more importantly because there is no "safe" savedata to store the most recent index in, due to there not being much savedata in sm64, 
        #and as a result the unused portions are very likely to be used by some hackers.
        #print("tetttt", self.sent_get_requests, ctx.stored_data)
        if f"sm64hack_junk_{ctx.team}_{ctx.slot}_{index}" not in self.sent_get_requests: #need to let it loop through to receive the results of this
            await ctx.send_msgs([{
                "cmd": "Get",
                "keys": [f"sm64hack_junk_{ctx.team}_{ctx.slot}_{index}" ]
            }])
            self.sent_get_requests.append(f"sm64hack_junk_{ctx.team}_{ctx.slot}_{index}")
            self.receive_items = True
        elif f"sm64hack_junk_{ctx.team}_{ctx.slot}_{index}" not in ctx.stored_data.keys():
            self.receive_items = True #australia ping
        elif not ctx.stored_data.get(f"sm64hack_junk_{ctx.team}_{ctx.slot}_{index}") and index not in self.traps_received_this_game:
            self.traps_received_this_game.append(index)
            #print(self.loops)
            if self.loops > 4 or name == "Coin":
                await ctx.send_msgs([{
                    "cmd": "Set",
                    "key": f"sm64hack_junk_{ctx.team}_{ctx.slot}_{index}",
                    "default": 0,
                    "want_reply": False,
                    "operations": [{"operation": "or", "value": 1}],
                }])
                return self.get_junk_item_write(name, coins)
            else:
                if (index, name) not in self.async_traps:
                    self.async_traps.append((index, name))
    
    def get_junk_item_write(self, name, coins=None):
        match name:
            case "Green Demon Trap":
                if self.flagPtr:
                    return (self.flagPtr, bytes.fromhex("00000069"), "RDRAM")
            case "Heave-Ho Trap":
                if self.flagPtr:
                    return (self.flagPtr, bytes.fromhex("0000006A"), "RDRAM")
            case "Mario Choir":
                if self.choirFlagPtr:
                    self.choir_active = 1
                    if random.choice([True, False]): #there's actually 2 choir banks :D
                        return (self.choirFlagPtr, bytes.fromhex("0000000A"), "RDRAM")
                    else:
                        return (self.choirFlagPtr, bytes.fromhex("00000008"), "RDRAM")
            case "Squish Trap":
                return (marioSquishPtr, bytes.fromhex("FE"), "RDRAM")
            case "Coin":
                return (coinPtr, (coins + 1).to_bytes(2), "RDRAM")
            
    def get_segmented_behavior(self, absolute_behavior, bank_13_ram_start):
        return 0x80000000 + int.from_bytes(bank_13_ram_start) + absolute_behavior
    
    async def update_ring_link(self, ctx, ring_link: int):
        """Helper function to set Ring Link connection tag on/off and update the connection if already connected."""
        old_tags = ctx.tags.copy()
        if ring_link != 0:
            ctx.tags.add("RingLink")
        else:
            ctx.tags -= {"RingLink"}
        if ring_link == 2:
            ctx.tags.add("HardRingLink")
        else:
            ctx.tags -= {"HardRingLink"}
        if old_tags != ctx.tags and ctx.server and not ctx.server.socket.closed:
            await ctx.send_msgs([{"cmd": "ConnectUpdate", "tags": ctx.tags}])
    
    def on_package(self, ctx, cmd, args):
        super().on_package(ctx, cmd, args)

        # --- RINGLINK RECEIVE ---
        if cmd == "Bounced":
            tags = args.get("tags", [])
            # Tag not in package or Tag not in slotdata
            if "RingLink" not in tags or "RingLink" not in ctx.tags:
                return

            data = args.get("data", {})
            amount = int(data.get("amount", 0))

            # Received from yourself
            if data.get("source", 0) == abs(int(hash(get_unique_identifier())/10000000000)):
                return

            if amount == 0:
                return

            print(f"[RingLink] Received {amount} coins")

            self.receiving_ring = True
            self.receiving_ring_amount = amount


    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        from CommonClient import logger
        try:
            if ctx.server is None or ctx.server.socket.closed or ctx.slot_data is None:
                return
            if self.flagPtr is None:
                trapPatch = pkgutil.get_data(__name__, "asm/trap_patch")
                choirPatch = pkgutil.get_data(__name__, "asm/choir_patch")
                self.choirFlagPtr = len(choirPatch) + choirPatchPtr - 4
                self.starIdPtr = len(trapPatch) + trapPatchPtr - 16
                self.flagPtr = len(trapPatch) + trapPatchPtr - 12
                self.greenDemonPtr = len(trapPatch) + trapPatchPtr - 8
                self.heaveHoPtr = len(trapPatch) + trapPatchPtr - 4
            reads = [
                (filesPtr[0], 0x70, "RDRAM"),         #0
                (filesPtr[1], 0x70, "RDRAM"),         #1
                (hpPtr, 0x2, "RDRAM"),                #2
                (starCountAPPtr1, 0x4, "RDRAM"),      #3
                (marioObjectPtr, 0x4, "RDRAM"),       #4
                (marioActionPtr, 0x4, "RDRAM"),       #5
                (marioFloorPtr, 0x4, "RDRAM"),        #6
                (marioYPosPtr, 0x4, "RDRAM"),         #7
                (marioFloorHeightPtr, 0x4, "RDRAM"),  #8
                (igtPtr, 0x4, "RDRAM"),               #9
                (0x2E0, 0x1, "RDRAM"),                #10, blank memory unless you run the victory.js script
                (levelPtr, 0x1, "RDRAM"),             #11
                (0x20, 0x14, "ROM"),                  #12, EEPROM name
                (areaPtr, 0x1, "RDRAM"),              #13
                (self.greenDemonPtr, 0x4, "RDRAM"),   #14
                (self.heaveHoPtr, 0x4, "RDRAM"),      #15
                (bank13RamStartPtr, 0x4, "RDRAM"),    #16
                (self.starIdPtr, 0x4, "RDRAM"),       #17
                (coinPtr, 0x2, "RDRAM")               #18
            ]
            
            

            read = await bizhawk.read(ctx.bizhawk_ctx, reads)
            if(int.from_bytes(read[9]) < 60):
                return #game isnt initialized yet so things might be fucky

            
            writes = []
            resettest = read[3]
            if(resettest.hex() != "24040001"):
                logger.info("Reminder: Save and load a savestate so that traps can take effect")
                self.receive_items = True
                
                trap_patch = pkgutil.get_data(__name__, "asm/trap_patch") #patches are external files for ease of editing them
                choir_patch = pkgutil.get_data(__name__, "asm/choir_patch")
                star_patch = pkgutil.get_data(__name__, "asm/star_patch")
                #print(hex(len(patch) + patchPtr))
                writes.extend([
                    (starCountAPPtr1, bytes.fromhex("24040001"), "RDRAM"),
                    (starCountAPPtr2, bytes.fromhex("24040001"), "RDRAM"),
                    (flagAPPtr, bytes.fromhex("24180002"), "RDRAM"),
                    (cannonAPPtr, bytes.fromhex("240E0002"), "RDRAM"),
                    (capAPPtr, bytes.fromhex("080A9BF7"), "RDRAM"),
                    (keyAPPtr1, bytes.fromhex("00000000"), "RDRAM"),
                    (keyAPPtr2, bytes.fromhex("00000000"), "RDRAM"),
                    (toad1APPtr, bytes.fromhex("0809DA70"), "RDRAM"),
                    (toad2APPtr, bytes.fromhex("0809DA7D"), "RDRAM"),
                    (toad3APPtr, bytes.fromhex("0809DA8A"), "RDRAM"),
                    (moatAPPtr, bytes.fromhex("10000005"), "RDRAM"),
                    (trapPatchPtr, trap_patch, "RDRAM"),
                    (choirPatchPtr, choir_patch, "RDRAM"),
                    (choirHookPtr, bytes.fromhex("0C09FFC0"), "RDRAM"),
                    (starPatchPtr, star_patch, "RDRAM")
                ])

            if self.loops == 0:
                self.eeprom = read[12].decode("ascii")
            if self.eeprom != read[12].decode("ascii"): #rom changed
                logger.info(f"Detected rom change, now playing {read[12].decode("ascii")}.")
                self.reset_data()
                ctx.slot_data = None
                ctx.finished_game = False
                return
            
            
            if(list(read[10])[0] == 69 and not ctx.finished_game and self.loops > 4): #this and patch are before mario exists check because they should be active even if mario doesn't exist
                print("tmtnf")
                ctx.finished_game = True                           #because victory is usually on stuff like end screen where mario doesn't exist
                await ctx.send_msgs([{                             #and patch is on file select usually
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL
                }])
            
            if int.from_bytes(read[4]) == 0: #mario doesn't exist yet
                await bizhawk.write(ctx.bizhawk_ctx, writes)
                return
            
            self.loops += 1

            
            file1data = list(read[0])
            if self.file1Stars is not None:
                if(file1data[5] != self.file1Stars[5]) and ctx.slot_data["Badges"]:
                    file1data[5] = self.file1Stars[5] #prevent badges from changing the flags, so they can be received correctly.
                    writes.append((filesPtr[0] + 0x5, bytearray(file1data[5:6]),"RDRAM"))
                else:
                    location_id_to_name = dict((value, key) for key, value in self.location_name_to_id.items()) #sync local stars with server, easier coordination if people are sharing a slot
                    index_course = dict((value, key) for key, value in courseIndex.items())
                    for location in ctx.checked_locations:
                        location_name = location_id_to_name[location]
                        if "Cannon" in location_name:
                            continue
                        if location_name in sr6_25_locations[1:]:
                            file1data[9] |= 1 << sr6_25_locations[1:].index(location_name)
                        elif location_name[:-7] in index_course:
                            file1data[index_course[location_name[:-7]]] |= 1 << int(location_name[-1]) - 1
                        elif location_name in self.items:
                            file1data[11] |= 1 << self.items.index(location_name) + 1
                    
                    writes.append((filesPtr[0], bytearray(file1data), "RDRAM"))

            file2data = list(read[1])
            file2flag = False
            if(self.file1Stars != file1data):
                locs = []
                self.file1Stars = file1data
                for i in range(len(self.file1Stars)):
                    if i in courseIndex:
                        for j in range(8):
                            bit = self.file1Stars[i] >> j & 0b00000001
                            if(bit == 1):
                                location_name = f"{courseIndex[i]} Star {j + 1}"
                                if(j == 7 and ctx.slot_data["Cannons"]):
                                    level = int.from_bytes(read[11])
                                    if(level_index[level] == i):
                                        location_name = f"{courseIndex[i]} Troll Star"
                                    elif level_index[level] + 1 == i or (i == 12 and level_index[level] == 8):
                                        if(i == 12):
                                            location_name = courseIndex[8] + " Cannon"
                                        else:
                                            location_name = courseIndex[i - 1] + " Cannon"
                                    writes.append((filesPtr[0] + i, bytearray([self.file1Stars[i] & 0b01111111]), "RDRAM")) #reset cannon flag so you can detect both troll stars and cannons
                                if(self.location_name_to_id[location_name] in ctx.server_locations):
                                    locs.append(self.location_name_to_id[location_name])
                    elif i == 37:
                        if(self.file1Stars[i] >> 7 & 0x1 and ctx.slot_data["Cannons"]):
                            location_name = courseIndex[36] + " Cannon"
                            if(self.location_name_to_id[location_name] in ctx.server_locations):
                                locs.append(self.location_name_to_id[location_name])
                    elif i == 9 and ctx.slot_data["sr6.25"]:
                        for j in range(8):
                            bit = self.file1Stars[i] >> j & 0b00000001
                            if bit == 1:
                                locs.append(self.location_name_to_id[sr6_25_locations[j+1]])
                    elif i == 10:
                        if self.file1Stars[i] & 0b00000010:
                            if(ctx.slot_data["sr3.5"]):
                                locs.append(self.location_name_to_id["Black Switch"])
                            elif(ctx.slot_data["sr6.25"]):
                                locs.append(self.location_name_to_id["Yellow Switch"])
                            elif(ctx.slot_data.get("moat")):
                                locs.append(self.location_name_to_id["Castle Moat"])
                    elif i == 11:
                        for j in range(1,6):
                            bit = self.file1Stars[i] >> j & 0x1
                            if bit == 1:
                                location_name = self.items[j - 1]
                                locs.append(self.location_name_to_id[location_name])
                #print(f"locs{locs}")
                await ctx.send_msgs([{"cmd": "LocationChecks", "locations": locs}])
                file2data = self.set_file_2_flags(self.file1Stars, file2data, ctx)
                file2flag = True
            
            if int.from_bytes(read[17]) > 7 and int.from_bytes(read[17]) < 255: #only star id 7 gives the previous level's cannon, 8+ do not and so i need to do some asm to store the id in a readable memory location
                level = int.from_bytes(read[11])
                location_name = f"{courseIndex[level_index[level]]} Troll Star"
                await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [self.location_name_to_id[location_name]]}])
                writes.append((self.starIdPtr, bytes.fromhex("00000000"), "RDRAM"))

            
            if(self.received_items != len(ctx.items_received) or self.receive_items):
                self.received_items = len(ctx.items_received)
                self.receive_items = False
                stars = 0
                starcount = 0
                keyCounter = 0
                badgeCounter = 0
                for index, item in enumerate(ctx.items_received):
                    item_name = sm64hack_items[item.item - self.base_id]
                    match item_name:
                        case "Power Star":
                            stars += 1
                        case "Progressive Key":
                            reversed = ctx.slot_data["ProgressiveKeys"] == 2
                            if keyCounter == 1:
                                self.flags[0 ^ reversed] = True
                                keyCounter = 2
                            else:
                                self.flags[1 ^ reversed] = True
                                keyCounter = 1
                        case "Key 1":
                            self.flags[1] = True
                        case "Key 2":
                            self.flags[0] = True
                        case "Metal Cap":
                            self.flags[3] = True
                        case "Vanish Cap":
                            self.flags[2] = True
                        case "Wing Cap":
                            self.flags[4] = True
                        case "Progressive Stomp Badge":
                            if badgeCounter == 0:
                                self.file1Stars[5] |= 16
                                badgeCounter = 1
                            else:
                                self.file1Stars[5] |= 32
                        case "Wall Badge":
                            self.file1Stars[5] |= 8
                        case "Triple Jump Badge":
                            self.file1Stars[5] |= 128
                        case "Lava Badge":    
                            self.file1Stars[5] |= 64
                        case "Yellow Switch":
                            self.moat = 1
                        case "Black Switch":
                            self.moat = 1
                        case "Castle Moat":
                            self.moat = 1
                        case "Overworld Cannon Star":
                            starcount += 1
                            self.cannons[12] = True
                        case "Bowser 2 Cannon Star":
                            starcount += 1
                            self.cannons[29] = True
                        case _:
                            if("Cannon" in item_name):
                                course = item_name[:-7]
                                course_num = list(filter(lambda key: courseIndex[key] == course,courseIndex))[0]
                                if(course_num == 8):
                                    self.cannons[12] = True
                                else:
                                    self.cannons[course_num + 1] = True
                            else:
                                write = await self.receive_junk_item(ctx, index, item_name, int.from_bytes(read[18]))
                                if write:
                                    writes.append(write)

                starcount += stars
                cannons = ctx.slot_data["Cannons"]
                if cannons:
                    if stars > 7:
                        file2data[8] = 127 + (128 if self.cannons[8] else 0)
                        stars -= 7
                    else:
                        file2data[8] = ((2 ** stars) - 1) + (128 if self.cannons[8] else 0)
                        stars = 0
                    for i in range(12,37):
                        if(stars > 7):
                            stars -= 7
                            file2data[i] = 127 + (128 if self.cannons[i] else 0)
                        else:
                            file2data[i] = ((2 ** stars) - 1) + (128 if self.cannons[i] else 0)
                            stars = 0
                    file2data[37] = file2data[37] | 128 if self.cannons[37] else 0
                else:
                    if stars > 8:
                        file2data[8] = 255
                        stars -= 8
                    else:
                        file2data[8] = ((2 ** stars) - 1) 
                        stars = 0
                    if ctx.slot_data["sr6.25"]: #extra stars
                        if stars > 8:
                            file2data[9] = 255
                            stars -= 8
                        else:
                            file2data[9] = ((2 ** stars) - 1) 
                            stars = 0
                    for i in range(12,37):
                        if (i == 12 or i == 29) and ctx.slot_data["sr6.25"]:
                            if(stars > 7):
                                stars -= 7
                                file2data[i] = 127 + (128 if self.cannons[i] else 0)
                            else:
                                file2data[i] = ((2 ** stars) - 1) + (128 if self.cannons[i] else 0)
                                stars = 0
                        else:
                            if(stars > 8):
                                stars -= 8
                                file2data[i] = 255
                            else:
                                file2data[i] = ((2 ** stars) - 1)
                                stars = 0

                writes.append((starsCountPtr, bytearray([starcount]), "RDRAM"))

                file2data = self.set_file_2_flags(self.file1Stars, file2data, ctx)
                file2flag = True

            if(file2flag == True):
                writes.append((filesPtr[1], bytearray(file2data), "RDRAM"))
            
            #greendemon
            if read[14].hex().upper().startswith('80'):
                if not self.green_demon_data:
                    self.green_demon_data = {"area":read[13], "level":read[11], "bhv":int.from_bytes(read[14]) & 0x7FFFFFFF}
                else:
                    if self.green_demon_data["area"] != read[13] or self.green_demon_data["level"] != read[11]:
                        self.green_demon_data = None
                        writes.append((self.greenDemonPtr, bytes.fromhex("00000000"), "RDRAM"))
                    else:
                        demon_reads = (
                            (self.green_demon_data["bhv"] + 0x74, 0x4, "RDRAM"), #0, active flag
                            (self.green_demon_data["bhv"] + 0x20C, 0x4, "RDRAM") #1, beh data
                        )
                        gread = await bizhawk.guarded_read(ctx.bizhawk_ctx, demon_reads, [(levelPtr, read[11], "RDRAM")])
                        if gread is not None:
                            active = int.from_bytes(gread[0])
                            behavior = gread[1]
                            if active == 0 or int.from_bytes(behavior) != self.get_segmented_behavior(0x4148, read[16]):
                                self.green_demon_data = None
                                writes.extend(((self.greenDemonPtr, bytes.fromhex("00000000"), "RDRAM"),
                                    (hpPtr, bytes.fromhex("0000"), "RDRAM")))
            
            #heaveho
            if read[15].hex().upper().startswith('80'): #sm64 animations are broken if you load an object in after you enter the level due to behaviorscript shit. this is a janky solution but it works
                addr = int.from_bytes(read[15]) & 0x7FFFFFFF
                heaveho_reads = (
                    (addr + 0x74, 0x4, "RDRAM"), #0, active flag
                    (addr + 0x20c, 0x4, "RDRAM"), #1, beh data
                    (addr + 0x3c, 0x4, "RDRAM") #2, anim
                )
                heave_read = await bizhawk.read(ctx.bizhawk_ctx, heaveho_reads)
                active = int.from_bytes(heave_read[0])
                behavior = heave_read[1]
                
                if active == 0 or int.from_bytes(behavior) != self.get_segmented_behavior(0x1548, read[16]):
                    writes.append((self.heaveHoPtr, bytes.fromhex("00000000"), "RDRAM"))
                elif heave_read[2].hex().upper() != "80735118":
                    writes.append((addr + 0x3c, bytes.fromhex("80735118"), "RDRAM"))

            #choir
            if self.choir_active == 2 and (time() - self.choir_timer) > self.choirs * 300:
                self.choir_active = 0
                self.choirs = 0
                writes.append((self.choirFlagPtr, bytes.fromhex("00000000"), "RDRAM"))

            # badges/choir
            if int.from_bytes(read[4]) != 0 and (int.from_bytes(read[11]) != self.level or int.from_bytes(read[13]) != self.area):
                self.level = int.from_bytes(read[11])
                if self.choir_active == 1:
                    self.choir_active = 2
                    self.choir_timer = time()
                    self.choirs += 1
                self.area = int.from_bytes(read[13])
                self.level_start_time = int.from_bytes(read[9])
            elif(ctx.slot_data["Badges"] and int.from_bytes(read[4]) != 0 and (int.from_bytes(read[9]) - self.level_start_time) > 150):
                hack_name = self.eeprom
                level = self.level
                badges_to_send = []
                match hack_name: #bit of a hack but itll work. tried to go through every object in the level for compatibility but that broke everything
                    case "STAR REVENGE 7      ":
                        match level:
                            case 0x07:
                                b = await self.get_level_badges((0x34B628,), level, ctx)
                                badges_to_send = [x for x in ["Super Badge"] if x not in b]
                            case 0x08:
                                b = await self.get_level_badges((0x3538C8,), level, ctx)
                                badges_to_send = [x for x in ["Wall Badge"] if x not in b]
                            case 0xA:
                                b = await self.get_level_badges((0x349288,), level, ctx)
                                badges_to_send = [x for x in ["Lava Badge"] if x not in b]
                            case 0xB:
                                b = await self.get_level_badges((0x34FB08,), level, ctx)
                                badges_to_send = [x for x in ["Ultra Badge"] if x not in b]
                            case 0x24:
                                b = await self.get_level_badges((0x34ECC8,), level, ctx)
                                badges_to_send = [x for x in ["Triple Jump Badge"] if x not in b]

                    case "STAR REVENGE 7.5KR  ":
                        match level:
                            case 0x11:
                                b = await self.get_level_badges((0x3473A8,), level, ctx)
                                badges_to_send = [x for x in ["Super Badge"] if x not in b]
                            case 0x13:
                                b = await self.get_level_badges((0x34B3C8, 0x343F68), level, ctx)
                                badges_to_send = [x for x in ["Wall Badge", "Triple Jump Badge"] if x not in b]
                            case 0xA:
                                b = await self.get_level_badges((0x348B68,), level, ctx)
                                badges_to_send = [x for x in ["Lava Badge"] if x not in b]
                            case 0xB:
                                b = await self.get_level_badges((0x34E808,), level, ctx)
                                badges_to_send = [x for x in ["Ultra Badge"] if x not in b]

                    case "STAR REVENGE 7.5edit":
                        match level:
                            case 0x11:
                                b = await self.get_level_badges((0x348B68,), level, ctx)
                                badges_to_send = [x for x in ["Super Badge"] if x not in b]
                            case 0x13:
                                b = await self.get_level_badges((0x345008, 0x34C208), level, ctx)
                                badges_to_send = [x for x in ["Wall Badge", "Triple Jump Badge"] if x not in b]
                            case 0xA:
                                b = await self.get_level_badges((0x348B68,), level, ctx)
                                badges_to_send = [x for x in ["Lava Badge"] if x not in b]
                            case 0xB:
                                b = await self.get_level_badges((0x34ECC8,), level, ctx)
                                badges_to_send = [x for x in ["Ultra Badge"] if x not in b]
                    case "STAR REVENGE 8 SOH  ":
                        match level:
                            case 0x14:
                                if self.area == 1: #area 2 is boss fight
                                    b = await self.get_level_badges((0x34C468,), level, ctx)
                                    badges_to_send = [x for x in ["Super Badge"] if x not in b]
                            case 0x1A:
                                b = await self.get_level_badges((0x342548,), level, ctx)
                                badges_to_send = [x for x in ["Ultra Badge"] if x not in b]
                    case "STAR REVENGE 8 edit ": #awesome's sr8 edit for AP
                        match level:
                            case 0x14:
                                if self.area == 1: #area 2 is boss fight
                                    b = await self.get_level_badges((0x34CB88,), level, ctx)
                                    badges_to_send = [x for x in ["Super Badge"] if x not in b]
                            case 0x1A:
                                b = await self.get_level_badges((0x342A08,), level, ctx)
                                badges_to_send = [x for x in ["Ultra Badge"] if x not in b]
                locs = []
                for badge in badges_to_send:
                    locs.append(self.location_name_to_id[badge])

                if locs != []:
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": locs}])
            
            

            # deathlink
            if read[2][0] != 0x00:
                self.death_flag = True
            if(ctx.slot_data.get("DeathLink") and self.death_flag and time() - self.death_time > 5):
                if "DeathLink" not in ctx.tags:
                    await ctx.update_death_link(True)
                
                if(self.last_death_link != ctx.last_death_link and self.last_death_link is not None):
                    self.death_flag = False
                    self.last_death_link = ctx.last_death_link
                    writes.append((hpPtr, bytes.fromhex("0000"), "RDRAM"))
                    self.death_time = time()
                elif self.last_death_link is None:
                    self.last_death_link = ctx.last_death_link
                else: #if you die naturally and get a deathlink on the same frame or whatever the deathlink takes priority to avoid loops
                    death = 0
                    death = await self.check_death(read,ctx)
                    if(death != 0):
                        self.death_time = time()
                        cs = causeStrings[death].replace("slot", ctx.player_names[ctx.slot])
                        self.death_flag = False
                        await ctx.send_death(cs)
                        self.last_death_link = ctx.last_death_link
            
            # ringlink
            if ctx.slot_data.get("RingLink") != 0:
                if "RingLink" not in ctx.tags:
                    await self.update_ring_link(ctx, ctx.slot_data.get("RingLink"))

                # Read current coins
                current = int.from_bytes(read[18])

                if self.receiving_ring:
                    self.receiving_ring = False

                    coins = self.receiving_ring_amount + current
                    self.receiving_ring_amount = 0

                    # Safety
                    coins = min(coins, 999)
                    coins = max(coins, 0)
                    self.supposed_ring_count = coins

                    # Write back
                    if coins != current:
                        writes.append((coinPtr, coins.to_bytes(2), "RDRAM"))
                        writes.append((coinVisualPtr, coins.to_bytes(2), "RDRAM"))

                    print(f"[RingLink] New coin total: {coins}")
                
                else:
                    if self.supposed_ring_count != current:
                        # Calc rings to send
                        link_type = "RingLink"
                        rings_to_send = current - self.supposed_ring_count

                        # Negative packets are only sent via hard ringlink
                        if rings_to_send < 0:
                            link_type = "HardRingLink"
                        
                        # If you don't have the HardRingLink tag then this gets skipped
                        if link_type in ctx.tags:
                            self.supposed_ring_count = current
                            await ctx.send_msgs([{
                                "cmd": "Bounce", "tags": [link_type],
                                "data": {
                                    "time": time(),
                                    "source": abs(int(hash(get_unique_identifier())/10000000000)), # the shit that makes sonic adventure not crash
                                    "amount": rings_to_send
                                }
                            }])


            
            #async traps
            if self.async_traps:
                if random.random() < (2/1731): #approx 1 every 5 minutes
                    trap = random.choice(self.async_traps)
                    self.async_traps.remove(trap)
                    logger.info(f"A trap has appeared!")
                    await ctx.send_msgs([{
                        "cmd": "Set",
                        "key": f"sm64hack_junk_{ctx.team}_{ctx.slot}_{trap[0]}",
                        "default": 0,
                        "want_reply": False,
                        "operations": [{"operation": "or", "value": 1}],
                    }])
                    writes.append(self.get_junk_item_write(trap[1]))

            #print(list(read[10])[0])
            await bizhawk.write(ctx.bizhawk_ctx, writes)
            
        except bizhawk.RequestFailedError:
            pass