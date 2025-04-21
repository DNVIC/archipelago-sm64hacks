#This is an alternative client mainly for linux users. 
#The main stardisplay client is the preferred client for windows.


import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from .ClientData import *
from .Locations import location_names
from .Data import sm64hack_items
from time import time
from struct import unpack
from NetUtils import ClientStatus


class SM64HackClient(BizHawkClient):
#Despite the fact this is a "BizHawkClient", this is not meant to use BizHawk
#Use Luna's Project64 with connector_pj64_generic.js
    game = "SM64 Romhack"
    system = "N64"

    base_id = 40693

    location_name_to_id = {name: id for
                    id, name in enumerate(location_names(), base_id)}
    
    items = ["Wing Cap", "Metal Cap", "Vanish Cap", "Key 1", "Key 2"] #order is seperate from items list in data
    
    def __init__(self) -> None:
        super().__init__()
        self.file1Stars = None
        self.received_items = 0
        self.flags = [False, False, False, False, False]
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
        self.death_timestamp = 0
        self.last_death_link = None
        self.level = None
        self.area = None
        self.level_start_time = None


    
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
    
    def set_file_2_flags(self, file1data, file2data) -> None:
        file2data[9] = file1data[9]
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

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        from CommonClient import logger
        try:
            if ctx.server is None or ctx.server.socket.closed or ctx.slot_data is None:
                return
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
                (0x2E0, 0x1, "RDRAM"),                 #10, blank memory unless you run the victory.js script
                ]
            
            if(ctx.slot_data["Badges"]):
                reads.append((levelPtr, 0x1, "RDRAM"))#11
                reads.append((0x20, 0x14, "ROM")) #12, EEPROM name
                reads.append((areaPtr, 0x1, "RDRAM"))


            read = await bizhawk.read(ctx.bizhawk_ctx, reads)
            if(int.from_bytes(read[9]) < 30):
                return #game isnt initialized yet so things might be fucky
            
            file1data = list(read[0])
            writes = []
            if self.file1Stars is not None:
                if(file1data[5] != self.file1Stars[5]) and ctx.slot_data["Badges"]:
                    file1data[5] = self.file1Stars[5] #prevent badges from changing the flags, so they can be received correctly.
                    writes.append((filesPtr[0] + 0x5, bytearray(file1data[5:6]),"RDRAM"))


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
                                    if(i == 12):
                                        location_name = courseIndex[8] + " Cannon"
                                    else:
                                        location_name = courseIndex[i - 1] + " Cannon"
                                if(self.location_name_to_id[location_name] in ctx.server_locations):
                                    locs.append(self.location_name_to_id[location_name])
                    elif i == 37:
                        if(self.file1Stars[i] >> 7 & 0x1 and ctx.slot_data["Cannons"]):
                            location_name = courseIndex[36] + " Cannon"
                            if(self.location_name_to_id[location_name] in ctx.server_locations):
                                locs.append(self.location_name_to_id[location_name])
                    elif i == 11:
                        for j in range(1,6):
                            bit = self.file1Stars[i] >> j & 0x1
                            if bit == 1:
                                location_name = self.items[j - 1]
                                locs.append(self.location_name_to_id[location_name])
                #print(f"locs{locs}")
                await ctx.send_msgs([{"cmd": "LocationChecks", "locations": locs}])
                file2data = self.set_file_2_flags(self.file1Stars, file2data)
                file2flag = True
                                

            
            if(self.received_items != len(ctx.items_received)):
                self.received_items = len(ctx.items_received)
                stars = 0
                keyCounter = 0
                badgeCounter = 0
                for item in ctx.items_received:
                    item_name = sm64hack_items[item.item - self.base_id]
                    match item_name:
                        case "Power Star":
                            stars += 1
                        case "Progressive Key":
                            if keyCounter == 1:
                                self.flags[0] = True
                                keyCounter = 2
                            else:
                                self.flags[1] = True
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
                        case _:
                            if("Cannon" in item_name):
                                course = item_name[:-7]
                                course_num = list(filter(lambda key: courseIndex[key] == course,courseIndex))[0]
                                if(course_num == 8):
                                    self.cannons[12] = True
                                else:
                                    self.cannons[course_num + 1] = True

                oldstars = stars
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
                    for i in range(12,37):
                        if(stars > 7):
                            stars -= 7
                            file2data[i] = 255
                        else:
                            file2data[i] = ((2 ** stars) - 1)
                            stars = 0
                            break

                writes.append((starsCountPtr, bytearray([oldstars]), "RDRAM"))

                file2data = self.set_file_2_flags(self.file1Stars, file2data)
                file2flag = True

            if(file2flag == True):
                writes.append((filesPtr[1], bytearray(file2data), "RDRAM"))
            resettest = read[3]
            if(resettest.hex() != "24040001"):
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
                    (toad3APPtr, bytes.fromhex("0809DA8A"), "RDRAM")
                ])
            
            # badges
            if ctx.slot_data["Badges"] and int.from_bytes(read[4]) != 0 and (int.from_bytes(read[11]) != self.level or int.from_bytes(read[13]) != self.area):
                self.level = int.from_bytes(read[11])
                self.area = int.from_bytes(read[13])
                self.level_start_time = int.from_bytes(read[9])
            elif(ctx.slot_data["Badges"] and int.from_bytes(read[4]) != 0 and (int.from_bytes(read[9]) - self.level_start_time) > 150):
                hack_name = read[12].decode("ascii")
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
                    case "STAR REVENGE 8 SOH  ":
                        match level:
                            case 0x14:
                                if self.area == 1: #area 2 is boss fight
                                    b = await self.get_level_badges((0x34C468,), level, ctx)
                                    badges_to_send = [x for x in ["Super Badge"] if x not in b]
                            case 0x1A:
                                b = await self.get_level_badges((0x342548,), level, ctx)
                                badges_to_send = [x for x in ["Ultra Badge"] if x not in b]
                locs = []
                for badge in badges_to_send:
                    locs.append(self.location_name_to_id[badge])

                if locs != []:
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": locs}])
            



            # deathlink
            if(ctx.slot_data.get("DeathLink") and int(time()) > (self.death_timestamp + 15)):
                if "DeathLink" not in ctx.tags:
                    await ctx.update_death_link(True)
                
                if(self.last_death_link != ctx.last_death_link and self.last_death_link is not None):
                    self.death_timestamp = int(time())
                    self.last_death_link = ctx.last_death_link
                    writes.append((hpPtr, bytes.fromhex("0000"), "RDRAM"))
                elif self.last_death_link is None:
                    self.last_death_link = ctx.last_death_link
                else: #if you die naturally and get a deathlink on the same frame or whatever the deathlink takes priority to avoid loops
                    death = 0
                    death = await self.check_death(read,ctx)
                    if(death != 0):
                        cs = causeStrings[death].replace("slot", ctx.player_names[ctx.slot])
                        self.death_timestamp = int(time())
                        await ctx.send_death(cs)
                        self.last_death_link = ctx.last_death_link

            #print(list(read[10])[0])
            if(list(read[10])[0] == 69 and not ctx.finished_game):
                ctx.finished_game = True
                await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL
                }])
            await bizhawk.write(ctx.bizhawk_ctx, writes)
            
        except bizhawk.RequestFailedError:
            pass