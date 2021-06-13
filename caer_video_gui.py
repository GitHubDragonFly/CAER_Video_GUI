# Simple tkinter GUI app example, designed to showcase some caer features for playing video
# Should only be used as a base to create a new GUI
# It can be re-designed, controls re-grouped and code improved

# Requirements: python3, caer and somewhat fast computer

# Run it either via IDLE or from command prompt / terminal with one of these commands:
# - 'python caer_video_gui.py'
# - 'python -m caer_video_gui'
# - 'python3 caer_video_gui.py'
# - 'python3 -m caer_video_gui'

# The following are the features:
# Video is displayed in external window
# Select the camera source to capture the video from (0 is usually default)
# Open and play a video file as well as loop it  (use the 'Open File >>' option and either browse locally or enter a URL)
# Scale the video, the smaller the size the faster the rendering
# Take a screenshot of the current video frame (saved to app's folder as PNG)

# Save camera video to a video file (saved to app's folder as AVI at 20fps) - !!! CAUTION !!! THE FILE COULD POSSIBLY GET LARGE
#  - This is currently set to use (*'h264') codec so check the following link to get the file for your OS:
#  - https://github.com/cisco/openh264/releases
#  - On Windows, it is sufficient to copy this dll file to C:\Windows\System32 folder
#  - Possibly replace it with (*'XVID') or (*'mp4v') - see code on line 179 or around that number
#  - Suggestion: leave the extension as '.avi' regardless of the codec

# The following effects can be applied:
# Gamma, Hue, Saturation, Sharpen, Gaussian Blur, Posterize and Solarize
# Edges and Emboss (which are mutually exclusive - you can only have one applied at the time)
# The more effects to be applied, the slower the video rendering will be

# Tested as working in Windows 10 with python v3.6.8

import platform
import threading

from tkinter import *
from tkinter import filedialog as fd

import caer

pythonVersion = platform.python_version()
app_closing = False

class play_file_video_thread(threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)
   def run(self):
      play_file_video()

class play_camera_video_thread(threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)
   def run(self):
      play_camera_video()

def select_video_source(*args):
    global video_file
    global video_cam
    global videoSelection

    selectedSource = videoSelection.get()

    if selectedSource == 'Open File >>':
            try:
                video_file = fd.askopenfilename(filetypes=(('All files', '*.*'),('AVI files', '*.avi'),('MKV files', '*.mkv'),('MP4 files', '*.mp4'),('MPG files', '*.mpg'),('WMV files', '*.wmv')))

                if video_file != '':
                    lblFileName['text'] = video_file
                    chbSaveVideo['state'] = 'disabled'
                    start_playing_file_video()
                else:
                    videoSelection.set('None')
                    popup_menu_video['bg'] = 'green'
                    popup_menu_video['bg'] = 'lightgreen'
            except Exception as e:
                print(str(e))
    elif selectedSource != 'None':
        # [-1:] is functional for 0 to 9 indexes, use [7:] instead to cover any index (provided all names still start with 'Camera_')
        video_cam = int(selectedSource[-1:])
        lblFileName['text'] = selectedSource
        chbSaveVideo['state'] = 'normal'
        start_playing_camera_video()

def start_playing_file_video():
    try:
        thread1 = play_file_video_thread()
        thread1.setDaemon(True)
        thread1.start()
    except Exception as e:
        print('unable to start play_file_video_thread, ' + str(e))

