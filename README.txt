       CALANDRPG
------------------------
Made By Mohamed Bentaher
________________________

~Description~
CalandRPG is a game demo designed to introduce new students to the high school CalandLyceum. This project was 
created by Mohamed Bentaher as a part of his high school subject (informatica) with the aim of learning more 
about Object Oriented Programming (OOP) in-depth.

~Tools~
For this project I used the python library called Pygame. Its a library that is used for, well, creating
games in python. 
For the art I used pixilart.com and a software called Aseprite. (Disclaimer, not all the art is made by me)

~Key Features~
As mentioned before, CalandRPG is an unfinished game demo. For it to be a final product, there was going 
to have some polishing to be done. However, the game still has alot of finished features that I like to mention:

- Map loading:  
                The maps in the game, including the school terrain and rooms, are based on simple .txt files. Each 
                tile corresponds to a character in the .txt file, making it easy to create and update maps for the 
                game. All map files can be found in the maps folder of the project. The player loads the next map 
                whenever they walk through a door and trigger an event.
- Spritesheet Renderer:
                All sprites in the game, including the ground, walls, player, enemies, and teachers, are based on 
                spritesheets. Spritesheets are images that contain multiple frames/tiles of a sprite in one image. 
                This means that only one image needs to be loaded for a sprite to be rendered and animated, which 
                improves performance by reducing file loading calls.
- Camera System:
                The gamescreen always has the player at its center thanks to the Camera System. This system tracks a 
                certain object and moves all other objects whenever the tracked object is no longer at the center of 
                the screen. This ensures that the tracked object will always be in the center of the screen. The camera 
                system could be used to create cutscenes, in which another object (e.g. a teacher) is at the center of 
                the screen performing some action.
- Dialogue System:
                To interact with teachers and receive directions/information in the game, a dialogue system was created. 
                When the player interacts with a teacher, an event is triggered, and a textbox with the corresponding text 
                appears. The dialogue system is designed to cut long sentences at the end of the textbox and continue them 
                on the next line if necessary.

    