from ursina import *

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


# Start Block Class
class StartBlock(Entity):
    def __init__(self, position = (0, 0, 0)):
        super().__init__(
            model = "cube",
            scale = (10, 0.8, 10),
            color = "#CACACA",
            collider = "box",
            texture = "white_cube",
            position = position,
        )

# End Block Class
class EndBlock(NormalBlock):
    def __init__(self, position = (0, 0, 0)):
        super().__init__(
            position = position
        )
        self.color = "#CACACA"

def to_tuple(string):
    return tuple(map(int, string.split(', ')))

class Level:
    def __init__(self,src):
        with open("./level/"+src) as source :
            elements = source.readlines()
            for index,elem in enumerate(elements):
                elements[index] = elem.strip("\n")
            self.title = elements.pop(0)
            print(self.title)
        self.blocks = []

        for blockToGenerate in elements:
            block = blockToGenerate.split(";")
            if block[0] == "NormalBlock" :
                self.blocks.append(NormalBlock(position=to_tuple(block[1])))
            elif block[0] == "JumpBlock" :
                self.blocks.append(JumpBlock(position=to_tuple(block[1]),power=float(block[2])))
            elif block[0] == "SpeedBlock" :
                self.blocks.append(SpeedBlock(position=to_tuple(block[1]),power=float(block[2])))
            elif block[0] == "SlowBlock" :
                self.blocks.append(SlowBlock(position=to_tuple(block[1]),power=float(block[2])))
            elif block[0] == "EndBlock" :
                self.finish = EndBlock(position=to_tuple(block[1]))
            elif block[0] == "StartBlock" :
                self.blocks.append(StartBlock(position=to_tuple(block[1])))
        self.disable()

    def disable(self):
        self.finish.disable()
        for block in self.blocks:
            block.disable()

    def enable(self):
        self.finish.enable()
        for block in self.blocks:
            block.enable()

if __name__ == "__main__":
    Level("1.level")