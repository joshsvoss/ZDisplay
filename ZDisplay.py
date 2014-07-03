#ZDisplay.py
#TODO methodize the row creation
#TODO try recieving a dictionary as input, possibly with multiple key, value pairs, use the 
#length to decide how many elements to generate
#TODO decide what fullscreen line to use via os version grab

""" This module contains the program for displaying Z-Firm stats
on screen.  Author: Joshua S. Voss,  Version: 1.0

Classes: Responsibilites
Parser: parses the .ini file and brings those specifications into the program as variables.
Passes them off to ZDisplay to build the view with.

ZDisplay: based on the arguments from teh parser (That may be too many arguments to pass,
perhaps join the classes?  Or another way of sharing scope?)  Call either Tkinter externally 
or inherited Tkinter member methods to form the display.  ZDisplay class should also own some
of its own methods to update the feed and perhaps actively change the display once built and running even.

See and run colors.py for all tkinter color options

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

    def __init__(self, parser): 
        #initialize data fields:
        self.parser = parser
        self.window = Tk() #open a window in tkinter
        self.numOfRows = int(parser.get("GeneralSection", "numofrows")) #possible namespace conflict here
        if self.numOfRows < 1:
            raise IOError("Must sepcify at least 1 row in config file.")

        #setup window
        self.screenWidth, self.screenHeight = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        print("Width: {0}  Height: {1}".format(str(self.screenWidth), str(self.screenHeight)))
        self.window.title('ZDisplay: Shiprush')
        self.window.wm_state("zoomed") #Maximize but with title bar
        #self.window.attributes("-zoomed", True) #This command needs to run on the pi, different attribute lost.  Comment the command above
        #self.window.attributes("-fulscreen", True) #Uncomment to maximize without title bar
        self.window.geometry("{0}x{1}".format(str(self.screenWidth-17), str(self.screenHeight-75)))  #I left this in in case the maximize doesn't work
        #width -17 is there because the windwo seems to be 17 pixels too wide.  Maybe because the transparent
        #windows border isn't indcluded?


    
        
    def buildWindow(self):
        """This method builds the visual elements of the display
        """   

        #Create frame1:
        frame1 = tkinter.Frame(self.window, bd = 10, relief = RAISED, background = self.parser.get('Row1Section', 'backgroundcolor')) #TODO deal with edge case: what if config is not filled in?
        frame1.pack(side="top", fill="both", expand="true")
        #create label1 inside of frame1
        label1 = tkinter.Label(frame1, bg = self.parser.get('Row1Section', 'backgroundcolor'),text="origial text!", font=("Times New Roman", 
                self.parser.get('Row1Section', 'fontsize')), fg = self.parser.get('Row1Section', 'textcolor')) #here's where you could set the font as a variable
        #I wonder if they're a way for label1 to just copy frame1's background attribute
        label1.pack(side="top", fill = "both", expand = "True") 

        #Import script:
        #Decide dynamically what to import from config file:
        scriptPath = self.parser.get("Row1Section", "path") #get the directory of script
        print("path to be inserted into sys.path: ", scriptPath)
        sys.path.insert(0, scriptPath) #add script directory to path
        print("sys.path: ", sys.path)
        moduleName = self.parser.get("Row1Section", "module")
        script1 = __import__(moduleName) #get module name, then import it

        #if we have another row, repeat exact same code block for row2...rowN.
        if self.numOfRows >= 2:
            #Create frame2:
            frame2 = tkinter.Frame(self.window, bd = 10, relief = RAISED, background = self.parser.get('Row2Section', 'backgroundcolor'))
            frame2.pack(side="top", fill="both", expand="true")
            #create label1 inside of frame1
            label2 = tkinter.Label(frame2, bg = self.parser.get('Row2Section', 'backgroundcolor'),text="origial text!", 
                                   font=("Times New Roman", self.parser.get('Row2Section', 'fontsize')), fg = self.parser.get('Row2Section', 'textcolor')) #here's where you could set the font as a variable
            #I wonder if they're a way for label1 to just copy frame1's background attribute
            label2.pack(side="top", fill = "both", expand = "True") 

            #Import script:
            #Decide dynamically what to import from config file:
            scriptPath = self.parser.get("Row2Section", "path") #get the directory of script
            print("path to be inserted into sys.path: ", scriptPath)
            sys.path.insert(0, scriptPath) #add script directory to path
            print("sys.path: ", sys.path)
            moduleName = self.parser.get("Row2Section", "module")
            script2 = __import__(moduleName) #get module name, then import it

        #if we have another row, repeat exact same code block for row3...rowN.
        if self.numOfRows >= 3:
            #Create frame3:
            frame3 = tkinter.Frame(self.window, bd = 10, relief = RAISED, background = self.parser.get('Row3Section', 'backgroundcolor'))
            frame3.pack(side="top", fill="both", expand="true")
            #create label1 inside of frame1
            label3 = tkinter.Label(frame3, bg = self.parser.get('Row3Section', 'backgroundcolor'), text="origial text!", 
                                   font=("Times New Roman", self.parser.get('Row3Section', 'fontsize')), fg = self.parser.get('Row3Section', 'textcolor'))
            #here's where you could set the font as a variable
            #I wonder if they're a way for label1 to just copy frame1's background attribute
            label3.pack(side="top", fill = "both", expand = "True") 

            #Import script:
            #Decide dynamically what to import from config file:
            scriptPath = self.parser.get("Row3Section", "path") #get the directory of script
            print("path to be inserted into sys.path: ", scriptPath)
            sys.path.insert(0, scriptPath) #add script directory to path
            print("sys.path: ", sys.path)
            moduleName = self.parser.get("Row3Section", "module")
            script3 = __import__(moduleName) #get module name, then import it

        #if we have another row, repeat exact same code block for row4...rowN.
        if self.numOfRows >= 4:
            #Create frame4:
            frame4 = tkinter.Frame(self.window, bd = 10, relief = RAISED, background = self.parser.get('Row4Section', 'backgroundcolor'))
            frame4.pack(side="top", fill="both", expand="true")
            #create label1 inside of frame1
            label4 = tkinter.Label(frame4, bg = self.parser.get('Row4Section', 'backgroundcolor'),text="origial text!", 
                                   font=("Times New Roman", self.parser.get('Row1Section', 'fontsize')), fg = self.parser.get('Row4Section', 'textcolor')) #here's where you could set the font as a variable
            #I wonder if they're a way for label1 to just copy frame1's background attribute
            label4.pack(side="top", fill = "both", expand = "True") 

            #Import script:
            #Decide dynamically what to import from config file:
            scriptPath = self.parser.get("Row4Section", "path") #get the directory of script
            print("path to be inserted into sys.path: ", scriptPath)
            sys.path.insert(0, scriptPath) #add script directory to path
            print("sys.path: ", sys.path)
            moduleName = self.parser.get("Row4Section", "module")
            script4 = __import__(moduleName) #get module name, then import it



        
            
            
        def update():
            label1.config(text = script1.returnTime()) #TODO: need to standardize the function name of figure out a way of grabbibg it from module
            if self.numOfRows >=2:
                label2.config(text = script2.callsInQueueToday(1104))
            if self.numOfRows >=3:
                label3.config(text = script3.callsInLastHour(1104))
            if self.numOfRows >=4:
                label4.config(text = script4.returnInt())
            #The method calls itself in another 1 second... then again...
            self.window.after(1000, update)

        #Start the script calling function:
        update()
        #displays the window
        self.window.mainloop() 


        """I'd like to keep this, have and update constatnly checking it's value and reseting the fontsize, but 
        I can't hardcode the number of rows and hence labelN it would be configing, 
        Is it possible to softocde it?  label%s?
        """
        ##Scale
        #scale1 = Scale(self.window, from_=12, to=80, orient=HORIZONTAL)
        #scale1.grid(row=1)

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
display.buildWindow()


