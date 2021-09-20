import tkinter
import threading
from tkinter.constants import LEFT
import win32gui,win32api,win32con
import time
import pyperclip
import pyautogui
class PkrWindow:
    def __init__(self):
        self.window_name = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        self.hwnd = win32gui.FindWindow(None,self.window_name)
        self.table_name ="Anonymt bord 2749 - 56773411 - NL Hold'em - kr5.00/10.00"
        try:
            self.big_blind = float(self.table_name.split("-")[3].split("/")[1])
        except:
            self.big_blind = 10.0
        self.custom_size = 0
        self.bb3vsSB = 9.5 #keybind shift+1 
        self.threeSB = 9.75 #keybind shift+2
        self.threesbLarge = 10.25 #keybind shift+3
        self.threebetBB = 11.25#keybind shift+4
        self.fourBetOP = 23.25
        self.bet_list = [5.5,self.bb3vsSB,self.threeSB,self.threesbLarge,self.threebetBB,self.fourBetOP]
        
        self.button_list = []
        self.root = tkinter.Tk()
        self.root.geometry("203x45")
        self.top = tkinter.Frame(self.root)
        self.top.pack()
        self.label = tkinter.Label(text="BB:"+str(self.big_blind)+"kr")
        self.label.pack()
        self.create_betbutton()
        self.thread = threading.Thread(target=self.get_last_active_poker_table,daemon=True)
        self.thread.start()

        self.root.mainloop()
        
    def create_betbutton(self):
        for size in self.bet_list:
            button = tkinter.Button(self.root,text=str(size),command= lambda in_size = size: self.write_Size(in_size))
            button.pack(in_=self.top,side=LEFT)
            self.button_list.append(button)

    def adjust_click_pos(self):
        self.table_geo =win32gui.GetWindowRect(self.hwnd)
        print(self.table_geo)
        betbox_x =  1223
        betbox_y = 862#868
        default_w = 1359    
        default_h = 1057
        t_x = abs(self.table_geo[0])
        t_y = abs(self.table_geo[1])
        t_w = abs(self.table_geo[2])-abs(t_x)
        t_h = abs(self.table_geo[3])-abs(t_y)
        print(t_x,t_y,t_w,t_h,"e")
        adjuster_x = ((t_w)/default_w) 
        adjuster_y = ((t_h)/default_h)
        self.x_adjusted =  adjuster_x*(betbox_x)
        self.y_adjusted = adjuster_y*(betbox_y )
        self.x_adjusted = int(self.x_adjusted)
        if t_w>470:
        
            self.y_adjusted = int(self.y_adjusted)
        else:
            self.x_adjusted = 435
            self.y_adjusted = 300
        print(self.x_adjusted,self.y_adjusted,"adjusted")
    def get_last_active_poker_table(self):
        while True:
            print(win32gui.GetCursorPos())

            if "NL Hold" in win32gui.GetWindowText(win32gui.GetForegroundWindow()) :
                self.table_name = win32gui.GetWindowText(win32gui.GetForegroundWindow())
                print(self.table_name.split("-"))
                for s in self.table_name.split("-"):
                    if "/" in s:
                        self.big_blind = float(s.split("/")[1])
                self.label.configure(text="BB:"+str(self.big_blind)+"kr")
                self.hwnd = win32gui.FindWindow(None,self.table_name)
                self.adjust_click_pos()
            elif  "table" in win32gui.GetWindowText(win32gui.GetForegroundWindow()):
                self.table_name = win32gui.GetWindowText(win32gui.GetForegroundWindow())
                print(self.table_name.split("-"))
                for s in self.table_name.split("-"):
                    if "/" in s:
                        self.big_blind = float(s.split(" ")[0].split("/")[1])
                self.label.configure(text="BB:"+str(self.big_blind)+"kr")
                self.hwnd = win32gui.FindWindow(None,self.table_name)
                self.adjust_click_pos()
            time.sleep(0.5)
    def write_Size(self,in_size):

        print(self.window_name,self.table_name)
        
        real_size = self.big_blind*in_size
        real_size = str(real_size)
        real_size = real_size.split(".")
        if real_size[1] == "0":
            real_size = real_size[0]
        else:
            try:

                real_size = real_size[0]+"."+real_size[1][0]+real_size[1][1]

            except:
                real_size =  real_size[0]+"."+real_size[1]
        
        lParam = win32api.MAKELONG(self.x_adjusted, self.y_adjusted)
        win32gui.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam) 
        win32gui.SendMessage(self.hwnd, win32con.WM_LBUTTONUP, 0, lParam)
        time.sleep(0.1)
        win32gui.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam) 
        win32gui.SendMessage(self.hwnd, win32con.WM_LBUTTONUP, 0, lParam)
        time.sleep(0.1)
        win32gui.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam) 
        win32gui.SendMessage(self.hwnd, win32con.WM_LBUTTONUP, 0, lParam)

        win32gui.SetForegroundWindow(self.hwnd)
        time.sleep(0.1)

        pyautogui.typewrite(real_size)
        
        #pyperclip.copy(real_size)

if __name__ == "__main__":
    
    pkr = PkrWindow()