saveBufferOffset = 0x207700

filesPtr = [0x207700, 0x207770, 0x2077E0, 0x207850]
hpPtr = 0x33B21E
igtPtr = 0x32D580

starCountAPPtr1 = 0x245000 + 0x35040
starCountAPPtr2 = 0x245000 + 0x35074
flagAPPtr = 0x245000 + 0x35198
cannonAPPtr = 0x245000 + 0x35344
capAPPtr = 0x245000 + 0x61FAC
keyAPPtr1 = 0x245000 + 0x34DB0
keyAPPtr2 = 0x245000 + 0x34DD4
toad1APPtr = 0x245000 + 0x319B0
toad2APPtr = 0x245000 + 0x319E4
toad3APPtr = 0x245000 + 0x31A18
moatAPPtr = 0x245000 + 0x751B0

marioActionPtr = 0x33B17C
marioFloorPtr = 0x33B1D8
marioYPosPtr = 0x33B1B0
marioFloorHeightPtr = 0x33B1E0
marioSquishPtr = 0x33B224

starsCountPtr = 0x33B21B

marioObjectPtr = 0x361158

objectListPtr = 0x33D488
objectListSize = 240
levelPtr = 0x32DDF9
areaPtr = 0x33B24A

trapPatchPtr = 0x29D4B8
choirPatchPtr = 0x27FF00
choirHookPtr = 0x3191E0
starPatchPtr = 0x279C88

bank13RamStartPtr = 0x33B400 + 4 * 0x13

coinPtr = 0x33B218

level_index = { #sm64's internal level ids are different than the ones used in save data
    16:8, #overworld
    6:8,
    26:8,
    9:12, #course 1-15
    24:13,
    12:14,
    5:15,
    4:16,
    7:17,
    22:18,
    8:19,
    23:20,
    10:21,
    11:22,
    36:23,
    13:24,
    14:25,
    15:26,
    17:27, #bowser 1/fight
    30:27,
    19:28, #bowser 2/fight
    33:28,
    21:29, #bowser 3/fight
    34:29,
    27:30, #slide
    28:31, #metal cap
    29:32, #wing cap
    18:33, #vanish cap
    31:34, #secrets 1-3
    20:35,
    25:36
}

courseIndex = {
    8:  "Overworld",
    12: "Course 1" ,
    13: "Course 2" ,
    14: "Course 3" ,
    15: "Course 4" ,
    16: "Course 5" ,
    17: "Course 6" ,
    18: "Course 7" ,
    19: "Course 8" ,
    20: "Course 9" ,
    21: "Course 10" ,
    22: "Course 11" ,
    23: "Course 12" ,
    24: "Course 13" ,
    25: "Course 14" ,
    26: "Course 15" ,
    27: "Bowser 1" ,
    28: "Bowser 2" ,
    29: "Bowser 3" ,
    30: "Slide" ,
    31: "Metal Cap" ,
    32: "Wing Cap" ,
    33: "Vanish Cap" ,
    34: "Secret 1" ,
    35: "Secret 2" ,
    36: "Secret 3"
}

causeStrings = [
    "this is not supposed to show up",
    "slot fell into something which acts like quicksand.",
    "slot really likes spinning around!",
    "slot became a tasty meal.",
    "slot couldn't find clean air.",
    "slot tried to breathe water.",
    "slot is not a good conductor of electricity.",
    "slot doesn't like extreme temperatures.",
    "slot fell into a deep abyss.",
    "The wind wasn't enough to save slot.",
    "slot died."
]

badge_dict = {
    0x80: "Triple Jump Badge",
    0x40: "Lava Badge",
    0x20: "Ultra Badge",
    0x10: "Super Badge",
    0x08: "Wall Badge"
}