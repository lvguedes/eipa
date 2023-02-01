import pyautogui as pa
import rpa
import pdb

SLEEP_SUBFLOWS_MENU = .5
SLEEP_FOCUS_SUBFLOW = .2
SLEEP_COPY_CONTENT = .8

def openSubflow(imgs: dict):
    # click the subflows menu
    rpa.click(imgs['subflows-icon'])

    # Press 'Down' arrow to select the next subflow
    # Press 'enter' to enter the subflow
    rpa.press_sequence("down", "enter", sleep=SLEEP_SUBFLOWS_MENU)

    # Focus on opened subflow with 3 tabs
    #rpa.press_sequence("tab", "tab", "tab", sleep=SLEEP_FOCUS_SUBFLOW)
    rpa.click(imgs['subflows-icon'], offset=(222, 58))
    
    #pdb.set_trace()
    # Select all the current flow and copy to clipboard
    rpa.press_sequence(("a", True), ("c", True), sleep=SLEEP_COPY_CONTENT)
    

def getSubflowName():
    pass

def saveSubflowTxt():
    pass

