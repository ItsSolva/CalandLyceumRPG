import pygame
from sprites import *
from teachers import *
from config import *
from tilemap import *
from data import *
import webbrowser
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("DroidSansMono.ttf", 32)
        self.running = True
        
        #Load all the spritesheets
        self.character_spritesheet = Spritesheet("img/Entities/characterr.png")
        self.ground_spritesheet = Spritesheet("img/Map/ground_spritesheet.png")
        self.door_spritesheet = Spritesheet("img/Map/door_spritesheet.png")
        self.enemy_spritesheet = Spritesheet("img/Entities/enemy.png")
        self.attack_spritesheet = Spritesheet("img/Overig/attack.png")
        self.shuriken_spritesheet = Spritesheet("img/Overig/shuriken.png")
        self.intro_background = pygame.image.load("img/UI Elements/raspberryham_UI_MAIN_MENU.png").convert()

        #Create some variables
        self.enemies_left = 0
        self.player_loc = [1,0]
        self.current_tutorial_index = 0
        self.state = "playing"

        #Create all the event objects
        self.talking = pygame.USEREVENT+1
        self.talking_event = pygame.event.Event(self.talking, status="start", txt="", message=False, entity=None)
        self.open_door = pygame.USEREVENT+2
        self.door_event = pygame.event.Event(self.open_door, loc="", coords = [])
        
    def createTilemap(self, map):
        #Loop through all the items of the map and check what type of tile it is
        for i, row in enumerate(map.data):
            for j, column in enumerate(row):
                g = Ground(self, j, i, 1, 0)
                #Create a type of wall tile object
                if column == "X":
                    Block(self, j, i, 3, 2)
                #Create a type of ground path tile object
                if column == "=":
                    Ground(self, j, i, 3, 0)
                #Create a type of wall tile object
                if column == "Q":
                    Block(self, j, i, 5, 2)
                #Create a window glass tile object
                if column == "G":
                    Ground(self, j, i, 4, 3)
                #Create a type of wall tile object
                if column == "W":
                    Block(self, j, i, 1, 2)
                #Create a type of ground path tile object
                if column == "-":
                    Ground(self, j, i, 2, 4)
                #Create an table object
                if column == "T":
                    Table(self, j, i)
                #Create an enemy object
                if column == "E":
                    Enemy(self, j, i)                  
                    self.enemies_left += 1
                #Create a door object and check what direction it's located
                if column == "D":
                    if j == 1:
                        Door(self, j, i, "west")
                    elif i == 1:
                        Door(self, j, i, "north")
                    elif j == map.tilewidth-2:
                        Door(self, j, i, "east")
                    elif i == map.tileheight-2:
                        Door(self, j, i, "south")
                    else:
                        Door(self, j, i, "")
                #Create a tutorial text object
                if column == "U":
                    g.kill()
                    Block(self, j, i, 0, 6)
                    Textbox(self, j*30, i*50, txt=self.create_dialogue_text(TUTORIAL_TEXT[self.current_tutorial_index], entity="text"), width=375, height=100, txt_size=15, local=True)
                    self.current_tutorial_index += 1
                #Create the Player object
                if column == "P":
                    Ground(self, j, i, 5, 1)
                    self.player = Player(self, j, i)
                #Create an human object
                if column == "F":
                    Human(self, j, i, create_human_spritesheet("img/Entities/male.png"), groet, name="human", quest=True)
                #Create the teacher object Hamersveld
                if column == "H":
                    Human(self, j, i, create_human_spritesheet("img/Entities/hamersveld.png"), groet, name="ham")
                #Create the teacher object Luken
                if column == "L":
                    Human(self, j, i, create_human_spritesheet("img/Entities/luken.png"), groet, name="luk")
                #Create an invisible barrier
                if column == "~":
                    g.kill()
                    Block(self, j, i, 0, 6)
    
    def create_dialogue_text(self, txt, entity):
        if entity == "ham":
            if map_loc[self.player_loc[0]][self.player_loc[1]] == "INF":
                txt_split = random.choice(groet) + ", welkom in het informatica lokaal!"
            elif map_loc[self.player_loc[0]][self.player_loc[1]] == "hall3":
                txt_split = "Het informatica lokaal is hier binnen. Hop, naar binnen!"
            else:
                txt_split = random.choice(groet) + ", ik ben meneer Hamersveld. Kom maar eens langs bij mijn lokaal!"
        elif entity == "luk":
            if map_loc[self.player_loc[0]][self.player_loc[1]] == "NL":
                txt_split = random.choice(groet) + ", welkom in het Nederlands lokaal!"
            elif map_loc[self.player_loc[0]][self.player_loc[1]] == "BIO":
                txt_split = random.choice(groet) + ", welkom in het biologie lokaal!"
            else:
                txt_split = random.choice(groet) + ", kom maar eens langs bij mijn lokaal!"
        elif entity == "text":
            txt_split = txt 
        else:
            txt_split = random.choice(groet)

        wordcount = 0
        text = []
        line = []

        #Max length per line is 55 characters
        if len(txt_split) > 60:
            txt_split = txt_split.split()
            #Loop through all the words
            for word in txt_split:
                #Check wether the max length has been reached
                if len(word) + wordcount >= 60:
                    #If the max length has been reached, check if a new line can be added to this page, add the line to the text list, empty the line, and reset the wordcount
                    text.append(line)
                    line = []
                    wordcount = 0

                #Add the word to the line
                wordcount += len(word)
                line.append(word)

            #Add the last line to the text list
            text.append(line)

        else:
            text.append(txt_split.split())

        return text
    
    #This gets excuted ONCE when the game starts
    def new(self):        
        #Create some variables
        self.playing = True
        self.map = Map("maps/0/hall0.txt")

        #Create all sprites groups
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.players = pygame.sprite.LayeredUpdates()
        self.humans = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.doors = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.grounds = pygame.sprite.LayeredUpdates()
        self.textboxes = pygame.sprite.LayeredUpdates()

        #Set the camera to the following width/height
        self.camera = Camera(self.map.width, self.map.height)
        
        #Create the map
        self.createTilemap(self.map)

    def events(self):
        #game loop events
        for event in pygame.event.get():
            #Check wether the close button has been pressed
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.intro_screen()
                if event.key == pygame.K_SPACE and self.state == "talking":
                    #Post the talking event with "stop" as status, which makes the dialogue stop
                    self.talking_event.status = "stop"
                    pygame.event.post(self.talking_event)

                    #Delete the textbox 
                    for t in self.textboxes:
                        t.destroy()
                
            #Check wether a talking event has been triggered
            if event.type == self.talking:
                #Create a textbox object
                if event.status == "start":
                    self.state = "talking"
                    if event.message:
                        txt = self.create_dialogue_text(event.txt, entity=event.entity.name)
                        Textbox(self, self.player.rect.x - 150, self.player.rect.y + 150, width = 300, height= 100, txt=txt, follow=event.message)
                    else:
                        self.player.freezed = True
                        for e in self.enemies:
                            e.freezed = True
                        txt = self.create_dialogue_text(event.txt, entity=event.entity.name)
                        Textbox(self, self.player.rect.x - 400, self.player.rect.y + 150, width = 800, height= 200, txt=txt)                
                
                #Delete the textbox and allow every sprite to move again
                else:
                    self.state = "playing"
                    self.player.freezed = False
                    for e in self.enemies:
                        e.freezed = False
            
            #Checkw wether a door opening event has been triggered
            if event.type == self.open_door:
                self.current_tutorial_index = 0
                #Delete all current tiles and sprites
                for b in self.all_sprites:
                    b.kill()
                
                #Check which direction the next room should be
                if event.loc == "east":
                    self.player_loc[1] += 1
                elif event.loc == "west":
                    self.player_loc[1] -= 1
                elif event.loc == "north":
                    self.player_loc[0] -= 1
                elif event.loc == "south":
                    self.player_loc[0] += 1
                else:
                    self.player_loc[1] = 1

                #Load the map file of the new room and load the new map
                m = Map(f"maps/{self.player_loc[1]}/{map_loc[self.player_loc[0]][self.player_loc[1]]}.txt")
                self.createTilemap(m)

                #Make the player spawn in front of the next door
                if event.loc == "east":
                    for d in self.doors:
                        if d.loc == "west":
                            self.player = Player(self, (d.rect.x + 64)/32, d.rect.y/32)
                elif event.loc == "west":
                    for d in self.doors:
                        if d.loc == "east":
                            self.player = Player(self, (d.rect.x - 64)/32, d.rect.y/32)
                elif event.loc == "north":
                    for d in self.doors:
                        if d.loc == "south":
                            self.player = Player(self, d.rect.x/32, (d.rect.y - 64)/32)
                elif event.loc == "south":
                    for d in self.doors:
                        if d.loc == "north":
                            self.player = Player(self, d.rect.x/32, (d.rect.y + 64)/32)
                else:
                    self.player = Player(self,3,5)
            
            #Check wether the Player is allowed to move
            if not self.player.freezed:
                if event.type == pygame.KEYDOWN:
                    #Check wether the Player has pressed the E key to interact
                    if event.key == pygame.K_e:
                        if self.player.facing == "up":
                            Interaction(self, self.player.rect.x, self.player.rect.y - TILE_SIZE)
                        if self.player.facing == "down":
                            Interaction(self, self.player.rect.x, self.player.rect.y + TILE_SIZE)
                        if self.player.facing == "left":
                            Interaction(self, self.player.rect.x - TILE_SIZE, self.player.rect.y)
                        if self.player.facing == "right":
                            Interaction(self, self.player.rect.x + TILE_SIZE, self.player.rect.y)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    #Throw a shuriken
                    if pygame.mouse.get_pressed()[0]:
                        Shuriken(self, WIN_WIDTH/2-16, WIN_HEIGHT/2-16)

    def update(self):
        #Let every sprite call its update methode
        self.all_sprites.update()
        #Make the camera follow the player
        self.camera.update(self.player)
    
    def draw(self):
        self.screen.fill(BLACK)
        #Let every sprite according to the Player's position to make sure that the Player is in the middle of the screen
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        self.clock.tick(FPS)
        pygame.display.update()
        
    def main(self):
        #Gameloop
        while self.playing:
            self.events()
            self.update()
            self.draw()
        
    #A possible game over screen
    def game_over(self):
        pass
    
    def intro_screen(self):
        intro = True

        buttons = []
        
        #Create the button objects
        play_button = Button(75,200, BLACK, "PLAY", 32)
        buttons.append(play_button)
        option_button = Button(75,300, BLACK, "OPTIONS", 32) 
        buttons.append(option_button)
        about_button = Button(75,400, BLACK, "ABOUT", 32)
        buttons.append(about_button)
        quit_button = Button(75,500, BLACK, "QUIT", 32)
        buttons.append(quit_button)

        while intro:
            for event in pygame.event.get():
                #Check wether the close button has been pressed
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        #Get the position of the mouse and check wether the mousebutton has been pressed 
                        mouse_pos = pygame.mouse.get_pos()

                        #Check wether the mousebutton has been pressed while the mouse is on the play button
                        if play_button.is_pressed(mouse_pos):
                            intro = False
                        if option_button.is_pressed(mouse_pos):
                            pass
                        if about_button.is_pressed(mouse_pos):
                            webbrowser.open('http://calandlyceum.nl')
                        if quit_button.is_pressed(mouse_pos):
                            self.playing = False
                            self.running = False
                            intro = False
            
            #Update the screen
            self.screen.blit(self.intro_background, (0,0))
            for b in buttons:
                self.screen.blit(b.image, b.rect)
            self.clock.tick(FPS)

            pygame.display.update()

g = Game()
g.intro_screen()
g.new()

while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()