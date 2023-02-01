from time import sleep
# To emulate user typing
import pyautogui as pa
import pyperclip as cb
import os
import shutil
import bot
import rpa

from json import loads

def readConf(path):
    with open(path) as confFile:
        config = loads(confFile.read())

    return config

def globalVars():
    global proj_dir
    global n_subflows
    global current_subflow
    global config
    global imgs

    imgs = {
        'rename-subflow': r'.\img\rename-subflow-txt.jpg',
        'add-icon': r'.\img\add_icon.JPG',
        'subflow-name': r'.\img\subflow-name-txt.jpg',
        'subflows-icon': r'.\img\subflow_icon.JPG',
        'when-sf-open': r'.\img\when-subflow-open.jpg'
    }
    
    confPath = r".\config.json"
    config = readConf(confPath)


def main():

    globalVars()

    proj_dir = r"C:\Users\lucas.silva\Documents\git\pipp"
    n_subflows = 58

    bot.PROJECT_DIR = r'test'

    bot.openSubflow(imgs)
    bot.getSubflowName(imgs)
    bot.saveSubflowTxt()


    # Alert that operation has ended
    pa.alert('Finished with success.')

if __name__ == '__main__':
    main()
