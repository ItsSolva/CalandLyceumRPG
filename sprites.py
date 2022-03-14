import pygame
from config import *
from tilemap import *
import math
import random

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()
    
    #Use the coords, width and height to cut out a sprite from a sprite sheet
    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0,0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.players
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        
        self.x_change = 0
        self.y_change = 0
        self.last_x_shifting = 0
        self.last_y_shifting = 0

        #Attributes for abilities
        self.dash_cooldown = 0
        self.sprint_cooldown = 0
        self.sprinting_time = 0
        self.projectile_counter = 0
        self.freezed = False
        
        #Attributes for animation
        self.facing = "down"
        self.animation_loop = 1
        self.animation_speed = 0.1
        
        #Create the Player image
        self.image = self.game.character_spritesheet.get_sprite(4, 1, self.width, self.height)
             
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        #Create lists of all sprites for animation
        self.down_animations = [self.game.character_spritesheet.get_sprite(37, 1, 23, 31),
                                self.game.character_spritesheet.get_sprite(5, 2, 23, 30),
                                self.game.character_spritesheet.get_sprite(69, 2, 23, 30)]

        self.up_animations = [self.game.character_spritesheet.get_sprite(37, 97, 23, 31),
                              self.game.character_spritesheet.get_sprite(5, 98, 24, 30),
                              self.game.character_spritesheet.get_sprite(68, 98, 24, 30)]

        self.left_animations = [self.game.character_spritesheet.get_sprite(37, 33, 23, 31),
                                self.game.character_spritesheet.get_sprite(5, 34, 24, 30),
                                self.game.character_spritesheet.get_sprite(68, 34, 24, 30)]

        self.right_animations = [self.game.character_spritesheet.get_sprite(37, 65, 23, 31),
                                self.game.character_spritesheet.get_sprite(5, 66, 24, 30),
                                self.game.character_spritesheet.get_sprite(68, 66, 24, 30)]
    
    def update(self):
        if not self.freezed:
            self.movement()
            self.animate()
            
            #Move the Player object and check for collision
            self.rect.x += self.x_change
            self.collision_blocks("x")
        
            self.rect.y += self.y_change
            self.collision_blocks("y")

            self.dash_cooldown += 0.05
            
            #Save the last movement in case another object has to follow the player
            self.last_x_shifting = self.x_change
            self.last_y_shifting = self.y_change

            #Reset the movement
            self.x_change = 0
            self.y_change = 0
    
    def movement(self):
        running = False
        #create a list with all pressed buttons
        self.keys = pygame.key.get_pressed()

        #Check which button has been pressed and make the Player move that direction
        #And update the facing attribute to animate the correct direction
        if self.keys[pygame.K_LEFT] or self.keys[pygame.K_a]:
            self.x_change -= PLAYER_SPEED
            self.facing = "left"

        if self.keys[pygame.K_RIGHT] or self.keys[pygame.K_d]:
            self.x_change += PLAYER_SPEED
            self.facing = "right"

        if self.keys[pygame.K_UP] or self.keys[pygame.K_w]:
            self.y_change -= PLAYER_SPEED
            self.facing = "up"

        if self.keys[pygame.K_DOWN] or self.keys[pygame.K_s]:
            self.y_change += PLAYER_SPEED
            self.facing = "down"

        #Check wether the shift button has been pressed and wether the player is allowed to sprint
        if self.keys[pygame.K_LSHIFT] and self.sprinting_time < 10 and (self.x_change != 0 or self.y_change != 0):
            self.x_change *= 2
            self.y_change *= 2
            self.sprinting_time += 0.05
            running = True
            self.animation_speed = 0.2
        
        #Check wether the sprint cooldown has passed
        elif self.sprinting_time >= 10:
            if self.sprint_cooldown > 10:
                self.sprint_cooldown = 0
                self.sprinting_time = 0
        
        #Reduce the sprint cooldown, if the Player isn't running
        if not running: 
            self.sprint_cooldown += 0.05
            self.animation_speed = 0.1

        #Check wether the Player wants and is allowed to dash
        if self.keys[pygame.K_x]:
            if self.dash_cooldown >= 4 and (self.x_change != 0 or self.y_change != 0):
                if self.x_change != 0 and not running:
                    self.x_change *= 50
                elif self.x_change != 0:
                    self.x_change *= 25
                if self.y_change != 0 and not running:
                    self.y_change *= 50
                elif self.y_change != 0:
                    self.y_change *= 25
                self.dash_cooldown = 0        
        
    def collision_blocks(self, direction):
        if direction == "x":
            #Check for collision between player and blocks
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
            
            #Check for collision between player and enemy
            hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right

        if direction == "y":
            #Check for collision between player and blocks
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
            
            #Check for collision between player and enemy
            hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
        
    def animate(self):
        #Check which direction the Player is facing and make the Player animate according to that direction
        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.down_animations[0]
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += self.animation_speed
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        
        elif self.facing == "up":
            if self.y_change == 0:
                self.image = self.up_animations[0]
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += self.animation_speed
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        elif self.facing == "right":
            if self.x_change == 0:
                self.image = self.right_animations[0]
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += self.animation_speed
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        elif self.facing == "left":
            if self.x_change == 0:
                self.image = self.left_animations[0]
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += self.animation_speed
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        
    def delete(self):
        #Suicide
        self.kill()

