from enum import Enum
from streets_common import StreetsAiType, StreetsCommonSingleNumber

class StreetsEventGroupType(Enum):
    WIN = 0
    LOSE = 1
    GENERAL = 2

class StreetsEventCount:
    NAME = 'SVE#'

    def __init__(self, eventCount: int):
        self.eventCount = eventCount

    def get_bytes(self):
        return StreetsCommonSingleNumber(self.NAME, self.eventCount).get_bytes()

class _StreetsEventCommonStart:
    NAME = 'TNVE'
    COMMON_START_LENGTH = 24

    def __init__(self, eventGroup: int, eventType: int, bonusTime: int, bonusMoney: int):
        self.length = self.COMMON_START_LENGTH
        self.eventGroup = eventGroup
        self.eventType = eventType
        self.bonusTime = bonusTime
        self.bonusMoney = bonusMoney
    
    def increase_length(self, amount):
        self.length = self.length + amount

    def reset_length(self):
        self.length = self.COMMON_START_LENGTH
    
    def get_bytes(self):
        data = bytearray()

        data.extend(self.NAME.encode('ascii'))
        data.extend(self.length.to_bytes(4, byteorder='little', signed=True))
        data.extend(self.eventGroup.to_bytes(4, byteorder='little', signed=True))
        data.extend(self.eventType.to_bytes(4, byteorder='little', signed=True))
        data.extend(self.bonusTime.to_bytes(4, byteorder='little', signed=True))
        data.extend(self.bonusMoney.to_bytes(4, byteorder='little', signed=True))

        return data

class _StreetsEventCommonEnd:
    MINIMUM_LENGTH = 15
    NULL_BYTE = b'\x00'
    END_MARKER = b'\xCD\xCD\xCD\xCD'

    def __init__(self, triggerCount: int, messageText: str, dramaticText: str, audioFile: str):
        self.triggerCount = triggerCount
        self.messageText = messageText
        self.dramaticText = dramaticText
        self.audioFile = audioFile
    
    def get_length(self):
        length = self.MINIMUM_LENGTH + len(self.messageText) + len(self.dramaticText) + len(self.audioFile)
        return length
    
    def get_bytes(self):
        data = bytearray()

        textLength = len(self.messageText) + len(self.dramaticText) + 2 # 2 is for null bytes

        data.extend(self.triggerCount.to_bytes(4, byteorder='little', signed=True))
        data.extend(textLength.to_bytes(4, byteorder='little', signed=True))
        data.extend(self.messageText.encode('ascii'))
        data.extend(self.NULL_BYTE)
        data.extend(self.dramaticText.encode('ascii'))
        data.extend(self.NULL_BYTE)
        data.extend(self.audioFile.encode('ascii'))
        data.extend(self.NULL_BYTE)
        data.extend(self.END_MARKER)

        return data

# Type 0
class StreetsEventKillEnemies:
    EVENT_TYPE = 0
    TYPE_SPECIFIC_FIELD_COUNT = 2
    TYPE_SPECIFIC_LENGTH = 12

    def __init__(self, eventGroup: int, bonusTime: int, bonusMoney: int, 
        killCount: int, aiType: StreetsAiType,
        triggerCount: int, messageText: str, dramaticText: str, audioFile: str):
        self.commonStart = _StreetsEventCommonStart(eventGroup, self.EVENT_TYPE, bonusTime, bonusMoney)
        self.killCount = killCount
        self.aiType = aiType
        self.commonEnd = _StreetsEventCommonEnd(triggerCount, messageText, dramaticText, audioFile)

        self.commonStart.increase_length(self.TYPE_SPECIFIC_LENGTH + self.commonEnd.get_length())
    
    def get_bytes(self):
        data = bytearray()

        data.extend(self.commonStart.get_bytes())
        data.extend(self.TYPE_SPECIFIC_FIELD_COUNT.to_bytes(4, byteorder='little', signed=True))
        data.extend(self.killCount.to_bytes(4, byteorder='little', signed=True))
        data.extend(self.aiType.value.to_bytes(4, byteorder='little', signed=True))
        data.extend(self.commonEnd.get_bytes())

        return data

# Type 1
class StreetsEventReachLocation:
    EVENT_TYPE = 1
    TYPE_SPECIFIC_FIELD_COUNT = 5
    TYPE_SPECIFIC_LENGTH = 24

    def __init__(self, eventGroup: int, bonusTime: int, bonusMoney: int, 
        unknown: int, topLeftX: int, topLeftY: int, bottomRightX: int, bottomRightY: int, 
        triggerCount: int, messageText: str, dramaticText: str, audioFile: str):
        self.commonStart = _StreetsEventCommonStart(eventGroup, self.EVENT_TYPE, bonusTime, bonusMoney)
        self.unknown = unknown
        self.topLeftX = topLeftX
        self.topLeftY = topLeftY
        self.bottomRightX = bottomRightX
        self.bottomRightY = bottomRightY
        self.commonEnd = _StreetsEventCommonEnd(triggerCount, messageText, dramaticText, audioFile)

        self.commonStart.increase_length(self.TYPE_SPECIFIC_LENGTH + self.commonEnd.get_length())
    
    def get_bytes(self):
        data = bytearray()

        data.extend(self.commonStart.get_bytes())
        data.extend(self.TYPE_SPECIFIC_FIELD_COUNT.to_bytes(4, byteorder='little', signed=True))
        data.extend(self.unknown.to_bytes(4, byteorder='little', signed=True))
        data.extend(self.topLeftX.to_bytes(4, byteorder='little', signed=True))
        data.extend(self.topLeftY.to_bytes(4, byteorder='little', signed=True))
        data.extend(self.bottomRightX.to_bytes(4, byteorder='little', signed=True))
        data.extend(self.bottomRightY.to_bytes(4, byteorder='little', signed=True))
        data.extend(self.commonEnd.get_bytes())

        return data

