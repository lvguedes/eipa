import pyautogui as pa
import concurrent.futures as cf
import multiprocessing as mp

from time import sleep

default_timeout = 60
default_confidence = .7
max_workers = 5

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

# finds the firt image that appears on screen
def waitAppearAny(imgs:list, timeout=default_timeout):
    with cf.ProcessPoolExecutor(max_workers=max_workers) as pool:
        futures = [pool.submit(waitAppear, img) for img in imgs]
        done, not_done = cf.wait(futures, return_when=cf.FIRST_COMPLETED)
        for f in not_done:
            f.cancel()
        for f in done:
            exception = f.exception()
            if exception:
                raise exception
            #print(f)
            print("Future: %s.\nFound image at position: %s" % (f, str(f.result())))
        pool.shutdown(wait=False)

    # kills all the pending futures (they're subprocesses of interpreter)
    for proc in mp.active_children():
        proc.kill()

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
