import rpa
import pyautogui as pa
import threading as th
import asyncio

img1 = "img/add_icon.JPG"
img2 = "img/subflow_icon.JPG"

imgsRenameSubflow = [
    "img/rename-subflow-txt.jpg",
    "img/subflow-name-txt.jpg"]

#rpa.waitAppear("./img/add_icon.JPG")
#pa.locateCenterOnScreen("./img/add_icon.JPG", confidence=.5)

#print(rpa.waitAppearAll(imgsRenameSubflow))

#rpa.default_confidence=.7
#print(rpa.waitDisappear(imgsRenameSubflow[0]))
#result = rpa.waitDisappear(img2)
#print(f"Result:\"{result}\" | Type of result: {type(result)}")
#print(rpa.waitDisappearAll(imgsRenameSubflow))

# t1 = th.Thread(target=rpa.waitAppear, args=[img1])
# t2 = th.Thread(target=rpa.waitAppear, args=[img2])

# t1.start()
# t2.start()

# if t1.join() or t2.join():
#     pass

# if not t2.is_alive():
#     print("t2 finished first")
# elif not t1.is_alive():
#     print("t1 finished first")

async def waitAppear2(img):
    rpa.waitAppear(img)

    if not g1.done():
        g1.cancel()
    elif not g2.done():
        g2.cancel()

async def main():
    global g1, g2
    #t1 = asyncio.create_task(waitAppear2(img1))
    #t2 = asyncio.create_task(waitAppear2(img2))

    g1 = asyncio.gather(waitAppear2(img1))
    g2 = asyncio.gather(waitAppear2(img2))

    await g1
    await g2




    # if task1.done():
    #     task2.cancel()
    # elif task2.done():
    #     task1.cancel()

asyncio.run(main())
#print(f"Result:\"{result}\" | Type of result: {type(result)}")
