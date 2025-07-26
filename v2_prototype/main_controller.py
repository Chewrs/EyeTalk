from New_alg_eyetalk import app_callback, user_app_callback_class, run_yolo 
import sys
import time
from gi.repository import Gst

import threading



# Start a timer in another thread to pause run_yolo
def pause_pipeline_later():
    time.sleep(15)

    user_data.running = False #  -> class app_callback_class & display_user_data_frame (gstreamer_app.py)
    user_data.app.pipeline.set_state(Gst.State.PAUSED)  # control with Gstreamer_app (New_alg_eyetalk.py -> gstreamer_app.py)
    print("Pausing pipeline...")
    
    time.sleep(2)
    user_data.running = True
    user_data.app.pipeline.set_state(Gst.State.PLAYING)




if __name__ == "__main__":
    threading.Thread(target=pause_pipeline_later, daemon=True).start()
    sys.argv = [sys.argv[0], '--input', 'rpi']
    user_data = user_app_callback_class()
    run_yolo(app_callback, user_data)