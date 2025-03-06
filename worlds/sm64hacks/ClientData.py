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

marioActionPtr = 0x33B17C
marioFloorPtr = 0x33B1D8
marioYPosPtr = 0x33B1B0
marioFloorHeightPtr = 0x33B1E0

starsCountPtr = 0x33B21B

marioObjectPtr = 0x361158

objectListPtr = 0x33D488
objectListSize = 240
levelPtr = 0x32DDF9
areaPtr = 0x33B24A

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