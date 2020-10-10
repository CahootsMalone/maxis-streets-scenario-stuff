from streets_ais import StreetsAiModel, StreetsAiSpawnTrigger, StreetsAiCount, StreetsAi
from streets_common import StreetsAiType
from streets_events import StreetsEventGroupType, StreetsEventCount, StreetsEventKillEnemies, StreetsEventReachLocation, StreetsEventDeliverPackages, StreetsEventEarnMoney, StreetsEventRoguesExplode, StreetsEventGroup
from streets_misc import StreetsCutscene, StreetsStartingCar, StreetsMisc1, StreetsMisc2
from streets_packages import StreetsPackageType, StreetsPickupType, StreetsPackageCount, StreetsPackage

# Event group numbers (values don't matter, provided there's no repetition)

GROUP_MISC = 100
GROUP_WIN = 0
GROUP_WATER_PACKAGE_SPAWN = 10
GROUP_ROGUES_SPAWN = 11
GROUP_ROGUES_ALL_EXPLODE = 12
GROUP_SPAWN_INFORMANT_BOMB_AND_ENEMIES = 13
GROUP_LOSE_1 = 20
GROUP_LOSE_2 = 21

# Miscellaneous scenario information

cityFileName = 'CustomScenarioDemo.sc2'
scenarioName = '* Custom Scenario Demo'
scenarioDescription = r"This is a custom scenario that was created using Python scripts I wrote after reverse-engineering the format of Streets of SimCity's scenario files. See https://github.com/CahootsMalone/maxis-streets-scenario-stuff for details, including the code used to generate this scenario."
timeLimit = 0 # 0 means no time limit
startX = 87
startY = 60
genericPackageCount = 0
genericPickupCount = 0

misc1 = StreetsMisc1(cityFileName, scenarioName, timeLimit, startX, startY, 
    genericPackageCount, genericPickupCount, scenarioDescription, StreetsCutscene.GRANNY, StreetsCutscene.GALAHAD)

# AIs

rogueSpeed1 = 25
rogueSpeed2 = 45
rogueSpeed3 = 35
rogueLevel = 0

ais = [
    # This rogue heads for the factory.
    StreetsAi(1, 0, StreetsAiType.ROGUE, 39, 53, 0, StreetsAiSpawnTrigger.EVENT_GROUP, GROUP_ROGUES_SPAWN, rogueSpeed1, 49, 62, rogueLevel, StreetsAiModel.DEFAULT_FOR_AI_TYPE),
    # This rogue heads for the condo.
    StreetsAi(1, 0, StreetsAiType.ROGUE, 41, 53, 0, StreetsAiSpawnTrigger.EVENT_GROUP, GROUP_ROGUES_SPAWN, rogueSpeed2, 67, 62, rogueLevel, StreetsAiModel.SPORT),
    # This rogue heads for city hall.
    StreetsAi(1, 0, StreetsAiType.ROGUE, 43, 53, 0, StreetsAiSpawnTrigger.EVENT_GROUP, GROUP_ROGUES_SPAWN, rogueSpeed3, 58, 58, rogueLevel, StreetsAiModel.COMPACT),
    # The informant. Its speed is set to zero to prevent it from driving around.
    StreetsAi(1, 0, StreetsAiType.ALLY, 92, 103, 0, StreetsAiSpawnTrigger.EVENT_GROUP, GROUP_SPAWN_INFORMANT_BOMB_AND_ENEMIES, 0, 0, 0, 0, StreetsAiModel.VILLAIN),
    # Some enemies.
    StreetsAi(1, 0, StreetsAiType.HUNTER, 12, 12, 0, StreetsAiSpawnTrigger.EVENT_GROUP, GROUP_SPAWN_INFORMANT_BOMB_AND_ENEMIES, 40, 0, 0, 4, StreetsAiModel.VILLAIN),
    StreetsAi(1, 0, StreetsAiType.HUNTER, 21, 12, 0, StreetsAiSpawnTrigger.EVENT_GROUP, GROUP_SPAWN_INFORMANT_BOMB_AND_ENEMIES, 40, 0, 0, 4, StreetsAiModel.VILLAIN),
    StreetsAi(1, 0, StreetsAiType.HUNTER, 12, 21, 0, StreetsAiSpawnTrigger.EVENT_GROUP, GROUP_SPAWN_INFORMANT_BOMB_AND_ENEMIES, 40, 0, 0, 4, StreetsAiModel.VILLAIN),
    StreetsAi(1, 0, StreetsAiType.HUNTER, 21, 21, 0, StreetsAiSpawnTrigger.EVENT_GROUP, GROUP_SPAWN_INFORMANT_BOMB_AND_ENEMIES, 40, 0, 0, 4, StreetsAiModel.VILLAIN),
]

