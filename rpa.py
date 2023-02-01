import pdb
import time
import pyautogui as pa
import concurrent.futures as cf
import multiprocessing as mp


from collections.abc import Callable

# Global Constants
DEFAULT_TIMEOUT = 60
DEFAULT_CONFIDENCE = .7
MAX_WORKERS = 5
DEFAULT_MOUSE_BUTTON = 'right'
DEFAULT_PRESS_SLEEP = .5
DEFAULT_CTRL_KEY = 'ctrl'

# generates the common timeout message
def _timeout_message(timeout,img,action):
    return \
        f"Reached timeout of {timeout}s while " +\
        f"waiting for the image {img} to "+\
        f"{action} on screen."

def _image_not_found_message(img):
    return \
        f"Image not found ({img}). " +\
        "ImageNotFoundException not thrown. " +\
        "Function has just returned None."

def _find_img(img, confidence=DEFAULT_CONFIDENCE):
    pos = pa.locateCenterOnScreen(
        img, confidence=confidence
    )
    if not pos:
        raise Exception(_image_not_found_message(img))

    return pos



# function that waits until an image appears on screen
# or reaches timeout
def waitAppear(img, timeout=DEFAULT_TIMEOUT, confidence=DEFAULT_CONFIDENCE, _slept=0):
    try:
        pos = _find_img(img, confidence)
    except Exception:
        time.sleep(1)
        _slept+=1
        print(f"Currently slept {_slept}s. Waiting for {img}")
        if _slept <= timeout:
            pos = waitAppear(img, _slept=_slept)
            return pos
        else:
            raise Exception(_timeout_message(timeout,img,'appear'))
    return pos


# waits for any img to disappear from screen
# within timeout
# Returns: True, if the image has disappeared
def waitDisappear(img, timeout=DEFAULT_TIMEOUT, confidence=DEFAULT_CONFIDENCE, _slept=0):
    while(True):
        try:
            pos = _find_img(img, confidence)
        except Exception:
            if _slept == 0:
                raise Exception(_image_not_found_message(img))
            return True
        time.sleep(1); _slept += 1
        print(f"Waits for {_slept}s; img: {img}")
        if _slept >= timeout:
            raise Exception(_timeout_message(timeout,img,'disappear'))
        if not pos:
            return True

        
def waitAppearAll(*args, timeout=DEFAULT_TIMEOUT, confidence=DEFAULT_CONFIDENCE):
    """Every image given must appear on screen otherwise will throw an exception"""
    positions = []
    for img in args:
        positions.append(
            waitAppear(img, timeout, confidence)
        )

    return positions


def waitDisappearAll(*args, timeout=DEFAULT_TIMEOUT, confidence=DEFAULT_CONFIDENCE):
    """Every image given must disappear from screen otherwise will throw an exception.
    It'll also throw an exception if when it's called it cannot find the image within
    the first second. That is, the image was not on screen when function started"""
    disappeared = False
    for img in args:
        disappeared = waitDisappear(img, timeout, confidence)

    return disappeared


def waitAny(imgs:list, wait_to:Callable, timeout=DEFAULT_TIMEOUT):
    """
    Parameters:
      imgs: list of paths to images in OS filesystems
      wait_to: Callable (function) which can be:
         waitAppear, waitDisappear
      timeout: the timeout to find the image
    Returns:
      A point representing where the image was found
    """
    result = None
    with cf.ProcessPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = [pool.submit(waitAppear, img) for img in imgs]
        done, not_done = cf.wait(futures, return_when=cf.FIRST_COMPLETED)
        for f in done:
            exception = f.exception()
            if exception:
                raise exception
            result = f.result()
            #print(f)
            print("Future: %s.\nFound image at position: %s" % (f, result))
        pool.shutdown(wait=False, cancel_futures=True)

    # kills all the pending futures (they're subprocesses of interpreter)
    for proc in mp.active_children():
        proc.kill()


def click(img, button=DEFAULT_MOUSE_BUTTON, timeout=DEFAULT_TIMEOUT, confidence=DEFAULT_CONFIDENCE, offset=tuple()):
    """Clicks in only one image with the possibility of offset."""
    pos = waitAppear(img, timeout=timeout, confidence=confidence)
    if type(offset) == tuple and len(offset) == 2:
        x, y = offset
        x += pos.x
        y += pos.y
    else:
        x = pos.x
        y = pos.y
    pa.click(x = x, y = y, button = button)
    return True

def press_sequence(*args, sleep=DEFAULT_PRESS_SLEEP, hold_ctrl=False, ctrl_key=DEFAULT_CTRL_KEY):
    """Press a one or more keyboard keys, once at a time. Can also hold ctrl
    for all keys through the keyword argument "ctrl_key" or in a key-by-key fashion
    passing each arg from args as a tuple in the format (key: str, ctrl: bool )
    """
    key = str()
    ctrl_seq = bool()
    for arg in args:
        if type(arg) == tuple:
            key, ctrl_seq = arg
        else:
            key = arg
            
        time.sleep(sleep)
        
        if ctrl_seq:
            with pa.hold(ctrl_key):
                pa.press(key)
        else:
            pa.press(key)
        

# # finds the firt image that appears on screen
# def waitAppearAny(imgs:list, timeout=DEFAULT_TIMEOUT):
#     with cf.ProcessPoolExecutor(max_workers=MAX_WORKERS) as pool:
#         futures = [pool.submit(waitAppear, img) for img in imgs]
#         done, not_done = cf.wait(futures, return_when=cf.FIRST_COMPLETED)
#         for f in done:
#             exception = f.exception()
#             if exception:
#                 raise exception
#             #print(f)
#             print("Future: %s.\nFound image at position: %s" % (f, f.result()))
#         pool.shutdown(wait=False, cancel_futures=True)

#     # kills all the pending futures (they're subprocesses of interpreter)
#     for proc in mp.active_children():
#         proc.kill()

# Here you pass the function (APPEAR or DISAPPEAR) to "wait_to" parameter
