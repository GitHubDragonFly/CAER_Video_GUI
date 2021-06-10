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
- Take a screenshot of the current video frame
- Scale the video

The following effects can be applied:
- Gamma, Hue, Saturation, Sharpen, Gaussian Blur, Posterize and Solarize
- Edges and Emboss (which are mutually exclusive - you can only have one applied at the time)

Tested as working in Windows 10 with python v3.6.8.

# CAER_Multi_Video_GUI
This particular version only allows playing videos from multiple sources and taking screenshots from either (no visual effects).

Requirements: the same as the above CAER_Video_GUI.

Running the app:  the same as the above CAER_Video_GUI, just change 'caer_video_gui' to 'caer_multi_video_gui'

## Functionality
- Up to 4 video windows can be opened (the smaller the video size the faster the rendering)
- Select either camera 0 or 1 or both to capture the video from (0 is usually default)
- Open and play either 1 or 2 video files as well as loop them
- Take a screenshot of the current video frame from any open window

# License
Licensed under MIT license.

# Trademarks
Any and all trademarks, either directly or indirectly mentioned, belong to their respective owners.

# Useful Resources
Check the other GUI examples in the [caer](https://github.com/jasmcaus/caer/tree/master/examples/GUI) repository as well as the [course](https://github.com/jasmcaus/opencv-course) with videos.
