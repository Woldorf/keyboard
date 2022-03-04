import pygame, json,threading,sys,time
from pynput import keyboard
from pygame.locals import *

"""Owned and maintained by Kurced Studios
Free to use if you credit Kurced Studios"""

"""
Changes:
    keys highlight even if SHIFT is pressed
    Settings screen
        create custom keyboards
    KB choosing screen:
        Display custom KBs
        Delete custom KBs
"""

pygame.init()
pygame.display.set_caption('Keyboad')

WINDOW = pygame.display.set_mode((915,300))
SCREENWIDTH=pygame.display.Info().current_w
SCREENHEIGHT=pygame.display.Info().current_h
keyHeight = 40
keyWidth = 40
fontSize = 15

backgroundColor = (50,0,230)
GREEN = (0,255,0)
RED = (255,0,0)

class Key(pygame.sprite.Sprite):
    def __init__(self,**kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.key1 = kwargs['key1']
        self.key2 = None
        self.name = kwargs['name']
        if 'key2' in kwargs:
            self.key2 = kwargs['key2']

        self.height = keyHeight
        self.width = keyWidth
        self.width = keyWidth * (kwargs['width'])

        self.rect = pygame.Rect(kwargs['xGap'],kwargs['yGap'],self.width,self.height)
        self.color = (0,0,0)
        self.textColor = (255,215,0)
        self.activeColor = (0,0,255)
        self.active = False

        self.text1 = pygame.font.Font("freesansbold.ttf",fontSize).render(self.key1,True,self.textColor)
        self.text1R = self.text1.get_rect(center=self.rect.center)
        if self.key2 != None:
            self.text2 = pygame.font.Font("freesansbold.ttf",fontSize).render(self.key2,True,self.textColor)
            self.text2R = self.text1.get_rect(centerx=self.rect.centerx,centery=self.rect.centery-10)
            self.text1R.centery = self.rect.centery+10
        
        if kwargs['name'] == ' ':
            self.color = backgroundColor

    def update(self,**kwargs):

        if self.active:
            color = self.activeColor
        else:
            color = self.color

        pygame.draw.rect(WINDOW,color,self.rect)
        kwargs['screen'].blit(self.text1,self.text1R)
        if self.key2 != None:
            kwargs['screen'].blit(self.text2,self.text2R)

class Text:
    def __init__(self,**kwargs):
        self.text=kwargs['text']
        self.color = kwargs['color']
        self.size = int(kwargs['size'])
        self.words = pygame.font.Font("freesansbold.ttf",self.size).render(self.text,True,self.color)
        self.rect = self.words.get_rect()
        if 'leftcords' in kwargs:
            x = kwargs['leftcords']['x']
            y = kwargs['leftcords']['y']
            self.rect.topleft = (x,y)
        elif 'rightcords' in kwargs:
            x = kwargs['rightcords']['x']
            y = kwargs['rightcords']['y']
            self.rect.topright = (x,y)
        else:
            x = kwargs['x']
            y = kwargs['y']
            self.rect.center = (x,y)

    def drawSelf(self):
        self.words = pygame.font.Font("freesansbold.ttf",self.size).render(self.text,True,self.color)
        WINDOW.blit(self.words,self.rect)

class CustomKey(pygame.sprite.Sprite):
    def __init__(self,**kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.key1 = kwargs['key1']
        self.name = kwargs['name']
        if 'key2' in kwargs:
            self.key2 = kwargs['key2']
        else:
            self.key2 = None
        self.color = (0,0,0)
        self.textColor = (255,215,0)
        self.activeColor = (0,0,255)
        self.active = False
        self.moving = kwargs['moving']
    
        self.width = kwargs['width']
        self.height = kwargs['height']
        self.rect = pygame.Rect((int(kwargs['left']),int(kwargs['top'])),(self.width,self.height))

        self.text1 = pygame.font.Font("freesansbold.ttf",fontSize).render(self.key1,True,self.textColor)
        self.text1R = self.text1.get_rect(center=self.rect.center)
        if self.key2 != None:
            self.text2 = pygame.font.Font("freesansbold.ttf",fontSize).render(self.key2,True,self.textColor)
            self.text2R = self.text1.get_rect(centerx=self.rect.centerx,centery=self.rect.centery-10)
            self.text1R.centery = self.rect.centery+10

    def update(self,**kwargs):
        if self.active:
            color = self.activeColor
        else:
            color = self.color

        if self.moving:
            if kwargs['kbbox'].collidepoint(kwargs['mousepos']):
                self.rect.topleft = (int(kwargs['mousepos'][0]-self.rect.width/2),int(kwargs['mousepos'][1]-self.rect.height/2)) 
                self.text1R.center = self.rect.center
                if self.key2 != None:
                    self.text2 = pygame.font.Font("freesansbold.ttf",fontSize).render(self.key2,True,self.textColor)
                    self.text2R = self.text1.get_rect(centerx=self.rect.centerx,centery=self.rect.centery-10)
                    self.text2R.centerx=self.rect.centerx
                    self.text2R.centery=self.rect.centery-10
                    self.text1R.centery = self.rect.centery+10

        self.text1 = pygame.font.Font("freesansbold.ttf",fontSize).render(self.key1,True,self.textColor)
        self.text1R = self.text1.get_rect(center=self.rect.center)
        if self.key2 != None:
            self.text2 = pygame.font.Font("freesansbold.ttf",fontSize).render(self.key2,True,self.textColor)
            self.text2R = self.text1.get_rect(centerx=self.rect.centerx,centery=self.rect.centery-10)
            self.text2R.centerx=self.rect.centerx
            self.text2R.centery=self.rect.centery-10
            self.text1R.centery = self.rect.centery+10

        pygame.draw.rect(kwargs['screen'],color,self.rect)
        if self.key2 != None:
            self.text2R = self.text1.get_rect(centerx=self.rect.centerx,centery=self.rect.centery-10)
            self.text2R.centerx=self.rect.centerx
            self.text2R.centery=self.rect.centery-10
            self.text1R.centery = self.rect.centery+10
            kwargs['screen'].blit(self.text2,self.text2R)
            kwargs['screen'].blit(self.text1,self.text1R)
        else:
            kwargs['screen'].blit(self.text1,self.text1R)

def getKBfile():
    with open('./format.json','r') as F:
        kbLines = json.load(F)
    return kbLines

def keyboardListenerSettings():
    global customkeys,settingsACTIVE
    with keyboard.Events() as events:
        for e in events:
            if not settingsACTIVE:
                return
            if not editing:
                if type(e) == keyboard.Events.Press:
                    keyAlready = False
                    for i in customkeys:
                        if i.moving:
                            keyAlready = True
                    if not keyAlready:
                        try:
                            customkeys.add(CustomKey(key1=str(e.key.char.lower()),key2=str(e.key.char.upper()),name=str(e.key.char.lower()),width=keyWidth,height=keyHeight,left=pygame.mouse.get_pos()[0],top=pygame.mouse.get_pos()[1],moving=True))
                        except Exception as E:
                            customkeys.add(CustomKey(key1=str(e.key.name),name=str(e.key.name),width=keyWidth,height=keyHeight,left=pygame.mouse.get_pos()[0],top=pygame.mouse.get_pos()[1],moving=True))

def keyboadListenerActive():
    global keyGroup
    with keyboard.Events() as events:
        for event in events:
            for i in keyGroup:
                try:
                    if event.key.char.lower() == i.name:
                        if type(event) == keyboard.Events.Press:
                            i.active = True
                        else:
                            i.active = False
                        break
                except:
                    if event.key.name == i.name:
                        if type(event) == keyboard.Events.Press:
                            i.active = True
                        else:
                            i.active = False
                        break
                        
def getkgroup(dictName):
    kblines = getKBfile()
    keyGroup = pygame.sprite.Group()
    verticleSpacing = 40
    horizontileSpacing = 15
    yGap = 5
    custom = False

    if dictName in kblines:
        keyboard = kblines[dictName]
    else:
        keyboard = kblines['CUSTUM'][dictName]
        custom = True
    if not custom:
        tempKeyList = []
        for index,row in enumerate(keyboard):
            xGap = 5
            for key in keyboard[row]:
                if 't2' in key:
                    tempKeyList.append(Key(key1=key['t1'],key2=key['t2'],width=key['size'],yGap=(index*verticleSpacing) + yGap,xGap=xGap,name=key['name']))
                else:
                    tempKeyList.append(Key(key1=key['t1'],width=key['size'],yGap=(index*verticleSpacing) + yGap,xGap=xGap,name=key['name']))
                xGap += tempKeyList[-1].width + horizontileSpacing
            yGap += 10
        for i in tempKeyList:
            if i == tempKeyList[0]:
                i.color == RED
            keyGroup.add(i)
    else:
        for index,key in enumerate(keyboard):
            if 't2' in key:
                keyGroup.add(CustomKey(key1=key['t1'],key2=key['t2'],width=key['width'],height=key['height'],left=key['left'],top=key['top'],moving=False,name=key['name']))
            else:
                keyGroup.add(CustomKey(key1=key['t1'],width=key['width'],height=key['height'],left=key['left'],top=key['top'],moving=False,name=key['name']))
    return keyGroup

def terminate():
    pygame.quit()
    sys.exit()

def boardType():
    kblines = getKBfile()
    wordlist = []
    templist = ['Please select a keyboard layout from the below options']
    for index,i in enumerate(kblines):
        if i == 'CUSTUM':
            break
        templist.append((str(index+1)+': '+i))

    for i in kblines['CUSTUM']:
        templist.append(str(index+1)+': '+str(i))
        index += 1
    templist.append('TAB to select, ENTER to confirm')

    for i in templist:
        if i == templist[0]:
            wordlist.append(Text(text=i,color=(255,255,255),size=30,x=SCREENWIDTH/2,y=SCREENHEIGHT/4))
        else:
            wordlist.append(Text(text=i,color=(255,255,255),size=30,x=SCREENWIDTH/2,y=yGap))
        yGap = wordlist[-1].rect.h + wordlist[-1].rect.bottom
    settings = Text(text='SETTINGS',color=(255,255,255),size=20,rightcords={'x':SCREENWIDTH-20,'y':20})

    pointer = 1
    while True:
        WINDOW.fill(backgroundColor)
        for i in wordlist:
            i.drawSelf()
        settings.drawSelf()
        pygame.display.update()
        for i in pygame.event.get():
            if i.type == QUIT:
                terminate()
            elif i.type == MOUSEBUTTONDOWN:
                mousepresses = pygame.mouse.get_pressed(num_buttons=3)
                mousepos = pygame.mouse.get_pos()
                if mousepresses[0] and settings.rect.collidepoint(mousepos):
                    kbSettings()
            elif i.type == KEYDOWN:
                if i.key == K_TAB:
                    pointer += 1
                    if pointer > len(wordlist[1:-1]):
                        pointer = 1
                    for index,i in enumerate(wordlist[1:-1]):
                        if index == pointer - 1:
                            wordlist[index + 1].color = (255,0,0)
                        else:
                            wordlist[index + 1].color = (255,255,255)
                elif i.key == K_RETURN:
                    kbname = wordlist[pointer].text[3:]
                    return kbname
                elif i.key == K_ESCAPE:
                    terminate()

def savecustomKB(kbbox,kbname):
    kblines = getKBfile()
    newKB = []
    for i in customkeys:
        if i.key2 != None:
            newKB.append({'name':i.name,'t1':i.key1,'t2':i.key2,'width':i.width,'height':i.height,'top':(i.rect.top - kbbox.top),'left':(i.rect.left - kbbox.left)})
        else:
            newKB.append({'name':i.name,'t1':i.key1,'width':i.width,'height':i.height,'top':(i.rect.top - kbbox.top),'left':(i.rect.left - kbbox.left)})
    kblines['CUSTUM'][kbname]=newKB
    with open('./format.json','w') as F:
        F.write(json.dumps(kblines,indent=2))

def kbSettings():
    #Larger window
    global customkeys,editing,settingsACTIVE
    settingsACTIVE = True

    settingWINDOW = pygame.display.set_mode((960,450))
    settingWIDTH = pygame.display.Info().current_w
    settingHEIGHT = pygame.display.Info().current_h

    textColor = (255,255,255)
    textSize = 30
    yGap = 13
    smalltSize = int(textSize - (textSize/6))

    textobjlist = [Text(text='SETTINGS - ESC TO EXIT',color=textColor,size=textSize,x=settingWIDTH/2,y=30)]
    helpwords = ['Drag and drop keys to a location','Press a key to add it to the layout','Right Click on an item to delete it from the layout']
    for i in helpwords:
        textobjlist.append(Text(text=i,color=textColor,size=smalltSize,x=settingWIDTH/2,y=textobjlist[-1].rect.bottom + yGap))

    settingwords = ['Press the base key then the modified key','Click off to close the menue','ENTER to begin sizing the key','HOLD SHIFT to lock the key to your mouse']
    settingWlist = []
    for i in settingwords:
        settingWlist.append(Text(text=i,color=GREEN,size=textSize/2,x=1,y=1))
    editing = False

    sizingwords = ['Arrow Keys to adjust the sizing','It will NOT invert, just get smaller','Click off or press ENTER to save']
    sizingWlist = []
    for i in sizingwords:
        sizingWlist.append(Text(text=i,color=GREEN,size=textSize/2,x=1,y=1))
    sizing = False
    resizedistance = 5

    save = Text(text='SAVE',color=RED,size=textSize/2,rightcords={'x':settingWIDTH - 20,'y':20})
    exit = Text(text='BACK',color=RED,size=textSize/2,rightcords={'x':settingWIDTH - 20,'y':save.rect.bottom + 20})
    savingwords = ['ENTER to confirm',''] #The last one NEEDS TO BE EMPTY and is what the name of the keyboard will be
    savingWlist = [Text(text='Please name your keyboard',color=textColor,size=textSize,x=settingWIDTH/2,y=settingHEIGHT/2)]
    yGap = 15
    for i in savingwords:
        savingWlist.append(Text(text=i,color=textColor,size=textSize,x=settingWIDTH/2,y=savingWlist[-1].rect.bottom + yGap))
    savingWlist[-1].size = textSize - 10
    saving = False

    customkeys = pygame.sprite.Group()

    #Bounding box:
    kbbox = pygame.rect.Rect(((settingWIDTH/2) - (SCREENWIDTH/2)),(settingHEIGHT-SCREENHEIGHT)-20,SCREENWIDTH,SCREENHEIGHT)
    
    listenerThread = threading.Thread(target=keyboardListenerSettings)
    listenerThread.daemon = True
    listenerThread.start()
    while True:
        for e in pygame.event.get():
            if e.type == QUIT:
                terminate()
            if editing:
                if e.type == TEXTINPUT:
                    if not edited1:
                        editingKey.key1 = e.text
                        edited1 = True
                    else:
                        editingKey.key2 = e.text
                        edited1 = False
                        editing = False
                        editingKey = None
                elif e.type == KEYDOWN:
                    if e.key == K_RETURN:
                        sizing = not sizing
                    if sizing:
                        if e.key == K_UP:
                            if editingKey.rect.height - resizedistance > 0:
                                editingKey.rect.height -= resizedistance
                        elif e.key == K_DOWN:
                            editingKey.rect.height += resizedistance
                        elif e.key == K_LEFT:
                            if editingKey.rect.width - resizedistance > 0:
                                editingKey.rect.width -= resizedistance
                        elif e.key == K_RIGHT:
                            editingKey.rect.width += resizedistance
                        elif e.key == K_LSHIFT or e.key == K_RSHIFT:
                            editingKey.moving = True
                elif e.type == KEYUP:
                    if e.key == K_LSHIFT or e.key == K_RSHIFT:
                        editingKey.moving = False
            elif sizing:
                if e.type == TEXTINPUT and len(savingWlist[-1].text) < 20:
                    savingWlist[-1].text += str(e.text)
                    savingWlist[-1].rect = savingWlist[-1].words.get_rect(center = (settingWIDTH/2,savingWlist[-1].rect.centery))
                elif e.type == KEYDOWN:
                    if len(savingWlist[-1].text) > 0:
                        if e.key == K_BACKSPACE:
                            savingWlist[-1].text = savingWlist[-1].text[:-1]
                        elif e.key == K_RETURN:
                            settingsACTIVE = False
                            savecustomKB(kbbox,savingWlist[-1].text)
                            return

            if e.type == MOUSEBUTTONDOWN:
                mousepresses = pygame.mouse.get_pressed(num_buttons=3)
                mousepos = pygame.mouse.get_pos()
                if mousepresses[0]:
                    if save.rect.collidepoint(mousepos):
                        saving = True
                        settingsACTIVE = False
                    elif exit.rect.collidepoint(mousepos):
                        return
                    for i in customkeys:
                        if i.rect.collidepoint(mousepos):
                            if i.moving:
                                i.moving = False
                                break
                            else:
                                editing = True
                                editingKey = i
                                edited1 = False
                                break
                        else:
                            editing = False
                            editingKey = None
                            sizing = False
                elif mousepresses[2]:
                    for i in customkeys:
                        if i.rect.collidepoint(mousepos):
                            customkeys.remove(i)

        settingWINDOW.fill(backgroundColor)
        pygame.draw.rect(settingWINDOW,RED,kbbox,width=3)
        customkeys.update(screen=settingWINDOW,mousepos=pygame.mouse.get_pos(),kbbox=kbbox)
        if editing:
            if not sizing:
                yGap = 0
                xGap = 10
                for i in settingWlist:
                    i.rect.right = int(editingKey.rect.left - xGap)
                    i.rect.bottom = int(editingKey.rect.centery + yGap)
                    i.drawSelf()
                    yGap += 15
            else:
                yGap = 0
                xGap = 10
                for i in sizingWlist:
                    i.rect.right = int(editingKey.rect.left - xGap)
                    i.rect.bottom = int(editingKey.rect.centery + yGap)
                    i.drawSelf()
                    yGap += 15
        if not saving:
            for i in textobjlist:
                i.drawSelf()
        else:
            for i in savingWlist:
                i.drawSelf()
        save.drawSelf()
        exit.drawSelf()
        pygame.display.flip()

#settingsScreen()
keyGroup = getkgroup(boardType())

mainThread = threading.Thread(target=keyboadListenerActive)
mainThread.daemon = True
mainThread.start()

WINDOW = pygame.display.set_mode((915,300))
while True:
    WINDOW.fill(backgroundColor)
    keyGroup.update(screen=WINDOW)
    for i in pygame.event.get():
        if i.type == QUIT:
            terminate()
    pygame.display.flip()