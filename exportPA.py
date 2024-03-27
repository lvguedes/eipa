import traceback
import pdb
import pyautogui as pa
import pyperclip as cb
import argparse as arg
import bot
import rpa
import multiprocessing
import sys

from json import loads

def parse_config():
    with open(bot.CONFIG_PATH) as confFile:
        config = loads(confFile.read())

#    bot.PROJECT_DIR = r'test'

def kernel():
    bot.SUBFLOW_NAME = str()
    #pdb.set_trace()
    bot.focusPadDesignerWin()
    if len(bot.PROCESSED_SUBFLOWS) > 0 or bot.SKIP_MAIN_SUBFLOW:
        bot.SUBFLOW_NAME = bot.getSubflowName(bot.IMGS)
    else:
        bot.SUBFLOW_NAME = bot.PAD_MAIN_SF_NAME
    bot.saveSubflowTxt()
    bot.openNextSubflow(bot.IMGS)
    bot.PROCESSED_SUBFLOWS.append(bot.SUBFLOW_NAME)

    print(f'Processed subflows: {bot.PROCESSED_SUBFLOWS}')

    
def driver():
    parse_config()
    while True:
        kernel()
        if bot.PROCESSED_SUBFLOWS.count(bot.SUBFLOW_NAME) > 1 or bot.REACHED_CREATE_SF_BUTTON:
            break

def main():
    try:
        driver()
    except Exception as e:
        traceback.print_exc()
        #print(e)
        print('\n\nWould you try again? [y/n] ', end='')
        answer = input()
        if answer == 'y':
            bot.SKIP_MAIN_SUBFLOW = False
            main()
        
def main_test():
    '''Function to test only the core of the
    process. That is, when executed with only one
    subflow'''
    kernel()
    
def process_cli_options():
    parser = arg.ArgumentParser(
        prog = 'Export / Import Power Automate',
        description = 'Export Subflows from PAD to text files'
    )
    parser.add_argument('-s', '--skip-main-sf', action='store_true', help='Skip main subflow?') # skip main subflow?
    parser.add_argument('-p', '--project-dir', default='.')
    args = parser.parse_args()

    bot.PROJECT_DIR = args.project_dir
    bot.SKIP_MAIN_SUBFLOW = args.skip_main_sf
    
if __name__ == '__main__':
    if sys.platform.startswith('win'):
        multiprocessing.freeze_support()
    process_cli_options()
    main()
    # main_test() # to test only one subflow
