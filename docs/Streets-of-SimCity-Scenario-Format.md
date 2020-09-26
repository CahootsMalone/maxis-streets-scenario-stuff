# Streets of SimCity Scenario Format

This document describes the format of the scenario files (`.scn`) used by 1997 Maxis game [Streets of SimCity](https://en.wikipedia.org/wiki/Streets_of_SimCity).

# Terms
The following terms are used in this document:
* Message text: text that appears during a mission, usually in the top-left of the screen (although optionally centred).
* Dramatic text: text that is rendered in the centre of the screen using large red letters. Each letter is a 3D model. This text enters and leaves the screen using a randomly-selected transition animation.

![Message text and dramatic text](text-types.png "Message text and dramatic text")

# General Notes

* The scenario file format is very similar to [Interchange File Format](https://en.wikipedia.org/wiki/Interchange_File_Format): it contains a variable number of named sections/chunks.
* The first eight bytes of each section contain the reversed four-letter section name (e.g., CITY is written YTIC) followed by the length of the section in bytes. All section lengths include the bytes containing the section name.
* All numeric values are little-endian.
* Text uses `\c` to indicate that text should be centred and `\n` for a newline. Sentences on the same line are usually separated by two spaces (a convention for monospaced text, albeit one that's less common now than it once was).
* When coordinates are specified, the top-left corner of the map is the origin. The x axis increases going right/east and the y axis increases going down/south. Note that this differs from the coordinate system used in SimCity 2000.

# Sections

## File Signature (MIFF)

MIFF likely stands for Maxis Interchange File Format.

Offset | Type | Length | Description
---|---|---|---
0 | Char | 4 | File signature (MIFF)
4 | ? | 4 | Unknown. Always 0x00000002.

## Miscellaneous Data (SCED)

SCED may stand for SimCity Editor Data, but that's just a guess.

Offset | Type | Length | Description
---|---|---|---
0 | Char | 4 | Name (DESC)
4 | Char | 4 | Unknown (CSTS). STSC probably stands for STreets of SimCity.
8 | ? | 4 | Unknown. Always 0x00000064.
12 | Int | 4 | File size in bytes. Appears to be used only for memory allocation (if at all) as a value larger than the actual size seems to cause no problems.
16 | ? | 4 | Unknown. Always 0x00000001.

## City Filename (CITY)

## Scenario Name (NAME)

## Time Limit (TIME)

## ? Checkpoint Bonus Time (CHKB)

## ? Bonus Money (BNUS)

## X Coordinate of Starting Location (LOCX)

## Y Coordinate of Starting Location (LOCY)

## ? Number of Random Packages (PACK)

## ? Number of Random Pickups (AMMO)

0 = no ammo pickups

## Number of Laps (LAPS)

## ? Name of some sort (IANM)

Empty string for most (all?) missions. Seems to be ignored if non-empty.

## Menu Description (ITXT) 

## ? Win Animation (WANM)

## Win Text (WTXT)

Ignored. Empty string for most missions, but not Galahad's Watch ones.

## ? Lose Animation (LANM)

## Lose Text (LTXT)

Ignored. Empty string for most missions, but not Galahad's Watch ones.

## ? (PRGN)

## Number of AI Definitions (#AIS)

Quantity: 1

## AI Definition (ANAI)

Quantity: N<sub>AIs</sub>

Offset | Type | Length | Description
---|---|---|---
0 | Char | 4 | Name (IANA)
4 | Int | 4 | Length (always 56 = 0x38)
8 | Int | 4 | Quantity
12 | Bool | 4 | Respawn (00 = disabled, 01 = enabled). Respawn time is 20 seconds per vehicle.
16 | Int | 4 | AI type (see list below)
20 | Int | 2 | X coordinate of spawn location (see notes below)
22 | Int | 2 | Y coordinate of spawn location (see notes below)
24 | Int | 4 | Unknown
28 | Bool | 4 | Spawn trigger (00 = elapsed time, 01 = event)
32 | Int | 4 | Spawn time (if trigger = 00) or number of trigger event (if trigger = 01)
36 | Int | 4 | Speed
40 | Int | 4 | Unknown/second speed value
44 | Int | 2 | X coordinate of target location (see notes below)
46 | Int | 2 | Y coordinate of target location (see notes below)
48 | Int | 4 | Level (0-4). See notes below.
52 | Int | 4 | Vehicle type (see list below)

### AI Types
* 0: Cop
* 1: Hunter
* 2: Racer
* 3: Rogue
* 4: Speeder
* 5: Courier
* 6: Boss
* 7: Ally (allies don't seem to attack enemies, but won't attack the player unless provoked)
* 8 or higher: Game crashes with "an unrecoverable error has occurred [...]" message

### Spawn Location
Set to (-1, -1) for a random location. For respawning AIs, note that a random location is only chosen for the first spawn: respawns will occur at the same location.

### Target Location
Appears to be ignored by all AI types besides rogues (which drive to the target location and explode).

### Notes on Level
* Range: [0, 4]. Values higher than 4 seem to be interpreted as 4.
* Affects hitpoints, attack frequency, and equipment (e.g., whether or not the AI is equipped with a shield).
* For races created with RaceEdit.exe, setting the difficulty to Easy, Medium, or Hard determines what levels are used for the AI racers.
  * Easy: levels 1 and 2.
  * Medium: levels 2 and 3.
  * Hard: levels 3 and 4.

### Vehicle Types
* 0 (0x0000): Default for specified AI type. Defaults:
  * Police car for Cop
  * Villain car for Hunter
  * Race for Racer
  * Van for Rogue
  * Sport for Speeder
  * Sport for Courier
  * Villain car for Boss
  * Sport for Ally
* 418 (0x01A2): Azzaroni (sport)
* 419 (0x01A3): StreetRat (compact)
* 420 (0x01A4): North Town Garage J57 (race)
* 421 (0x01A5): AirHawk (sedan)
* 422 (0x01A6): HMX Utility Van (van)
* 423 (0x01A7): Police car
* 478 (0x01DC): Villain car
* Other values appear to revert to the default for specified the AI type.

## Number of Event Definitions (#EVS)

Quantity: 1

## Event Definition (EVNT)

## Objective Labels (LABL)

Used in the objective screen that appears when the F3 key is held. The relative direction (e.g., "Northwest") is appended by the game.

Delimited with 0x01.

Empty labels (0x01 0x01) are valid.

It looks like the first non-empty label may be used for objectives that precede it. (Or there's a label for every event and only some events use non-empty ones.)

Quantity: 1

## Number of Checkpoint Definitions (CHK#)

## Checkpoint Definition (CHCK)

Quantity: N<sub>checkpoints</sub>

## "Episode" (Mission) Data (EPSD)

Quantity: 1
Offset | Type | Length | Description
--- | --- | --- | ---
0 | Char | 4 | Name (DSPE)
4 | Size | 4 | Length (always 32 = 0x20)
8 | Bool | 4 | Car lot (00 = enabled, 01 = disabled; yes, it's the opposite of what you'd expect)
12 | Bool | 4 | Cash reset (00 = user's current global cash total is used with specified amount of cash added, 01 = start with specified amount of cash)
16 | Int | 4 | Starting cash (if 0xFFFFFF and cash reset is 0x00, cash is inherited from previous mission in series) 
20 | Bool | 4 | Unknown.
24 | Bool | 4 | Unknown. Usually 0x01 for the first mission in a series or standalone missions, but first GW mission has it set to 0x00 and second GW mission has it set to 0x01.
28 | Int | 4 | Starting car (see value below)

### Starting Cars
* 0: "TempCar" (random vehicle) or inherit from previous mission
* 1: StreetRat
* 2: J57
* 3: AirHawk
* 4: Azzaroni
* 5: HMX Utility Van
* 6 or higher: game crashes

## Number of Package Definitions (#PKG)

Quantity: 1

Offset | Type | Length | Description
--- | --- | --- | ---
0 | Char | 4 | Name (GKP#)
4 | Int | 4 | Length (always 12 = 0x0C)
8 | Int | 4 | Number of packages (N<sub>packages</sub>)

## Package Definition (APAK)

Quantity: N<sub>packages</sub>

Offset | Type | Length | Description
--- | --- | --- | ---
0 | Char | 4 | Name (KAPA)
4 | Int | 4 | Length
8 | Int | 4 | Package type (00 = normal, 01 = money or story element, 02 = item)
12 | Int | 4 | Money earned (package type = 00 or 01) OR type of pickup (package type = 02). The money earned may be negative, as for the package near the bottom of the map in race 7.
16 | Int | 4 | Number of event group that makes package appear (0xFFFFFFFF = there from the beginning)
20 | Int | 2 | X coordinate of pickup location
22 | Int | 2 | Y coordinate of pickup location
24 | Int | 2 | X coordinate of delivery location (for items, same as pickup X)
26 | Int | 2 | Y coordinate of delivery location (for items, same as pickup Y)
28 | Char | 0-N | Message text that appears when the package is picked up. Optional.
Varies | N/A | 1 | Delimiter: 01
28 | Char | 0-N | Message text that appears when the package is delivered. Optional.
Varies | N/A | 1 | Delimiter: 01
Varies | Char | 0-N | Dramatic text that appears when the package is picked up. Optional. If the package is a bomb, the word "BOMB" also appears.
Varies | N/A | 1 | Delimiter: 01
Varies | Char | 0-N | Dramatic text that appears when the package is delivered. Optional.
Varies | N/A | 1 | Delimiter: 01
Varies | Char | 0-N | Name of a sound file played when the package is picked up. Optional.
Varies | N/A | 1 | Delimiter: 01
Varies | Char | 0-N | Name of a sound file played when the package is delivered. Optional.
Varies | N/A | 1 | Delimiter: 01
Varies | N/A | 4 | Delimiter: CD CD CD CD

### Pickup Types
* 0: Empty package (for story elements, e.g., fishing bait retrieved at start of first Galahad mission)
* 1: Bullets
* 2: Mines
* 3: Missiles
* 4: Oil cans
* 5: Smoke canisters
* 6: Monkey wrench (repair)
* 7: Monkey wrench (repair)
* 8: Gas
* 9: Gas
* 10: Armor add
* 11: Armor add
* 12: Battery
* 13: Machine gun
* 14: Missile launcher
* 15: Smoke screen
* 16: Mine dropper
* 17: Oil slick
* 18: Shield
* 19: Military radar
* 20: Hopper
* 21: Airfoil
* 22: Bomb. Bombs can only be carried for a limited time before they explode; this duration is proportional to the distance between the pickup and delivery locations. Bombs detonate five seconds after delivery.
* 23 or higher: Empty package (like 0)

## Event Group (EVTG)

Quantity: 0 or more

Offset | Type | Length | Description
--- | --- | --- | ---
0 | Char | 4 | Name (GTVE)
4 | Int | 4 | Length
8 | Int | 4 | Number
12 | Int | 4 | Type (see below)
16 | Bool | 2 | Whether or not nuclear explosion event should be triggered
18 | Char | 1-N | Null-terminated message text (if none, a single 00 byte)
Varies | Char | 1-N | Null-terminated dramatic text (if none, a single 00 byte)
Varies | N/A | 2 | Delimiter: CD CD

### Event Group Types
* 0: Win. When all events associated with this group have occurred, the player will win.
* 1: Lose. When all events associated with this group have occurred, the player will lose.
* 2: General. Used to trigger the appearance of packages, AI vehicles, etc.