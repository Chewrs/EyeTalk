EyeTalk v2 Prototype - README
=============================

This is the second prototype of the EyeTalk project, designed to run on a Raspberry Pi 5 with Hailo-8 AI accelerator support.
It includes a new detection and tracking algorithm, and provides voice feedback using a threaded speech on device system.

Setup Instructions
------------------

1. Clone this repository and enter the project folder:
```
   git clone https://github.com/Chewrs/EyeTalk.git
   cd Eyetalk/v2_prototype
```
2. Run the installation script to install all required packages:
```
   ./install.sh
```

3. Set up the environment variables:
```
   source setup_env.sh
```

4. Run the EyeTalk program:
```
   python3 New_alg_eyetalk.py -i rpi
```

Notes
-----
- Make sure you have raspberry pi camera installed.
- This version is optimized for Raspberry Pi 5 with the Hailo-8 accelerator.
