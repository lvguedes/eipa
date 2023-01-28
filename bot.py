import pyautogui

from time import sleep
from json import loads


global config
confPath = r".\config.json"
with open(confPath) as confFile:
    config = loads(confFile.read())


def clickSubflowsDropDown():
    # Recognize the subflows icon on screen and return its position
    # (centepr of image)
    try:
        pos_subflow_button = pyautogui.locateCenterOnScreen(
            config['button_subflows'], confidence=.5)
        sleep(2)
    except Exception:
        print("Image not found!")
        print(config['button_subflows'])

    # show the recognized image's position
    print(pos_subflow_button)

    # move mouse to that position
    pyautogui.moveTo(pos_subflow_button)

    # Left handed mouse click
    pyautogui.click(button=config['mouse_main_button'])

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
        with pyautogui.hold(config['ctrl_key']):
            pyautogui.press('c')

        current_subflow = pc.paste() + '.txt'

        # Esc to quit the rename dialog and return to source code
        pyautogui.press('esc')
    else:
        current_subflow = "Main.txt"

    return current_subflow


def openSubflow(count,wait=config['wait_subflow_open']):
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
    with pyautogui.hold(config['ctrl_key']):
        pyautogui.press('a')

    # The process of selecting can be slow if the subflow has a lot of
    # steps
    sleep(wait + 1)

    # Press CTRL + C to copy the selection
    with pyautogui.hold(config['ctrl_key']):
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

