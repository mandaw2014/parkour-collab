from ursina import *

# Normal Block Class


class NormalBlock(Draggable):
    def __init__(self, position=(0, 0, 0), **kwargs):
        super().__init__(
            model="cube",
            scale=Vec3(3, 0.8, 3),
            color="#AFFF3C",
            collider="box",
            texture="white_cube",
            position=position,
            parent=scene
        )
        print(self.parent)
        for key, value in kwargs.items():
            setattr(self, key, value)

# Jump Block Class


class JumpBlock(Draggable):
    def __init__(self, position=(0, 0, 0), power=1, **kwargs):
        super().__init__(
            model="cube",
            scale=Vec3(3, 0.8, 3),
            color="#FF8B00",
            collider="box",
            texture="white_cube",
            position=position,
            parent=scene
        )
        self.power = power
        for key, value in kwargs.items():
            setattr(self, key, value)

# Speed Block Class


class SpeedBlock(Draggable):
    def __init__(self, position=(0, 0, 0), power=1, **kwargs):
        super().__init__(
            model="cube",
            scale=Vec3(3, 0.5, 8),
            color="#53FFF5",
            collider="box",
            texture="white_cube",
            position=position,
            parent=scene
        )
        self.power = power
        for key, value in kwargs.items():
            setattr(self, key, value)

# Slow Block Class


class SlowBlock(Draggable):
    def __init__(self, position=(0, 0, 0), power=1, **kwargs):
        super().__init__(
            model="cube",
            scale=Vec3(3, 0.5, 15),
            color="#FF453F",
            collider="box",
            texture="white_cube",
            position=position,
            parent=scene
        )
        self.power = power
        for key, value in kwargs.items():
            setattr(self, key, value)

# Start Block Class


class StartBlock(Draggable):
    def __init__(self, position=(0, 0, 0), rotation=(0, 0, 0), **kwargs):
        super().__init__(
            model="cube",
            scale=(10, 0.8, 10),
            color="#CACACA",
            collider="box",
            texture="white_cube",
            position=position,
            rotation=rotation,
            parent=scene
        )

        for key, value in kwargs.items():
            setattr(self, key, value)

# End Block Class


class EndBlock(NormalBlock):
    def __init__(self, position=(0, 0, 0), **kwargs):
        super().__init__(
            position=position
        )
        self.color = "#CACACA"
        for key, value in kwargs.items():
            setattr(self, key, value)

# Weird Block Class


class WeirdBlock(Draggable):
    def __init__(self, position=(0, 0, 0), power=1, **kwargs):
        super().__init__(
            model="cube",
            scale=Vec3(3, 0.5, 15),
            color="#7116FE",
            collider="box",
            texture="white_cube",
            position=position,
            parent=scene
        )
        self.power = power
        for key, value in kwargs.items():
            setattr(self, key, value)

# Wall Class


class Wall(Draggable):
    def __init__(self, position=(0, 0, 0), **kwargs):
        super().__init__(
            model="cube",
            scale=(5, 4, 1),
            color="#AFFF3C",
            collider="box",
            texture="white_cube",
            position=position,
            rotation=(0, 0, 90),
            parent=scene
        )
        for key, value in kwargs.items():
            setattr(self, key, value)

# Fake Block Class


class FakeBlock(Draggable):
    def __init__(self, position=(0, 0, 0), **kwargs):
        super().__init__(
            model="cube",
            scale=Vec3(3, 0.8, 3),
            color="#25B701",
            texture="white_cube",
            position=position,
            parent=scene
        )
        for key, value in kwargs.items():
            setattr(self, key, value)


def to_tuple(string):
    return tuple(map(int, string.split(', ')))


class Level:
    def __init__(self, src=None):
        if src:
            self.load(src)
            self.disable()
        else:
            self.title = ""
            self.blocks = []
            self.finish = None

    def disable(self):
        self.finish.disable()
        for block in self.blocks:
            block.disable()

    def enable(self):
        self.finish.enable()
        for block in self.blocks:
            block.enable()

    def clear(self):
        self.title = ""
        for entity in self.blocks:
            destroy(entity)
        self.blocks = []
        if self.finish:
            destroy(self.finish)
        self.finish = None

    def load(self, src):
        with open(src) as source:
            elements = source.readlines()
            for index, elem in enumerate(elements):
                elements[index] = elem.strip("\n")
            self.title = elements.pop(0)
            print(self.title)
        self.blocks = []

        for blockToGenerate in elements:
            block = blockToGenerate.split(";")
            if block[0] == "NormalBlock":
                self.blocks.append(NormalBlock(position=to_tuple(
                    block[1]), rotation=to_tuple(block[2])))
            elif block[0] == "JumpBlock":
                self.blocks.append(JumpBlock(position=to_tuple(
                    block[1]), rotation=to_tuple(block[2]), power=float(block[-1])))
            elif block[0] == "SpeedBlock":
                self.blocks.append(SpeedBlock(position=to_tuple(
                    block[1]), rotation=to_tuple(block[2]), power=float(block[-1])))
            elif block[0] == "SlowBlock":
                self.blocks.append(SlowBlock(position=to_tuple(
                    block[1]), rotation=to_tuple(block[2]), power=float(block[-1])))
            elif block[0] == "WeirdBlock":
                self.blocks.append(WeirdBlock(position=to_tuple(
                    block[1]), rotation=to_tuple(block[2]), power=float(block[-1])))
            elif block[0] == "FakeBlock":
                self.blocks.append(FakeBlock(position=to_tuple(
                    block[1]), rotation=to_tuple(block[2])))
            elif block[0] == "Wall":
                self.blocks.append(Wall(position=to_tuple(
                    block[1]), rotation=to_tuple(block[2])))
            elif block[0] == "EndBlock":
                self.finish = EndBlock(position=to_tuple(
                    block[1]), rotation=to_tuple(block[2]))
            elif block[0] == "StartBlock":
                self.blocks.append(StartBlock(position=to_tuple(
                    block[1]), rotation=to_tuple(block[2])))

    def save(self):
        output = self.title
        for element in self.blocks+[self.finish]:
            output += "\n"
            if hasattr(element,"power"):
                 output += type(element).__name__+";"+str(tuple(int(val) for val in tuple(element.position)))[1:-1]+";"+str(
                    tuple(int(val) for val in tuple(element.rotation)))[1:-1]+";"+str(element.power)
            else :
                 output += type(element).__name__+";"+str(tuple(int(val) for val in tuple(element.position)))[
                        1:-1]+";"+str(tuple(int(val) for val in tuple(element.rotation)))[1:-1]
        return output


if __name__ == "__main__":
    Level("1.level")
