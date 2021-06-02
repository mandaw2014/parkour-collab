import tkinter
from level_editor_copy import * 
from ursina import *
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton
from ursina.prefabs.file_browser_save import FileBrowserSave
from tkinter import filedialog as fd

app = Ursina()
ed = EditorCamera()
window = tkinter.Tk()
window.withdraw()

currentLevel = Level()

xyText = Text(text="", position=(0.5, -0.4))

# def on_submit(paths):
#     currentLevel.clear()
#     currentLevel.load(str(paths[0]))
#     currentLevel.enable()

def pickLevel():
    filename = fd.askopenfilename(initialdir='.', title='Open Level', filetypes=(('Level Files', '.level*'), ('All Files', '*.*')))

    currentLevel.clear()
    
    currentLevel.load(filename)

def newLevel():
    currentLevel.clear()

def saveLevel():
    # wp = FileBrowserSave(file_type = '.level')
    # wp.file_name_field.text_field.text = 'new_map'
    leveldata = currentLevel.save()
    filesave = fd.asksaveasfile(mode='w', defaultextension=".level")
    if filesave is None:
        return

    filesave.write(leveldata)
    filesave.close()

def to_tuple(string):
    return tuple(map(float, string.split(',')))

def updateElem(entity,buttons):
    pos = to_tuple(buttons[[but.name for but in buttons].index("pos")].text)
    entity.position = pos
    rot = to_tuple(buttons[[but.name for but in buttons].index("rot")].text)
    entity.rotation = rot
    if hasattr(entity,'power') :
        entity.power = float(buttons[5].text)

def showInfo(entity):
    pass
    # content = [
    #         Text('Position:'),
    #         InputField(name='pos',default_value=str(tuple(entity.position))[1:-1],limit_content_to = ContentTypes.float+"-"),
    #         Text('Rotation:'),
    #         InputField(name='rot',default_value=str(tuple(entity.rotation))[1:-1],limit_content_to = ContentTypes.float+"-")
    # ]
    # if hasattr(entity,'power') :
    #     content.append(Text('Power:'))
    #     content.append(InputField(name='power',default_value = str(entity.power),limit_content_to = ContentTypes.float))

        
    # content.append(Button(text='Update', color=color.azure))
    # content.append(Button(text='Delete', color=color.azure))
    # content.append(Button(text='Close', color=color.azure))
    # wp = WindowPanel(
    # title=str(entity),
    # content=content
    # )
    # wp.content[-1].on_click = Func(destroy,wp)
    # wp.content[-2].on_click = Func(delBlock,wp,entity)
    # wp.content[-3].on_click = Func(updateElem,entity,wp.content)

def delBlock(wp,entity):
    currentLevel.blocks.remove(entity)
    destroy(entity)
    destroy(wp)

def newBlock(button):
    # print(button.text)
    # print(eval(button.text)(position = (0,0,0)))
    currentLevel.blocks.append(eval(button.text)(position = (0,0,0)))

# DropdownMenu(text='File')
DropdownMenu('File', buttons=(
    DropdownMenuButton('New',on_click = newLevel),
    DropdownMenuButton('Open',on_click = pickLevel),
    DropdownMenuButton('Save', on_click = saveLevel)
    ))

b = (Button(text='StartBlock', color="#CACACA",text_color = color.black),
    Button(text='NormalBlock', color = "#AFFF3C",text_color = color.black),
    Button(text='SlowBlock', color = "#FF453F"),
    Button(text='SpeedBlock', color = "#53FFF5",text_color = color.black),
    Button(text='JumpBlock', color = "#FF8B00"),
    Button(text='EndBlock', color="#CACACA",text_color = color.black))

for index,but in enumerate(b):
    but.on_click = Func(newBlock,but)
    but.fit_to_text()
    but.position = (.8,index*.08)

def input(key):

    if key == "a down":
        print("woah")

    if key == 'scroll down':
        camera.fov += (0.75 * 250 * time.dt)

    if key == 'scroll up':
        camera.fov -= (0.75 * 250 * time.dt)

    if key == "o":
        ed.disable()
        camera.orthographic = True  

    if key == "n":
        camera.orthographic = False
        ed.enable()


def update():
    if "Block" in str(type(mouse.hovered_entity)):
        xyText.text = "X = {}\nY = {}".format(mouse.hovered_entity.x, mouse.hovered_entity.y)

app.run()
window.mainloop()