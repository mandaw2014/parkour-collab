from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader

app = Ursina()

pivot = Entity()
DirectionalLight(parent=pivot, y=2, z=3, shadows=True)


class NormalBlock(Entity):
    def __init__(self, position = (0, 0, 0)):
        super().__init__(
            model = "cube",
            scale = Vec3(3, 0.8, 3),
            color = "#AFFF3C",
            collider = "box",
            texture = "white_cube",
            position = position,
            shader = lit_with_shadows_shader
        )

class JumpBlock(Entity):
    def __init__(self, position = (0, 0, 0)):
        super().__init__(
            model = "cube",
            scale = Vec3(3, 0.8, 3),
            color = "#FF8B00",
            collider = "box",
            texture = "white_cube",
            position = position,
            shader = lit_with_shadows_shader
        )

class SpeedBlock(Entity):
    def __init__(self, position = (0, 0, 0)):
        super().__init__(
            model = "cube",
            scale = Vec3(3, 0.5, 8),
            color = "#53FFF5",
            collider = "box",
            texture = "white_cube",
            position = position,
            shader = lit_with_shadows_shader
        )


player = FirstPersonController()
player.speed = 6
player.jump_height = 4

sky = Sky(texture = 'sky')

#Level01

block_1 = NormalBlock(position = (0, 1, 9))
block_1_1 = NormalBlock(position = (0, 2, 14))
block_1_2 = NormalBlock(position = (0, 3, 19))
block_1_3 = NormalBlock(position = (0, 4, 24))
block_1_4 = NormalBlock(position = (5, 5, 24))
block_1_5 = NormalBlock(position = (10, 6, 24))
block_1_6 = JumpBlock(position = (17, 2, 24))
block_1_7 = NormalBlock(position = (25, 10, 24))
block_1_8 = SpeedBlock(position = (25, 10, 33))

ground_1 = Entity(model = "cube", scale_x = 10, scale_z = 10, collider = "box", texture = "white_cube", color = "#CACACA", shader = lit_with_shadows_shader)
finishBlock_1 = Entity(model = "cube", scale_x = 5, scale_z = 5, collider = "box", texture = "white_cube", color = "#CACACA", position = (25, 10, 45), shader = lit_with_shadows_shader)

def speed():
    player.speed = 6

def update():
    if held_keys["escape"]:
        application.quit()

    if player.position.y <= -50:
        player.position = Vec3(0, 20, 0)

    if held_keys["g"]:
        player.position = Vec3(0, 0, 0)

    hit = raycast(player.position, player.down, distance=2, ignore=[player,])
    if hit.entity == block_1_6:
        player.jump_height = 20
    elif hit.entity != block_1_6:
        player.jump_height = 4

    if hit.entity == block_1_8:
        player.speed = 20
        invoke(speed, delay=5)

    if hit.entity == finishBlock_1:
        invoke(destroy, delay = 3)
        player.position = Vec3(0,0,0)
    
    if block_2_2.enabled == True:
        if hit.entity == block_2_2:
            player.jump_height = 40
        elif hit.entity != block_2_2:
            player.jump_height = 4

    if block_2_5.enabled == True:
        if hit.entity == block_2_5:
            player.speed = 20
            invoke(speed, delay=5)

def destroy():
    block_1.disable()
    block_1_1.disable()
    block_1_2.disable()
    block_1_3.disable()
    block_1_4.disable()
    block_1_5.disable()
    block_1_6.disable()
    block_1_7.disable()
    block_1_8.disable()
    ground_1.disable()
    finishBlock_1.disable()

    ground_2.enable()
    finishBlock_2.enable()
    block_2.enable()
    block_2_1.enable()
    block_2_2.enable()
    block_2_3.enable()
    block_2_4.enable()
    block_2_5.enable()
    block_2_6.enable()

#Level02

ground_2 = Entity(model = "cube", scale_x = 10, scale_z = 10, collider = "box", texture = "white_cube", color = "#CACACA", shader = lit_with_shadows_shader)
finishBlock_2 = Entity(model = "cube", scale_x = 5, scale_z = 5, collider = "box", texture = "white_cube", color = "#CACACA", position = (0, 12, 75), shader = lit_with_shadows_shader)

block_2 = NormalBlock(position = (0, 1, 9))
block_2_1 = NormalBlock(position = (0, 2, 15))
block_2_2 = JumpBlock(position = (0, -20, 25))
block_2_3 = NormalBlock(position = (0, 10, 30))
block_2_4 = NormalBlock(position = (0, 10, 37))
block_2_5 = SpeedBlock(position = (0, 10, 45))
block_2_6 = NormalBlock(position = (0, 11, 65))

ground_2.disable()
finishBlock_2.disable()
block_2.disable()
block_2_1.disable()
block_2_2.disable()
block_2_3.disable()
block_2_4.disable()
block_2_5.disable()
block_2_6.disable()


app.run()