from picamera2 import Picamera2
import time
from PIL import Image

class CameraHandler:
    def __init__(self):
        self.picam2 = Picamera2()
        config = self.picam2.create_still_configuration(
            main={"size": (4608, 2592)},
            controls={"AfMode": 1}  # Single AF
        )
        self.picam2.configure(config)
        self.picam2.start()
        time.sleep(1)

    def capture_image(self, output_path: str):
        try:
        # 🔄 Trigger autofocus (on center by default, since no AfWindow)
            self.picam2.set_controls({
                "AfMode": 1,
                "AfTrigger": 0
            })
            time.sleep(1)
            self.picam2.capture_file(output_path)
            print(f"Image captured and saved to: {output_path}")
            print(self.picam2.camera_properties)

            # Proper resize
            img = Image.open(output_path)
            resized = img.resize((1280, 720), Image.LANCZOS)  # Use LANCZOS for high-quality downsampling
            resized.save(output_path, format='JPEG', quality=100, optimize=True)  # Explicit format
            #print("Image resized and compressed.")

        except Exception as e:
            print(f"Error capturing image: {e}")

    def close(self):
        """
        Closes the camera. It's important to call this when done with the camera.
        """
        self.picam2.stop()
        print("Camera closed.")

if __name__ == "__main__":
    # Example usage:
    camera = CameraHandler()
    try:
        # Define a path to save the image. Make sure the directory exists.
        # For demonstration, saving in the current directory.
        image_path = "/home/che/Desktop/stt_with_ai/captured_image.jpg"
        camera.capture_image(image_path)
    finally:
        camera.close()
       
