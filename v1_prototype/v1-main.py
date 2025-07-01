import cv2
from ultralytics import YOLO
import numpy as np
import time
from collections import defaultdict # For tracking object presence


import requests
import pygame


def speak(text, lang='th-TH'):
    url = "https://translate.google.com/translate_tts"
    params = {
        "ie": "UTF-8",
        "q": text,
        "tl": lang,
        "client": "tw-ob"
    }
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, params=params, headers=headers)

    with open("temp.mp3", "wb") as f:
        f.write(response.content)

    # Use pygame to play audio
    pygame.mixer.init()
    pygame.mixer.music.load("temp.mp3")

    pygame.time.wait(500) #To not start playing before loading

    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue


def get_label_thai(index): 
    return coco_labels_thai.get(index, "ไม่ทราบ")

def where_is_object(x):
    if x < 100:
        return "ทางขวา" #flip from real world
    elif x > 540:
        return "ทางซ้าย" #flip from real world
    else:
        return "ตรงกลาง"

coco_labels_thai = {
    0: 'คน', 1: 'จักรยาน', 2: 'รถยนต์', 3: 'มอเตอร์ไซค์', 4: 'เครื่องบิน',
    5: 'รถบัส', 6: 'รถไฟ', 7: 'รถบรรทุก', 8: 'เรือ', 9: 'ไฟจราจร',
    10: 'หัวดับเพลิง', 11: 'ป้ายหยุด', 12: 'มิเตอร์จอดรถ', 13: 'ม้านั่ง',
    14: 'นก', 15: 'แมว', 16: 'สุนัข', 17: 'ม้า', 18: 'แกะ',
    19: 'วัว', 20: 'ช้าง', 21: 'หมี', 22: 'ม้าลาย', 23: 'ยีราฟ',
    24: 'กระเป๋าเป้', 25: 'ร่ม', 26: 'กระเป๋าถือ', 27: 'เนคไท', 28: 'กระเป๋าเดินทาง',
    29: 'จานร่อน', 30: 'สกี', 31: 'สโนว์บอร์ด', 32: 'ลูกบอลกีฬา', 33: 'ว่าว',
    34: 'ไม้เบสบอล', 35: 'ถุงมือเบสบอล', 36: 'สเก็ตบอร์ด', 37: 'กระดานโต้คลื่น', 38: 'ไม้เทนนิส',
    39: 'ขวด', 40: 'แก้วไวน์', 41: 'ถ้วย', 42: 'ส้อม', 43: 'มีด',
    44: 'ช้อน', 45: 'ชาม', 46: 'กล้วย', 47: 'แอปเปิ้ล', 48: 'แซนด์วิช',
    49: 'ส้ม', 50: 'บร็อกโคลี', 51: 'แครอท', 52: 'ฮ็อตด็อก', 53: 'พิซซ่า',
    54: 'โดนัท', 55: 'เค้ก', 56: 'เก้าอี้', 57: 'โซฟา', 58: 'ต้นไม้ในกระถาง',
    59: 'เตียง', 60: 'โต๊ะอาหาร', 61: 'โถส้วม', 62: 'ทีวี', 63: 'แล็ปท็อป',
    64: 'เมาส์', 65: 'รีโมต', 66: 'คีย์บอร์ด', 67: 'โทรศัพท์มือถือ', 68: 'ไมโครเวฟ',
    69: 'เตาอบ', 70: 'เครื่องปิ้งขนมปัง', 71: 'อ่างล้างจาน', 72: 'ตู้เย็น',
    73: 'หนังสือ', 74: 'นาฬิกา', 75: 'แจกัน', 76: 'กรรไกร', 77: 'ตุ๊กตาหมี',
    78: 'ไดร์เป่าผม', 79: 'แปรงสีฟัน'
}

# === SETTINGS ===
MODEL_PATH = "yolo11n.pt"  #Replace with model path
USB_CAMERA_INDEX = 0  #Index of the USB camera (0 for first camera)
RESOLUTION = (640, 480)
CONF_THRESHOLD = 0.3 


# === INIT YOLO WITH TRACKING ===
model = YOLO(MODEL_PATH)
labels = model.names



# === INIT CAMERA ===
cap = cv2.VideoCapture(USB_CAMERA_INDEX)
cap.set(3, RESOLUTION[0])
cap.set(4, RESOLUTION[1])

# === TRACKING STATE ===
object_presence = defaultdict(int)   # Tracks how long an object is present
object_absence = defaultdict(int)    # Tracks how long an object is missing
object_status: dict[int, bool] = {}   # int -> bool (e.g., "ID" -> True if active)

print("Running object tracker. Press Ctrl+C to stop.")
print("info: model=", MODEL_PATH, "camera index=", USB_CAMERA_INDEX, "resolution=", RESOLUTION, "confidence threshold=", CONF_THRESHOLD)

speak("เริ่มต้นระบบช่วยมอง", lang='th-TH')

id_to_name: dict[int, str] = {}  #Store object ID and Thai label 

while True:
    start_time = time.time() #for whole processing time

    ret, frame = cap.read()
    if not ret:
        print("Camera error. Exiting.")
        break


    start = time.time() #for YOLO inference time

    # Run YOLO tracking
    results = model.track(frame, persist=True, verbose=False)[0]
    detections = results.boxes
    ids = results.boxes.id
    print("YOLO inference time:", time.time() - start)
    

    # Use placeholder if IDs not available
    if ids is None:
        ids = [None] * len(detections)

    seen_ids = set()
    

    # Pjocess each detection
    for i, det in enumerate(detections):
        coords = det.xyxy.cpu().numpy().squeeze().astype(int)
        xmin,ymin,xmax,ymax =coords
        # Calculate center coordinates
        xavg = (xmax-xmin)/2
        yavg = (ymax-ymin)/2

        conf = det.conf.item()
        class_id = int(det.cls.item())
        label = labels[class_id]
        obj_id = int(ids[i]) if ids[i] is not None else None

        if conf < CONF_THRESHOLD or obj_id is None:
            continue

        seen_ids.add(obj_id)

        # Update presence counters
        object_presence[obj_id] += 1
        object_absence[obj_id] = 0

        # If seen 3 times in a row, and not yet marked as active
        if object_presence[obj_id] ==2 and not object_status.get(obj_id, False): 
            text =  f"✅ ID {obj_id} ({label}) entered view at [{xavg},{yavg}]"

            thai_lable = get_label_thai(class_id)
            id_to_name[obj_id] = thai_lable # Store Thai label for the object ID, for when it disappears.
            where_x = where_is_object(xavg)

            print(text)
            speak(f"เห็น{thai_lable} อยู่ที่{where_x}",lang='th-TH')
            object_status[obj_id] = True


    # Process objects that disappeared
    for obj_id in list(object_status.keys()):
        if obj_id not in seen_ids:
            object_absence[obj_id] += 1
            object_presence[obj_id] = 0
 
            if object_absence[obj_id] == 2 and object_status.get(obj_id, False):
                print(f"❌ ID {obj_id} left view ")
                thai_lable = id_to_name.get(obj_id, "ไม่ทราบ")
                speak(f"ไม่เห็น{thai_lable}แล้ว",lang='th-TH')
                object_status[obj_id] = False
    print("Processing time:", time.time() - start_time)

