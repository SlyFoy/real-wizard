from collections import deque
import cv2
import numpy as np
import time
from picamera2 import Picamera2


# One second to cast a spell
full_spell_time = 1
framerate = 15
frames_per_spell = full_spell_time * framerate

def rolling_long_exposure():
    # Set up our PiCamera
    camera = Picamera2()
    camera.resolution = (640, 480)  # You may change this
    camera.framerate = framerate  # Set the framerate at 24 fps

    
    print("Starting up")
    camera.start_preview()

    # Allow camera to warmup
    time.sleep(0.1)

    # Setup our variables for buffer and counter
    buffer = deque(maxlen=frames_per_spell) # a deque only stores the latest spell
    frame_counter = 0

    # Capture continuously
    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        # Add the latest frame to the buffer and the buffer only stores the latest frames
        img = frame.array
        buffer.append(img * 1.0 / frames_per_spell)  # Scale before adding
        
        # Stack those images every 5 frames
        frame_counter += 1
        if frame_counter % frames_per_spell == 0:
            stack_img = sum(buffer)  # pixel-wise sum of images
            # Normalize stack image to 8-bit (0-255)
            stack_img = cv2.normalize(stack_img, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
            
            print(f"stacked{frame_counter//frames_per_spell}.jpg")
            # Write out our stacked image to a file
            cv2.imwrite(f"stacked{frame_counter//frames_per_spell}.jpg", stack_img)
        
        # Clear the stream in preparation for the next frame
        raw_capture.truncate(0)

rolling_long_exposure()