def play_file_video():
    import caer as cr1

    global currentImage
    global close_video_window
    global checkVarLoop

    if not video_file is None:
        capture1 = None
        close_video_window = False
        popup_menu_video['state'] = 'disabled'
        popup_menu_scale['state'] = 'disabled'
        closeBtn['state'] = 'normal'
        screenshotBtn['state'] = 'normal'
        chbLoop['state'] = 'normal'

        try:
            capture1 = cr1.core.cv.VideoCapture(video_file)

            while True:
                isTrue, frame = capture1.read()

                if isTrue:
                    if scaleSelection.get() != '1.00':
                        width = int(frame.shape[1] * float(scaleSelection.get()))
                        height = int(frame.shape[0] * float(scaleSelection.get()))

                        dimensions = (width, height)

                        frame = cr1.core.cv.resize(frame, dimensions, interpolation = caer.core.cv.INTER_AREA)

                    currentImage = cr1.to_tensor(frame, cspace='bgr')
                    adjust_ghsps()
                else:
                    if checkVarLoop.get() == 1:
                        capture1.release()
                        capture1 = cr1.core.cv.VideoCapture(video_file)
                    else:
                        break

                if cr1.core.cv.waitKey(20) & 0xFF == ord('d') or app_closing or close_video_window:
                    break
        except Exception as e:
            print(str(e))

        if not app_closing:
            popup_menu_video['state'] = 'normal'
            popup_menu_scale['state'] = 'normal'
            closeBtn['state'] = 'disabled'
            screenshotBtn['state'] = 'disabled'
            checkVarLoop.set(0)
            chbLoop['state'] = 'disabled'
            videoSelection.set('None')
            lblFileName['text'] = ''
            reset_ghsps()

        capture1.release()
        cr1.core.cv.destroyAllWindows()

def start_playing_camera_video():
    try:
        thread2 = play_camera_video_thread()
        thread2.setDaemon(True)
        thread2.start()
    except Exception as e:
        print('unable to start play_camera_video_thread, ' + str(e))

def play_camera_video():
    import caer as cr2

    global currentImage
    global close_video_window
    global checkVarSaveVideo
    global video_out

    if not video_cam is None:
        capture2 = None
        close_video_window = False
        popup_menu_video['state'] = 'disabled'
        popup_menu_scale['state'] = 'disabled'
        closeBtn['state'] = 'normal'
        screenshotBtn['state'] = 'normal'

        try:
            capture2 = cr2.core.cv.VideoCapture(video_cam)

            capture2_width = int(capture2.get(cr2.core.cv.CAP_PROP_FRAME_WIDTH))
            capture2_height = int(capture2.get(cr2.core.cv.CAP_PROP_FRAME_HEIGHT))

            vw_fourcc = cr2.core.cv.VideoWriter_fourcc(*'h264') # or try using (*'XVID') or (*'mp4v')
            video_out = cr2.core.cv.VideoWriter('Camera_' + str(video_cam) + '.avi', vw_fourcc, 20.0, (capture2_width, capture2_height))

            while True:
                isTrue, frame = capture2.read()

                if isTrue:
                    if scaleSelection.get() != '1.00':
                        width = int(frame.shape[1] * float(scaleSelection.get()))
                        height = int(frame.shape[0] * float(scaleSelection.get()))

                        dimensions = (width, height)

                        frame = cr2.core.cv.resize(frame, dimensions, interpolation = caer.core.cv.INTER_AREA)
                    
                    currentImage = cr2.to_tensor(frame, cspace='bgr')
                    adjust_ghsps()
                else:
                    break

                if cr2.core.cv.waitKey(20) & 0xFF == ord('d') or app_closing or close_video_window:
                    break
        except Exception as e:
            print(str(e))

        if not app_closing:
            popup_menu_video['state'] = 'normal'
            popup_menu_scale['state'] = 'normal'
            closeBtn['state'] = 'disabled'
            screenshotBtn['state'] = 'disabled'
            videoSelection.set('None')
            lblFileName['text'] = ''
            checkVarSaveVideo.set(0)
            chbSaveVideo['state'] = 'disabled'
            reset_ghsps()

        capture2.release()
        cr2.core.cv.destroyAllWindows()

def take_screenshot():
    global take_a_screenshot
    global screenshot_count

    take_a_screenshot = True
    screenshot_count += 1

def close_video():
    global close_video_window

    close_video_window = True

def image_show(frame):
    global take_a_screenshot

    if take_a_screenshot:
        if videoSelection.get() == 'Open File >>':
            caer.core.cv.imwrite('./Video_File_Screenshot_' + str(screenshot_count) + '.png', frame)
        else:
            caer.core.cv.imwrite('./' + 'Camera_' + str(video_cam) + '_Screenshot_' + str(screenshot_count) + '.png', frame)

        take_a_screenshot = False

    if checkVarSaveVideo.get() == 1:
        video_out.write(frame)

    caer.core.cv.imshow('Video', frame)

