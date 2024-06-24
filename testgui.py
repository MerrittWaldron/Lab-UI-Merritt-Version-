import tkinter as tk
import sys

import os
from tkinter.ttk import Progressbar
from threading import Thread
from Fermentation_Curves import fermcurve
from ABV_control_chart import abvchart
from Batch_History import batchreport
from DO_control_chart import DOchart
from OG_optimization import optog

rootdir = os.getcwd()

class Std_redirector(object):
    def __init__(self, widget):
        self.widget = widget

    def write(self, string):
        self.widget.insert(END, string)
        self.widget.see(END)

    def flush(self):
        pass

# These functions are pulling in the user entered variable for each button
def reset():
    os.chdir(rootdir)
    sys.stdout = sys.__stdout__

    myUI.pbar.stop()


def ferm():
    fermcurve(myUI.ferm_brand.get())


def abv():
    abvchart(abv_brand.get())


def report():
    batchreport(report_batch.get())
    

def do():
    DOchart(do_brand.get(), plot_points.get())

    
def opt():
    optog(og_brand.get())


# Generates plots where applicable
def runfunc(func):
    myUI.pbar.start(interval=175)
    func()
    myUI.pbar.stop()

    for file in os.listdir():
        if 'plot' in file:
            newwin = tk.Toplevel(myUI)
            newwin.configure(bg='white')
            newwin.iconphoto(False, myUI.icon)

            im = tk.PhotoImage(file=file)
            plot = tk.Label(newwin, image=im, bg='white')
            plot.image = im
            plot.grid(row=0, column=0)

            os.remove(file)


def runthread(func):
    Thread(target=runfunc, args=(func,)).start()

# These functions are running the functions behind each button
def plotferm():
    runthread(ferm)


def plotabv():
    runthread(abv)


def makereport():
    runthread(report)
    
    
def plotdo():
    runthread(do)
    
    
def plotog():
    runthread(opt)


class LabUIApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.configure(bg='white')
        self.title('Baxter Lab GUI V2.1.0')
        #self.canvas = tk.Canvas(self, height=900, width=800, bg='#ffa700')
        self.icon = tk.PhotoImage(file='Stowaway.png')
        self.iconphoto(False, self.icon)
        self.photo = tk.PhotoImage(file='BaxterLogo.png')
        self.photo = self.photo.subsample(3, 3)
        self.logo = tk.Label(self, image=self.photo, bg='white')
        self.logo.image = self.photo
        self.logo.grid(row=0, column=0, columnspan=4)

        self.pbar = Progressbar(self, length=50, mode='determinate')
        self.pbar.grid(row=1, column=0, columnspan=4, pady=5, sticky='ew') 
        self.ferm_brand = tk.StringVar()
        self.ferm_brand.set("IPA")   # default value
        self.abv_brand = tk.StringVar()
        self.abv_brand.set("IPA")    # default value
        self.report_batch = tk.StringVar()
        self.do_brand = tk.StringVar()
        self.do_brand.set("ALL")    # default value
        self.batch = tk.StringVar()
        self.og_brand = tk.StringVar()
        self.og_brand.set("IPA")    # default value
        self.plot_points = tk.StringVar()
        self.plot_points.set('100')  
        #b1 = tk.Button(self, text="print to stdout", command=self.print_stdout).grid(column=0, row=0)
        #b2 = tk.Button(self, text="print to stderr", command=self.print_stderr).grid(column=0, row=1)
        tk.Button(self, text='Reset', command=reset,font=('calibri', 12), 
            bg='red', relief='groove', width=12).grid(sticky = 'w',column=0, row=2)

        # # Plotting Standard Fermentation Curve
        tk.Label(self, text='Fermentation Curve', font=('calibri', 12), 
            bg='lightblue', relief='groove').grid(sticky='w', column=0, row=3)
        tk.Label(self, text='Brand Code: ', font=('calibri', 12), 
            bg='gray', relief='groove', width=20,justify='left').grid(sticky='w',column=1, row=3)
        tk.Entry(self, textvariable=self.ferm_brand).grid(column=3, row=3)
        tk.Button(self, text='Plot', command=plotferm,bg='green').grid(column=4, row=3)
        
#  create new frame that will contain output text frame with scrollbar
        #self.frame2 = tk.Frame(self, highlightbackground="black", highlightcolor="black", highlightthickness=4, bg='#2c2f33')
        tk.Label(self, text='Output ', font=('calibri', 12),
            bg='white', relief='groove', height=20,width=40,justify='left').grid(sticky='w',column=0, row=11,columnspan=4)
        # #  create a Scrollbar and associate it with txt
        self.scrollb2 = tk.Scrollbar(self)(column=2,row=10)
        #self.scrollb2.pack(side='right', fill='y')

        # #  create a Text widget
        #self.txt2 = tk.Text(self, font=("Calibri", 12), borderwidth=3, wrap='word', undo=True,
        #                 yscrollcommand=self.scrollb2.set).grid(sticky='w',column=0, row=11)
        # self.scrollb2.config(command=self.txt2.yview)

    def print_stdout(self):
        '''Illustrate that using 'print' writes to stdout'''
        print("this is stdout")

    def print_stderr(self):
        '''Illustrate that we can write directly to stderr'''
        sys.stderr.write("this is stderr\n")


class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, string):
        self.widget.configure(state="normal")
        self.widget.insert("end", string, (self.tag,))
        self.widget.configure(state="disabled")

myUI = LabUIApp()
#  redirecting output from script to Tkinter Text window
#sys.stdout = Std_redirector(myUI.txt2)
myUI.mainloop()