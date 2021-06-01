from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from player import Player
import time

# App/Window
app = Ursina()

normalSpeed = 1
boostSpeed  = 3

normalJump = 0.35
boostJump  = 0.8

# Sky texture
sky_texture = load_texture("assets/sky.png")

# Normal Block Class
class NormalBlock(Entity):
    def __init__(self, position = (0, 0, 0)):
        super().__init__(
            model = "cube",
            scale = Vec3(3, 0.8, 3),
            color = "#AFFF3C",
            collider = "box",
            texture = "white_cube",
            position = position,
        )

# Jump Block Class
class JumpBlock(Entity):
    def __init__(self, position = (0, 0, 0),power=1):
        super().__init__(
            model = "cube",
            scale = Vec3(3, 0.8, 3),
            color = "#FF8B00",
            collider = "box",
            texture = "white_cube",
            position = position,
        )
        self.power = power

# Speed Block Class
class SpeedBlock(Entity):
    def __init__(self, position = (0, 0, 0),power=1):
        super().__init__(
            model = "cube",
            scale = Vec3(3, 0.5, 8),
            color = "#53FFF5",
            collider = "box",
            texture = "white_cube",
            position = position,
        )
        self.power = power

# Slow Block Class
class SlowBlock(Entity):
    def __init__(self, position = (0, 0, 0),power=1):
        super().__init__(
            model = "cube",
            scale = Vec3(3, 0.5, 15),
            color = "#FF453F",
            collider = "box",
            texture = "white_cube",
            position = position,
        )
        self.power = power

# Player
player = Player("cube",(0,2,0),"box",controls='wasd')
player.SPEED = normalSpeed
player.jump_height = normalJump

# Sky
sky = Sky(texture = "assets/sky")

# Lighting
light = PointLight(parent = camera, position = (0, 10, -1.5))
light.color = color.white

AmbientLight(color = color.rgba(100, 100, 100, 0.1))

def speed():
    player.SPEED = normalSpeed

def resetPlayer():
    player.SPEED = normalSpeed
    player.position = Vec3(0,2,0)
    player.jump_height = normalJump
    player.rotation =(0,0,0)

resetPlayer()

def update():

    # Stops the player from falling forever
    if player.position.y <= -50:
        resetPlayer()


    # What entity the player hits
    hit = raycast(player.position, player.down, distance=2, ignore=[player,])
    
    if hit.hit :
        player.jump_height = normalJump
        player.SPEED = normalSpeed
        if type(hit.entity) == SpeedBlock :
            player.SPEED = boostSpeed * hit.entity.power

        elif type(hit.entity) == SlowBlock :
            player.SPEED = boostSpeed/hit.entity.power

        elif type(hit.entity) == JumpBlock :
            player.jump_height = boostJump * hit.entity.power

    if finishBlock_1.enabled == True and hit.entity == finishBlock_1:
        destroyLevel01()
        resetPlayer()

    if finishBlock_2.enabled == True and hit.entity == finishBlock_2:
        destroyLevel02()
        resetPlayer()

def input(key):
    # Restart the level
    if key == "g":
        resetPlayer()
    # Escape button quits
    elif key == "escape":
        application.quit()

#Level01
level1 = [NormalBlock(position = (0, 1, 9)),NormalBlock(position = (0, 2, 14)),NormalBlock(position = (0, 3, 19)),NormalBlock(position = (0, 4, 24)),NormalBlock(position = (5, 5, 24)),NormalBlock(position = (10, 6, 24)),JumpBlock(position = (17, 2, 24)),NormalBlock(position = (25, 10, 24)),SpeedBlock(position = (25, 10, 33)),Entity(model = "cube", scale_x = 10, scale_z = 10, collider = "box", texture = "white_cube", color = "#CACACA")]
finishBlock_1 = Entity(model = "cube", scale_x = 5, scale_z = 5, collider = "box", texture = "white_cube", color = "#CACACA", position = (25, 10, 45))


#Level02

level2 = [NormalBlock(position = (0, 1, 9)),NormalBlock(position = (0, 2, 15)),JumpBlock(position = (0, -20, 25),power=2),NormalBlock(position = (0, 10, 30)),NormalBlock(position = (0, 10, 37)),SpeedBlock(position = (0, 10, 45)),NormalBlock(position = (0, 11, 60)),Entity(model = "cube", scale_x = 10, scale_z = 10, collider = "box", texture = "white_cube", color = "#CACACA")]
finishBlock_2 = Entity(model = "cube", scale_x = 5, scale_z = 5, collider = "box", texture = "white_cube", color = "#CACACA", position = (0, 11, 67))

for block in level2 :
    block.disable()
finishBlock_2.disable()

#Level03

level3 = [Entity(model = "cube", scale_x = 10, scale_z = 10, collider = "box", texture = "white_cube", color = "#CACACA"), SpeedBlock(position = (0, 0, 13)),SpeedBlock(position = (0, 0, 32),power = 1.5), SpeedBlock(position = (0, 0, 58),power = 2),SpeedBlock(position = (0, 0, 80),power = 2.5),SpeedBlock(position = (0, 0, 120),power = 3.5),SpeedBlock(position = (0, 0, 180),power = 4),SpeedBlock(position = (0, 0, 240),power = 5), SlowBlock(position = (0, 0, 300),power = 1.5)]
finishBlock_3 = Entity(model = "cube", scale_x = 10, scale_z = 10, collider = "box", texture = "white_cube", color = "#CACACA", position = (0, 0, 315))

for block in level3 :
    block.disable()
finishBlock_3.disable()


def destroyLevel01():
    for block in level1 :
        block.disable()

    finishBlock_1.disable()

    for block in level2 :
        block.enable()
    finishBlock_2.enable()
    player.SPEED = normalSpeed
    player.jump_height = normalJump

def destroyLevel02():
    for block in level2 :
        block.disable()
    finishBlock_2.disable()

    finishBlock_3.enable()
    for block in level3 :
        block.enable()
    player.SPEED = normalSpeed
    player.jump_height = normalJump

app.run()
