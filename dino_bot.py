import pyautogui
import mss
import numpy as np
import time

pyautogui.time.sleep(3)

c = 10
last_time = time.time()
frames = 0

with mss.mss() as sct:
    while 1:
        x, y = pyautogui.position()
        frames += 1

        monitor = {"top": y - c, "left": x - c, "width": 2 * c, "height": 2 * c}
        img = np.array(sct.grab(monitor))

        brightness = img[:,:,:3].mean(axis=2)

        if (brightness < 128).any():  # obstacle detected
            pyautogui.hotkey("space")

        if frames % 200 == 0:
            print(f"Frames: {frames / (time.time() - last_time)}")
            last_time = time.time()
            frames = 0