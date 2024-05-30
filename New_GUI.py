# Written by Caitlin Keady, 2024

import tkinter as tk
import os
from tkinter.ttk import Progressbar
from threading import Thread
from Fermentation_Curves import fermcurve
from ABV_control_chart import abvchart
from Batch_History import batchreport
from DO_control_chart import DOchart
from OG_optimization import optog

rootdir = os.getcwd()


# These functions are pulling in the user entered variable for each button
def reset():
    os.chdir(rootdir)
    pb.stop()


def ferm():
    fermcurve(ferm_brand.get())


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
    pb.start(interval=175)
    func()
    pb.stop()

    for file in os.listdir():
        if 'plot' in file:
            newwin = tk.Toplevel(window)
            newwin.configure(bg='white')
            newwin.iconphoto(False, icon)

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

# Setting up the layour and colors
window = tk.Tk()
output_frame = tk.Frame(window)
#  redirecting output from script to Tkinter Text window
# PAULMsys.stdout = Std_redirector(my_gui.txt2)
window.configure(bg='white')
window.title('Baxter Lab GUI V2.1.0')
icon = tk.PhotoImage(file='Stowaway.png')
window.iconphoto(False, icon)

photo = tk.PhotoImage(file='BaxterLogo.png')
photo = photo.subsample(3,3)
logo = tk.Label(window, image=photo, bg='white')
logo.image = photo
logo.grid(row=0, column=0, columnspan=4)

pb = Progressbar(window, length=50, mode='determinate')
pb.grid(row=1, column=0, columnspan=4, pady=5, sticky='ew')

ferm_brand = tk.StringVar()
ferm_brand.set("ALL")   # default value
abv_brand = tk.StringVar()
abv_brand.set("IPA")    # default value
report_batch = tk.StringVar()
do_brand = tk.StringVar()
do_brand.set("ALL")    # default value
batch = tk.StringVar()
og_brand = tk.StringVar()
og_brand.set("IPA")    # default value
plot_points = tk.StringVar()
plot_points.set('100')

# Reset button
tk.Button(window, text='Reset', command=reset, font=('calibri', 12), 
          bg='#ec4c2f', relief='groove', width=12,).grid(row=2, column=0, columnspan=4)


# Plotting Standard Fermentation Curve
tk.Label(window, text='Fermentation Curve', font=('calibri bold', 12), 
    bg='white').grid(row=3, column=0, columnspan=2, pady=(25, 5))
#e = tk.Entry(window, text='Brand Code: ', font=('calibri', 12), bg='white', 
         #relief='flat').grid(row=4, column=0, pady=2)
tk.Label(window, text='Brand Code: ', font=('calibri', 12), 
         bg='white', relief='flat').grid(row=4, column=0)

tk.Entry(window, textvariable=ferm_brand).grid(row=4, column=1)

#ferm_brand = e.get()
tk.Button(window, text='Plot', command=plotferm, font=('calibri', 12), 
           bg='#ec4c2f', relief='groove', width=12,).grid(row=5, column=1, sticky='ew')


# Plotting ABV Control Chart

tk.Label(window, text='ABV Control Chart', font=('calibri bold', 12), 
         bg='white').grid(row=6, column=0, columnspan=2, pady=(25, 5))
tk.Label(window, text='Brand Code: ', font=('calibri', 12), bg='white', 
         relief='flat').grid(row=7, column=0)

tk.Entry(window, textvariable=abv_brand).grid(row=7, column=1)

tk.Button(window, text='Plot', command=plotabv, font=('calibri', 12), 
          bg='#ec4c2f', relief='groove').grid(row=8, column=1, pady=2, sticky='ew')


# Plotting DO Control Chart

tk.Label(window, text='DO Control Chart', font=('calibri bold', 12), 
         bg='white').grid(row=9, column=0, columnspan=2, pady=(25, 5))

tk.Label(window, text='Brand Code: ', font=('calibri', 12), bg='white', 
         relief='flat').grid(row=10, column=0)

tk.Label(window, text='Plot Points: ', font=('calibri', 12), bg='white', 
         relief='flat').grid(row=11, column=0)

tk.Entry(window, textvariable=do_brand).grid(row=10, column=1)

tk.Entry(window, textvariable=plot_points).grid(row=11, column=1)

tk.Button(window, text='Plot', command=plotdo, font=('calibri', 12), 
          bg='#ec4c2f', relief='groove').grid(row=12, column=1, pady=2, sticky='ew')


# Create Batch Report
tk.Label(window, text='Batch Report', font=('calibri bold', 12), 
         bg='white').grid(row=3, column=2, columnspan=2, pady=(25, 5))
tk.Label(window, text='Batch: ', font=('calibri', 12), 
         bg='white', relief='flat').grid(row=4, column=2)

tk.Entry(window, textvariable=report_batch).grid(row=4, column=3)

tk.Button(window, text='Make Report', command=makereport, font=('calibri', 12), 
          bg='#ec4c2f', relief='groove').grid(row=5, column=3, pady=2, sticky='ew')


# Plotting OG optimization
tk.Label(window, text='Optimize OG Target', font=('calibri bold', 12), 
         bg='white').grid(row=6, column=2, columnspan=2, pady=(25, 5))
tk.Label(window, text='Brand Code:', font=('calibri', 12), bg='white', 
         relief='flat').grid(row=7, column=2)

tk.Entry(window, textvariable=og_brand).grid(row=7, column=3)


tk.Button(window, text='Plot', command=plotog, font=('calibri', 12), 
          bg='#ec4c2f', relief='groove').grid(row=8, column=3, pady=2, sticky='ew')

tk.Label(output_frame, text='Output', font=('calibri', 12), bg='lightblue', 
         relief='flat').grid(row=15, column=2)

window.mainloop()
