# CAER_Video_GUI
Video GUI python example for [caer](https://github.com/jasmcaus/caer), with rather simple interface which allows applying some visual effects to the video. Caer is a python library used for Computer or Machine Vision, with the power of [OpenCV](https://opencv.org/), so make sure to read everything you can in that repository.

Requirements: python3 with tkinter, caer and somewhat of a fast computer.

Run it either via IDLE or from command prompt / terminal with one of these commands:
- 'python caer_video_gui.py'
- 'python -m caer_video_gui'
- 'python3 caer_video_gui.py'
- 'python3 -m caer_video_gui'

## Functionality
- Video is displayed in external window (the smaller the video size the faster the rendering)
- Select the camera source to capture the video from (0 is usually default)
- Open and play a video file as well as loop it (use the 'Open File >>' option and either browse locally or enter a URL)
- Scale the video
- Take a screenshot of the current video frame (files will be saved in the app's folder)

- Save camera video to a video file (saved to app's folder as AVI at 20fps) - !!! CAUTION !!! THE FILE COULD POSSIBLY GET LARGE
  - This is currently set to use (*'h264') codec so check this [link](https://github.com/cisco/openh264/releases) to get the file for your OS
  - Make sure to get the correct version since on my computer it was asking for v1.8.0 while currently the latest is v2.1.1
  - On Windows, it is sufficient to copy this dll file to C:\Windows\System32 folder
  - Possibly replace the codec with (*'XVID') or (*'mp4v') - see code on line 179 or around that number
  - Suggestion: leave the extension as '.avi' regardless of the choice of codec

The following effects can be applied:
- Gamma, Hue, Saturation, Sharpen, Gaussian Blur, Posterize, Solarize and Sobel Gradient
- Edges and Emboss (which are mutually exclusive - you can only have one applied at the time)

The more effects applied the slower the frame processing.

Face Detection:
- Only applicable to camera stream
- Its functionality might be questionable on modified frames so no transformations will be applied
- Side effect seems to be dropped frames (at least on my computer):
  - Displayed video might slow down a bit
  - Saved video might speed up a bit

Tested as working in Windows 10 with python v3.6.8.

# CAER_Multi_Video_GUI
This particular version only allows playing videos from multiple sources and taking screenshots from either (no visual effects).

Requirements: the same as the above CAER_Video_GUI.

Running the app:  the same as the above CAER_Video_GUI, just change 'caer_video_gui' to 'caer_multi_video_gui'

## Functionality
- Up to 4 video windows can be opened (the smaller the video size the faster the rendering)
- Select either camera 0 or 1 or both to capture the video from (0 is usually default)
- Open and play either 1 or 2 video files as well as loop them
- Take a screenshot of the current video frame from any open window (files will be saved in the app's folder)

# CAER_Image_GUI
This is an expanded version of the app found [here](https://github.com/jasmcaus/caer/blob/master/examples/GUI/caer_gui.py). See the screenshot in the `screenshots` folder.

It additionally supports SVG and GIF files but does require, in addition to caer and matplotlib, installing the python `pyvips` package with pip as well as `pyvips libraries`, so
make sure to read the [pyvips](https://libvips.github.io/libvips/install.html) installation instructions.

Also make sure to understand that any foreign SVG files could pose a security risk, so maybe check this [SVG Sanitizer Test](http://svg.enshrined.co.uk/) page for a little bit of additional help.

Read all the comments inside the file itself.

# License
Licensed under MIT license.

# Trademarks
Any and all trademarks, either directly or indirectly mentioned, belong to their respective owners.

# Useful Resources
Check the other GUI examples in the [caer](https://github.com/jasmcaus/caer/tree/master/examples/GUI) repository as well as the [course](https://github.com/jasmcaus/opencv-course) with videos.
