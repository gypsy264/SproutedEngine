import time
import engine
frame = 0
previous_time = 0
def ShowFrame():
    global frame, previous_time
    frame += 1
    current_time = time.time() * 1000
    elapsed_time = current_time - previous_time
    if elapsed_time > 1000:
        fps = frame * 1000 / elapsed_time
        print("Frame rate: {:.2f} fps".format(fps))
        previous_time = current_time
        frame = 0