import pygame, json,threading,sys
from pynput import keyboard
from pygame.locals import *

"""Owned and maintained by Kurced Studios
Free to use if you credit Kurced Studios"""

pygame.init()
pygame.display.set_caption('Keyboad')

WINDOW = pygame.display.set_mode((915,300))
SCREENWIDTH=pygame.display.Info().current_w
SCREENHEIGHT=pygame.display.Info().current_h

TPS = 40
TPSCLOCK = pygame.time.Clock()

keyHeight = 40
keyWidth = 40
fontSize = 15

backgroundColor = (50,0,230)

with open('./format.json','r') as F:
    kbLines = json.load(F)

class Key:
    def __init__(self,**kwargs):
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

    def drawSelf(self):

        if self.active:
            color = self.activeColor
        else:
            color = self.color

        pygame.draw.rect(WINDOW,color,self.rect)
        WINDOW.blit(self.text1,self.text1R)
        if self.key2 != None:
            WINDOW.blit(self.text2,self.text2R)

class Text:
    def __init__(self,dict=None,**kwargs):
        if dict != None:
            kwargs = dict
        self.text=kwargs['text']
        self.color = kwargs['color']
        self.size = kwargs['size']
        self.words = pygame.font.Font("freesansbold.ttf",self.size).render(self.text,True,self.color)
        self.rect = self.words.get_rect()
        if 'leftcords' in kwargs:
            self.x = kwargs['leftcords']['x']
            self.y = kwargs['leftcords']['y']
            self.rect.topleft = (self.x,self.y)
        elif 'rightcords' in kwargs:
            self.x=kwargs['rightcords']['x']
            self.y=kwargs['rightcords']['y']
            self.rect.topright = (self.x,self.y)
        else:
            self.x = kwargs['x']
            self.y = kwargs['y']
            self.rect.center = (self.x,self.y)

    def drawSelf(self):
        self.words = pygame.font.Font("freesansbold.ttf",self.size).render(self.text,True,self.color)
        WINDOW.blit(self.words,self.rect)

def getkgroup(choice):
    keyList = []
    verticleSpacing = 40
    horizontileSpacing = 15
    yGap = 5
    if choice == 1:
        keyboard = kbLines['DVORAK']
    elif choice == 2:
        keyboard = kbLines['QWERTY']

    for index,i in enumerate(keyboard):
        xGap = 5
        for key in keyboard[i]:
            if 't2' in key['out']:
                keyList.append(Key(key1=key['out']['t1'],key2=key['out']['t2'],width=key['size'],yGap=(index*verticleSpacing) + yGap,xGap=xGap,name=key['name']))
            else:
                keyList.append(Key(key1=key['out']['t1'],width=key['size'],yGap=(index*verticleSpacing) + yGap,xGap=xGap,name=key['name']))
            xGap += keyList[-1].width + horizontileSpacing
        yGap += 10
    return keyList

def keyPress(key):
    for i in keyList:
        try:
            if key.char == i.name:
                i.active = True
                break
        except:
            if key.name == i.name:
                i.active = True
                break

def keyRelease(key): 
    for i in keyList:
        try:
            if key.char == i.name:
                i.active = False
                break
        except:
            if key.name == i.name:
                i.active = False
                break

def terminate():
    pygame.quit()
    sys.exit()

def boardType():
    wordlist = []
    templist = ['Please select a keyboard layout from the below options']
    for index,i in enumerate(kbLines):
        templist.append((str(index+1)+': '+i))

    templist.append('TAB to select, ENTER to confirm')
    for i in templist:
        if i == templist[0]:
            wordlist.append(Text(text=i,color=(255,255,255),size=30,x=SCREENWIDTH/2,y=SCREENHEIGHT/4))
        else:
            wordlist.append(Text(text=i,color=(255,255,255),size=30,x=SCREENWIDTH/2,y=yGap))
        yGap = wordlist[-1].rect.h + wordlist[-1].rect.bottom
    pointer = 0
    while True:
        WINDOW.fill(backgroundColor)
        for i in wordlist:
            i.drawSelf()
        pygame.display.update()
        for i in pygame.event.get():
            if i.type == QUIT:
                terminate()
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
                    return pointer

keyList = getkgroup(boardType())

def main():
    global keyList
    with keyboard.Events() as events:
        for event in events:
            for i in keyList:
                try:
                    if event.key.char == i.name:
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

mainThread = threading.Thread(target=main)
mainThread.daemon = True
mainThread.start()

iteration = 0
while True:
    WINDOW.fill(backgroundColor)
    for i in keyList:
        i.drawSelf()
    for i in pygame.event.get():
        if i.type == QUIT:
            terminate()
    TPSCLOCK.tick(TPS)
    pygame.display.flip()
