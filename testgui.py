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
    #myUI.pbar.start(interval=175)
    func()
    #myUI.pbar.stop()

    for file in os.listdir():
        if 'plot' in file:
            newwin = tk.Toplevel(myUI)
            newwin.configure(bg='white')
            #newwin.iconphoto(False, myUI.icon)

            #im = tk.PhotoImage(file=file)
            #plot = tk.Label(newwin, image=im, bg='white')
            plot = tk.Label(newwin, bg='white')

            #plot.image = im
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
        labUI = tk.Frame(self)
        #labUI.configure(bg='white')
        #labUI.title('Baxter Lab GUI V2.1.0')
        #labUI.pack(side="top", fill="x")
        #self.icon = tk.PhotoImage(file='Stowaway.png')
        #labUI.iconphoto(False, icon)

        #self.photo = tk.PhotoImage(file='BaxterLogo.png')
        #self.photo = photo.subsample(3, 3)
        #self.logo = tk.Label(labUI, image=photo, bg='white')
        #self.logo.image = photo
        #self.logo.grid(row=0, column=0, columnspan=4)

        #pbar = Progressbar(labUI, length=50, mode='determinate')
        #pbar.grid(row=1, column=0, columnspan=4, pady=5, sticky='ew') 
        self.ferm_brand = tk.StringVar()
        self.ferm_brand.set("ALL")   # default value
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
        resetb = tk.Button(self, text='Reset', command=reset,font=('calibri', 12), 
            bg='red', relief='groove', width=12).grid(sticky = 'w',column=0, row=2)

        # # Plotting Standard Fermentation Curve
        fmcurveLB1 = tk.Label(self, text='Fermentation Curve', font=('calibri', 12), 
            bg='lightblue', relief='groove').grid(sticky='w', column=0, row=3)
        fmcurveLB2 = tk.Label(self, text='Brand Code: ', font=('calibri', 12), 
            bg='gray', relief='groove', width=20,justify='left').grid(sticky='w',column=1, row=3)
        #fmentry = tk.Entry(self, textvariable=ferm_brand).grid(column=3, row=3)
        fmbutton = tk.Button(self, text='Plot', command=plotferm,bg='green').grid(column=4, row=3)
        #window.pack()

        #self.text = tk.Text(self, wrap="word").grid(column=0, row=10)
        #self.text.pack(side="top", fill="both", expand=True)
        #self.text.tag_configure("stderr", foreground="#b22222")

        #sys.stdout = TextRedirector(self.text, "stdout")
        #sys.stderr = TextRedirector(self.text, "stderr")

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
print('class', myUI.ferm_brand)
myUI.mainloop()