# -*- coding: utf-8 -*-

from time import sleep
# To emulate user typing
import pyautogui
import pyperclip as pc
import os
import shutil
# to use the input dir message window
import easygui

# configuration variables
ctrl = 'ctrl'
mouse_main_button = 'left'
# you might increase it if your project is big
waitSubflowOpen = 3
baseWait = 1

#proj_dir = 'c:/Users/lsilva46' + \
#           '/OneDrive - Capgemini/Documents/git/protheus-invoice-posting'

# script variables
button_subflows = './img/subflow_icon.JPG'
current_subflow = ''


def checkProjDir():
    if os.path.isdir(proj_dir):
        # if yes delete it and all its contents after warning the user
        print(proj_dir, 'exists')
        # prompt the user if he wants to delete it
        deleteDir = pyautogui.prompt(
            text="Do you want to delete "+proj_dir+"? [yes/no]")
        if deleteDir == 'yes':
            # if yes, delete everything
            shutil.rmtree(proj_dir)
        else:
            # if not, exit
            exit()
    else:
        # if no, create a new empty dir
        print(proj_dir, 'doesn\'t exists. Creating a new one...')

    # create a new proj_dir for all cases that doesn't exit
    os.mkdir(proj_dir)

def getSubflowName(count):
    if count != 0:
        # press F2 to get the subflow's name
        pyautogui.press('f2')

        # wait for the rename dialog to appear
        sleep(1)

        # copy the sublflow's name to clipboard
        with pyautogui.hold(ctrl):
            pyautogui.press('c')

        current_subflow = pc.paste() + '.txt'

        # Esc to quit the rename dialog and return to source code
        pyautogui.press('esc')
    else:
        current_subflow = "Main.txt"

    return current_subflow

def clickSubflowsDropDown():
    # Recognize the subflows icon on screen and return its position
    # (centepr of image)
    try:
        pos_subflow_button = pyautogui.locateCenterOnScreen(
            button_subflows, confidence=.5)
        sleep(2)
    except Exception:
        print("Image not found!")
        print(button_subflows)

    # show the recognized image's position
    print(pos_subflow_button)

    # move mouse to that position
    pyautogui.moveTo(pos_subflow_button)

    # Left handed mouse click
    pyautogui.click(button=mouse_main_button)

def openSubflow(count,wait=waitSubflowOpen):
    # Press 'Down' arrow to select the next subflow
    # (The first iteration doesn't nneed this step)
    if count != 0:
        pyautogui.press('down')

    sleep(1)

    # Press 'enter' to enter the subflow
    pyautogui.press('enter')

    # wait for the subflow to open (take a while if subflow has many
    # steps)
    sleep(wait)


def focusSelectCopySubflow(wait=1):
    # The minimum sleep time is 1s
    if (wait < 1):
        wait = 1

    # Press 'down' to focus in source code
    pyautogui.press('down')

    sleep(wait)

    # select the first line of the source code
    pyautogui.press('home')

    sleep(wait - 0.7)

    # Press CTRL + A to select all the source
    with pyautogui.hold(ctrl):
        pyautogui.press('a')

    # The process of selecting can be slow if the subflow has a lot of
    # steps
    sleep(wait + 1)

    # Press CTRL + C to copy the selection
    with pyautogui.hold(ctrl):
        pyautogui.press('c')

    # The copy process can be slow if the subflow has many steps
    sleep(wait + 1)

def genContentStr():
    # put the contents of clipboard in content and print it
    content = pc.paste()
    content = content.replace('\r', '')

    print(content)

    # encode shall return the bytes and not the string 
    content = content.encode('utf-8')

    return content

def main():
    global proj_dir
    global n_subflows
    
    proj_dir = easygui.diropenbox(
        msg='Select the path to your project directory',
        title='Project Directory'
    )

    # ask the user for the number of subflows
    n_subflows = pyautogui.prompt(
        text='What is the number of subflows in your project?',
        title='Prompt Number of Subflows'
    )

    # Check if proj_dir exists, if so remove it
    #checkProjDir()
    # Don't recreate (git repository would have been deleted), just update
    # the files within proj_dir
    
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
                openSubflow(++waitSubflowOpen)
                focusSelectCopySubflow(++baseWait)
                content = genContentStr()
                with open(proj_dir + '\\' + current_subflow, 'wb') as fw:
                    fw.write(content)
                
        print('\n-----------')
        print('saving to the %s\\%s\n\n\n\n' %(proj_dir, current_subflow) )
    
    # Alert that operation has ended
    pyautogui.alert('Finished with success.')
    
    #pyautogui.moveTo(10,10)
    # to click with the right button
    #pyautogui.click(buttom='right')


if __name__ == '__main__':
    main()
