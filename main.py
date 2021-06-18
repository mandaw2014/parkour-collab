from ursina import *
from player import Player
from level import *

# App/Window
app = Ursina()

normalSpeed = 1
boostSpeed  = 3

normalJump = 0.3
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


def update():

    # Stops the player from falling forever
    if player.position.y <= -50:
        resetPlayer()


    # What entity the player hits
    hit = boxcast(origin=player.position, direction=player.down,
                       distance=player.scale_y/2+abs(1), ignore=[player, ])
    
    if hit.hit :
        player.jump_height = normalJump
        player.SPEED = normalSpeed
        camera.rotation_z = 0
        if type(hit.entity) == SpeedBlock :
            player.SPEED = boostSpeed * hit.entity.power

        elif type(hit.entity) == SlowBlock :
            player.SPEED = boostSpeed/hit.entity.power

        elif type(hit.entity) == JumpBlock :
            player.jump_height = boostJump * hit.entity.power

        elif type(hit.entity) == WeirdBlock :
            camera.rotation_z = 180


    if hit.entity == level1.finish:
        level1.disable()
        level2.enable()
        resetPlayer()

    elif hit.entity == level2.finish:
        level2.disable()
        level3.enable()
        resetPlayer()

    elif hit.entity == level3.finish:
        level3.disable()
        level4.enable()
        resetPlayer()

    elif hit.entity == level4.finish:
        level4.disable()
        level5.enable()
        resetPlayer()

    elif hit.entity == level5.finish:
        level5.disable()
        level6.enable()
        resetPlayer()

    elif hit.entity == level6.finish:
        level6.disable()
        level7.enable()
        resetPlayer()

    elif hit.entity == level7.finish:
        level7.disable()
        level8.enable()
        resetPlayer()


    elif hit.entity == level8.finish:
        level8.disable()
        level9.enable()
        resetPlayer()
        
def input(key):
    # Restart the level
    if key == "g":
        resetPlayer()
    # Escape button quits
    elif key == "escape":
        application.quit()

#Level01
level1 = Level("level/1.level")

#Level02
level2 = Level("level/2.level")


#Level03
level3 = Level("level/3.level")

#Level04
level4 = Level("level/4.level")

#Level05
level5 = Level("level/5.level")

#Level06
level6 = Level("level/6.level")

#Level07
level7 = Level("level/7.level")

#Level08
level8 = Level("level/8.level")

#Level09
level9 = Level("level/9.level")


level1.enable()
resetPlayer()

app.run()
