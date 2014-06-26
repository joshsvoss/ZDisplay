#ZDisplay.py
""" This module contains the program for displaying Z-Firm stats
on screen.  Author: Joshua S. Voss,  Version: 1.0

Classes: Responsibilites
Parser: parses the .ini file and brings those specifications into the program as variables.
Passes them off to ZDisplay to build the view with.

ZDisplay: based on the arguments from teh parser (That may be too many arguments to pass,
perhaps join the classes?  Or another way of sharing scope?)  Call either Tkinter externally 
or inherited Tkinter member methods to form the display.  ZDisplay class should also own some
of its own methods to update the feed and perhaps actively change the display once built and running even.

"""
import tkinter
from tkinter import * #if using python 2 change to Tkinter
import configparser
from tkinter import font
#from ttk import * #Themed Tk.  Is this working??
import sys #for command line arguments
import threading
import time
from datetime import datetime
from threading import Timer




    #button clicked command
def buttonClicked(var):
    var.set(localScript()) #Why is this executing before it's pressed?
    pass


def localScript():
    return str(datetime.now().time())


class ZDisplay(object): #TODO maybe just make it inherit from Tk()??? would be it's own window?  Any downside?

    def __init__(self, parser): #maybe parser shoud be a separate class so it can first parse, then construct ZDisplay?
        
        print("in init method!")
        
        self.parser = parser
        self.window = Tk() #open a window in tkinter
        self.numOfRows = int(parser.get("GeneralSection", "numofrows")) #possible namespace conflict here
        if self.numOfRows < 1:
            raise IOError("Must sepcify at least 1 row in config file.")

        #setup window
        print("numOfRows: ", self.numOfRows)
        self.screenWidth, self.screenHeight = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        print("Width: {0}  Height: {1}".format(str(self.screenWidth), str(self.screenHeight)))
        self.window.title('Shiprush LiveDisplay')
        self.window.wm_state("zoomed") #Maximize but with title bar
        #self.window.attributes("-fulscreen", True) #Uncomment to maximize without title bar
        self.window.geometry("{0}x{1}".format(str(self.screenWidth-17), str(self.screenHeight-75)))  #I left this in in case the maximize doesn't work
        #width -17 is there because the windwo seems to be 17 pixels too wide.  Maybe because the transparent
        #windows border isn't indcluded?

    def specGet(self, section, option):
        return self.parser.get(section, option)

    def build(self):
        #Row and colum configure:
        self.window.rowconfigure(1, weight = 1)
        self.window.rowconfigure(2, weight = 1)
        self.window.rowconfigure(3, weight = 1)
        self.window.columnconfigure(1, weight = 1)
        self.window.columnconfigure(2, weight = 1)



        #Scale
        scale1 = Scale(self.window, from_=12, to=80, orient=HORIZONTAL)
        scale1.grid(row=1)

        #create two seperate frames for two seperate rows:
        #top frame:
        textVar1 = StringVar()
        textVar1.set("Before the button's pressed!!") #Why is this coming out as the function id not the return value?
        topFrame = tkinter.Frame(self.window, width=self.screenWidth +1000, height = self.screenHeight/2, bd = 5, relief = RAISED, padx = 20, pady = 12)
        topFrame.grid(row=1)

        #Create a frame on the bottom now
        bottomFrame = tkinter.Frame(self.window, bg="black", width = self.screenWidth, height = self.screenHeight/2, bd = 20, relief = RAISED)
        bottomFrame.grid(row=2)

        #display a label insdie the top frame
        topLabel = tkinter.Label(topFrame, wraplength=(self.screenWidth//2), bg = self.specGet("Row1Section", "backgroundcolor"), 
                                 textvariable=textVar1, fg="red", font=("Times New Roman", scale1.get()))
        topLabel.grid(row=1) #didn't work, still in middle left. acnhor nw maybe?

        #display label inside the bottom frame
        bottomLabel = tkinter.Label(bottomFrame, anchor=W, wraplength=(self.screenWidth//2), text="Shiprush bottom data!", fg="blue", font=("Times New Roman", scale1.get()))
        bottomLabel.config(activebackground="black") #Unclear that this does anything
        bottomLabel.grid(row=2) #didn't work

        #Button
        button1 = Button(self.window, text="Refresh", width = 30, command = lambda: buttonClicked(textVar1)) #add command
        button1.grid(row=1, column=2)

        #Import script:
        #Decide dynamically what to import from config file:
        scriptPath = self.parser.get("Row1Section", "path") #get the directory of script
        print("path to be inserted into sys.path: ", scriptPath)
        sys.path.insert(0, scriptPath) #add script directory to path
        print("sys.path: ", sys.path)
        moduleName = self.parser.get("Row1Section", "module")
        script = __import__(moduleName) #get module name, then import it


        def update():
            textVar1.set(script.returnTime())
            self.window.after(1000, update)
        
        #Just to experiment with slider
        def updatePad():
            bottomLabel.config(pady = scale1.get()) #set padding according to scale
            self.window.after(10, updatePad)

        update()
        updatePad()
        #displays the window
        self.window.mainloop() 


    #define?
    def __str__(self):
        pass
    
    #this is returned when one simply types in 'variableName' in the REPL
    def __repr__(self):
        return "ZDisplay(%s)" % str(self)


  
    

#Program begins running here:
#check command line argument for filepath to config:
argsList = sys.argv
if len(argsList) <2:
    print("ERROR: please provide config file filepath as cmd line argument.") #TODO is the .err stream?
    sys.exit(2)
#otherwise, use the arg to find the .ini file:

#parse the config file
parser = configparser.ConfigParser() #Instantiate object
parser.read(argsList[1])

#Now going to pass ConfigParser object to ZDisplay, and display it using build()
display = ZDisplay(parser)
display.build()