# Type 2
class StreetsEventDeliverPackages:
    EVENT_TYPE = 2
    TYPE_SPECIFIC_FIELD_COUNT = 5
    TYPE_SPECIFIC_LENGTH = 24

    def __init__(self, eventGroup: int, bonusTime: int, bonusMoney: int, 
        packageCount: int, topLeftX: int, topLeftY: int, bottomRightX: int, bottomRightY: int,
        triggerCount: int, messageText: str, dramaticText: str, audioFile: str):
        self.commonStart = _StreetsEventCommonStart(eventGroup, self.EVENT_TYPE, bonusTime, bonusMoney)
        self.packageCount = packageCount
        self.topLeftX = topLeftX
        self.topLeftY = topLeftY
        self.bottomRightX = bottomRightX
        self.bottomRightY = bottomRightY
        self.commonEnd = _StreetsEventCommonEnd(triggerCount, messageText, dramaticText, audioFile)

        self.commonStart.increase_length(self.TYPE_SPECIFIC_LENGTH + self.commonEnd.get_length())
    
    def get_bytes(self):
        data = bytearray()

        data.extend(self.commonStart.get_bytes())
        data.extend(self.TYPE_SPECIFIC_FIELD_COUNT.to_bytes(4, byteorder='little', signed=True))
        data.extend(self.packageCount.to_bytes(4, byteorder='little', signed=True))
        data.extend(self.topLeftX.to_bytes(4, byteorder='little', signed=True))
        data.extend(self.topLeftY.to_bytes(4, byteorder='little', signed=True))
        data.extend(self.bottomRightX.to_bytes(4, byteorder='little', signed=True))
        data.extend(self.bottomRightY.to_bytes(4, byteorder='little', signed=True))
        data.extend(self.commonEnd.get_bytes())

        return data

# Type 3
class StreetsEventEarnMoney:
    EVENT_TYPE = 3
    TYPE_SPECIFIC_FIELD_COUNT = 1
    TYPE_SPECIFIC_LENGTH = 8

    def __init__(self, eventGroup: int, bonusTime: int, bonusMoney: int, 
        moneyAmount: int,
        triggerCount: int, messageText: str, dramaticText: str, audioFile: str):
        self.commonStart = _StreetsEventCommonStart(eventGroup, self.EVENT_TYPE, bonusTime, bonusMoney)
        self.moneyAmount = moneyAmount
        self.commonEnd = _StreetsEventCommonEnd(triggerCount, messageText, dramaticText, audioFile)

        self.commonStart.increase_length(self.TYPE_SPECIFIC_LENGTH + self.commonEnd.get_length())
    
    def get_bytes(self):
        data = bytearray()

        data.extend(self.commonStart.get_bytes())
        data.extend(self.TYPE_SPECIFIC_FIELD_COUNT.to_bytes(4, byteorder='little', signed=True))
        data.extend(self.moneyAmount.to_bytes(4, byteorder='little', signed=True))
        data.extend(self.commonEnd.get_bytes())

        return data

# Type 4
class StreetsEventRoguesExplode:
    EVENT_TYPE = 4
    TYPE_SPECIFIC_FIELD_COUNT = 1
    TYPE_SPECIFIC_LENGTH = 8

    def __init__(self, eventGroup: int, bonusTime: int, bonusMoney: int, 
        unknown: int,
        triggerCount: int, messageText: str, dramaticText: str, audioFile: str):
        self.commonStart = _StreetsEventCommonStart(eventGroup, self.EVENT_TYPE, bonusTime, bonusMoney)
        self.unknown = unknown
        self.commonEnd = _StreetsEventCommonEnd(triggerCount, messageText, dramaticText, audioFile)

        self.commonStart.increase_length(self.TYPE_SPECIFIC_LENGTH + self.commonEnd.get_length())
    
    def get_bytes(self):
        data = bytearray()

        data.extend(self.commonStart.get_bytes())
        data.extend(self.TYPE_SPECIFIC_FIELD_COUNT.to_bytes(4, byteorder='little', signed=True))
        data.extend(self.unknown.to_bytes(4, byteorder='little', signed=True))
        data.extend(self.commonEnd.get_bytes())

        return data

class StreetsEventGroup:
    NAME = 'GTVE'
    MINIMUM_LENGTH = 22
    NULL_BYTE = b'\x00'
    END_MARKER = b'\xCD\xCD'

    def __init__(self, groupNumber: int, groupType: StreetsEventGroupType, explosion: bool, messageText: str, dramaticText: str):
        self.groupNumber = groupNumber
        self.groupType = groupType
        self.explosion = explosion
        self.messageText = messageText
        self.dramaticText = dramaticText
    
    def get_bytes(self):
        data = bytearray()

        lengthIncludingText = self.MINIMUM_LENGTH + len(self.messageText) + len(self.dramaticText)

        data.extend(self.NAME.encode('ascii'))
        data.extend(lengthIncludingText.to_bytes(4, byteorder='little', signed=True))
        data.extend(self.groupNumber.to_bytes(4, byteorder='little', signed=True))
        data.extend(self.groupType.value.to_bytes(4, byteorder='little', signed=True))
        data.extend(self.explosion.to_bytes(2, byteorder='little', signed=True))
        data.extend(self.messageText.encode('ascii'))
        data.extend(self.NULL_BYTE)
        data.extend(self.dramaticText.encode('ascii'))
        data.extend(self.NULL_BYTE)
        data.extend(self.END_MARKER)

        return data