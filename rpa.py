import pyautogui as pa
import threading as th

from time import sleep

default_timeout = 60
default_confidence = .7

# generates the common timeout message
def _timeout_message(timeout,img,action):
    return \
        f"Reached timeout of {timeout}s while " +\
        f"waiting for the image {img} to "+\
        f"{action} on screen."


# function that waits until an image appears on screen
# or reaches timeout
def waitAppear(img, timeout=default_timeout, _slept=0):
    try:
        pos = pa.locateCenterOnScreen(
            img, confidence=default_confidence
        )
        if not pos:
            raise Exception(
                f"Image not found ({img}). "+
                "ImageNotFoundException not thrown. "+
                "Function has just returned None."
            )
        return pos

    except Exception:
        sleep(1)
        _slept+=1
        print(f"Currently slept {_slept}s.")
        if _slept <= timeout:
            pos = waitAppear(img, _slept=_slept)
            return pos
        else:
            raise Exception(_timeout_message(timeout,img,'appear'))


def waitAppearAll(imgs:list, timeout=default_timeout):
    positions = []
    for img in imgs:
        positions.append(
            waitAppear(img, timeout=timeout)
        )

    return positions

# finds
def waitAppearAny(imgs:list, timeout=default_timeout):
    for img in imgs:
        try:
            pos = waitAppear(img, timeout=timeout)
            if pos:
                break
        except Exception:
            continue
    if not pos:
        raise Exception(
            f"Images {imgs} not found on screen."
        )


# waits for any img to disappear from screen
# within timeout
# Returns: True, if the image has disappeared
def waitDisappear(img, timeout=default_timeout):
    _slept = 0
    while(True):
        pos = pa.locateCenterOnScreen(
            img, confidence=default_confidence
        )
        sleep(1)
        _slept += 1
        print(f"Waits for {_slept}s")
        if _slept >= timeout:
            raise Exception(_timeout_message(timeout,img,'disappear'))
        if not pos:
            return True

def waitDisappearAll(imgs:list, timeout=default_timeout):
    disappeared = False
    for img in imgs:
        disappeared = waitDisappear(img, timeout=timeout)

    return disappeared