aiCount = StreetsAiCount(len(ais))

# Events

bonusTime = 0
bonusMoney = 0

rogEvtUnkVal = 0 # Rogue events have a value I haven't been able to figure out.
locEvtUnkVal = 0 # Location events have a value I haven't been able to figure out.

# Location events in the mission-win event group block all location events that follow them.
#
# A location event in the mission-win group can only occur after all the events before it that are either:
#   a) in the mission-win group OR
#   b) location events
# have occurred.
#
# See the format documentation for details.
events = [
    StreetsEventReachLocation(GROUP_MISC, bonusTime, bonusMoney, locEvtUnkVal, 87, 60, 87, 60, 1, r'\cWelcome to the custom scenario demo!\nHold F3 to see your current objective(s).', 'Welcome', ''),
    
    StreetsEventReachLocation(GROUP_MISC, bonusTime, bonusMoney, locEvtUnkVal, 79, 32, 95, 40, 1, '\\cYou didn\'t think coming here would result in instant victory, did you?', 'Nice try', 'horn1.wav'),
    StreetsEventReachLocation(GROUP_MISC, bonusTime, bonusMoney, locEvtUnkVal, 56, 58, 60, 62, 0, '', 'City hall', ''),
    StreetsEventReachLocation(GROUP_MISC, bonusTime, bonusMoney, locEvtUnkVal, 25, 52, 35, 68, 0, '', 'Depot', ''),
    StreetsEventReachLocation(GROUP_MISC, bonusTime, bonusMoney, locEvtUnkVal, 4, 4, 29, 29, 0, '\\cThe lair of the mayor\'s evil twin.', 'Lair', ''),

    StreetsEventReachLocation(GROUP_MISC, bonusTime, bonusMoney, locEvtUnkVal, 94, 60, 94, 60, 1, r'\cBEWARE!\nThis road leads to Forbidden Island!', 'Forbidden', 'lickums3.wav'),
    StreetsEventReachLocation(GROUP_LOSE_1, bonusTime, bonusMoney, locEvtUnkVal, 123, 60, 123, 60, 1, '', '', ''),

    # ==========================================================================

    StreetsEventReachLocation(GROUP_WIN, bonusTime, bonusMoney, locEvtUnkVal, 74, 59, 76, 61, 1, r'\cGrab some cash, then bribe the mayor for a lucrative municipal contract.', 'Cash', 'radar.wav'),

    # --------------------------------------------------------------------------

    StreetsEventEarnMoney(GROUP_WIN, bonusTime, bonusMoney, 4, 1, r"\cFour dollars is probably enough to bribe the mayor.", '4 dollars', ''),
    StreetsEventReachLocation(GROUP_WIN, bonusTime, -4, locEvtUnkVal, 58, 58, 58, 58, 1, r'\cThe mayor accepts your bribe.\n"The Hilltop Marina contract is all yours!"', '', 'radar.wav'),

    # --------------------------------------------------------------------------

    StreetsEventReachLocation(GROUP_WATER_PACKAGE_SPAWN, bonusTime, bonusMoney, locEvtUnkVal, 44, 96, 46, 98, 1, '', '', ''),
    StreetsEventReachLocation(GROUP_WIN, bonusTime, bonusMoney, locEvtUnkVal, 45, 97, 45, 97, 1, '', '', 'radar.wav'),

    # --------------------------------------------------------------------------

    StreetsEventDeliverPackages(GROUP_WIN, bonusTime, 500000, 1, 0, 0, 0, 0, 1, '', '', ''), # Water delivery.
    StreetsEventReachLocation(GROUP_WIN, bonusTime, bonusMoney, locEvtUnkVal, 41, 80, 41, 80, 1, '', '', 'radar.wav'),

    # --------------------------------------------------------------------------

    StreetsEventReachLocation(GROUP_ROGUES_SPAWN, bonusTime, bonusMoney, locEvtUnkVal, 39, 58, 43, 62, 1, '', '', ''),
    StreetsEventReachLocation(GROUP_WIN, bonusTime, bonusMoney, locEvtUnkVal, 40, 59, 42, 61, 1, '', '', 'radar.wav'),

    # --------------------------------------------------------------------------

    StreetsEventReachLocation(GROUP_SPAWN_INFORMANT_BOMB_AND_ENEMIES, bonusTime, bonusMoney, locEvtUnkVal, 70, 81, 123, 127, 1, '', '', ''),
    StreetsEventReachLocation(GROUP_WIN, bonusTime, bonusMoney, locEvtUnkVal, 90, 102, 93, 106, 1, '\\c"The rogues were sent by the mayor\'s evil twin.\\nHis secret lair is the Braun Llama Dome.\\nBuy an airfoil, then take this bomb and blow up the Dome."', 'Informant', 'radar.wav'),

    # --------------------------------------------------------------------------

    StreetsEventReachLocation(GROUP_WIN, bonusTime, bonusMoney, locEvtUnkVal, 9, 9, 24, 24, 1, '', '', 'radar.wav'),

    # --------------------------------------------------------------------------

    StreetsEventDeliverPackages(GROUP_WIN, bonusTime, bonusMoney, 2, 0, 0, 0, 0, 1, '', '', ''), # Bomb delivery.
    StreetsEventReachLocation(GROUP_WIN, bonusTime, bonusMoney, locEvtUnkVal, 23, 100, 27, 104, 1, r'\cThe mayor is delighted.\n"Thanks for killing my evil twin!"', '', 'cheers2.wav'),

    # ==========================================================================

    StreetsEventRoguesExplode(GROUP_ROGUES_ALL_EXPLODE, bonusTime, bonusMoney, rogEvtUnkVal, 3, r'\cA rogue exploded!', '', 'misllpu.wav'),

    StreetsEventKillEnemies(GROUP_LOSE_2, bonusTime, bonusMoney, 1, StreetsAiType.ALLY, 1, '', '', ''),
]