def set_edges():
    global show_emboss

    if show_edges.get() == 1:
        sliderLowThreshold['state'] = 'normal'
        show_emboss.set(0)
    else:
        sliderLowThreshold['state'] = 'disabled'

def set_emboss():
    global show_edges

    if show_emboss.get() == 1:
        sliderEmboss['state'] = 'normal'
        show_edges.set(0)
        low_threshold.set(50)
    else:
        sliderEmboss['state'] = 'disabled'
        emboss.set(114)

def adjust_ghsps(*args):
    global transformedImage

    if not currentImage is None:
        transformedImage = currentImage

        # apply all required transformations to current frame
        
        if hue.get() != 0.0:
            transformedImage = caer.transforms.adjust_hue(currentImage, hue.get())
        
        if saturation.get() != 1.0:
            transformedImage = caer.transforms.adjust_saturation(transformedImage, saturation.get())
        
        if imgGamma.get() != 1.05:
            transformedImage = caer.transforms.adjust_gamma(transformedImage, imgGamma.get())

        if sharpen.get() != 8.9:
            sharpenKernel = caer.data.np.array([[-1, -1, -1], [-1, sharpen.get(), -1], [-1, -1, -1]])
            transformedImage = caer.core.cv.filter2D(transformedImage, -1, sharpenKernel)

        gb = gaussian_blur.get()

        if gb > 1:
            transformedImage = caer.core.cv.GaussianBlur(transformedImage, (gb + 1, gb + 1), caer.core.cv.BORDER_DEFAULT)

        if posterize.get() < 6:
            transformedImage = caer.transforms.posterize(transformedImage, posterize.get())

        if solarize.get() < 255:
            transformedImage = caer.transforms.solarize(transformedImage, solarize.get())

        if show_edges.get() == 1:
            transformedImage = caer.core.cv.Canny(transformedImage, low_threshold.get(), low_threshold.get() * 2)

        if show_emboss.get() == 1:
            embossKernel = caer.data.np.array([[0, 1, 0], [0, 0, 0], [0, -1, 0]])
            transformedImage = caer.core.cv.filter2D(transformedImage, -1, embossKernel) + emboss.get()

        image_show(transformedImage)

def reset_ghsps():
    global currentImage
    global transformedImage
    global imgGamma
    global hue
    global saturation
    global gaussian_blur
    global posterize
    global solarize
    global show_edges
    global low_threshold
    global sharpen
    global show_emboss
    global emboss

    currentImage = None
    transformedImage = None

    # reset all sliders
    imgGamma.set(1.05)
    hue.set(0.0)
    saturation.set(1.0)
    gaussian_blur.set(0)
    posterize.set(6)
    solarize.set(255)
    show_edges.set(0)
    low_threshold.set(50)
    sharpen.set(8.9)
    show_emboss.set(0)
    emboss.set(114)
    sliderEmboss['state'] = 'disabled'
    sliderLowThreshold['state'] = 'disabled'

    caer.core.cv.destroyAllWindows()

