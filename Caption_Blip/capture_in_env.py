import subprocess

output_file = "image.jpg"
subprocess.run([
    "libcamera-still",
    "-o", output_file,
    "-t", "1000"
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print(f"Image saved as {output_file}")