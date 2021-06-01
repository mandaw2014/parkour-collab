from level import * 
from ursina import *
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton
from ursina.prefabs.file_browser_save import FileBrowserSave

app = Ursina()
_ed = EditorCamera()

currentLevel = Level()

def on_submit(paths):
    currentLevel.clear()
    currentLevel.load(str(paths[0]))
    currentLevel.enable()

def pickLevel():
    fb = FileBrowser(file_types=('.level'), enabled=True,on_submit = on_submit)

def newLevel():
    currentLevel.clear()

def saveLevel():
    
    wp = FileBrowserSave(file_type = '.level')
    wp.file_name_field.text_field.text = 'new_map'
    wp.data = currentLevel.save()

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
    content = [
            Text('Position:'),
            InputField(name='pos',default_value=str(tuple(entity.position))[1:-1],limit_content_to = ContentTypes.float+"-"),
            Text('Rotation:'),
            InputField(name='rot',default_value=str(tuple(entity.rotation))[1:-1],limit_content_to = ContentTypes.float+"-")
    ]
    if hasattr(entity,'power') :
        content.append(Text('Power:'))
        content.append(InputField(name='power',default_value = str(entity.power),limit_content_to = ContentTypes.float))

        
    content.append(Button(text='Update', color=color.azure))
    content.append(Button(text='Delete', color=color.azure))
    content.append(Button(text='Close', color=color.azure))
    wp = WindowPanel(
    title=str(entity),
    content=content
    )
    wp.content[-1].on_click = Func(destroy,wp)
    wp.content[-2].on_click = Func(delBlock,wp,entity)
    wp.content[-3].on_click = Func(updateElem,entity,wp.content)

def delBlock(wp,entity):
    currentLevel.blocks.remove(entity)
    destroy(entity)
    destroy(wp)

def newBlock(button):
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
for index,but in enumerate(b) :
    but.on_click = Func(newBlock,but)
    but.fit_to_text()
    but.position = (.8,index*.08)
def input(key):
    if key == 'left mouse down':
       if "Block" in str(type(mouse.hovered_entity)):
           showInfo(mouse.hovered_entity) 
app.run()