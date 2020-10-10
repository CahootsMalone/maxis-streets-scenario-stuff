from enum import Enum
from streets_common import StreetsCommonSingleNumber, StreetsCommonString

# TODO check that these are all valid
class StreetsCutscene(Enum):
    DEFAULT = ''
    ZIPPY = 'zippy'
    GALAHAD = 'galahad'
    GRANNY = 'granny'
    RACER = 'racer'

class StreetsStartingCar(Enum):
    RANDOM_OR_INHERIT = 0
    COMPACT = 1
    RACE = 2
    SEDAN = 3
    SPORT = 4
    VAN = 5

class StreetsMisc1:
    # Parameters of little interest for scenarios (mainly race-related).
    CHECKPOINT_BONUS_TIME = 0
    MONEY_BONUS = 0
    LAP_COUNT = 0
    EMPTY_STRING = ''

    def __init__(self, 
        cityFilename: str, 
        scenarioName: str, 
        timeLimit: int, 
        startX: int, 
        startY: int,
        genericPackageCount: int,
        genericPickupCount: int,
        scenarioDescription: str,
        winCutscene: StreetsCutscene,
        loseCutscene: StreetsCutscene):
        self.cityFilename = cityFilename
        self.scenarioName = scenarioName
        self.timeLimit = timeLimit
        self.startX = startX
        self.startY = startY
        self.genericPackageCount = genericPackageCount
        self.genericPickupCount = genericPickupCount
        self.scenarioDescription = scenarioDescription
        self.winCutscene = winCutscene
        self.loseCutscene = loseCutscene
    
    def get_bytes(self):
        data = bytearray()

        data.extend('MIFF'.encode('ascii'))
        data.extend(int(2).to_bytes(4, byteorder='little', signed=True)) # Always 2
        data.extend('DECS'.encode('ascii'))
        data.extend('CSTS'.encode('ascii'))
        data.extend(int(100).to_bytes(4, byteorder='little', signed=True)) # Always 100
        data.extend(int(100000).to_bytes(4, byteorder='little', signed=True)) # File size (just a large number here since it doesn't have to be exact)
        data.extend(int(1).to_bytes(4, byteorder='little', signed=True)) # Always 1
        data.extend(StreetsCommonString('YTIC', self.cityFilename).get_bytes())
        data.extend(StreetsCommonString('EMAN', self.scenarioName).get_bytes())
        data.extend(StreetsCommonSingleNumber('EMIT', self.timeLimit).get_bytes())
        data.extend(StreetsCommonSingleNumber('BKHC', self.CHECKPOINT_BONUS_TIME).get_bytes())
        data.extend(StreetsCommonSingleNumber('SUNB', self.MONEY_BONUS).get_bytes())
        data.extend(StreetsCommonSingleNumber('XCOL', self.startX).get_bytes())
        data.extend(StreetsCommonSingleNumber('YCOL', self.startY).get_bytes())
        data.extend(StreetsCommonSingleNumber('KCAP', self.genericPackageCount).get_bytes())
        data.extend(StreetsCommonSingleNumber('OMMA', self.genericPickupCount).get_bytes())
        data.extend(StreetsCommonSingleNumber('SPAL', self.LAP_COUNT).get_bytes())
        data.extend(StreetsCommonString('MNAI', self.EMPTY_STRING).get_bytes())
        data.extend(StreetsCommonString('TXTI', self.scenarioDescription).get_bytes())
        data.extend(StreetsCommonString('MNAW', self.EMPTY_STRING).get_bytes())
        data.extend(StreetsCommonString('TXTW', self.winCutscene.value).get_bytes())
        data.extend(StreetsCommonString('MNAL', self.EMPTY_STRING).get_bytes())
        data.extend(StreetsCommonString('TXTL', self.loseCutscene.value).get_bytes())
        data.extend(StreetsCommonSingleNumber('NGRP', 0).get_bytes()) # Unknown

        return data

class StreetsMisc2:
    LABEL_DELIMITER = b'\x01'
    CHECKPOINT_COUNT = 0

    def __init__(self, objectiveLabels: list, isCarLotEnabled: bool, startingMoney: int, startingCar: StreetsStartingCar):
        self.objectiveLabels = objectiveLabels
        self.isCarLotEnabled = isCarLotEnabled
        self.startingMoney = startingMoney
        self.startingCar = startingCar
    
    def get_bytes(self):
        labelLength = 8 + sum([len(label) for label in self.objectiveLabels]) + len(self.objectiveLabels)

        data = bytearray()

        data.extend('LBAL'.encode('ascii'))
        data.extend(labelLength.to_bytes(4, byteorder='little', signed=True))
        for label in self.objectiveLabels:
            data.extend(label.encode('ascii'))
            data.extend(self.LABEL_DELIMITER)
        data.extend(StreetsCommonSingleNumber('KHC#', self.CHECKPOINT_COUNT).get_bytes())
        data.extend('DSPE'.encode('ascii'))
        data.extend(int(32).to_bytes(4, byteorder='little', signed=True)) # Length of EPSD section.
        data.extend((not(self.isCarLotEnabled)).to_bytes(4, byteorder='little', signed=True))
        data.extend(int(1).to_bytes(4, byteorder='little', signed=True))
        data.extend(self.startingMoney.to_bytes(4, byteorder='little', signed=True))
        data.extend(int(1).to_bytes(4, byteorder='little', signed=True)) # Unknown; usually 1 for standalone missions.
        data.extend(int(1).to_bytes(4, byteorder='little', signed=True)) # Also unknown; usually 1 for standalone missions.
        data.extend(self.startingCar.value.to_bytes(4, byteorder='little', signed=True))

        return data
