from enum import Enum

class StreetsAiType(Enum):
    COP = 0
    HUNTER = 1
    RACER = 2
    ROGUE = 3
    SPEEDER = 4
    COURIER = 5
    BOSS = 6
    ALLY = 7

class StreetsCommonSingleNumber:
    LENGTH = 12

    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value
    
    def get_bytes(self):
        data = bytearray()

        data.extend(self.name.encode('ascii'))
        data.extend(self.LENGTH.to_bytes(4, byteorder='little', signed=True))
        data.extend(self.value.to_bytes(4, byteorder='little', signed=True))

        return data

class StreetsCommonString:
    NULL_BYTE = b'\x00'

    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value
    
    def get_bytes(self):
        length = 9 + len(self.value)

        data = bytearray()

        data.extend(self.name.encode('ascii'))
        data.extend(length.to_bytes(4, byteorder='little', signed=True))
        data.extend(self.value.encode('ascii'))
        data.extend(self.NULL_BYTE)

        return data