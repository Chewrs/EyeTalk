import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib
import os
import numpy as np
import cv2
import hailo

from hailo_apps_infra.hailo_rpi_common import (
    get_caps_from_pad, #not using
    get_numpy_from_buffer, #not using
    app_callback_class,
)
from hailo_apps_infra.detection_pipeline import GStreamerDetectionApp


from speak import QueuedTTS # for text-to-speech
import Name_Eng_to_thai # for Coco items translation

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


    def is_object_in_center(self, xmin, xmax, ymin, ymax,label, screen_width=1280, screen_height=720, margin=100):

        #center of the screen
        screen_center_x = screen_width // 2 
        screen_center_y = screen_height // 2

        # Calculate the center "area" of the screen with margin
        central_screen_x = [(screen_center_x - margin), (screen_center_x + margin)]
        central_screen_y = [(screen_center_y - margin), (screen_center_y + margin)]
        #print(f"central_screen_x: {central_screen_x}, central_screen_y: {central_screen_y}")
        # Calculate the center of the object
        obj_center_x = (xmin + xmax) / 2
        obj_center_y = (ymin + ymax) / 2

        # Scale the object center to the screen size
        obj_center_x_scaled = obj_center_x * screen_width
        obj_center_y_scaled = obj_center_y * screen_height


        if obj_center_x_scaled > central_screen_x[0] and obj_center_x_scaled < central_screen_x[1]:
            if obj_center_y_scaled > central_screen_y[0] and obj_center_y_scaled < central_screen_y[1]:
                return True
        else:
            return False


#Text to speech with threading
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


    # Count the number of frames (hailo_rpi_common -> gstreamer_app.py)
    user_data.increment()


    # Get the caps from the pad
    format, width, height = get_caps_from_pad(pad)


    # ----- Not using ------
    # If the user_data.use_frame is set to True, we can get the video frame from the buffer
    user_data.use_frame = False  # Set this to True to use the frame
    frame = None
    if user_data.use_frame and format is not None and width is not None and height is not None:
        # Get video frame
        frame = get_numpy_from_buffer(buffer, format, width, height)


    # Decode the detections from the buffer
    roi = hailo.get_roi_from_buffer(buffer)
    detections = roi.get_objects_typed(hailo.HAILO_DETECTION)

    # Parse the detections
    seen_label = set() #reset every frame

    # Go through each detection in the buffer/frame
    for detection in detections:

        # get info of each detection
        label = detection.get_label()
        bbox = detection.get_bbox()
        confidence = detection.get_confidence()

        # defind the bbox coordinates
        xmin = float(bbox.xmin())
        xmax = float(bbox.xmax())
        ymin = float(bbox.ymin())
        ymax = float(bbox.ymax())


        #Only count if object is in the center of the screen
        if user_data.is_object_in_center(xmin, xmax, ymin, ymax, label):
            seen_label.add(label)  # Add label to the "set" of seen labels


            # --- increment the detection count of each object label ---
            if label not in user_data.object_save: # add new object to object_save: dict[label: couut]
                user_data.object_save[label] = 1

            elif label in user_data.object_save and user_data.object_save[label] < 20: #increase seen cout to existing object
                if user_data.object_status.get(label, False) is False: # for new object.
                    if confidence > 0.6:  # harder for unverified object aka (status = False)
                        user_data.object_save[label] += 1
                        print(f"detected {label} {user_data.object_save[label]} times")

                else: 
                    user_data.object_save[label] += 1


            # ----Speak the new verified object-----
            if user_data.object_save[label] >= 5 and user_data.object_status.get(label, False) is False:
                user_data.object_status[label] = True  # Mark the object as active
                print('Object detected:', label) 
                safe_speak(user_data.sp, f" {Name_Eng_to_thai.get_english_to_thai_dict(label)}")
       
        

    # ---- DELETE activated object that is not detect ----
    active_objects = [label for label, status in user_data.object_status.items() if status]
    for label in active_objects:

        #print(f"Active object: {label}, Count: {user_data.object_save[label]}") #print active objects and their counts

        if label not in seen_label:
            user_data.object_save[label] -= 1

            # If the object has not been seen for a while, mark it as inactive (20 frames)
            if user_data.object_save[label] <= 1:
                user_data.object_status[label] = False

                print('Object not detected:', label)
                #safe_speak(user_data.sp, f"ไม่เห็น {Name_Eng_to_thai.get_english_to_thai_dict(label)}")
    

    #### Print the FPS status
    if user_data.get_count() % 100 == 0: #every 100 frames
        print(f"frame{user_data.get_count()}, fps: {1/(time.time()-start):.2f}")
    

    return Gst.PadProbeReturn.OK



def run_yolo(app_callback, user_data):
    safe_speak(user_data.sp, "เริ่มต้นการทำงาน") #speak

    app = GStreamerDetectionApp(app_callback, user_data) 
    user_data.app = app # let user_data access the GStreamerDetectionApp (gstreamer_app.py)
    app.run()

if __name__ == "__main__":
    user_data = user_app_callback_class()
    safe_speak(user_data.sp, "เริ่มต้นการทำงาน") #speak
    app = GStreamerDetectionApp(app_callback, user_data) 
    app.run()



