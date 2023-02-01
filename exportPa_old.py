from time import sleep
# To emulate user typing
import pyautogui
import pyperclip as pc
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
        'subflows-icon': r'.\img\subflow_icon.JPG'
    }
    
    confPath = r".\config.json"
    config = readConf(confPath)


def main():

    globalVars()

    
    proj_dir = r"C:\Users\lucas.silva\Documents\git\pipp"
    n_subflows = 58

    # Repeat for the number of subflows plus the Main
    for count in range(int(n_subflows) + 1):
        clickSubflowsDropDown()
        sleep(1)
        openSubflow(count=count)
        
        # get the subflow's name
        current_subflow = getSubflowName(count)
        
        print('The current subflow\'s name is:', current_subflow)
    
        sleep(0.5)
    
        focusSelectCopySubflow()
    
        content = genContentStr()
    
        # Now we can access through clipboard and save directly in a file
        # wihtout RPA manipulations
    
        # create a new file and paste the contents of clipboard to it
    
        with open(proj_dir + '\\' + current_subflow, 'wb') as fw:
            fw.write(content)
        with open(
                proj_dir + '\\' + current_subflow,
                mode='r',
                encoding='utf-8'
        ) as fr:
            content = fr.read()
            #print("\n\nCONTENT READ:\n%s" %(content))
            while (content + '.txt') == current_subflow:
                print("ERROR while getting the subflow's contents.")
                print("Trying again...\n")
                openSubflow(++config['wait_subflow_open'])
                focusSelectCopySubflow(++config['base_wait'])
                content = genContentStr()
                with open(proj_dir + '\\' + current_subflow, 'wb') as fw:
                    fw.write(content)
                
        print('\n-----------')
        print('saving to the %s\\%s\n\n\n\n' %(proj_dir, current_subflow) )
    
    # Alert that operation has ended
    pyautogui.alert('Finished with success.')

def main_test():
    globalVars()
    bot.openSubflow(imgs)
    
if __name__ == '__main__':
    main_test()
