import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw
# https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html

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

typeNames = {
    0 : 'empty package (story element)',
    1 : 'machine gun ammo',
    2 : 'mines',
    3 : 'missile ammo',
    6 : 'monkey wrench (repair)',
    7 : 'monkey wrench (repair)',
    10 : 'armor add',
    11 : 'armor add',
    13 : 'machine gun',
    14 : 'missile launcher',
    15 : 'smoke screen', 
    16 : 'mine dropper',
    17 : 'oil slick',
    18 : 'shield',
    19 : 'military radar',
    20 : 'hopper',
    21 : 'airfoil',
    22 : 'bomb'
}

MAP_DIM = 128
SCALE = 16

for filePath in files:
    filePath = basePath + filePath

    print('='*64)
    print(filePath)

    pickupMap = Image.new('RGB', (SCALE*MAP_DIM, SCALE*MAP_DIM), color = 'white')
    draw = ImageDraw.Draw(pickupMap)
    
    with open(filePath, 'rb') as file:
        data = file.read();
        byteCount = len(data);

        for offset in range(byteCount - 4):
            marker = data[offset:offset+4]
            if marker == b'KAPA': # APAK = a package?
                posPackType = offset + 8;
                posType = offset + 12;
                posPickupX = offset + 20
                posPickupY = offset + 22
                posDeliveryX = offset + 24
                posDeliveryY = offset + 26

                packType = int.from_bytes(data[posPackType:posPackType+4], byteorder='little')

                pType = int.from_bytes(data[posType:posType+4], byteorder='little', signed=True)

                pickupX = int.from_bytes(data[posPickupX:posPickupX+2], byteorder='little')
                pickupY = int.from_bytes(data[posPickupY:posPickupY+2], byteorder='little')
                deliveryX = int.from_bytes(data[posDeliveryX:posDeliveryX+2], byteorder='little')
                deliveryY = int.from_bytes(data[posDeliveryY:posDeliveryY+2], byteorder='little')

                description = ''
                descIndex = offset + 28;
                while (int.from_bytes(data[descIndex:descIndex+1], byteorder='little') != 1):
                    description = description + chr(data[descIndex])
                    descIndex = descIndex + 1
                
                if (not description):
                    description = "N/A"

                #print(f"Package at ({pickupX},{pickupY}) to ({deliveryX},{deliveryY})")

                if (True):#pickupX == deliveryX and pickupY == deliveryY):
                    #draw.point((pickupX,pickupY), fill = 'red')

                    x = SCALE*pickupX;
                    y = SCALE*pickupY;

                    draw.rectangle([(x,y),
                                    (x+SCALE-1, y+SCALE-1)], fill = 'red')

                    typeName = '?'

                    if pType in typeNames:
                        typeName = typeNames[pType]

                    print(f"Package type: {packType}. Location: ({pickupX},{pickupY}). Money/item: {pType} ({typeName}). Description: {description}")

                    draw.text((x,y), f"{pType}", fill = 'black')

    # Save map
    scriptPath = os.path.dirname(os.path.realpath(sys.argv[0]))
    inFile = Path(filePath).stem
    outName = scriptPath + "/" + inFile + "-pickup-map.png"
    pickupMap.save(outName, "PNG")
