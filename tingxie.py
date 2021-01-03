# 用于听写的小程序
# 使用python GUI-- tkinter
# 尝试多线程
# 2020年12月31日

import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter.filedialog as fd
from tkinter.messagebox import showinfo
import threading
import os,time
from datetime import datetime
import sys
import pyttsx3

def pre_init():
    if not os.path.exists('E:\\小学学习\\闽教版4年级上册单词表.txt'):
        raise IOError('File not found.')
    print("init...")

class TX(threading.Thread):   #听写
    def __init__(self,filename, units):
        super(TX, self).__init__()
        self.__running_flag = threading.Event()
        self.__running_flag.set()
        self.__pause_flag = threading.Event()
        self.__pause_flag.set()  # 为true时不暂停，false时暂停
        self.__filename = filename
        self.__unit = units
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 50)
        self.engine.stop()

        # voices = self.engine.getProperty('voices')
        # self.engine.setProperty('voice', voices[1].id)
        
        self.delay = 5
        self.times = 3
        

    def get_word(self):
        with open(self.__filename,'r') as x:
            line = x.readlines()
            for iu in self.__unit:
#                wordlist = line[iu-1].strip().split(',')
                wordlist = line[iu].strip().split(',')
                for eachword in wordlist:
                    yield eachword
    
    def check_contain_chinese(self,check_str):
        for ch in check_str:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False

    def run(self):
        self.__running_flag.set()
        self.nextword = self.get_word()
        app.log("start..in....")
        while self.__running_flag.is_set():
            self.__pause_flag.wait()
            word = next(self.nextword)
            app.log(word)
            voices = self.engine.getProperty('voices')
            if self.check_contain_chinese(word) :
                self.engine.setProperty('voice', voices[0].id)
            else:
                self.engine.setProperty('voice', voices[1].id)

            for _ in range(0,self.times):
                #print(eachword)
                self.engine.say(word)
                self.engine.runAndWait()
                time.sleep(len(word)*0.1)
            time.sleep(self.delay)
        

    def stop(self):
        self.__pause_flag.set()

    def troggle(self):
        # app.log("from:")
        app.log(self.__pause_flag.is_set())
        if self.__pause_flag.is_set():
            self.__pause_flag.clear()
        else:
            self.__pause_flag.set()

    def returnStatus(self):
        tempStr = "正在运行" if self.__running_flag.is_set() else "不在运行"
        tempStr += " | "
        tempStr += "没有暂停" if self.__pause_flag.is_set() else "暂停"

        tempStr += "|" + "每词间隔：%d 秒| 每词重复%d 次" % (self.delay ,self.times)
        return tempStr

    def close(self):
         self.__running_flag.clear()


   

class App():
    def __init__(self,parent=None,*args,**kwargs):
        # init GUI
        # Grid.columnconfigure(parent, 1, weight=1)
        # Grid.rowconfigure(parent, 0, weight=1)   

        self.manually_tab = parent
        self.filename = 'E:\\小学学习\\wordlist.txt'

        self.entry_f = StringVar(parent,self.filename)
        self.Entryf = ttk.Entry(parent,textvariable=self.entry_f)
        self.Entryf.grid(row=0, column=0, columnspan=3, sticky="WE",padx=10)


        self.open_button = ttk.Button(
            parent,
            text='Open a File',
            command=self.select_file
        )
        self.open_button.grid(row=0, column=3,sticky="W")

        # log window
        self.log_content = Listbox(parent, selectmode=EXTENDED, bg='#FFFFFF')
        self.log_content.grid(row=1, column=0,columnspan=4, padx=5, pady=5, sticky='NSWE')

        self.btn_start = ttk.Button(self.manually_tab, text=u"开始学习", command=self.start_click)
        self.btn_start.grid(row=2, column=0, padx=5, pady=5)

        self.btn_pause = ttk.Button(self.manually_tab, text=u"暂停学习", command=self.pause_click)
        self.btn_pause.grid(row=2, column=1, padx=5, pady=5)

        self.btn_quit = ttk.Button(self.manually_tab, text=u"退出学习", command=self.quit_click)
        self.btn_quit.grid(row=2, column=2, padx=5, pady=5)       


        self.vbar = ttk.Scrollbar(
            parent, orient=VERTICAL, command=self.log_content.yview)
        self.log_content.configure(yscrollcommand=self.vbar.set)
        self.vbar.grid(row=1, column=4, sticky='NS')

        self.status = tk.StringVar()
        self.statuslabel = ttk.Label(parent,textvariable=self.status) #,font=('Arial', 13))
        self.statuslabel.grid(row=7, column=0, columnspan=20, padx=5, pady=5)
        self.status.set("状态栏：")

        self.lb = Listbox(parent, selectmode='multiple')
        self.lb.grid(row=0,column=4, rowspan = 3)



    def log(self, logstring, printtime=True):
        if printtime:
            self.log_content.insert(END, u'%s %s' % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), logstring))
        else:
            self.log_content.insert(END, u'    %s' % (logstring))

        self.log_content.see(END)    

    def select_file(self):
        filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
        )

        self.filename = fd.askopenfilename(
            title='Open a file',
            initialdir='E:\\小学学习\\',
            filetypes=filetypes)

        showinfo(
            title='Selected File',
            message=self.filename
        )
        self.entry_f.set(self.filename)
        if not os.path.exists(self.filename):
            raise IOError('File not found.')
        else:
            self.log(self.filename + " 加载完成.")

        with open(self.filename,'r') as x:
            line = x.readlines()
        print(line)
        self.lb.delete(0,END)
        for i in range(len(line)):
            self.lb.insert('end','unit '+str(i+1))


    def start_click(self):
        if self.lb.curselection :
            self.txjob = TX(self.filename,self.lb.curselection())
            self.txjob.setDaemon(True)  # the thread die when the main thread dies.
            self.log("start")
            self.txjob.start()
            self.status.set(self.txjob.returnStatus())
            self.btn_start['state']=tk.DISABLED
        else:
            showinfo(title='Warning',message="请选择要")
              

    def pause_click(self):
        # self.log("pause")
        self.txjob.troggle()
        print(self.txjob.returnStatus())
        self.status.set(self.txjob.returnStatus())

    def quit_click(self):
        self.log("exit")
        self.txjob.close()
        self.btn_start['state']=tk.NORMAL
        

if __name__ == '__main__':
    print("fdfaf")
    pre_init()
    root = Tk()
    global app
    app = App(parent=root)
    root.geometry('531x320')
    root.title(u'tx v1')
    root.mainloop()