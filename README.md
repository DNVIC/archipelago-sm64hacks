My little archipelago world for (most) Super Mario 64 Romhacks. Shuffles keys, stars, caps, and cannons throughout the worlds

## How to use this world:

First, create a json file using [this website](http://dnvic.com/ArchipelagoGenerator/index.html), using a .jsml file. You can get a .jsml file for a hack by loading up a hack in PJ64/Mupen64/Retroarch, opening [stardisplay](https://github.com/aglab2/SM64StarDisplay) (or [the stardisplay client](https://github.com/DNVIC/Archipelago-StarDisplay))

Then, get the .jsml file from the layout folder located where the stardisplay .exe is.

Input the jsml file into the website, and fill out the requirements for everything in the hack, by clicking on the stars, cannons, caps/keys, or courses. Most hacks only really have star and key requirements, and maybe per-star cap requirements, but some hacks have more complicated requirements. If a cannon exists, select it, hit the exists checkbox, add requirements, and hit save. Same with keys/caps. Conditional requirements are a bit more confusing, but are necessary if for example you can get to a level with either the vanish cap or key 2. You'd create one conditional requirement for the vanish cap, and one for key 2, and that'll make it so only one is required.

Click on the victory text at the bottom, and put whatever is required to achieve "Victory" in the hack. As it is, this will not be automatically be achieved in the rando when you get it, since its impossible to know what constitutes victory for an arbitrary hack, but its still important since the rando makes sure that victory is possible.

Export the .json file, and put it in the same folder as the archipelago .exe (or generate.py)

Copy the template.yaml, change json_file to be the json file you just made (and if you want keys to be progressive, enable that as well), and place it in the worlds folder.

Once your world is generated, open the hack you want to play, and delete/move file 2 (this is important)

Use [this](https://github.com/DavidSM64/SimpleArmipsGui/releases/tag/1.3.2) program to apply starcount.asm to the rom file (preferably copy it beforehand, since this will modify the original rom file)

Open the rom in PJ64/Mupen/Retroarch, open [the stardisplay client](https://github.com/DNVIC/Archipelago-StarDisplay), right click -> archipelago, log in, and you should be ready to go! 

## Anticipated Questions
Q: Why does this exist? Why not just use the regular randomizer?

A: I wanted to add sm64 romhacks to archipelago, since the "normal" world only supports vanilla sm64 (and even then, it's the PC port, while I prefer playing stuff via emulator)

Q: You said (most) romhacks, what hacks aren't supported?

A: Basically any decomp hack will probably not ever be supported since this uses MIPS assembly code to change certain parts of the game to read from File 2 (easiest way to implement it, sm64's code is a mess), and when you recompile a rom from source and edit basically anything, the compiler will shift all of these pointers the assembly code relies upon, which causes the assembly code to fail completely. 

Any binary hack with 8 stars per level is not currently supported, nor is Decades Later or Star Revenge 6.25. I want both to work at some point, but that some point might be a bit away depending on how lazy I am (8 stars per level should be simple, but decades later/6.25 won't be so simple, and both would require special code to support them in particular)

Q: Why doesn't this use BizHawk, and instead this weird thing called "star display"?

A: Laziness, and practicality. On the part of laziness, all of the memory reading and writing is already implemented into the base code of stardisplay, which is useful since it means giving items to and from the game is super easy since all the hard work is done for me. On the part of practicality, no one in the SM64 romhack community uses BizHawk (for various reasons), and a bunch of hacks use the More Objects Patch which afaik breaks on all the graphics plugins in BizHawk. Whereas StarDisplay supports a bunch of emulators, basically all the main ones people in the community use. 

Q: Why aren't objects randomized?

A: The current "best" object randomizer for SM64 hacks is like 6 years old and super janky. If you want an object randomizer, put your rom through [this](https://github.com/aGlitch/Mario-64-Randomizer) after you apply the ASM patch. I'm planning on making a better one as part of this project, but it's not done yet.

Q: Can you randomize X?

A: Feel free to pitch ideas to me, but reminder that this world is meant to be generalized to most hacks. A lot of stuff either requires significant amounts of custom code (difficult to do without potentially infringing on already-existing custom code in current hacks), or is difficult to implement in a system that allows it to work for more than one hack.

## Future ideas (in approximate order of greatest to least priority)
* Support for hacks with 8 stars per level
* Better object and music shuffler
* Custom items for specific hacks (Badges in sr7/7.5/8, sm64oot, probably others im not thinking of)
* Client with Mac/Linux support (StarDisplay does not currently support Mac/Linux) (could probably fork the relevant parts of stardisplay and recompile as a purely console application)
* Ideas I have for dynamic locations that could be interesting
* Some sort of way to know what items you're sending to other people in-game
* Presets for major/important hacks (probably every megapack hack)

## Credits
* aglab2 - Making StarDisplay (the main program that the client is built off of)
* Shin3 - Helping a lot with the ASM code
* SheepSquared - Testing
* KingToad74EE - Testing
* Agyroth - Testing
* A bunch of archipelago worlds I ended up referencing when making this.

Below this is the main archipelago readme, felt like i should keep it since this repo has basically their whole code, but its unchanged so dont read it if you only care about repo-specific things

# [Archipelago](https://archipelago.gg) ![Discord Shield](https://discordapp.com/api/guilds/731205301247803413/widget.png?style=shield) | [Install](https://github.com/ArchipelagoMW/Archipelago/releases)

Archipelago provides a generic framework for developing multiworld capability for game randomizers. In all cases,
presently, Archipelago is also the randomizer itself.

Currently, the following games are supported:

* The Legend of Zelda: A Link to the Past
* Factorio
* Minecraft
* Subnautica
* Slay the Spire
* Risk of Rain 2
* The Legend of Zelda: Ocarina of Time
* Timespinner
* Super Metroid
* Secret of Evermore
* Final Fantasy
* Rogue Legacy
* VVVVVV
* Raft
* Super Mario 64
* Meritous
* Super Metroid/Link to the Past combo randomizer (SMZ3)
* ChecksFinder
* ArchipIDLE
* Hollow Knight
* The Witness
* Sonic Adventure 2: Battle
* Starcraft 2
* Donkey Kong Country 3
* Dark Souls 3
* Super Mario World
* Pokémon Red and Blue
* Hylics 2
* Overcooked! 2
* Zillion
* Lufia II Ancient Cave
* Blasphemous
* Wargroove
* Stardew Valley
* The Legend of Zelda
* The Messenger
* Kingdom Hearts 2
* The Legend of Zelda: Link's Awakening DX
* Clique
* Adventure
* DLC Quest
* Noita
* Undertale
* Bumper Stickers
* Mega Man Battle Network 3: Blue Version
* Muse Dash
* DOOM 1993
* Terraria
* Lingo
* Pokémon Emerald
* DOOM II
* Shivers
* Heretic
* Landstalker: The Treasures of King Nole
* Final Fantasy Mystic Quest
* TUNIC
* Kirby's Dream Land 3
* Celeste 64
* Zork Grand Inquisitor
* Castlevania 64
* A Short Hike
* Yoshi's Island
* Mario & Luigi: Superstar Saga
* Bomb Rush Cyberfunk
* Aquaria
* Yu-Gi-Oh! Ultimate Masters: World Championship Tournament 2006
* A Hat in Time
* Old School Runescape
* Kingdom Hearts 1
* Mega Man 2
* Yacht Dice
* Faxanadu
* Saving Princess
* Castlevania: Circle of the Moon
* Inscryption

For setup and instructions check out our [tutorials page](https://archipelago.gg/tutorial/).
Downloads can be found at [Releases](https://github.com/ArchipelagoMW/Archipelago/releases), including compiled
windows binaries.

## History

Archipelago is built upon a strong legacy of brilliant hobbyists. We want to honor that legacy by showing it here.
The repositories which Archipelago is built upon, inspired by, or otherwise owes its gratitude to are:

* [bonta0's MultiWorld](https://github.com/Bonta0/ALttPEntranceRandomizer/tree/multiworld_31)
* [AmazingAmpharos' Entrance Randomizer](https://github.com/AmazingAmpharos/ALttPEntranceRandomizer)
* [VT Web Randomizer](https://github.com/sporchia/alttp_vt_randomizer)
* [Dessyreqt's alttprandomizer](https://github.com/Dessyreqt/alttprandomizer)
* [Zarby89's](https://github.com/Ijwu/Enemizer/commits?author=Zarby89)
  and [sosuke3's](https://github.com/Ijwu/Enemizer/commits?author=sosuke3) contributions to Enemizer, which make up the
  vast majority of Enemizer contributions.

We recognize that there is a strong community of incredibly smart people that have come before us and helped pave the
path. Just because one person's name may be in a repository title does not mean that only one person made that project
happen. We can't hope to perfectly cover every single contribution that lead up to Archipelago, but we hope to honor
them fairly.

### Path to the Archipelago

Archipelago was directly forked from bonta0's `multiworld_31` branch of ALttPEntranceRandomizer (this project has a
long legacy of its own, please check it out linked above) on January 12, 2020. The repository was then named to
_MultiWorld-Utilities_ to better encompass its intended function. As Archipelago matured, then known as
"Berserker's MultiWorld" by some, we found it necessary to transform our repository into a root level repository
(as opposed to a 'forked repo') and change the name (which came later) to better reflect our project.

## Running Archipelago

For most people, all you need to do is head over to
the [releases page](https://github.com/ArchipelagoMW/Archipelago/releases), then download and run the appropriate
installer, or AppImage for Linux-based systems.

If you are a developer or are running on a platform with no compiled releases available, please see our doc on
[running Archipelago from source](docs/running%20from%20source.md).

## Related Repositories

This project makes use of multiple other projects. We wouldn't be here without these other repositories and the
contributions of their developers, past and present.

* [z3randomizer](https://github.com/ArchipelagoMW/z3randomizer)
* [Enemizer](https://github.com/Ijwu/Enemizer)
* [Ocarina of Time Randomizer](https://github.com/TestRunnerSRL/OoT-Randomizer)

## Contributing

To contribute to Archipelago, including the WebHost, core program, or by adding a new game, see our
[Contributing guidelines](/docs/contributing.md).

## FAQ

For Frequently asked questions, please see the website's [FAQ Page](https://archipelago.gg/faq/en/).

## Code of Conduct

Please refer to our [code of conduct](/docs/code_of_conduct.md).