eventCount = StreetsEventCount(len(events))

# More miscellaneous scenario information

# Objective labels are shown when the F3 key is held, but only for events in a mission-win group.
# However, any events before or between mission-win events need labels (even though they're not used).
# Overall, labels are optional; an empty array is valid, as are individual empty strings.
objectiveLabels = [
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    # ===================
    'Pick up money.',
    # -------------------
    '', # Use automatic label for money event.
    'Bribe the mayor.',
    # -------------------
    '', # Spawn water package.
    'Pick up a package for Hilltop Marina.',
    # -------------------
    'Deliver the package to Hilltop Marina.',
    'Wander north after making the delivery.',
    # -------------------
    '', # Spawn rogues.
    'Keep heading north.',
    # -------------------
    '', # Spawn informant and bomb package.
    'Meet with your informant (stop the rogues first, if you want).',
    # -------------------
    'Grab the bomb, then go to the lair of the mayor\'s evil twin.',
    # -------------------
    'Blow up the Braun Llama Dome.',
    'Visit the mayor at Hilltop Marina once you\'re done.',
    # ===================
    # Labels aren't required for events after the last event associated with a mission-win group.
    ]
isCarLotEnabled = False
startingMoney = 0

misc2 = StreetsMisc2(objectiveLabels, isCarLotEnabled, startingMoney, StreetsStartingCar.SEDAN)

# Packages