class Human(pygame.sprite.Sprite):
    def __init__(self, game, x, y, image_list, text, name="", quest=False):
        self.game = game
        self._layer = HUMAN_LAYER
        self.groups = self.game.all_sprites, self.game.humans
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.x_change = 0
        self.y_change = 0

        self.name = name

        #Attributes for animation
        self.facing = "down"
        self.animation_loop = 1
        
        #Create dictionary for all sprites for animation
        self.image_list = image_list
        self.image = self.image_list["down"][0]

        #Attributes for talking
        self.text = text
        self.quest = quest
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.animate()

    def animate(self):
        #Check which direction the Player is facing and make the Player animate according to that direction
        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.image_list["down"][0]
            else:
                self.image = self.image_list["down"][math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        
        elif self.facing == "up":
            if self.y_change == 0:
                self.image = self.image_list["up"][0]
            else:
                self.image = self.image_list["up"][math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        elif self.facing == "right":
            if self.x_change == 0:
                self.image = self.image_list["right"][0]
            else:
                self.image = self.image_list["right"][math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        elif self.facing == "left":
            if self.x_change == 0:
                self.image = self.image_list["left"][0]
            else:
                self.image = self.image_list["left"][math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = HUMAN_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.x_change = 0
        self.y_change = 0

        #Attributes for animation
        self.facing = random.choice(["left", "right", "up", "down"])
        self.animation_loop = 1

        #Attributes for random movement
        self.movement_loop_x = 0
        self.movement_loop_y = 0
        self.max_travel = random.randint(10, 30)

        self.freezed = False

        self.text = "123456789012345678901234567890123456789012345678901234567890123456789012345678901"

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

class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y, sx, sy):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        
        self.image = self.game.ground_spritesheet.get_sprite(sx*32, sy*32, self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y, sx, sy):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.grounds
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        
        self.image = self.game.ground_spritesheet.get_sprite(sx * 32, sy * 32, self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Door(pygame.sprite.Sprite):
    def __init__(self, game, x, y, loc):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.doors
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        #Store location of the door object (North, East, South or West)
        self.loc = loc

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        #Create all sprites for animation
        self.image = self.game.door_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.animations = [self.game.door_spritesheet.get_sprite(32, 0, self.width, self.height),
                           self.game.door_spritesheet.get_sprite(64, 0, self.width, self.height)]
        self.animation_loop = 0
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    
    def door_open(self):
        #Animation for opening the door
        self.image = self.animations[math.floor(self.animation_loop)]
        if self.animation_loop < 1.9:
            self.animation_loop += 0.2

    def collision(self):
        #Check wether the Player has collided with the door object
        interaction = pygame.sprite.spritecollide(self, self.game.players, False)            
        if interaction:
            #Post the door opening event, with the location of the collided door
            self.game.door_event.loc = self.loc
            self.game.door_event.coords = [self.rect.x,self.rect.y]
            pygame.event.post(self.game.door_event)
    
    def update(self):
        #Allow the door to open when there are no enemies left
        if self.game.enemies_left <= 0:
            self.door_open()
        self.collision()

class Interaction(pygame.sprite.Sprite):
    def __init__(self, game, x ,y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.animation_loop = 0
        self.image = self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        #Create lists of all sprites for animation
        self.right_animations = [self.game.attack_spritesheet.get_sprite(0, 64, self.width, self.height),
                                 self.game.attack_spritesheet.get_sprite(32, 64, self.width, self.height),
                                 self.game.attack_spritesheet.get_sprite(64, 64, self.width, self.height),
                                 self.game.attack_spritesheet.get_sprite(96, 64, self.width, self.height),
                                 self.game.attack_spritesheet.get_sprite(128, 64, self.width, self.height)]

        self.down_animations = [self.game.attack_spritesheet.get_sprite(0, 32, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(32, 32, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(64, 32, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(96, 32, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(128, 32, self.width, self.height)]

        self.left_animations = [self.game.attack_spritesheet.get_sprite(0, 96, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(32, 96, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(64, 96, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(96, 96, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(128, 96, self.width, self.height)]

        self.up_animations = [self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height),
                              self.game.attack_spritesheet.get_sprite(32, 0, self.width, self.height),
                              self.game.attack_spritesheet.get_sprite(64, 0, self.width, self.height),
                              self.game.attack_spritesheet.get_sprite(96, 0, self.width, self.height),
                              self.game.attack_spritesheet.get_sprite(128, 0, self.width, self.height)]

    def update(self):
        self.animate()
        self.collide()
    
    def collide(self):
        #Check wether the Player interacted with a human object
        hits = pygame.sprite.spritecollide(self, self.game.humans, False)
        if hits:
            #Check wether the human object has dialogue
            if len(hits[0].text) > 0 and hits[0].quest:
                self.game.talking_event.message = True     
            elif len(hits[0].text) > 0:  
                self.game.talking_event.message = False
            
            #Post the talking event with the dialogue text
            self.game.talking_event.status = "start"
            self.game.talking_event.entity = hits[0]
            self.game.talking_event.txt = hits[0].text
            pygame.event.post(self.game.talking_event)

            self.kill()

                
    def animate(self):
        #Check which direction the Player is facing and create the animation according to that direction
        direction = self.game.player.facing

        if direction == "up":
            self.image = self.up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            
            #Delete the interaction object when the animation has finished
            if self.animation_loop >= 5:
                self.kill()
        
        if direction == "down":
            self.image = self.down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            
            #Delete the interaction object when the animation has finished
            if self.animation_loop >= 5:
                self.kill()
        
        if direction == "left":
            self.image = self.left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5

            #Delete the interaction object when the animation has finished
            if self.animation_loop >= 5:
                self.kill()
        
        if direction == "right":
            self.image = self.right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5

            #Delete the interaction object when the animation has finished
            if self.animation_loop >= 5:
                self.kill()

class Shuriken(pygame.sprite.Sprite):
    def __init__(self, game, x ,y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.width = TILE_SIZE/2
        self.height = TILE_SIZE/2

        self.velocity()        

        self.animation_loop = 0
        self.life_countdown = 0
        self.game.player.projectile_counter += 0

        self.image = self.game.shuriken_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        #Create lists of all sprites for animation
        self.animations = [self.game.shuriken_spritesheet.get_sprite(0, 0, self.width, self.height),
                           self.game.shuriken_spritesheet.get_sprite(17, 0, self.width, self.height),
                           self.game.shuriken_spritesheet.get_sprite(34, 0, self.width, self.height),
                           self.game.shuriken_spritesheet.get_sprite(51, 0, self.width, self.height)]

    def update(self):
        self.animate()
        self.collide()
        self.movement()
    
    def collide(self):
        #Check wether the shuriken has hit an enemy
        hits = pygame.sprite.spritecollide(self, self.game.enemies, True)

        #Reduce the amount of enemies and projectiles and delete the shuriken when the shuriken hit an enemy
        if hits:
            self.game.enemies_left -= 1
            self.game.player.projectile_counter -= 1
            self.kill()
        
        #Delete the shuriken if it hasn't hit anything for too long
        if self.life_countdown >= 20:
            self.game.player.projectile_counter -= 1
            self.kill()

        self.life_countdown += 0.1
    
    def movement(self):

        self.pos+=self.vel
        self.rect.x, self.rect.y = self.pos
    
    def velocity(self):
        #Get the distant between the mouse and the player (who is in the middle of the screen)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        x = WIN_WIDTH/2
        y = WIN_HEIGHT/2
        self.dx = int(mouse_x - x) / 50
        self.dy = int(mouse_y - y) / 50

        #Create vectors of the position and direction of movement of the shuriken
        vec = pygame.math.Vector2
        self.pos=vec(self.game.player.rect.x, self.game.player.rect.y)
        self.vel=vec(self.dx, self.dy) 

    def animate(self):
        self.image = self.animations[math.floor(self.animation_loop)]
        self.animation_loop += 0.5
        if self.animation_loop >= 4:
            self.animation_loop = 0

class Textbox(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width=700, height=200, text_color=(0,0,0), txt="", txt_size=15, follow=False):
        self.game = game
        self._layer = TOP_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        #This attritbute is to check if the textbox has to follow the player
        self.follow = follow

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        #Create the text object to display on top of the textbox object
        self.txt_size = txt_size
        self.font = pygame.font.Font("DroidSansMono.ttf", self.txt_size)
        self.text_color = text_color
        self.txt = txt
        self.current_page = 0
        
        #Create the textbox image
        self.image = pygame.image.load("img/dialogue_box_basic.png").convert()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=[x,y])
        
        #Display the text on top of the textbox
        for i, line in enumerate(self.txt):
            print(line)
            self.txt_surf = self.font.render(" ".join(line), True, self.text_color)
            self.txt_rect = self.txt_surf.get_rect(topleft=(40, 40 + 25*i)) 
            self.image.blit(self.txt_surf, self.txt_rect)

    def update(self):
        self.skip()
        if self.follow:
            self.follow_player()

    def follow_player(self):
        #Make the textbox move the same direction as the Player
        self.rect.x += self.game.player.last_x_shifting
        self.rect.y += self.game.player.last_y_shifting
    
    def skip(self):
        #Check wether the spacebar has been pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            #Post the talking event with "stop" as status, which makes the dialogue stop
            self.game.talking_event.status = "stop"
            pygame.event.post(self.game.talking_event)

            #Delete the textbox 
            self.kill()

class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font("pixel_font.ttf", fontsize)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg

        self.image = pygame.image.load("img/button.png")
        self.image = pygame.transform.scale(self.image, (300,70))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, False, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False
