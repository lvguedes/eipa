import easygui as eg
import exportPA
import importPA
import pyautogui
import cv2
import os
from tkinter import *
from tkinter.ttk import *

def main():
    reply = eg.buttonbox(
        "Select a feature:",
        choices=["Export","Import"]
    )
    print(reply)
    os.system('cls' if os.name == 'nt' else 'clear')
    
    if reply == "Export":
        exportPA.main()
    elif reply == "Import":
        importPA.main()
    else:
        pyautogui.alert("Something went wrong!")

if __name__ == '__main__':
    root = Tk()
    img = PhotoImage(file = "./ico/little.png")
    root.iconphoto(True, img)
    root.destroy()

    main()
