import pygame
from config import *
from tilemap import *
import math
import random

class Human(pygame.sprite.Sprite):
    def __init__(self, game, x, y, type, facing):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.type = type

        self.x_change = 0
        self.y_change = 0
        self.freezed = False

        self.facing = facing
        self.animation_loop = 1
        self.movement_loop_x = 0
        self.movement_loop_y = 0
        self.max_travel = random.randint(10, 30)

        self.text = "Hello, I'm Joe, Welcome to the Caland, I mean... YOUR DEATH"

        self.image = self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.down_animations = [self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height),
                                self.game.enemy_spritesheet.get_sprite(35, 2, self.width, self.height),
                                self.game.enemy_spritesheet.get_sprite(68, 2, self.width, self.height)]

        self.up_animations = [self.game.enemy_spritesheet.get_sprite(3, 34, self.width, self.height),
                              self.game.enemy_spritesheet.get_sprite(35, 34, self.width, self.height),
                              self.game.enemy_spritesheet.get_sprite(68, 34, self.width, self.height)]

        self.left_animations = [self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height),
                                self.game.enemy_spritesheet.get_sprite(35, 98, self.width, self.height),
                                self.game.enemy_spritesheet.get_sprite(68, 98, self.width, self.height)]

        self.right_animations = [self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height),
                                 self.game.enemy_spritesheet.get_sprite(35, 66, self.width, self.height),
                                 self.game.enemy_spritesheet.get_sprite(68, 66, self.width, self.height)]

    def update(self):
        if not self.freezed:
            if not self.teacher:
                self.movement()
                self.animate()

            self.rect.x += self.x_change 
            self.collision_blocks("x")

            self.rect.y += self.y_change
            self.collision_blocks("y")

            self.x_change = 0
            self.y_change = 0
    
    def movement(self):
        if self.facing == "left":
            self.x_change -= ENEMY_SPEED
            self.movement_loop_x -= 1
            if self.movement_loop_x <= -self.max_travel:
                self.facing = random.choice(["left", "right", "up", "down"])

        if self.facing == "right":
            self.x_change += ENEMY_SPEED
            self.movement_loop_x += 1
            if self.movement_loop_x >= self.max_travel:
                self.facing = random.choice(["left", "right", "up", "down"])

        if self.facing == "down":
            self.y_change += ENEMY_SPEED
            self.movement_loop_y += 1
            if self.movement_loop_y >= self.max_travel:
                self.facing = random.choice(["left", "right", "up", "down"])

        if self.facing == "up":
            self.y_change -= ENEMY_SPEED
            self.movement_loop_y -= 1
            if self.movement_loop_y <= -self.max_travel:
                self.facing = random.choice(["left", "right", "up", "down"])
    
    def collision_blocks(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    
        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def animate(self):
        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.down_animations[0]
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        
        elif self.facing == "up":
            if self.y_change == 0:
                self.image = self.up_animations[0]
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        elif self.facing == "right":
            if self.x_change == 0:
                self.image = self.right_animations[0]
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        elif self.facing == "left":
            if self.x_change == 0:
                self.image = self.left_animations[0]
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
    
    def delete(self):
        self.kill()
