from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.clock import Clock
from functools import partial
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
import threading
import time
import random
from kivy.config import Config


global Size 
Size = 50 #размер плитки
arr = [2, 1, 4, 5, 32, 12, 1]
Width = 370
if(len(arr) * Size + 20 > Width):
    Width = len(arr) * Size + 20

class ClassName(object):
    """docstring for ClassName"""
    def __init__(self, arg):
        super(ClassName, self).__init__()
        self.arg = arg

        

Config.set('kivy', 'keyboard_mode', 'systemanddoc')
Window.size = (Width, 600)
Window.minimum_width, Window.minimum_height = (Width, 400)
Window.clearcolor = (.48, .56, .65, 1)


Speed = 0.3
SelectQS = False
StopSort = True
Text = ''
FixIndex = []
for i in range(len(arr)):
    FixIndex.append(i)

# def StartThread(fl):
#     thread1 = threading.Thread(target=GnomeSort, args=(arr, fl))
#     thread2 = threading.Thread(target=QuickSort, args=(arr, 0, len(arr) - 1, fl))
#     thread1.start()
#     thread2.start()

def StartGnomeSort(fl):
    thread = threading.Thread(target=GnomeSort, args=(arr, fl))
    thread.start()

def StartQuickSort(fl):
    thread = threading.Thread(target=QuickSort, args=(arr, 0, len(arr) - 1, fl))
    thread.start()

def ResetButtons(fl):
    for i in range(len(arr)):
        fl.children[len(arr) - i - 1].text = str(arr[i])
        fl.children[len(arr) - i - 1].pos = (10 + Size*i, 50)
        fl.children[len(arr) - i - 1].background_color = [0.34, 0, 2.55, 1]

def GetRestart(self):
    global FixIndex
    for i in range(len(arr)):
        arr[i] = random.randint(0, 999)
        FixIndex[i] = i
    global StopSort
    global Text
    Text = ''
    StopSort = True
    ResetButtons(self.parent.parent.children[1])


def StartButton(instance):
    global StopSort
    if StopSort:
        instance.text = 'Стоп'
        StartAnimation(instance)
    else:
        instance.text = 'Старт'
        GetRestart(instance)

def StartAnimation(instance):
    global StopSort
    global SelectQS
    StopSort = False
    if SelectQS:
        StartQuickSort(instance.parent.parent.children[1])
    else:
        StartGnomeSort(instance.parent.parent.children[1])

def QuickSort(arr, l, r, fl):
    time.sleep(0.5)
    global Text
    global Speed
    global FixIndex
    global StopSort
    if StopSort:
        return
    if l >= r:
        return
    else:
        ShowArray(l, r, fl)
        time.sleep(Speed*3)
        Text += 'подмассив ' + str(l) + ' - ' + str(r) + '\n'
        fl.parent.children[2].children[0].text = Text
        fl.children[len(arr) - FixIndex[l] - 1].background_color = [1, 1, 1, 1]
        fl.children[len(arr) - FixIndex[r] - 1].background_color = [1, 1, 1, 1]
        temp = random.randint(l, r)
        q = arr[temp] #random.choice(arr[l:r + 1])
        fl.children[len(arr) - FixIndex[temp] - 1].background_color = [2.32, .88, .96, 1]
        i = l
        j = r
        while i <= j:
            while arr[i] < q:
                i += 1
            while arr[j] > q:
                j -= 1
            if i <= j: 
                arr[i], arr[j] = arr[j], arr[i]
                if i != j:
                    GetShufle(i, j, fl)
                Text += str(i) + ' [' + str(arr[i]) + '] меняем с ' + str(j) + ' [' + str(arr[j]) + ']\n'
                time.sleep(Speed * 3)
                i += 1
                j -= 1
                fl.children[len(arr) - FixIndex[l] - 1].background_color = [0.34, 0, 2.55, 1]
                fl.children[len(arr) - FixIndex[r] - 1].background_color = [0.34, 0, 2.55, 1]
                fl.children[len(arr) - FixIndex[temp] - 1].background_color = [0.34, 0, 2.55, 1]
                QuickSort(arr, l, j, fl)
                QuickSort(arr, i, r, fl)
        fl.children[len(arr) - FixIndex[temp] - 1].background_color = [0.34, 0, 2.55, 1]


