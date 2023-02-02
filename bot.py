import pyautogui as pa
import pyperclip as cb
import rpa
import pdb
import pywinauto as pwa


SLEEP_SUBFLOWS_MENU = .5
SLEEP_FOCUS_SUBFLOW = .2
SLEEP_COPY_CONTENT = 2
SUBFLOW_NAME = str()
SUBFLOW_CONTENTS = str()
SUBFLOW_EXTENSION = '.txt'
PROJECT_DIR = str()
PAD_DESIGNER_EXE = f'C:\Program Files (x86)\Power Automate Desktop\PAD.Designer.exe'

def focusPadDesignerWin():
    app = pwa.Application().connect(path=PAD_DESIGNER_EXE)
    app.window().set_focus()
    

def openNextSubflow(imgs: dict):
    # click the subflows menu
    rpa.click(imgs['subflows-icon'])

    # Press 'Down' arrow to select the next subflow
    # Press 'enter' to enter the subflow
    rpa.press_sequence("down", "enter", sleep=SLEEP_SUBFLOWS_MENU)

    # Focus on opened subflow with 3 tabs
    #rpa.press_sequence("tab", "tab", "tab", sleep=SLEEP_FOCUS_SUBFLOW)
    rpa.click(imgs['subflows-icon'], offset=(222, 58))
    
def getSubflowName(imgs: dict):
    global SUBFLOW_NAME

    # wait subflow open (button subflows changes from gray to white)
    rpa.waitAppear(imgs['when-sf-open'])
    
    # Press "f2" to open the edit subflow name pop-up
    rpa.press_sequence("f2")

    # Wait for the pop-up to appear
    rpa.waitAppearAll(imgs['rename-subflow'], imgs['subflow-name'])

    # The focus comes already in the text box, so just copy to clipboard with c-c
    #pdb.set_trace()
    rpa.press_sequence("c", hold_ctrl=True)

    SUBFLOW_NAME = cb.paste()

    # Press esc to close the edit subflow name pop-up
    rpa.press_sequence("esc")

    # Wait the pop-up close
    try:
        rpa.waitDisappearAll(imgs['rename-subflow'], imgs['subflow-name'])
    except Exception:
        # no matter if it disappears to quick and no have time to see it
        # the first time.
        pass

    return SUBFLOW_NAME


def saveSubflowTxt():
    global SUBFLOW_CONTENTS
    
    # Select all the current flow and copy to clipboard
    rpa.press_sequence(("a", True), ("c", True), sleep=SLEEP_COPY_CONTENT)

    SUBFLOW_CONTENTS = cb.paste()
    SUBFLOW_CONTENTS = SUBFLOW_CONTENTS.replace('\r', '')
    # good place to print
    SUBFLOW_CONTENTS = SUBFLOW_CONTENTS.encode('utf-8')

    #pdb.set_trace()
    print(f'Writing {SUBFLOW_NAME}...', end='')
    try:
        with open(PROJECT_DIR + '\\' + SUBFLOW_NAME + SUBFLOW_EXTENSION, 'wb') as fw:
            fw.write(SUBFLOW_CONTENTS)
        print(' success')
    except Exception as e:
        print(' failed')
        raise e
