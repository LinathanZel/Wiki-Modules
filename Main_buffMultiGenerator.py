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
    outputThing.insert(END,printTemplate(elementThing.get().lower(),int(rarityThing.current()+1),skillsArr[skillThing.current()]))
    
def openGithub():
    webbrowser.open('https://github.com/LinathanZel')

def updateFiles():
    outputThing.delete(1.0,END)
    outputThing.insert(END,"Updating files... Please wait.")
    buffGenerator.update()
    outputThing.delete(1.0,END)
    outputThing.insert(END,"Completed update. Please restart this application.")
    
filename = "unit.json.txt"
buildNum = "Build 1.0.3"
try:
    #print("Attempting to load file data from " + filename + "...")
    with open(filename) as data_file:
        data = json.load(data_file)
    #print("Success loading file data!")
except FileNotFoundError:
    print("Failure to load file data. Attempting online datamine...")
    try:
        with urlopen(datamine_url) as url:
            data = json.loads(url.read().decode())
        print("Success loading datamine!")
    except HTTPError:
        print("Failure to load datamine...")
        units = {}
skillsArr = ['bb','sbb','ubb']
listView = Tk()
listView.title("Multi Unit Buffs Generator")
Label(listView,text="Print entire list.").grid(row=0,column=1,pady=5)
Label(listView,text="Element:").grid(row=2,column=0,pady=5)
Label(listView,text="Rarity:").grid(row=2,column=1,pady=5)
Label(listView,text="Skill:").grid(row=2,column=2,pady=5)
unitName=StringVar()
outputThing=Text(listView,height=30,width=90,bd=2)
outputThing.grid(row=1,column=0,padx=5,columnspan=3)
elementThing=ttk.Combobox(listView,state="readonly",values=['Fire','Water','Earth','Thunder','Light','Dark'])
elementThing.grid(row=4,column=0)
elementThing.current(0)
rarityThing=ttk.Combobox(listView,state="readonly",values=['1★','2★','3★','4★','5★','6★','7★','Omni'])
rarityThing.grid(row=4,column=1)
rarityThing.current(0)
skillThing=ttk.Combobox(listView,state="readonly",values=['Brave Burst','Super Brave Burst','Ultimate Brave Burst'])
skillThing.grid(row=4,column=2)
skillThing.current(0)
Label(listView,text="Coded by Linathan\nGithub: https://github.com/LinathanZel").grid(row=6,column=1,pady=5)
Label(listView,text=buildNum).grid(row=5,column=2,pady=5)
Button(listView,text="Update",command=updateFiles,width=12).grid(row=5,column=0,pady=5)
Button(listView,text="BF Wiki",command=openWiki,width=12).grid(row=6,column=0,pady=5)
Button(listView,text="Generate",command=toOutput,width=12).grid(row=5,column=1,pady=5)
Button(listView,text="GitHub",command=openGithub,width=12).grid(row=6,column=2,pady=5)

def printTemplate(element,rarity,skill):
    copy = "{{#switch:{{{1|}}}\n"
    #print("{{#switch:{{{1|}}}")
    for r in data.keys():
            if data[r]['rarity'] == rarity and data[r]['element'] == element and skill in data[r].keys():
                    try:
                            copy = copy + "|" + str(r) + "=" + str(buffGenerator.printBuffs(r,skill) + "\n")
                            #print("|" + str(r) + "=" + str(buffGenerator.printBuffs(r,'bb')))
                    except:
                            pass
    copy = copy + "}}"
    return copy

if __name__ == "__main__":
    listView.mainloop()
