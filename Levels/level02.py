from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

# App/Window
app = Ursina()

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
    def __init__(self, position = (0, 0, 0)):
        super().__init__(
            model = "cube",
            scale = Vec3(3, 0.8, 3),
            color = "#FF8B00",
            collider = "box",
            texture = "white_cube",
            position = position,
        )

# Speed Block Class
class SpeedBlock(Entity):
    def __init__(self, position = (0, 0, 0)):
        super().__init__(
            model = "cube",
            scale = Vec3(3, 0.5, 8),
            color = "#53FFF5",
            collider = "box",
            texture = "white_cube",
            position = position,
        )

# Slow Block Class
class SlowBlock(Entity):
    def __init__(self, position = (0, 0, 0)):
        super().__init__(
            model = "cube",
            scale = Vec3(3, 0.5, 15),
            color = "#FF453F",
            collider = "box",
            texture = "white_cube",
            position = position,
        )

# Player
player = FirstPersonController()
player.speed = 6
player.jump_height = 4

# Sky
sky = Sky(texture = "../assets/sky")

# Level 02 platforms
ground_2 = Entity(model = "cube", scale_x = 10, scale_z = 10, collider = "box", texture = "white_cube", color = "#CACACA")
finishBlock_2 = Entity(model = "cube", scale_x = 5, scale_z = 5, collider = "box", texture = "white_cube", color = "#CACACA", position = (0, 11, 67))

block_2 = NormalBlock(position = (0, 1, 9))
block_2_1 = NormalBlock(position = (0, 2, 15))
block_2_2 = JumpBlock(position = (0, -20, 25))
block_2_3 = NormalBlock(position = (0, 10, 30))
block_2_4 = NormalBlock(position = (0, 10, 37))
block_2_5 = SpeedBlock(position = (0, 10, 45))
block_2_6 = NormalBlock(position = (0, 11, 60))

def speed():
    player.speed = 6

def update():
    # Escape button quits
    if held_keys["escape"]:
        application.quit()

    # Stops the player from falling forever
    if player.position.y <= -50:
        player.position = Vec3(0, 20, 0)
        player.speed = 6
        player.jump_height = 4

    # Restart the level
    if held_keys["g"]:
        player.position = Vec3(0, 0, 0)
        player.speed = 6
        player.jump_height = 4

    # What entity the player hits
    hit = raycast(player.position, player.down, distance=2, ignore=[player,])
    
    if block_2_2.enabled == True:
        if hit.entity == block_2_2:
            player.jump_height = 40
        elif hit.entity != block_2_2:
            player.jump_height = 4

    if block_2_5.enabled == True:
        if hit.entity == block_2_5:
            player.speed = 20
            invoke(speed, delay=3)

app.run()