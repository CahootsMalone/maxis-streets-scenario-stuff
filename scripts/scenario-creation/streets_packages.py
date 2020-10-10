from enum import Enum
from streets_common import StreetsCommonSingleNumber

class StreetsPackageType(Enum):
    NORMAL = 0
    MONEY = 1
    PICKUP = 2

class StreetsPickupType(Enum):
    EMPTY = 0
    BULLETS = 1
    MINES = 2
    MISSILES = 3
    OIL_CANS = 4
    SMOKE_CANISTERS = 5
    MONKEY_WRENCH_1 = 6
    MONKEY_WRENCH_2 = 7
    GAS_1 = 8
    GAS_2 = 9
    ARMOR_ADD_1 = 10
    ARMOR_ADD_2 = 11
    BATTERY = 12
    MACHINE_GUN = 13
    MISSILE_LAUNCHER = 14
    SMOKE_SCREEN = 15
    MINE_DROPPER = 16
    OIL_SLICK = 17
    SHIELD = 18
    MILITARY_RADAR = 19
    HOPPER = 20
    AIRFOIL = 21
    BOMB = 22

class StreetsPackageCount:
    NAME = 'GKP#'

    def __init__(self, packageCount: int):
        self.packageCount = packageCount

    def get_bytes(self):
        return StreetsCommonSingleNumber(self.NAME, self.packageCount).get_bytes()

class StreetsPackage:
    NAME = 'KAPA'

    STRING_DELIMITER = b'\x01'
    END_MARKER = b'\xCD\xCD\xCD\xCD'

    def __init__(self, 
        packageType: StreetsPackageType, 
        packageReward: int, 
        eventGroup: int,
        pickupX: int,
        pickupY: int,
        deliveryX: int,
        deliveryY: int,
        pickupMessageText: str,
        deliveryMessageText: str,
        pickupDramaticText: str,
        deliveryDramaticText: str,
        pickupSound: str,
        deliverySound: str):
        self.packageType = packageType
        self.packageReward = packageReward
        self.eventGroup = eventGroup
        self.pickupX = pickupX
        self.pickupY = pickupY
        self.deliveryX = deliveryX
        self.deliveryY = deliveryY
        self.pickupMessageText = pickupMessageText
        self.deliveryMessageText = deliveryMessageText
        self.pickupDramaticText = pickupDramaticText;
        self.deliveryDramaticText = deliveryDramaticText
        self.pickupSound = pickupSound
        self.deliverySound = deliverySound
    
    def get_bytes(self):

        length = 38 + len(self.pickupMessageText) + len(self.deliveryMessageText) + len(self.pickupDramaticText) + len(self.deliveryDramaticText) + len(self.pickupSound) + len(self.deliverySound)

        data = bytearray()

        data.extend(self.NAME.encode('ascii'))
        data.extend(length.to_bytes(4, byteorder='little', signed=True))
        data.extend(self.packageType.value.to_bytes(4, byteorder='little', signed=True))
        data.extend(self.packageReward.to_bytes(4, byteorder='little', signed=True))
        data.extend(self.eventGroup.to_bytes(4, byteorder='little', signed=True))
        data.extend(self.pickupX.to_bytes(2, byteorder='little', signed=True))
        data.extend(self.pickupY.to_bytes(2, byteorder='little', signed=True))
        data.extend(self.deliveryX.to_bytes(2, byteorder='little', signed=True))
        data.extend(self.deliveryY.to_bytes(2, byteorder='little', signed=True))
        data.extend(self.pickupMessageText.encode('ascii'))
        data.extend(self.STRING_DELIMITER)
        data.extend(self.deliveryMessageText.encode('ascii'))
        data.extend(self.STRING_DELIMITER)
        data.extend(self.pickupDramaticText.encode('ascii'))
        data.extend(self.STRING_DELIMITER)
        data.extend(self.deliveryDramaticText.encode('ascii'))
        data.extend(self.STRING_DELIMITER)
        data.extend(self.pickupSound.encode('ascii'))
        data.extend(self.STRING_DELIMITER)
        data.extend(self.deliverySound.encode('ascii'))
        data.extend(self.STRING_DELIMITER)
        data.extend(self.END_MARKER)

        return data