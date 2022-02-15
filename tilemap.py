import random
import pygame
from config import *

class Map:
    def __init__(self, filename):
        self.data = []
        self.file = filename
        with open(self.file, "rt") as f:
            for line in f:
                if "\n" in line:
                    line = line[0: int(len(line) - 1)]
                    self.data.append(line)
                else:
                    self.data.append(line)

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILE_SIZE
        self.height = self.tileheight * TILE_SIZE

class RandomMapMaker:
    def __init__(self, width, height):
        self.data = []
        self.tilewidth = width
        self.tileheight = height
        self.width = self.tilewidth * TILE_SIZE
        self.height = self.tileheight * TILE_SIZE

        items = []
        for x in range(300):
            items.append(".")
        for x in range(10):
            items.append("B")
        for x in range(1):
            items.append("E")
        
        for x in range(1):
            items.append("L")

        row = ""
        map_file = open("random_map.txt", "w")

        door_x = random.randint(3, self.tilewidth-3)
        door_y = random.randint(1, self.tileheight-3)
        for y in range(self.tileheight):
            for x in range(self.tilewidth):
                if y == 0 or x == 0 or y == self.tileheight-1 or x == self.tilewidth-1:
                    row += "B"
                elif x == round(self.tilewidth/2) and y == round(self.tileheight/2) and level == 0:
                    row += "P"
                else:
                    if x == door_x and y == door_y:
                        row += "D"
                    else:
                        i = random.choice(items)                 
                        row += i
            map_file.write(row)
            map_file.write("\n")                
            self.data.append(row)
            row = ""
        map_file.close()
        

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)
    
    def update(self, target):
        x = -target.rect.x + int(WIN_WIDTH / 2)
        y = -target.rect.y + int(WIN_HEIGHT / 2)

       # x = min(0, x)
       # y = min(0, y)
       # x = max(-(self.width - WIN_WIDTH), x)
       # y = max(-(self.height - WIN_HEIGHT), y)
        self.camera = pygame.Rect(x, y, self.width, self.height)
    
    def set_width_height(self, width, height):
        self.width = width
        self.height = height

map_loc = [
    [".",    "NL",   "BIO",  "INF"  ],
    ["hall0","hall1","hall2","hall3"],
    [".",    "X",    "X",    "X"    ]
]

