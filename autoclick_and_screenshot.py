import pyautogui
import time

NUM_FRAMES = 6562

time.sleep(3)

for i in range(NUM_FRAMES):
    print(i)
    pyautogui.click(650, 150)
    time.sleep(4)

    im = pyautogui.screenshot()
    im.save(f'bad_apple_output/frame{i:04}.png')
