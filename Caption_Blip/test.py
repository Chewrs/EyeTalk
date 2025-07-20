# main.py (your venv project)
import subprocess

subprocess.run(["python3", "camera_capture.py"])
print("Image captured from outside env")