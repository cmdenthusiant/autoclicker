import time,pynput,threading,tkinter,math,base64,icon,os,random,string
isSettingKey = False
mouseController = pynput.mouse.Controller()
keyboardController = pynput.keyboard.Controller()

class gui:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title('Autoclicker by quiet#0875')
        self.window.wm_maxsize(600,400)
        self.window.wm_minsize(600,400)
        self.window.geometry('600x400')
        self.setWindowIcon()
        self.toggleKeys = []
        self.addEventBtn = tkinter.Button(self.window,text='+',width=2,height=1,command=self.addToggleKey)
        self.addEventBtn.grid(column=0,row=0)
        self.window.mainloop()
    def addToggleKey(self):
        newKey = key(self)
        self.toggleKeys.append(newKey)
        row = len(self.toggleKeys) * 50
        self.addEventBtn.place(x=0,y=row)
    def setWindowIcon(self):
        iconName = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        iconfile = open(iconName+'.ico','wb+')
        iconfile.write(base64.b64decode(icon.iconImg))
        iconfile.close()
        self.window.iconbitmap(iconName+'.ico')
        os.remove(iconName+'.ico')

class key:
    def __init__(self,gui):
        self.gui = gui
        self.window = gui.window
        self.key = None
        self.HotKey = pynput.keyboard.Key.f5
        self.interval = 100
        self.Status = False
        self.lastInterval = 100
        self.keyLabel = tkinter.Label(self.window,text="Key:")
        self.keyBtn = tkinter.Button(self.window,text=str(self.key),command=self.keyBtnPressed)
        self.intervalLabel = tkinter.Label(self.window,text="Interval(ms):")
        self.intervalInput = tkinter.Entry(self.window,width=10)
        self.intervalInput.bind("<Enter>",lambda x:self.intervalInput.configure(state="normal"))
        self.intervalInput.bind("<Leave>",lambda x:self.intervalInput.configure(state="readonly"))
        self.intervalInput.bind("<Key>",self.IntervalInput)
        self.intervalInput.insert(tkinter.END,'100')
        self.intervalInfo = tkinter.Label(self.window,text="-1 if Toggle")
        self.HotKeyLabel = tkinter.Label(self.window,text="HotKey:")
        self.HotKeyBtn = tkinter.Button(self.window,text="f5",command=self.HotKeyBtnPressed)
        self.StatusLabel = tkinter.Label(self.window,text='status: Stopped')
        self.allElem = [
            self.keyLabel,
            self.keyBtn,
            self.intervalLabel,
            self.intervalInput,
            self.intervalInfo,
            self.HotKeyLabel,
            self.HotKeyBtn,
            self.StatusLabel
        ]
        row = (len(self.gui.toggleKeys)+1) * 50
        for e in self.allElem:
            e.grid()
        self.keyLabel.place(x=50,y=row-25)
        self.keyBtn.place(x=90,y=row-25)
        self.intervalLabel.place(x=180,y=row-25)
        self.intervalInput.place(x=260,y=row-25)
        self.intervalInfo.place(x=260,y=row)
        self.HotKeyLabel.place(x=360,y=row-25)
        self.HotKeyBtn.place(x=420,y=row-25)
        self.StatusLabel.place(x=500,y=row-25)
        self.HotKeyListeners = [
            pynput.mouse.Listener(on_click=lambda a1,a2,key,a4:self.HotKeyPressed(key)),
            pynput.keyboard.Listener(on_press=self.HotKeyPressed)
        ]
        for listener in self.HotKeyListeners: listener.start()
        self.PressKeyThread = None
        self.PressKeyThreadNo = 0
    def keyBtnPressed(self):
        global isSettingKey
        self.key = None
        isSettingKey = True
        mouseListener = pynput.mouse.Listener(on_click=self.mouseClickedKey)
        keyboardListener = pynput.keyboard.Listener(on_press=self.keyboardPressedKey)
        mouseListener.start()
        keyboardListener.start()
        threading.Thread(target=self.keyBtnPressedWait,args=([mouseListener,keyboardListener],)).start()
    def keyBtnPressedWait(self,listeners):
        global isSettingKey
        timeLeft = 3.0
        while timeLeft>0:
            self.keyBtn['text'] = 'Listening... ' + str(math.ceil(timeLeft))
            if self.key != None:break
            timeLeft -= 0.1
            time.sleep(0.1)
        isSettingKey = False
        self.keyBtn['text'] = str(self.key) if self.key == None or type(self.key) == pynput.keyboard.KeyCode else (('mouse' if type(self.key) == pynput.mouse.Button else '') + str(self.key.name))
        for listener in listeners: listener.stop()
    def mouseClickedKey(self,a1,a2,key,a4):
        if key != pynput.mouse.Button.unknown: self.key=key
    def keyboardPressedKey(self,key):
        self.key = key
    def IntervalInput(self,e=None):
        interval = self.intervalInput.get()
        neg = 1
        if interval.startswith('-'):
            neg = -1
            interval = interval[1:]
        if not interval.isdigit():
            neg = 1
            interval = self.lastInterval
        self.interval = neg * int(interval)
        self.lastInterval = neg * int(interval)
    def HotKeyBtnPressed(self):
        global isSettingKey
        self.HotKey = None
        isSettingKey = True
        mouseListener = pynput.mouse.Listener(on_click=self.mouseClickedHotKey)
        keyboardListener = pynput.keyboard.Listener(on_press=self.keyboardPressedHotKey)
        mouseListener.start()
        keyboardListener.start()
        threading.Thread(target=self.HotKeyBtnPressedWait,args=([mouseListener,keyboardListener],)).start()
    def HotKeyBtnPressedWait(self,listeners):
        global isSettingKey
        timeLeft = 3.0
        while timeLeft>0:
            self.HotKeyBtn['text'] = 'Listening... ' + str(math.ceil(timeLeft))
            if self.HotKey != None:break
            timeLeft -= 0.1
            time.sleep(0.1)
        isSettingKey = False
        self.HotKeyBtn['text'] = str(self.HotKey) if self.HotKey == None or type(self.HotKey) == pynput.keyboard.KeyCode else (('mouse' if type(self.HotKey) == pynput.mouse.Button else '') + str(self.HotKey.name))
        for listener in listeners: listener.stop()
    def mouseClickedHotKey(self,a1,a2,key,a4):
        if key != pynput.mouse.Button.unknown: self.HotKey=key
    def keyboardPressedHotKey(self,key):
        self.HotKey = key
    def updateStatus(self):
        self.StatusLabel['text'] = 'status: ' + ["Stopped","Started"][self.Status]
    def HotKeyPressed(self,key):
        if key != self.HotKey or self.key == None or isSettingKey:return
        self.Status = not self.Status
        self.updateStatus()
        self.IntervalInput()
        if self.Status:
            self.PressKeyThreadNo += 1
            self.PressKeyThread = threading.Thread(target=self.PressKeyLoop,args=(self.PressKeyThreadNo,))
            self.PressKeyThread.start()
    def PressKeyLoop(self,No):
        while self.Status and self.key != None and self.PressKeyThreadNo == No:
            if isSettingKey: continue
            if type(self.key) == pynput.mouse.Button:
                if self.interval == -1:
                    mouseController.press(self.key)
                    break
                else: mouseController.click(self.key)
            else:
                if self.interval == -1:
                    keyboardController.press(self.key)
                    break
                else: keyboardController.tap(self.key)
            if self.interval != -1: time.sleep(self.interval/1000)

gui()