import os
import sys
from pathlib import Path
import re

def PrintEventHeader():
    colWidth = 8
    col1 = 'Size'
    col2 = 'Group'
    col3 = 'Type'
    col4 = 'v1'
    col5 = 'v2'
    col6 = 'v3'
    col7 = 'v4'
    col8 = 'xTL'
    col9 = 'yTL'
    col10 = 'xBR'
    col11 = 'yBR'
    print(f'{col1:{colWidth}}|{col2:{colWidth}}|{col3:{colWidth}}|{col4:{colWidth}}|{col5:{colWidth}}|{col6:{colWidth}}|{col7:{colWidth}}|{col8:{colWidth}}|{col9:{colWidth}}|{col10:{colWidth}}|{col11:{colWidth}}|')

def PrintEvent(data, offset):
    colWidth = 8
    size = int.from_bytes(data[offset+4:offset+8], byteorder='little')
    eventGroupNumber = int.from_bytes(data[offset+8:offset+12], byteorder='little')
    type = int.from_bytes(data[offset+12:offset+16], byteorder='little')
    v1 = int.from_bytes(data[offset+16:offset+20], byteorder='little', signed=True)
    v2 = int.from_bytes(data[offset+20:offset+24], byteorder='little', signed=True)
    v3 = int.from_bytes(data[offset+24:offset+28], byteorder='little', signed=True)
    v4 = int.from_bytes(data[offset+28:offset+32], byteorder='little', signed=True)
    xTL = int.from_bytes(data[offset+32:offset+36], byteorder='little', signed=True)
    yTL = int.from_bytes(data[offset+36:offset+40], byteorder='little', signed=True)
    xBR = int.from_bytes(data[offset+40:offset+44], byteorder='little', signed=True)
    yBR = int.from_bytes(data[offset+44:offset+48], byteorder='little', signed=True)

    # if (type != 1):
    #     return

    print(f'{size:{colWidth}}|{eventGroupNumber:{colWidth}}|{type:{colWidth}}|{v1:{colWidth}}|{v2:{colWidth}}|{v3:{colWidth}}|{v4:{colWidth}}|{xTL:{colWidth}}|{yTL:{colWidth}}|{xBR:{colWidth}}|{yBR:{colWidth}}|')

    #print(data[offset+4:offset+size].hex('|', -4))

    eventString = (data[offset:offset+size]).decode('ascii', 'replace')
    eventString = re.sub(r'[^\x20-\x7e]',r'_', eventString)
    print(eventString)

    uniqueTypes.add(type)
    if (True):
        uniqueV1.add(v1)
        uniqueV2.add(v2)
        uniqueV3.add(v3)
        uniqueV4.add(v4)

def PrintEventGroupHeader():
    colWidth = 8
    col1 = 'Size'
    col2 = 'Number'
    col3 = 'v1'
    col4 = 'v2'

    print('Event Groups')
    print(f'{col1:{colWidth}}|{col2:{colWidth}}|{col3:{colWidth}}|{col4:{colWidth}}')

def PrintEventGroup(data, offset):
    colWidth = 8
    length = int.from_bytes(data[offset+4:offset+8], byteorder='little')
    number = int.from_bytes(data[offset+8:offset+12], byteorder='little')
    v1 = int.from_bytes(data[offset+12:offset+16], byteorder='little')
    v2 = int.from_bytes(data[offset+16:offset+18], byteorder='little')

    print(f'{length:{colWidth}}|{number:{colWidth}}|{v1:{colWidth}}|{v2:{colWidth}}')
    
    if (length != 22):
        eventString = (data[offset:offset+length]).decode('ascii', 'replace')
        eventString = re.sub(r'[^\x20-\x7e]',r'_', eventString)
        print(eventString)

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

uniqueTypes = set()
uniqueV1 = set()
uniqueV2 = set()
uniqueV3 = set()
uniqueV4 = set()

earlyCutOutCounter = 0
for filePath in files:
    # if earlyCutOutCounter > 17:
    #     break
    earlyCutOutCounter = earlyCutOutCounter + 1

    filePath = basePath + filePath

    print('='*64)
    print(filePath)

    with open(filePath, 'rb') as file:
        data = file.read();
        byteCount = len(data);

        offset = 0
        foundEvents = False

        markerEventCount = b'SVE#'
        markerEvent = b'TNVE'
        marketEventGroup = b'GTVE'

        eventCount = 0

        firstEventGroup = True

        while True:
            marker = data[offset:offset+4]
            length = int.from_bytes(data[offset+4:offset+8], byteorder='little')
            
            if marker == markerEventCount:
                eventCount = int.from_bytes(data[offset+8:offset+12], byteorder='little')
                print(f"There are {eventCount} events.")
                PrintEventHeader()
                if eventCount == 0:
                    break
                #foundEvents = True
                offset = offset + length
            elif marker == markerEvent:
                PrintEvent(data, offset)
                offset = offset + length
            elif marker == marketEventGroup:
                if firstEventGroup:
                    PrintEventGroupHeader()
                    firstEventGroup = False
                    foundEvents = True
                PrintEventGroup(data, offset)
                offset = offset + length
            else:
                if foundEvents:
                    break
                offset = offset + 1

print(f'Type: {uniqueTypes}')
print(f'v1: {uniqueV1}')
print(f'v2: {uniqueV2}')
print(f'v3: {uniqueV3}')
print(f'v4: {uniqueV4}')




