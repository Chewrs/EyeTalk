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


from speak import TTS # for text-to-speech
from collections import defaultdict  # For tracking object presence

# -----------------------------------------------------------------------------------------------
# User-defined class to be used in the callback function
# -----------------------------------------------------------------------------------------------
# Inheritance from the app_callback_class
class user_app_callback_class(app_callback_class):
    def __init__(self):
        super().__init__()
        self.sp = TTS(engine='offline', lang='th') # Initialize the TTS engine
        self.object_presence = defaultdict(int) # Tracks how long an object is present
        self.object_absence = defaultdict(int)  # Tracks how long an object is missing
        self.object_status: dict[int, bool] = {}   # int -> bool (e.g., "ID" -> True if active)

    def new_function(self):  # New function example
        return "The meaning of life is: "
    

# -----------------------------------------------------------------------------------------------
# User-defined callback function
# -----------------------------------------------------------------------------------------------

# This is the callback function that will be called when data is available from the pipeline
def app_callback(pad, info, user_data):

    # Get the GstBuffer from the probe info
    buffer = info.get_buffer()
    # Check if the buffer is valid
    if buffer is None:
        return Gst.PadProbeReturn.OK


    # Using the user_data to count the number of frames
    user_data.increment()
    string_to_print = ''
    #string_to_print = f"Frame count: {user_data.get_count()}\n"

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
    seen_id = set()
    for detection in detections:
        # get info of each detection
        label = detection.get_label()
        bbox = detection.get_bbox()
        confidence = detection.get_confidence()

        # Get track ID
        track_id = 0
        track = detection.get_objects_typed(hailo.HAILO_UNIQUE_ID)
        if len(track) == 1:
            track_id = track[0].get_id()
        
        seen_id.add(track_id)
        user_data.object_presence[track_id] += 1
        user_data.object_absence[track_id] =0

        if user_data.object_presence[track_id] >= 10 and not user_data.object_status.get(track_id, False):
            # If the object has been present for more than 10 frames and was not previously detected
            string_to_print = f"Object {track_id} detected with label {label} and confidence {confidence:.2f}\n"
            print(f"[DEBUG] Detected label: {label}")
            user_data.sp.speak(f"เห็น {label}")
            user_data.object_status[track_id] = True  # Mark as detected
        elif user_data.object_presence[track_id] < 10:
            print(f"[DEBUG] Object {track_id},{label} is  not present long enough {user_data.object_presence[track_id]} frames")


    for track_id in list(user_data.object_status.keys()):
        if track_id not in seen_id:
            user_data.object_absence[track_id] += 1
            user_data.object_presence[track_id] = 0
            if user_data.object_absence[track_id] >= 30 and user_data.object_status.get(track_id, False):
                # If the object has been absent for more than 10 frames and was previously detected
                string_to_print += f"Object {track_id} no longer detected\n"
                #user_data.sp.speak(f"วัตถุ {track_id} หายไป")
                user_data.object_status[track_id] = False



    #print(string_to_print)
    return Gst.PadProbeReturn.OK

if __name__ == "__main__":
    # Create an instance of the user app callback class

    user_data = user_app_callback_class()
    app = GStreamerDetectionApp(app_callback, user_data)
    app.run()
