from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

# App/Window
app = Ursina()

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

# Lighting
light = PointLight(parent = camera, position = (0, 10, -1.5))
light.color = color.white

AmbientLight(color = color.rgba(100, 100, 100, 0.1))

# Level 03 platforms
ground_3 = Entity(model = "cube", scale_x = 10, scale_z = 10, collider = "box", texture = "white_cube", color = "#CACACA")
block_3_1 = SpeedBlock(position = (0, 0, 13))
block_3_2 = SpeedBlock(position = (0, 0, 32))
block_3_3 = SpeedBlock(position = (0, 0, 58))
block_3_4 = SpeedBlock(position = (0, 0, 80))
block_3_5 = SpeedBlock(position = (0, 0, 120))
block_3_6 = SpeedBlock(position = (0, 0, 180))
block_3_7 = SpeedBlock(position = (0, 0, 240))
block_3_8 = SlowBlock(position = (0, 0, 300))

finishBlock_3 = Entity(model = "cube", scale_x = 10, scale_z = 10, collider = "box", texture = "white_cube", color = "#CACACA", position = (0, 0, 315))

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

    if hit.entity == block_3_1:
        player.speed = 20
    if hit.entity == block_3_2:
        player.speed = 30
    if hit.entity == block_3_3:
        player.speed = 40
    if hit.entity == block_3_4:
        player.speed = 50
    if hit.entity == block_3_5:
        player.speed = 70
    if hit.entity == block_3_6:
        player.speed = 100
    if hit.entity == block_3_7:
        player.speed = 120
    if hit.entity == block_3_8:
        player.speed = 6

app.run()
