from enum import Enum
from streets_common import StreetsAiType, StreetsCommonSingleNumber

class StreetsAiModel(Enum):
    DEFAULT_FOR_AI_TYPE = 0
    SPORT = 418
    COMPACT = 419
    RACE = 420
    SEDAN = 421
    VAN = 422
    COP = 423
    VILLAIN = 476

class StreetsAiSpawnTrigger(Enum):
    TIME = 0
    EVENT_GROUP = 1

class StreetsAiCount:
    NAME = 'SIA#'

    def __init__(self, aiCount: int):
        self.aiCount = aiCount

    def get_bytes(self):
        return StreetsCommonSingleNumber(self.NAME, self.aiCount).get_bytes()

class StreetsAi:
    NAME = 'IANA'
    LENGTH = 56

    def __init__(self, quantity: int, shouldRespawn: bool, aiType: StreetsAiType, spawnX: int, spawnY: int, 
        roamRadius: int, spawnTrigger: StreetsAiSpawnTrigger, spawnValue: int, speed: int, targetX: int, targetY: int,
        level: int, model: StreetsAiModel):
        self.quantity = quantity
        self.shouldRespawn = shouldRespawn
        self.aiType = aiType
        self.spawnX = spawnX
        self.spawnY = spawnY
        self.roamRadius = roamRadius
        self.spawnTrigger = spawnTrigger
        self.spawnValue = spawnValue
        # A single speed is used for both here since each AI type seems to ignore one of the two.
        self.speed1 = speed
        self.speed2 = speed
        self.targetX = targetX
        self.targetY = targetY
        self.level = level
        self.model = model
    
    def get_bytes(self):
        data = bytearray()

        data.extend(self.NAME.encode('ascii'))
        data.extend(self.LENGTH.to_bytes(4, byteorder='little', signed=True))
        data.extend(self.quantity.to_bytes(4, byteorder='little', signed=True))
        data.extend(self.shouldRespawn.to_bytes(4, byteorder='little', signed=True))
        data.extend(self.aiType.value.to_bytes(4, byteorder='little', signed=True))
        data.extend(self.spawnX.to_bytes(2, byteorder='little', signed=True))
        data.extend(self.spawnY.to_bytes(2, byteorder='little', signed=True))
        data.extend(self.roamRadius.to_bytes(4, byteorder='little', signed=True))
        data.extend(self.spawnTrigger.value.to_bytes(4, byteorder='little', signed=True))
        data.extend(self.spawnValue.to_bytes(4, byteorder='little', signed=True))
        data.extend(self.speed1.to_bytes(4, byteorder='little', signed=True))
        data.extend(self.speed2.to_bytes(4, byteorder='little', signed=True))
        data.extend(self.targetX.to_bytes(2, byteorder='little', signed=True))
        data.extend(self.targetY.to_bytes(2, byteorder='little', signed=True))
        data.extend(self.level.to_bytes(4, byteorder='little', signed=True))
        data.extend(self.model.value.to_bytes(4, byteorder='little', signed=True))

        return data