from time import sleep
# To emulate user typing
import pyautogui
import pyperclip as pc
# File and directory low level operations
import os
# To remove a directory and all its contents
import shutil
# Regex functionality
import re
# to use the input dir message window
import easygui

# if keyboard is remapped
ctrl = 'ctrl'
mouse_main_button = 'left'
button_subflows = './img/subflow_icon.JPG'
button_add = './img/add_icon.JPG'
#proj_dir = 'c:/Users/lsilva46/testproj'
#proj_dir = 'c:/Users/lsilva46' + \
#    '/OneDrive - Capgemini/Documents/git/protheus-invoice-posting'
sc_extension = '.txt'
source_files = []
debug = True

# class to store each source file information
class SourceCodeFile:
    def __init__(self, name, number):
        self.name = name
        self.number = number
        path = proj_dir + '/' + name + sc_extension
        # normalizing the path to file
        self.path = os.path.abspath(path)

def sortFunction(sfObj):
    if sfObj.number == None:
        number = 0
    else:
        number = int(sfObj.number)

    return number

def getSourceFiles():
    for scFile in os.listdir(proj_dir):
        matchObjNum = re.search(r"(\d+)", scFile)
        matchObjName = re.search(r"(\w+\d*)\.(\w+)", scFile)
        if matchObjNum:
            #print('File:', scFile)
            #print('Number:', matchObjNum.group())
            number = matchObjNum.group()
        else:
            #print('Nothing found', scFile)
            #print('Number: ', matchObjNum)
            number = 0;

        if matchObjName:
            print('File:', matchObjName.group(1))
            name=matchObjName.group(1)
        else:
            print('Name not found', scFile)
            name='not_a_source'
        print('Number:', number)

        if name != 'README' and name != 'not_a_source':
            source_files.append(SourceCodeFile(
                name=name, number=number
            ))

# click in Subflows icon
def recognizeClick(img_path, add_x=0, add_y=0):
    # Recognize the subflows icon on screen and return its position
    # (centepr of image)
    try:
        pos_subflow_button = pyautogui.locateCenterOnScreen(
            img_path, confidence=.7)
        sleep(1)
    except Exception:
        print("Image not found!")

    # show the recognized image's position
    print('Recognized image\'s position',
          pos_subflow_button)
    print('x = ', pos_subflow_button[0])
    print('y = ', pos_subflow_button[1])

    # move mouse to that position
    pyautogui.moveTo(
        pos_subflow_button[0] + add_x,
        pos_subflow_button[1] + add_y)

    sleep(1)
    
    # Left handed mouse click
    pyautogui.click(button=mouse_main_button)

    sleep(1)

def main():
    global proj_dir
    proj_dir = easygui.diropenbox(
        msg='Select the path to your project directory',
        title='Project Directory'
    )

    # Read the directory proj_dir and create the objects with name and
    # number as separated attributes. Then these objects are put in the
    # list source_files
    getSourceFiles()

    # seeing if the objects are indeed in the list
    #for current in source_files:
    #    print(current.name)
    #    print(current.number)

    # sorting the files according to their numbers
    source_files.sort(key=sortFunction)

    print('\nSource files after sorting:')
    for current in source_files:
        print(current.name)
        print(current.number)
        print(current.path,'\n')

    for currentSourceFile in source_files:
        # Shows if the contents of each file are in the clipboard
        #print(pc.paste())

        ### Begin RPA Code

        if currentSourceFile.number != 0:
            # click on Subflows button
            recognizeClick(img_path=button_subflows)
            # click on Add New Subflow button
            recognizeClick(img_path=button_add)
            # write string from variable to window
            pyautogui.write(currentSourceFile.name, interval=0.1)
            # press Enter to open the new Subflow tab
            sleep(1)
            pyautogui.press('enter')

        # click on code sub window (right below Main tab icon)
        recognizeClick(img_path=button_subflows, add_x=50, add_y=30)

        # open the SourceFile as read only and copy its contents to
        # clipboard
        with open(currentSourceFile.path, "rb") as openedSF:
            print('currentSourcefile.name =', currentSourceFile.name)
            print('currentSourcefile.number =', currentSourceFile.number)
            sfContents = openedSF.read()
            pc.copy(sfContents.decode('utf-8'))
            print('File path:', currentSourceFile.path)
            print('\nContents from clipboard...')
            print('\n', pc.paste())
            if pc.paste() == '':
                print('Clipboard is void')
                print('Contents of openedSF.read()...\n')
                print(openedSF.read())

        # paste contents from clipboard to code window
        with pyautogui.hold(ctrl):
            pyautogui.press('v')

        sleep(2)

    pyautogui.alert('Finished!')

if __name__ == "__main__":
    main()
