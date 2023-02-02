import pdb
import pyautogui as pa
import pyperclip as cb
import bot
import rpa

from json import loads

PROCESS_MAIN_SUBFLOW = True
PROCESSED_SUBFLOWS = list()
CONFIG = None
IMGS = {
    'rename-subflow': r'.\img\rename-subflow-txt.jpg',
    'add-icon': r'.\img\add_icon.JPG',
    'subflow-name': r'.\img\subflow-name-txt.jpg',
    'subflows-icon': r'.\img\subflow_icon.JPG',
    'when-sf-open': r'.\img\when-subflow-open.jpg'
}
CONFIG_PATH = r'.\config.json'
PAD_MAIN_SF_NAME = 'Main'

def parse_config():
    with open(CONFIG_PATH) as confFile:
        config = loads(confFile.read())

    bot.PROJECT_DIR = r'test'

def kernel():
    global PROCESSED_SUBFLOWS

    bot.SUBFLOW_NAME = str()
    bot.focusPadDesignerWin()
    if len(PROCESSED_SUBFLOWS) > 0 or not PROCESS_MAIN_SUBFLOW:
        bot.SUBFLOW_NAME = bot.getSubflowName(IMGS)
    else:
        bot.SUBFLOW_NAME = PAD_MAIN_SF_NAME
    bot.saveSubflowTxt()
    bot.openNextSubflow(IMGS)
    PROCESSED_SUBFLOWS.append(bot.SUBFLOW_NAME)

    print(f'Processed subflows: {PROCESSED_SUBFLOWS}')

    
def driver():
    parse_config()
    while True:
        kernel()
        if PROCESSED_SUBFLOWS.count(bot.SUBFLOW_NAME) > 1:
            break

def main():
    global PROCESS_MAIN_SUBFLOW
    
    try:
        driver()
    except Exception as e:
        print(e)
        print('\n\nWould you try again? [y/n] ', end='')
        answer = input()
        if answer == 'y':
            bot.PROCESS_MAIN_SUBFLOW = False
            driver()
        
    # Alert that operation has ended
    pa.alert('Finished with success.')

def main_test():
    '''Function to test only the core of the
    process. That is, when executed with only one
    subflow'''
    kernel()
    
def process_cli_options():
    pass
    
if __name__ == '__main__':
    main()
    # main_test() # to test only one subflow
