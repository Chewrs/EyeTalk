import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib
import os
import numpy as np
import cv2
import hailo

from hailo_apps_infra.hailo_rpi_common import (
    get_caps_from_pad,
    get_numpy_from_buffer,
    app_callback_class,
)
from hailo_apps_infra.detection_pipeline import GStreamerDetectionApp


from speak import QueuedTTS # for text-to-speech
from collections import defaultdict  # For tracking object presence
import time
import threading

# -----------------------------------------------------------------------------------------------
# User-defined class to be used in the callback function
# -----------------------------------------------------------------------------------------------
# Inheritance from the app_callback_class
class user_app_callback_class(app_callback_class):
    def __init__(self):
        super().__init__()
        self.sp = QueuedTTS(engine='offline', lang='th')
        self.object_presence = defaultdict(int) # Tracks how long an object is present
        self.object_absence = defaultdict(int)  # Tracks how long an object is missing

        self.object_status: dict[str, bool] = {}   # lable -> bool (e.g., "label" -> True if active)
        self.object_save: dict[str,int] = {}

    def get_english_to_thai_dict(self,word):
        eng_to_thai =  {
            "person": "คน",
            "cell phone": "โทรศัพท์มือถือ",
            "bottle": "ขวดน้ำ",
            "remote": "รีโมท",
            "book": "หนังสือ",
            "bag": "กระเป๋า",
            "car": "รถยนต์",
            "chair": "เก้าอี้",
            "table": "โต๊ะ",
            "pen": "ปากกา",
            "latop": "คอมพิวเตอร์",
            "fan": "พัดลม",
            "cup":"แก้วน้ำ"
        }
        return eng_to_thai.get(word.lower(), "อื่นๆ") 
    
def safe_speak(sp, text):
    threading.Thread(target=sp.speak, args=(text,), daemon=True).start()

# -----------------------------------------------------------------------------------------------
# User-defined callback function
# -----------------------------------------------------------------------------------------------

# This is the callback function that will be called when data is available from the pipeline
def app_callback(pad, info, user_data):
    start = time.time()  # Start time for performance measurement
    # Get the GstBuffer from the probe info
    buffer = info.get_buffer()
    # Check if the buffer is valid
    if buffer is None:
        return Gst.PadProbeReturn.OK


    # Using the user_data to count the number of frames
    user_data.increment()


    # Get the caps from the pad
    format, width, height = get_caps_from_pad(pad)

    # If the user_data.use_frame is set to True, we can get the video frame from the buffer
    user_data.use_frame = False  # Set this to True to use the frame
    frame = None
    if user_data.use_frame and format is not None and width is not None and height is not None:
        # Get video frame
        frame = get_numpy_from_buffer(buffer, format, width, height)

    # Get the detections from the buffer
    roi = hailo.get_roi_from_buffer(buffer)
    detections = roi.get_objects_typed(hailo.HAILO_DETECTION)

    # Parse the detections
    detection_count = 0 
    seen_label = set()
    obj_this_frame: dict[str, int] = {}  # Tracks the object in each frame

    # Go through each detection in the buffer
    for detection in detections:
        # get info of each detection
        label = detection.get_label()
        bbox = detection.get_bbox()
        confidence = detection.get_confidence()


        seen_label.add(label)  # Add label to the "set" of seen labels

        # increment the detection count of each object label
        if label not in user_data.object_save: #add new object to object_save: dict[label: couut]
            user_data.object_save[label] = 1
        elif label in user_data.object_save and user_data.object_save[label] < 20: #increase seen cout to existing object
            if user_data.object_status.get(label, False) is False: # for new object.
                if confidence > 0.6:  # harder for unverified object aka (status = False)
                    user_data.object_save[label] += 1
            else: 
                user_data.object_save[label] += 1


        # Speak the new verified object
        if user_data.object_save[label] >= 10 and user_data.object_status.get(label, False) is False:
            user_data.object_status[label] = True  # Mark the object as active
            print('Object detected:', label)
            safe_speak(user_data.sp, f"เห็น {user_data.get_english_to_thai_dict(label)}")
        

    # Delete activate object that is not detect
    active_objects = [label for label, status in user_data.object_status.items() if status]
    for label in active_objects:

        #print(f"Active object: {label}, Count: {user_data.object_save[label]}") #print active objects and their counts

        if label not in seen_label:
            user_data.object_save[label] -= 1

            if user_data.object_save[label] <= 1:
                user_data.object_status[label] = False

                print('Object not detected:', label)
                safe_speak(user_data.sp, f"ไม่เห็น {user_data.get_english_to_thai_dict(label)}")
    

    #### Print the object status
    if user_data.get_count() % 100 == 0:
        print(f"frame{user_data.get_count()}, fps: {1/(time.time()-start):.2f}")
    

    return Gst.PadProbeReturn.OK

if __name__ == "__main__":
    # Create an instance of the user app callback class

    user_data = user_app_callback_class()
    app = GStreamerDetectionApp(app_callback, user_data)
    app.run()
