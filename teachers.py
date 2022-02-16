from sprites import Spritesheet

def create_human_spritesheet(file):
    spritesheet = Spritesheet(file)

    down =  [spritesheet.get_sprite(35, 0, 26, 32),
             spritesheet.get_sprite(3,  1, 26, 32),
             spritesheet.get_sprite(67, 1, 26, 32)]

    left =  [spritesheet.get_sprite(36, 32, 25, 32),
             spritesheet.get_sprite(4,  33, 25, 31),
             spritesheet.get_sprite(68, 33, 25, 31)]

    right = [spritesheet.get_sprite(36, 64, 25, 32),
             spritesheet.get_sprite(4 , 65, 25, 31),
             spritesheet.get_sprite(68, 65, 25, 31)]

    up =    [spritesheet.get_sprite(36, 96, 26, 32),
             spritesheet.get_sprite(4,  97, 26, 31),
             spritesheet.get_sprite(68, 97, 26, 31)]

    image = {"down":down, "left":left, "right":right, "up":up}

    return image