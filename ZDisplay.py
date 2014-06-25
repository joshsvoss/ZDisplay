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

import tkinter #if using python 2 change to Tkinter
from tkinter import *
import configparser
from tkinter import font
#from ttk import * #Themed Tk.  Is this working??
import sys #for command line arguments

#possible action to be performed when botton is clicked



class ZDisplay(object): #TODO maybe just make it inherit from Tk()??? would be it's own window?  Any downside?

    def __init__(self, configFilepath): #maybe parser shoud be a separate class so it can first parse, then construct ZDisplay?
        #open a window in tkinter
        print("in init method!")
        self.configFilepath = configFilepath
        self.window = Tk()
        self.numOfRows = None #possible namespace conflict here
        self.screenWidth, self.screenHeight = window.winfo_screenwidth(), window.winfo_screenheight()
        print("Width: {0}  Height: {1}".format(str(screenWidth), str(screenHeight)))
        self.window.title('Shiprush LiveDisplay')
        self.window.geometry("{0}x{1}".format(str(screenWidth-17), str(screenHeight-75)))  #Reset according to screen
        #width -17 is there because the windwo seems to be 17 pixels too wide.  Maybe because the transparent
        #windows border isn't indcluded?

        #Scale
        scale1 = Scale(window, from_=12, to=80, orient=HORIZONTAL)
        scale1.grid(row=10, column=0, sticky=(S, E))

        #create two seperate frames for two seperate rows:
        #top frame:
        leftFrame = tkinter.Frame(window, width=screenWidth, height = screenHeight/2, bd = 30, relief = RAISED)
        leftFrame.pack(side="top", padx=5, pady=50)

        #Create a frame on the bottom now
        rightFrame = tkinter.Frame(window, bg="black", width=screenWidth, height = screenHeight/2, bd = 20, relief = RAISED)
        rightFrame.pack(side="top", padx=5, pady=30)

        #display a label insdie the top frame
        topLabel = tkinter.Label(leftFrame, wraplength=(screenWidth//2), text="Shiprush left data!", fg="Moccasin", font=("Times New Roman", scale1.get()))
        topLabel.config(activebackground="black")
        topLabel.pack(side="top") #didn't work, still in middle left. acnhor nw maybe?

        #display label inside the bottom frame
        bottomLabel = tkinter.Label(rightFrame, anchor=W, wraplength=(screenWidth//2), text="Shiprush right data!", fg="Moccasin", font=("Times New Roman", scale1.get()))
        bottomLabel.config(activebackground="black") #Unclear that this does anything
        bottomLabel.pack(side="bottom") #didn't work

        #Button
        button1 = Button(window, text="Refresh", width = 30, command=buttonClicked)
        button1.pack(side="bottom")


        #topLabel.after(1000, updateFontFromScale())
        window.mainloop() #displays the window



    
        
    #update method
    def updateFontFromScale():
        topLabel.config(fg="red")
        topLabel.config(padx=scale1.get())

        #call this function continoutsly
        #labelRef.after(1000, updateFontFromScale)

    #button clicked command
    def buttonClicked():
        print("button clicked command runngin!")
        updateFontFromScale

   #define?
    def __str__(self):
        pass
    
    #this is returned when one simply types in 'variableName' in the REPL
    def __repr__(self):
        return "ZDisplay(%s)" % str(self)


    """ Any reason to make this guy my own class inherting from config parser?
    or is there no reason for that and I just make an instace of the imported module?  
    doesn't hurt to inherit I guess just gives me added flexibility.  
    """
   
    def parse():
        #parse the config file
        parser = configparser.ConfigParser() #Instantiate object
        parser.read(self.configFilepath)

        self.numOfRows = int(parser.get("GeneralSection", "NumOfRows"))
        print("Number of rows:", self.numOfRows)

        #Use nested for looop to recieve all of the config options, depending on numOfRows


        #Construct a ZDisplay object passing it the parameters
    
        #TODO possible delete
        #based on numOfRows, read in all of the filepaths in the config file
        #TODO Should each row be done seperately instead? serial instead of paralel?
        #scriptPathList = list()
        #for i in range(1, (numOfRows + 1)) :
        #    scriptPathList.append(parser.get("RowsSection", "Row%s.py" % i)) #Get specified script filepath

        #print(scriptPathList)


#Program begins running here:
#check command line argument for filepath to config:
argsList = sys.argv
if len(argsList) <2:
    print("ERROR: please provide config file filepath as cmd line argument.") #TODO is the .err stream?
    sys.exit(2)
#otherwise, use the arg to find the .ini file:
zdisplay = ZDisplay(argsList[1])
#ZDisplay.parse(argsList[1])




 