def main():
    global root
    global lblFileName
    global currentImage
    global transformedImage
    global sliderSolarize
    global imgGamma
    global hue
    global saturation
    global gaussian_blur
    global posterize
    global solarize
    global show_edges
    global sliderLowThreshold
    global low_threshold
    global sharpen
    global show_emboss
    global sliderEmboss
    global emboss
    global toolbar

    global popup_menu_image
    global videoSelection
    global scaleSelection
    global popup_menu_video
    global popup_menu_scale
    global video_file
    global video_cam
    global closeBtn
    global screenshotBtn
    global checkVarLoop
    global chbLoop
    global checkVarSaveVideo
    global chbSaveVideo
    global close_video_window
    global take_a_screenshot
    global screenshot_count

    # create our main window
    root = Tk()
    root.config(background='black')
    root.geometry('1075x102')
    root.resizable(0,0)

    # the following works for a single screen setup
    # if using a multi-screen setup then see the following link:
    # Ref: https://stackoverflow.com/questions/3129322/how-do-i-get-monitor-resolution-in-python/56913005#56913005
    screenDPI = root.winfo_fpixels('1i')
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    root.title('CAER Video GUI - Python v' + pythonVersion + '  (Screen : ' + str(screen_width) + ' x ' + str(screen_height) + '   ' + str(int(screenDPI)) + 'dpi)')

    currentImage, transformedImage = None, None

    video_file, video_cam = None, None
    take_a_screenshot = False
    screenshot_count = 0
    close_video_window = False

    # bind the 'q' keyboard key to quit
    root.bind('q', lambda event:root.destroy())

    #-----------------------------------------------------------------------

    # add a frame to hold video controls
    frame1 = Frame(root, background='black')
    frame1.pack(side=TOP, pady=3, fill=X)

    # create a label for the frame
    lblVideo = Label(frame1, text='Video', fg='yellow', bg='black', width=5, font='Helvetica 9')
    lblVideo.pack(side=LEFT, padx=5, pady=2)

    # create the video selection variable and choices
    videoSelection = StringVar()
    videoChoices = ['None', 'Open File >>', 'Camera_0', 'Camera_1', 'Camera_2', 'Camera_3']
    videoSelection.set('None')
    videoSelection.trace('w', select_video_source)

    # create the video selection popup menu
    popup_menu_video = OptionMenu(frame1, videoSelection, *videoChoices)
    popup_menu_video['width'] = 10
    popup_menu_video['bg'] = 'lightgreen'
    popup_menu_video.pack(side=LEFT, padx=2)

    # create a label for the video scaling
    lblScale = Label(frame1, text='Video Scale', fg='yellow', bg='black', font='Helvetica 9')
    lblScale.pack(side=LEFT, padx=2)

    # create the video scale selection variable and choices
    scaleSelection = StringVar()
    scaleChoices = ['2.00', '1.75', '1.50', '1.00', '0.75', '0.50', '0.25']
    scaleSelection.set('1.00')

    # create the video scale selection popup menu
    popup_menu_scale = OptionMenu(frame1, scaleSelection, *scaleChoices)
    popup_menu_scale['width'] = 3
    popup_menu_scale['font'] = 'Helvetica 10'
    popup_menu_scale['bg'] = 'lightgreen'
    popup_menu_scale.pack(side=LEFT, padx=2)

    # add Close Video button
    closeBtn = Button(frame1, text='Close Video', width=10, fg='blue', bg='lightgrey', state='disabled', relief=RAISED, command=close_video)
    closeBtn.pack(side=LEFT, padx=5)

    # add Screenshot button
    screenshotBtn = Button(frame1, text='Screenshot', width=10, fg='blue', bg='lightgrey', state='disabled', relief=RAISED, command=take_screenshot)
    screenshotBtn.pack(side=LEFT, padx=5)

    # add Loop checkbox
    checkVarLoop = IntVar()
    chbLoop = Checkbutton(frame1, text='Loop ', variable=checkVarLoop, bg='lightgrey', fg='blue', font='Helvetica 8', state='disabled')
    checkVarLoop.set(0)
    chbLoop.pack(side=LEFT, padx=5)

    # add Save Video checkbox
    checkVarSaveVideo = IntVar()
    chbSaveVideo = Checkbutton(frame1, text='Save Video ', variable=checkVarSaveVideo, bg='lightgrey', fg='blue', font='Helvetica 8', state='disabled')
    checkVarSaveVideo.set(0)
    chbSaveVideo.pack(side=LEFT, padx=5)

    # add exit button
    exitBtn = Button(frame1, text='Exit', width=7, fg='red', bg='lightgrey', relief=RAISED, command=root.destroy)
    exitBtn.pack(side=LEFT, padx=5)

    # create a label to show the name of the local image file opened by user
    lblFileName = Label(frame1, text='', fg='yellow', bg='black', font='Helvetica 10')
    lblFileName.pack(side=RIGHT, padx=10, pady=2)

    #-----------------------------------------------------------------------

    # add a frame to hold slider controls
    frame2 = Frame(root, background='black')
    frame2.pack(side=TOP, pady=5, fill=X)

    # create the image gamma slider control
    imgGamma = DoubleVar()
    sliderGamma = Scale(frame2, label='Gamma', variable=imgGamma, troughcolor='blue', from_=0.1, to=2.0, resolution=0.05, sliderlength=15, showvalue=False, orient=HORIZONTAL)
    sliderGamma.pack(side=LEFT, padx=5, pady=2)
    imgGamma.set(1.05)

    # create the image hue slider control
    hue = DoubleVar()
    sliderHue = Scale(frame2, label='Hue', variable=hue, troughcolor='blue', from_=-0.5, to=0.5, resolution=0.05, sliderlength=15, showvalue=False, orient=HORIZONTAL)
    sliderHue.pack(side=LEFT, pady=2)
    hue.set(0.0)

    # create the image saturation slider control
    saturation = DoubleVar()
    sliderSaturation = Scale(frame2, label='Saturation', variable=saturation, troughcolor='blue', from_=0.0, to=2.0, resolution=0.1, sliderlength=15, showvalue=False, orient=HORIZONTAL)
    sliderSaturation.pack(side=LEFT, padx=5, pady=2)
    saturation.set(1.0)

    # create the image sharpen slider control
    sharpen = DoubleVar()
    sliderSharpen = Scale(frame2, label='Sharpen', variable=sharpen, troughcolor='blue', from_=7.9, to=9.9, resolution=0.05, sliderlength=15, showvalue=False, orient=HORIZONTAL)
    sliderSharpen.pack(side=LEFT, pady=2)
    sharpen.set(8.9)

    # create the image Gaussian Blur slider control
    gaussian_blur = IntVar()
    sliderGaussianBlur = Scale(frame2, label='Gaussian Blur', variable=gaussian_blur, troughcolor='blue', from_=0, to=10, resolution=2, sliderlength=15, showvalue=False, orient=HORIZONTAL)
    sliderGaussianBlur.pack(side=LEFT, padx=5, pady=2)
    gaussian_blur.set(0)

    # create the image posterize slider control
    posterize = IntVar()
    sliderPosterize = Scale(frame2, label='Posterize', variable=posterize, troughcolor='blue', from_=6, to=1, resolution=1, sliderlength=15, showvalue=False, orient=HORIZONTAL)
    sliderPosterize.pack(side=LEFT, pady=2)
    posterize.set(6)

    # create the image solarize slider control
    solarize = IntVar()
    sliderSolarize = Scale(frame2, label='Solarize', variable=solarize, troughcolor='blue', from_=255, to=0, resolution=1, sliderlength=15, showvalue=False, orient=HORIZONTAL)
    sliderSolarize.pack(side=LEFT, padx=5, pady=2)
    solarize.set(255)

    # add 'Edges' checkbox
    show_edges = IntVar()
    chbShowEdges = Checkbutton(frame2, variable=show_edges, command=set_edges)
    chbShowEdges.pack(side=LEFT, anchor=S, pady=2)
    show_edges.set(0)

    # create the image edges low threshold slider control
    low_threshold = IntVar()
    sliderLowThreshold = Scale(frame2, label='Edges Thresh', variable=low_threshold, troughcolor='blue', from_=100, to=0, resolution=1, sliderlength=15, showvalue=False, orient=HORIZONTAL)
    sliderLowThreshold['state'] = 'disabled'
    sliderLowThreshold.pack(side=LEFT, padx=5, pady=2)
    low_threshold.set(50)

    # add 'Emboss' checkbox
    show_emboss = IntVar()
    chbShowEmboss = Checkbutton(frame2, variable=show_emboss, command=set_emboss)
    chbShowEmboss.pack(side=LEFT, anchor=S, pady=2)
    show_emboss.set(0)

    # create the image emboss slider control
    emboss = IntVar()
    sliderEmboss = Scale(frame2, label='Emboss Thresh', variable=emboss, troughcolor='blue', from_=128, to=99, resolution=1, sliderlength=15, showvalue=False, orient=HORIZONTAL)
    sliderEmboss['state'] = 'disabled'
    sliderEmboss.pack(side=LEFT, padx=5, pady=2)
    emboss.set(114)

    #-----------------------------------------------------------------------

    # set the minimum window size to the current size
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())

    root.mainloop()

if __name__=='__main__':
    main()
    app_closing = True