def GnomeSort(arr, fl):
    global StopSort
    global FixIndex
    text = ''
    if StopSort:
        return
    time.sleep(Speed)
    position = 0
    while(position < len(arr)):
        fl.children[len(arr) - FixIndex[position] - 1].background_color = [2.32, .88, .96, 1]
        if(position > 0):
            fl.children[len(arr) - FixIndex[position - 1] - 1].background_color = [1, 1, 1, 1]
        if StopSort:
            return
        fl.parent.children[2].children[0].text = text
        
        time.sleep(Speed * 3)
        if position == 0 or arr[position] >= arr[position - 1]:
            position += 1
        else:
            arr[position], arr[position - 1] = arr[position - 1], arr[position]
            GetShufle(position, position - 1, fl)
            text += str(position - 1) + ' [' + str(arr[position - 1]) + '] меняем с ' + str(position) + ' [' + str(arr[position]) + ']\n'
            position -= 1

def GetShufle(index1, index2, fl):
    #global Size
    anim1 = Animation(y = Size*2, duration = Speed)
    anim1 += Animation(x = 10 + Size*index2, duration = Speed)
    anim1 += Animation(y = 50, duration = Speed)
    anim2 = Animation(y = Size*3, duration = Speed)
    anim2 += Animation(x = 10 + Size*index1, duration = Speed)
    anim2 += Animation(y = 50, duration = Speed)
    FixIndex[index1], FixIndex[index2] = FixIndex[index2], FixIndex[index1]
    anim1.start(fl.children[len(arr) - FixIndex[index2] - 1])
    anim2.start(fl.children[len(arr) - FixIndex[index1] - 1])

def ShowArray(startIndex, endIndex, fl):
    #global Size
    while startIndex <= endIndex:
        anim = Animation(y = Size/2, duration = Speed)
        anim += Animation(y = 50, duration = Speed)
        anim.start(fl.children[len(arr) - FixIndex[startIndex] - 1])
        startIndex += 1


def Generation(arr, self):
    global Size
    fl = FloatLayout(
        size = (100, 10),
        size_hint = (1, 1))
    for i in range(len(arr)):
        b = Button(
            text = str(arr[i]),
            size = (Size, Size),
            size_hint = (None, None),
            background_color =  [0.34, 0, 2.55, 1],
            pos = (10 + Size*i, 50)) #on_press = self.ChangeArr
        fl.add_widget(b)
    return fl

def SelectQuicksort(instance):
    global SelectQS
    if SelectQS:
        SelectQS = False
        instance.text = 'GnomeSort'
    else:
        SelectQS = True
        instance.text = 'QuickSort'

def AddSpeed(instance):
    global Speed
    Speed += 0.1

def ReduceSpeed(instance):
    global Speed
    if Speed > 0.1:
        Speed -= 0.1

def GenerateMenu():
    menu = BoxLayout(size_hint = (1, 1),
                    orientation='horizontal',
                    padding = [10, 0, 0, 0])
    menu.add_widget(Button(text = 'Start',
                        size_hint = (None, None),
                        size = (50, 20),
                        on_press = StartButton))
    menu.add_widget(Button(text = 'GnomeSort',
                        size_hint = (None, None),
                        size = (100, 20),
                        on_press = SelectQuicksort))
    menu.add_widget(Button(text='замедлить',
                        size_hint = (None, None),
                        size = (100, 20),
                        on_press = AddSpeed))
    menu.add_widget(Button(text='ускорить',
                        size_hint = (None, None),
                        size = (100, 20),
                        on_press = ReduceSpeed))
    return menu

class BestApp(App):
    def ChangeArr(button, self):
        content = BoxLayout(orientation='vertical')
        content.add_widget(TextInput(text='0',
                            size_hint = (1, None),
                            size=(0, 60),
                            multiline=False,
                            input_filter = 'int'))
        content.add_widget(Button(text='изменить', on_press=Get))
        popup = Popup(title='Изменить кнопку',
                        content=content,
                        size_hint=(None, None),
                        size=(200, 200))
        popup.open()

    def build(self):
        self.title = 'Sort'
        bl = BoxLayout(orientation='vertical')
        fl = Generation(arr, self)
        textBox = BoxLayout()
        textBox.add_widget(Label(text='История'))
        bl.add_widget(textBox)
        bl.add_widget(fl)
        bl.add_widget(GenerateMenu())
        return bl

if __name__ == '__main__':
    BestApp().run()