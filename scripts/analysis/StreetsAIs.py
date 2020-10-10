import os
import sys
from pathlib import Path
import re

basePath = 'C:/SimStreetsX/StreetsCD/scenarios/'

files = ["Doofus/zippy1.scn",
         "Doofus/zippy2.scn",
         "Doofus/zippy3.scn",
         "Doofus/zippy4.scn",
         "Doofus/zippy5.scn",
         "Doofus/zippy6.scn",
         "Galahad/Gal1.scn",
         "Galahad/Gal2.scn",
         "Galahad/Gal3.scn",
         "Galahad/Gal4.scn",
         "Galahad/Gal5.scn",
         "Galahad/Gal6.scn",
         "Granny/Granny1.scn",
         "Granny/Granny2.scn",
         "Granny/Granny3.scn",
         "Granny/Granny4.scn",
         "Granny/Granny5.scn",
         "Granny/Granny6.scn",
         "Movie/Apocal.scn",
         "Movie/Arena.scn",
         "Movie/DeathMall.scn",
         "Movie/DrugRaid.scn",
         "Movie/FWar.scn",
         "Movie/Glory.scn",
         "Movie/Mayhem.scn",
         "Movie/Niceguy.scn",
         "Race/Race01.scn",
         "Race/Race02.scn",
         "Race/Race03.scn",
         "Race/Race04.scn",
         "Race/Race05.scn",
         "Race/Race06.scn",
         "Race/Race07.scn",
         "Race/Race08.scn",
         "Race/Race09.scn",
         "Race/Race10.scn"]



def PrintAiHeader():
    colWidth = 8
    col1 = 'Length'
    col2 = 'Quantity'
    col3 = 'Respawn'
    col4 = 'AI type'
    col5 = 'SpawnX'
    col6 = 'SpawnY'
    col7 = '?1'
    col8 = 'SpwnTrig'
    col9 = 'SpTmOrTg' # Spawn time or trigger number
    col10 = 'Speed'
    col11 = '?2'
    col12 = 'TargX'
    col13 = 'TargY'
    col14 = 'Level'
    col15 = 'Vehicle'
    print(f'{col1:{colWidth}}|{col2:{colWidth}}|{col3:{colWidth}}|{col4:{colWidth}}|{col5:{colWidth}}|{col6:{colWidth}}|{col7:{colWidth}}|{col8:{colWidth}}|{col9:{colWidth}}|{col10:{colWidth}}|{col11:{colWidth}}|{col12:{colWidth}}|{col13:{colWidth}}|{col14:{colWidth}}|{col15:{colWidth}}|')

aiTypes = [
    'Cop',
    'Hunter',
    'Racer',
    'Rogue',
    'Speeder',
    'Courier',
    'Boss',
    'Ally',
]

def PrintAi(data, offset):
    colWidth = 8
    size = int.from_bytes(data[offset+4:offset+8], byteorder='little')
    quantity = int.from_bytes(data[offset+8:offset+12], byteorder='little')
    respawn = int.from_bytes(data[offset+12:offset+16], byteorder='little')
    aiType = int.from_bytes(data[offset+16:offset+20], byteorder='little', signed=True)
    spawnX = int.from_bytes(data[offset+20:offset+22], byteorder='little', signed=True)
    spawnY = int.from_bytes(data[offset+22:offset+24], byteorder='little', signed=True)
    v1 = int.from_bytes(data[offset+24:offset+28], byteorder='little', signed=True)
    spawnType = int.from_bytes(data[offset+28:offset+32], byteorder='little', signed=True)
    spawnInfo = int.from_bytes(data[offset+32:offset+36], byteorder='little', signed=True)
    speed = int.from_bytes(data[offset+36:offset+40], byteorder='little', signed=True)
    v2 = int.from_bytes(data[offset+40:offset+44], byteorder='little', signed=True)
    targX = int.from_bytes(data[offset+44:offset+46], byteorder='little', signed=True)
    targY = int.from_bytes(data[offset+46:offset+48], byteorder='little', signed=True)
    v3 = int.from_bytes(data[offset+48:offset+52], byteorder='little', signed=True)
    vehicle = int.from_bytes(data[offset+52:offset+56], byteorder='little', signed=True)

    uniqueV1.add(v1)
    uniqueV2.add(v2)
    uniqueV3.add(v3)

    aiType = aiTypes[aiType]

    # if aiType != 'Ally':
    #     return

    #if spawnX == targX and spawnY == targY:
    #    return
    #if spawnX != -1 and spawnY != -1:
    #    return

    #if v1 == 0:
    #    return

    #if speed != v2:
    #    return

    row = f'{size:{colWidth}}|' \
            f'{quantity:{colWidth}}|' \
            f'{respawn:{colWidth}}|' \
            f'{aiType:{colWidth}}|' \
            f'{spawnX:{colWidth}}|' \
            f'{spawnY:{colWidth}}|' \
            f'{v1:{colWidth}}|' \
            f'{spawnType:{colWidth}}|' \
            f'{spawnInfo:{colWidth}}|' \
            f'{speed:{colWidth}}|' \
            f'{v2:{colWidth}}|' \
            f'{targX:{colWidth}}|' \
            f'{targY:{colWidth}}|' \
            f'{v3:{colWidth}}|' \
            f'{vehicle:{colWidth}}|'
    
    print(row)

uniqueV1 = set()
uniqueV2 = set()
uniqueV3 = set()

for filePath in files:
    filePath = basePath + filePath

    print('='*64)
    print(filePath)

    with open(filePath, 'rb') as file:
        data = file.read();
        byteCount = len(data);

        offset = 0
        foundAi = False

        markerAiCount = b'SIA#'
        markerAi = b'IANA'

        aiCount = 0

        firstEventGroup = True

        while True:
            marker = data[offset:offset+4]
            length = int.from_bytes(data[offset+4:offset+8], byteorder='little')
            
            if marker == markerAiCount:
                aiCount = int.from_bytes(data[offset+8:offset+12], byteorder='little')
                print(f"There are {aiCount} events.")
                PrintAiHeader()
                if aiCount == 0:
                    break
                foundAi = True
                offset = offset + length
            elif marker == markerAi:
                PrintAi(data, offset)
                offset = offset + length
            else:
                if foundAi:
                    break
                offset = offset + 1

print(f'v1: {sorted(uniqueV1)}')
print(f'v2: {sorted(uniqueV2)}')
print(f'v3: {sorted(uniqueV3)}')