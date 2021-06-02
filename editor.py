import tkinter
from level_editor_copy import * 
from ursina import *
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton
from ursina.prefabs.file_browser_save import FileBrowserSave
from tkinter import filedialog as fd

app = Ursina()
ed = EditorCamera()
tkWindow = tkinter.Tk()
tkWindow.withdraw()

currentLevel = Level()

xyzText = Text(text="", position=(0.5, -0.4))

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

def updateElem(entity):
    if len(info) == 2 and info[1].visible:
        entity.power = float(info[1].text)

info=[]

def showInfo(entity):
    global info
    if hasattr(entity,'power') :
        if info == []:
            info = [Text('Power:',position = (-0.85,-0.4)),
                    InputField(name='power',default_value = str(entity.power),limit_content_to = ContentTypes.float,position = (-0.6,-0.45))]
        else:
            destroy(info[1])
            info[1]= InputField(name='power',default_value = str(entity.power),limit_content_to = ContentTypes.float,position = (-0.6,-0.45))
    else :
        for i in info :
            i.visible = False

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

currentEntity = None

def input(key):
    if len(info) == 2 and info[1].active :
        updateElem(currentEntity)
    else :
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

        if key == "left mouse down":
            if "Block" in str(type(mouse.hovered_entity)):
                showInfo(currentEntity)

def update():
    global currentEntity
    if "Block" in str(type(mouse.hovered_entity)):
        currentEntity = mouse.hovered_entity
    
    if currentEntity :
        xyzText.text = "X = {}\nY = {}\nZ = {}".format(currentEntity.x, currentEntity.y, currentEntity.z)

app.run()
tkWindow.mainloop()