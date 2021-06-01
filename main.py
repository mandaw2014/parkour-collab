from ursina import *
from player import Player
from level import *

# App/Window
app = Ursina()

normalSpeed = 1
boostSpeed  = 3

normalJump = 0.35
boostJump  = 0.8

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
    camera.rotation_x = 0

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


    if hit.entity == level1.finish:
        level1.disable()
        level2.enable()
        resetPlayer()

    elif hit.entity == level2.finish:
        level2.disable()
        level3.enable()
        resetPlayer()

        

def input(key):
    # Restart the level
    if key == "g":
        resetPlayer()
    # Escape button quits
    elif key == "escape":
        application.quit()

#Level01
level1 = Level("1.level")

#Level02

level2 = Level("2.level")


#Level03

level3 = Level("3.level")


level1.enable()

app.run()
