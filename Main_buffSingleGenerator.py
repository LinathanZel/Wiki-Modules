import json
import os
from urllib.request import urlopen
from urllib.error import HTTPError
from pprint import pprint
from tkinter import *
from tkinter import ttk
import buffGenerator
import webbrowser

def openWiki():
    webbrowser.open('https://bravefrontierglobal.fandom.com/wiki/Brave_Frontier_Wiki')

def toOutput():
    outputThing.delete(1.0,END)
    outputThing.insert(END,printTemplate(inputThing.get("1.0",'end-1c')))
    
def openGithub():
    webbrowser.open('https://github.com/LinathanZel')

def updateFiles():
    dbbGenerator.update()

buildNum = "Build 1.0.0"
skillsArr = ['bb','sbb','ubb']
listView = Tk()
listView.title("Unit Buff Generator")
Label(listView,text="Print entire list.").grid(row=0,column=1,pady=5)
unitName=StringVar()
outputThing=Text(listView,height=30,width=90,bd=2)
outputThing.grid(row=1,column=0,padx=5,columnspan=3)
Label(listView,text="Burst Name").grid(row=3,column=1,pady=5)
inputThing=Text(listView,height=1,width=25,bd=2)
inputThing.grid(row=4,column=0,pady=5,columnspan=3)
Label(listView,text="Coded by Linathan\nGithub: https://github.com/LinathanZel").grid(row=6,column=1,pady=5)
Label(listView,text=buildNum).grid(row=5,column=2,pady=5)
skillThing=ttk.Combobox(listView,state="readonly",values=['Brave Burst','Super Brave Burst','Ultimate Brave Burst'])
skillThing.grid(row=4,column=2)
skillThing.current(0)
Button(listView,text="Update",command=updateFiles,width=12).grid(row=5,column=0,pady=5)
Button(listView,text="BF Wiki",command=openWiki,width=12).grid(row=6,column=0,pady=5)
Button(listView,text="Generate",command=toOutput,width=12).grid(row=5,column=1,pady=5)
Button(listView,text="GitHub",command=openGithub,width=12).grid(row=6,column=2,pady=5)


def printTemplate(name):
    #print(findName(str(name)))
    #print("{{#switch:{{{1|}}}")
    try:
            copy = buffGenerator.printBuffs(buffGenerator.findName(str(name)),skillsArr[skillThing.current()])
    except:
            copy = "Error in fetching for " + str(name)
    return copy

if __name__ == "__main__":
    listView.mainloop()
