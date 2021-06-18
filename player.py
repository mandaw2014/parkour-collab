from ursina import *
import math

sign = lambda x: -1 if x < 0 else (1 if x > 0 else 0)


class Player(Entity):
    def __init__(self, model, position, collider, scale=(1, 1, 1), SPEED=3, velocity=(0, 0, 0), MAXJUMP=1, gravity=1, controls="wasd", **kwargs):

        super().__init__(model="cube", position=position,
                         scale=(1, 1, 1), visible_self=False)
        self.collider = BoxCollider(
            self, center=Vec3(0, 1, 0), size=Vec3(1, 2, 1))
        mouse.locked = True
        camera.parent = self
        camera.position = (0, 2, 0)
        camera.rotation = (0, 0, 0)
        camera.fov = 100
        self.velocity_x, self.velocity_y, self.velocity_z = velocity
        self.SPEED = SPEED
        self.MAXJUMP = MAXJUMP
        self.jump_count = 0
        self.gravity = gravity
        self.jump_height = 0.3
        self.slope = 40
        self.controls = controls
        self.sensibility = 150
        self.cursor = [Entity(parent=camera.ui, model="cube", color=color.black,
                              texture="assets/scope", scale=.02, rotation_y=90)]
        for key, value in kwargs.items():
            try:
                setattr(self, key, value)
            except:
                print(key, value)

    def update(self):

        y_movement = self.velocity_y * time.dt

        direction = (0, sign(y_movement), 0)
        yRay = boxcast(origin=self.world_position, direction=direction,
                        distance=self.scale_y/2+abs(y_movement), ignore=[self, ])
        if yRay.hit:
            move = False
            self.jump_count = 0
            self.velocity_y = 0
        else :
            self.y += y_movement
            self.velocity_y -= self.gravity * time.dt * 25

        x_movement = (self.forward[0]*held_keys[self.controls[0]] +
                      self.left[0]*held_keys[self.controls[1]] +
                      self.back[0]*held_keys[self.controls[2]] +
                      self.right[0]*held_keys[self.controls[3]]) * time.dt*6 * self.SPEED

        z_movement = (self.forward[2]*held_keys[self.controls[0]] +
                      self.left[2]*held_keys[self.controls[1]] +
                      self.back[2]*held_keys[self.controls[2]] +
                      self.right[2]*held_keys[self.controls[3]]) * time.dt*6 * self.SPEED

        if x_movement != 0:
            direction = (sign(x_movement), 0, 0)
            xRay = boxcast(origin=self.world_position, direction=direction,
                           distance=self.scale_x/2+abs(x_movement), ignore=[self, ],thickness = (1,1))

            if not xRay.hit:
                self.x += x_movement
            else:
                TopXRay = raycast(origin=self.world_position-(0, self.scale_y/2-.1, 0),
                                  direction=direction,distance = self.scale_x/2+math.tan(math.radians(self.slope))*.1, 
                                  ignore=[self, ])

                if not TopXRay.hit:
                    self.x += x_movement
                    HeightRay = raycast(origin=self.world_position+(sign(x_movement)*self.scale_x/2, -self.scale_y/2, 0),
                                        direction=(0,1,0), ignore=[self, ])
                    if HeightRay.hit :
                        self.y += HeightRay.distance

        if z_movement != 0:
            direction = (0, 0, sign(z_movement))
            zRay = boxcast(origin=self.world_position, direction=direction,
                           distance=self.scale_z/2+abs(z_movement), ignore=[self, ],thickness = (1,1))

            if not zRay.hit:
                self.z += z_movement
            else:
                TopZRay = raycast(origin=self.world_position-(0, self.scale_y/2-.1, 0),
                                  direction=direction,distance = self.scale_z/2+math.tan(math.radians(self.slope))*.1, 
                                  ignore=[self, ])

                if not TopZRay.hit:
                    self.z += z_movement
                    HeightRay = raycast(origin=self.world_position+(0, -self.scale_y/2, sign(z_movement)*self.scale_z/2),
                                     direction=(0,1,0), ignore=[self, ])
                    if HeightRay.hit :
                        self.y += HeightRay.distance


        camera.rotation_x -= mouse.velocity[1] * self.sensibility
        self.rotation_y += mouse.velocity[0] * self.sensibility
        camera.rotation_x = min(max(-80, camera.rotation_x), 80)

    def input(self, key):
        if key == 'space':
            if self.jump_count < self.MAXJUMP:
                self.velocity_y = self.jump_height * 40
                self.jump_count += 1


if __name__ == '__main__':
    app = Ursina()
    window.exit_button.input = None

    player = Player(model='cube', position=(0, 2, 0),
                    collider='box', SPEED=1, color=color.orange)

    ground = Entity(model='plane', scale_x=100, scale_z=100, collider='box', texture="brick",
                    double_sided=True, texture_scale=(50, 50))

    wall1 = Entity(model="cube", scale=(1, 1, 1), collider='box',
                   color=color.dark_gray, x=0, z=5, y=0.5)
    wall2 = Entity(model="cube", scale=(3, 1, 1), collider='box',
                   color=color.dark_gray, x=8, z=5, y=0.5)
    roof = Entity(model="cube", scale=(3, 1, 1), collider='box',
                  color=color.dark_gray, x=3, z=5, y=1.55)
    spleen = Entity(model="cube", scale=(1, 1, 3), collider='mesh',
                    color=color.dark_gray, x=3, z=6.5, y=0.5, rotation=(35, 0, 0))

    spleen2 = Entity(model="cube", scale=(1, 1, 3), collider='mesh',
                     color=color.dark_gray, x=6, z=1.5, y=0.5, rotation=(-40, 90, 0))
                     
    roof = Entity(model="cube", scale=(3, 1, 1), collider='box',
                  color=color.dark_gray, x=8.3, z=1.5, y=1.35)

    Sky(texture="skybox", texture_scale=(1, 1, 1))

    light = PointLight(parent=player, position=(0, 1.1, -1.5))
    light.color = color.white

    AmbientLight(color=color.rgba(100, 100, 100, 0.1))

    app.run()
