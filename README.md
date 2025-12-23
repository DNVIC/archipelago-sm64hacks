# NOTE: Use and discussion of this apworld (unfortunately) is not allowed anymore in the main archipelago server. Please join [this one](https://discord.gg/Nu4X9gmGDR) instead, if you want help, or just want to share a json file

My little archipelago world for (most) Super Mario 64 Romhacks. Currently shuffles keys, stars, caps, cannons, and troll stars throughout the worlds
Special support for Star Revenges 3.5, 6.25, 7, 7.5, and 8 as well!

## How to use this world:

Video guide [here](https://youtu.be/ugKJhTIC1OE), text guide below, use whichever you prefer. (though it's pretty complicated, the video guide is more thorough)
Video guide is a bit outdated but it's recommended if you are making your own JSON file, if you are using an existing one the text guide is more than sufficient

Have a quick look through [this repo](https://github.com/DNVIC/sm64hack-archipelago-jsons) first, there's a good chance there's a json file for a hack you want to play in there, especially if it's a major and/or popular hack. If it's in there, the logic for the hack will be automatically downloaded when you generate your game (you do NOT need to download it), and therefore you can head straight to [generation](#Generation), though make sure to note down the name of the json file.

### JSON Creation

First, create a json file using [this website](http://dnvic.com/ArchipelagoGenerator/index.html), using a .jsml file. You can get a .jsml file for a hack by loading up a hack in PJ64/Mupen64/Retroarch, opening [stardisplay](https://github.com/aglab2/SM64StarDisplay), and finding the layout folder in the same folder the exe file is in.

Then, get the .jsml file from the layout folder located where the stardisplay .exe is.

Input the jsml file into the website, and fill out the requirements for everything in the hack, by clicking on the stars, cannons, caps/keys, troll stars, or course names. Most hacks only really have star and key requirements, and maybe per-star cap requirements, but some hacks have more complicated requirements. If a cannon exists, select it, hit the exists checkbox, add requirements, and hit save. Same with keys/caps/troll stars. Conditional requirements are a bit more confusing, but are necessary if for example you can get to a level with either the vanish cap or key 2. You'd create one conditional requirement for the vanish cap, and one for key 2, and that'll make it so only one is required.

Click on the victory text at the bottom, and put whatever is required to achieve "Victory" in the hack. As it is, this will not be automatically be achieved in the rando when you get it, since its impossible to know what constitutes victory for an arbitrary hack, but its still important since the rando makes sure that victory is possible. If you want to, you can say when you get victory by running the "Victory.js" script when playing the game. It's the honor system, but the best I can do.

Export the .json file, and put it in the sm64hack_jsons folder (specifically inside the custom_jsons folder in there) inside the archipelago root directory (if it does not exist, try generating a sample game with something like superMario64.json and it should work afterwards)

### Generation

Copy the template.yaml from the releases, change json_file to be the json file you want to use (just the name of the file, if it's in a subdirectory it will find it), and place it in the players folder.
There's a few settings you can modify, progressive keys makes keys a progressive item, in some hacks this is a good idea as key 2 stuff is locked entirely behind key 1, whereas others its not. Each json has a default progressive key value, but if you want to change it for your specific game you can. You can also choose to randomize troll stars, if your hack supports it, though many hacks do not as they don't have troll stars.


### Client

Once your world is generated, open the hack you want to play, and delete/move files A and B (this is important)

Open the rom in [Luna's Project64](https://github.com/Luna-Project64), and open the generic bizhawk client (DO NOT use BizHawk, despite the name. It might work on BizHawk, but I haven't tested it and I am not providing any support to BizHawk users.) Go to Debugger -> Scripts (enable debugger if it isn't enabled), download the two .js files from the releases page, put them in the scripts folder (the scripts folder is in the folder that opens when you hit the ... button in the bottom left, if it doesnt open, go to the main window, help->appdata, and make a folder named "Scripts" there, though this shouldn't be an issue with up-to-date versions), run the 'connector_pj64_generic.js', and you should be ready to go! 

## Anticipated Questions
Q: Why does this exist? Why not just use the regular randomizer?

A: I wanted to add sm64 romhacks to archipelago, since the "normal" world only supports vanilla sm64 (and even then, it's the PC port, while I prefer playing stuff via emulator)

Q: You said (most) romhacks, what hacks aren't supported?

A: Basically any decomp hack will probably not ever be supported since this uses MIPS assembly code to change certain parts of the game to read from File 2 (easiest way to implement it, sm64's code is a mess), and when you recompile a rom from source and edit basically anything, the compiler will shift all of these pointers the assembly code relies upon, which causes the assembly code to fail completely. 

Some more complicated binary hacks/hacks with a lot of stars, like Decades Later and SM64OoT are not currently supported. Eventually, the goal is to get these hacks supported though.
In the far future, it might be possible to create little C library for decomp hacks, which if the hack is compiled with the library, the hack will be archipelago-compatible. Though that requires the hack to have its source code released, and it's a bit too much work for me for now.

Q: Why don't you support BizHawk even though this uses the "bizhawk client"?

A: BizHawk is a crappy emulator for SM64 hacks, it is not good at all for them, it will break in certain hacks. Whereas Luna's Project64 was literally made specifically for SM64 hacks. If you *really* want to use bizhawk, I have no way of stopping you. I will not provide support however, as I have no way of knowing whether or not it's a problem with my code, or just a problem with BizHawk

Q: Why aren't objects randomized?

A: The current "best" object randomizer for SM64 hacks is like 6 years old and super janky. If you want an object randomizer, put your rom through [this](https://github.com/aGlitch/Mario-64-Randomizer) after you apply the ASM patch. I'm planning on making a better one as part of this project, but it's a lot of effort.

Q: Can you randomize X?

A: Feel free to pitch ideas to me, but reminder that this world is meant to be generalized to most hacks. A lot of stuff either requires significant amounts of custom code (difficult to do without potentially infringing on already-existing custom code in current hacks), or is difficult to implement in a system that allows it to work for more than one hack.

## Future ideas (in approximate order of greatest to least priority)
* Better/more functional JSON editor
* Level tickets
* Move rando
* Better object and music shuffler
* Custom items for specific hacks (sm64oot, probably others im not thinking of)
* Some sort of way to know what items you're sending to other people in-game

## Credits
* aglab2 - Making StarDisplay (referencing the StarDisplay code was really helpful in figuring out where pointers were)
* ShiN3 - Helping a lot with the ASM code (which doesn't exist anymore as it's now edited in RAM in the client)
* SheepSquared - Testing
* KingToad74EE - Testing
* Agyroth - Testing
* HeralayanSalty - Making a good bit of the bizhawk client connector script
* Awesome7285 - Usually being the first one to find any bugs in my code
* Everyone who submitted JSON files for the github repo
* A bunch of archipelago worlds I ended up referencing when making this.

Below this is the main archipelago readme, felt like i should keep it since this repo has basically their whole code, but its unchanged so dont read it if you only care about repo-specific things

# [Archipelago](https://archipelago.gg) ![Discord Shield](https://discordapp.com/api/guilds/731205301247803413/widget.png?style=shield) | [Install](https://github.com/ArchipelagoMW/Archipelago/releases)

Archipelago provides a generic framework for developing multiworld capability for game randomizers. In all cases,
presently, Archipelago is also the randomizer itself.

Currently, the following games are supported:

* The Legend of Zelda: A Link to the Past
* Factorio
* Subnautica
* Risk of Rain 2
* The Legend of Zelda: Ocarina of Time
* Timespinner
* Super Metroid
* Secret of Evermore
* Final Fantasy
* VVVVVV
* Raft
* Super Mario 64
* Meritous
* Super Metroid/Link to the Past combo randomizer (SMZ3)
* ChecksFinder
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
* Civilization VI
* The Legend of Zelda: The Wind Waker
* Jak and Daxter: The Precursor Legacy
* Super Mario Land 2: 6 Golden Coins
* shapez
* Paint
* Celeste (Open World)
* Choo-Choo Charles

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