packages = [
    StreetsPackage(StreetsPackageType.MONEY, 1, -1, 74, 59, 74, 59, 'A single dollar.', '', '', '', '', ''),
    StreetsPackage(StreetsPackageType.MONEY, 1, -1, 75, 59, 75, 59, 'A single dollar.', '', '', '', '', ''),
    StreetsPackage(StreetsPackageType.MONEY, 1, -1, 74, 61, 74, 61, 'A single dollar.', '', '', '', '', ''),
    StreetsPackage(StreetsPackageType.MONEY, 1, -1, 75, 61, 75, 61, 'A single dollar.', '', '', '', '', ''),

    # Note that the player is awarded money in the package delivery event, not in the package itself.
    # This ensures that the magnitude of Hilltop Marina's payment remains a surprise.
    # (Package value is shown in the objective screen.)
    StreetsPackage(StreetsPackageType.NORMAL, 0, GROUP_WATER_PACKAGE_SPAWN, 45, 97, 27, 102, 'Water for Hilltop Marina.', r'Hilltop Marina thanks you for the water.\n"Here, have five hundred thousand dollars."', 'Water', 'Jackpot', '', ''),
    
    StreetsPackage(StreetsPackageType.PICKUP, StreetsPickupType.MACHINE_GUN.value, GROUP_ROGUES_SPAWN, 33, 58, 33, 58, '', '', '', '', 'gunpu.wav', ''),
    StreetsPackage(StreetsPackageType.PICKUP, StreetsPickupType.MACHINE_GUN.value, GROUP_ROGUES_SPAWN, 31, 60, 31, 60, '', '', '', '', 'gunpu.wav', ''),
    StreetsPackage(StreetsPackageType.PICKUP, StreetsPickupType.MACHINE_GUN.value, GROUP_ROGUES_SPAWN, 35, 60, 35, 60, '', '', '', '', 'gunpu.wav', ''),
    StreetsPackage(StreetsPackageType.PICKUP, StreetsPickupType.MACHINE_GUN.value, GROUP_ROGUES_SPAWN, 33, 62, 33, 62, '', '', '', '', 'gunpu.wav', ''),
    StreetsPackage(StreetsPackageType.PICKUP, StreetsPickupType.MILITARY_RADAR.value, GROUP_ROGUES_SPAWN, 33, 60, 33, 60, '', '', '', '', 'rdrlock.wav', ''),

    StreetsPackage(StreetsPackageType.PICKUP, StreetsPickupType.BOMB.value, GROUP_SPAWN_INFORMANT_BOMB_AND_ENEMIES, 93, 104, 18, 18, '', '', '', '', '', ''),
]

for x in range(25, 30):
    for y in range(58, 63):
        packages.append(StreetsPackage(StreetsPackageType.PICKUP, StreetsPickupType.BULLETS.value, GROUP_ROGUES_SPAWN, x, y, x, y, '', '', '', '', '', ''))

for x in range(31, 36):
    for y in range(52, 57):
        packages.append(StreetsPackage(StreetsPackageType.PICKUP, StreetsPickupType.BULLETS.value, GROUP_ROGUES_SPAWN, x, y, x, y, '', '', '', '', '', ''))

for x in range(31, 36):
    for y in range(64, 69):
        packages.append(StreetsPackage(StreetsPackageType.PICKUP, StreetsPickupType.BULLETS.value, GROUP_ROGUES_SPAWN, x, y, x, y, '', '', '', '', '', ''))

packageCount = StreetsPackageCount(len(packages))

# Event groups

eventGroups = [
    
    StreetsEventGroup(GROUP_WIN, StreetsEventGroupType.WIN, False, r"\cYou've won the custom scenario demo!", 'Victory'),
    StreetsEventGroup(GROUP_ROGUES_SPAWN, StreetsEventGroupType.GENERAL, False, r'\cRogues are on the loose!\nStopping them is optional.\nThere are weapons west of here.', 'Rogues'),

    # Because this event group is of the GENERAL type, the player won't lose if all the rogues explode.
    StreetsEventGroup(GROUP_ROGUES_ALL_EXPLODE, StreetsEventGroupType.GENERAL, False, r'\cAll the rogues exploded!', 'Oh well'),

    StreetsEventGroup(GROUP_LOSE_1, StreetsEventGroupType.LOSE, True, r'\cForbidden Island strikes again!', 'Uh oh'),

    StreetsEventGroup(GROUP_WATER_PACKAGE_SPAWN, StreetsEventGroupType.GENERAL, False, '', ''),

    StreetsEventGroup(GROUP_SPAWN_INFORMANT_BOMB_AND_ENEMIES, StreetsEventGroupType.GENERAL, False, '', ''),

    StreetsEventGroup(GROUP_LOSE_2, StreetsEventGroupType.LOSE, False, r'\cYour informant is dead!', 'Murder'),
]

# Write to file

outBytes = bytearray()
outBytes.extend(misc1.get_bytes())
outBytes.extend(aiCount.get_bytes())
for ai in ais:
    outBytes.extend(ai.get_bytes())
outBytes.extend(eventCount.get_bytes())
for event in events:
    outBytes.extend(event.get_bytes())
outBytes.extend(misc2.get_bytes())
outBytes.extend(packageCount.get_bytes())
for package in packages:
    outBytes.extend(package.get_bytes())
for eventGroup in eventGroups:
    outBytes.extend(eventGroup.get_bytes())

outPath = 'CustomScenarioDemo.scn'

with open(outPath, 'wb') as file:
    file.write(outBytes)