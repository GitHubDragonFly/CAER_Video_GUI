# Simple tkinter GUI app example, designed to showcase some caer features for playing video
# Should only be used as a base to create a new GUI
# It can be re-designed, controls re-grouped and code improved

# Requirements: python3, caer

# Run it either via IDLE or from command prompt / terminal with one of these commands:
# - 'python caer_multi_video_gui.py'
# - 'python -m caer_multi_video_gui'
# - 'python3 caer_multi_video_gui.py'
# - 'python3 -m caer_multi_video_gui'

# Up to 4 video windows can be opened
# Select either camera 0 or 1 or both to capture the video from (0 is usually default)
# Open and play either 1 or 2 video files as well as loop them
# Take a screenshot of the current video frame for any open window

# Tested as working in Windows 10 with python v3.6.8

from tkinter import *
from tkinter import filedialog as fd

import threading
import platform
from caer import __version__ as ver

class play_file_1_video_thread(threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)
   def run(self):
      play_file_1_video()

class play_file_2_video_thread(threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)
   def run(self):
      play_file_2_video()

class play_camera_0_video_thread(threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)
   def run(self):
      play_camera_0_video()

class play_camera_1_video_thread(threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)
   def run(self):
      play_camera_1_video()

app_closing = False
pythonVersion = platform.python_version()
caerVersion = ver

def select_video_1_file(*args):
    global video_file_1
    global source1Selection

    selectedSource1 = source1Selection.get()

    try:
        if selectedSource1 == 'Open File >>':
            video_file_1 = fd.askopenfilename(filetypes=(('All files', '*.*'),('AVI files', '*.avi'),('MKV files', '*.mkv'),('MP4 files', '*.mp4'),('MPG files', '*.mpg'),('WMV files', '*.wmv')))

            if video_file_1 != '':
                start_playing_file_1_video()
            else:
                source1Selection.set('None')
                popup_menu_source1['bg'] = 'green'
                popup_menu_source1['bg'] = 'lightgreen'
    except Exception as e:
        print(str(e))

def start_playing_file_1_video():
    try:
        thread1 = play_file_1_video_thread()
        thread1.setDaemon(True)
        thread1.start()
    except Exception as e:
        print('unable to start play_file_1_video_thread, ' + str(e))

def play_file_1_video():
    import caer as cr1

    global close_video_1_window
    global source1Selection
    global take_1_screenshot
    global checkVar1Loop

    if not video_file_1 is None:
        capture1 = None
        close_video_1_window = False
        popup_menu_source1['state'] = 'disabled'
        popup_menu_scale1['state'] = 'disabled'
        closeBtn1['state'] = 'normal'
        screenshotBtn1['state'] = 'normal'
        chb1Loop['state'] = 'normal'

        try:
            capture1 = cr1.core.cv.VideoCapture(video_file_1)

            while True:
                isTrue, frame = capture1.read()

                if isTrue:
                    if scale1Selection.get() != '1.00':
                        width = int(frame.shape[1] * float(scale1Selection.get()))
                        height = int(frame.shape[0] * float(scale1Selection.get()))

                        dimensions = (width, height)

                        frame = cr1.core.cv.resize(frame, dimensions, interpolation = cr1.core.cv.INTER_AREA)

                        cr1.core.cv.imshow(video_file_1, frame)
                    else:
                        cr1.core.cv.imshow(video_file_1, frame)

                    if take_1_screenshot:
                        cr1.core.cv.imwrite('./Screenshot_Video_1_' + str(screenshot1_count) + '.png', frame)
                        take_1_screenshot = False
                else:
                    if checkVar1Loop.get() == 1:
                        capture1.release()
                        capture1 = cr1.core.cv.VideoCapture(video_file_1)
                    else:
                        break

                if cr1.core.cv.waitKey(20) & 0xFF == ord('d') or app_closing or close_video_1_window:
                    break
        except Exception as e:
            print(str(e))

        if not app_closing:
            popup_menu_source1['state'] = 'normal'
            popup_menu_scale1['state'] = 'normal'
            closeBtn1['state'] = 'disabled'
            screenshotBtn1['state'] = 'disabled'
            checkVar1Loop.set(0)
            chb1Loop['state'] = 'disabled'
            source1Selection.set('None')

        capture1.release()
        cr1.core.cv.destroyAllWindows()

def select_video_2_file(*args):
    global video_file_2
    global source2Selection

    selectedSource2 = source2Selection.get()

    try:
        if selectedSource2 == 'Open File >>':
            video_file_2 = fd.askopenfilename(filetypes=(('All files', '*.*'),('AVI files', '*.avi'),('MKV files', '*.mkv'),('MP4 files', '*.mp4'),('MPG files', '*.mpg'),('WMV files', '*.wmv')))

            if video_file_2 != '':
                start_playing_file_2_video()
            else:
                source2Selection.set('None')
                popup_menu_source2['bg'] = 'green'
                popup_menu_source2['bg'] = 'lightgreen'
    except Exception as e:
        print(str(e))

def start_playing_file_2_video():
    try:
        thread2 = play_file_2_video_thread()
        thread2.setDaemon(True)
        thread2.start()
    except Exception as e:
        print('unable to start play_file_2_video_thread, ' + str(e))

def play_file_2_video():
    import caer as cr2

    global close_video_2_window
    global source2Selection
    global take_2_screenshot
    global checkVar2Loop

    if not video_file_2 is None:
        capture2 = None
        close_video_2_window = False
        popup_menu_source2['state'] = 'disabled'
        popup_menu_scale2['state'] = 'disabled'
        closeBtn2['state'] = 'normal'
        screenshotBtn2['state'] = 'normal'
        chb2Loop['state'] = 'normal'

        try:
            capture2 = cr2.core.cv.VideoCapture(video_file_2)

            while True:
                isTrue, frame = capture2.read()

                if isTrue:
                    if scale2Selection.get() != '1.00':
                        width = int(frame.shape[1] * float(scale2Selection.get()))
                        height = int(frame.shape[0] * float(scale2Selection.get()))

                        dimensions = (width, height)

                        frame = cr2.core.cv.resize(frame, dimensions, interpolation = cr2.core.cv.INTER_AREA)

                        cr2.core.cv.imshow(video_file_2, frame)
                    else:
                        cr2.core.cv.imshow(video_file_2, frame)

                    if take_2_screenshot:
                        cr2.core.cv.imwrite('./Screenshot_Video_2_' + str(screenshot2_count) + '.png', frame)
                        take_2_screenshot = False
                else:
                    if checkVar2Loop.get() == 1:
                        capture2.release()
                        capture2 = cr2.core.cv.VideoCapture(video_file_2)
                    else:
                        break

                if cr2.core.cv.waitKey(20) & 0xFF == ord('d') or app_closing or close_video_2_window:
                    break
        except Exception as e:
            print(str(e))

        if not app_closing:
            popup_menu_source2['state'] = 'normal'
            popup_menu_scale2['state'] = 'normal'
            closeBtn2['state'] = 'disabled'
            screenshotBtn2['state'] = 'disabled'
            checkVar2Loop.set(0)
            chb2Loop['state'] = 'disabled'
            source2Selection.set('None')

        capture2.release()
        cr2.core.cv.destroyAllWindows()

def select_camera_0_source(*args):
    selectedSource5 = source5Selection.get()

    try:
        if selectedSource5 == 'Camera_0':
            start_playing_camera_0_video()
    except Exception as e:
        print(str(e))

def start_playing_camera_0_video():
    try:
        thread5 = play_camera_0_video_thread()
        thread5.setDaemon(True)
        thread5.start()
    except Exception as e:
        print('unable to start play_camera_0_video_thread, ' + str(e))

def play_camera_0_video():
    import caer as cr5

    global close_video_5_window
    global source5Selection
    global take_5_screenshot

    capture5 = None
    close_video_5_window = False
    popup_menu_source5['state'] = 'disabled'
    popup_menu_scale5['state'] = 'disabled'
    closeBtn5['state'] = 'normal'
    screenshotBtn5['state'] = 'normal'

    try:
        capture5 = cr5.core.cv.VideoCapture(0)

        while True:
            isTrue, frame = capture5.read()

            if isTrue:
                if scale5Selection.get() != '1.00':
                    width = int(frame.shape[1] * float(scale5Selection.get()))
                    height = int(frame.shape[0] * float(scale5Selection.get()))

                    dimensions = (width, height)

                    frame = cr5.core.cv.resize(frame, dimensions, interpolation = cr5.core.cv.INTER_AREA)

                    cr5.core.cv.imshow('Camera_0', frame)
                else:
                    cr5.core.cv.imshow('Camera_0', frame)

                if take_5_screenshot:
                    cr5.core.cv.imwrite('./Screenshot_Camera_0_' + str(screenshot5_count) + '.png', frame)
                    take_5_screenshot = False
            else:
                break

            if cr5.core.cv.waitKey(20) & 0xFF == ord('d') or app_closing or close_video_5_window:
                break
    except Exception as e:
        print(str(e))

    if not app_closing:
        popup_menu_source5['state'] = 'normal'
        popup_menu_scale5['state'] = 'normal'
        closeBtn5['state'] = 'disabled'
        screenshotBtn5['state'] = 'disabled'
        source5Selection.set('None')

    capture5.release()
    cr5.core.cv.destroyAllWindows()

def select_camera_1_source(*args):
    selectedSource6 = source6Selection.get()

    try:
        if selectedSource6 == 'Camera_1':
            start_playing_camera_1_video()
    except Exception as e:
        print(str(e))

def start_playing_camera_1_video():
    try:
        thread6 = play_camera_1_video_thread()
        thread6.setDaemon(True)
        thread6.start()
    except Exception as e:
        print('unable to start play_camera_1_video_thread, ' + str(e))

def play_camera_1_video():
    import caer as cr6

    global close_video_6_window
    global source6Selection
    global take_6_screenshot

    capture6 = None
    close_video_6_window = False
    popup_menu_source6['state'] = 'disabled'
    popup_menu_scale6['state'] = 'disabled'
    closeBtn6['state'] = 'normal'
    screenshotBtn6['state'] = 'normal'

    try:
        capture6 = cr6.core.cv.VideoCapture(1)

        while True:
            isTrue, frame = capture6.read()

            if isTrue:
                if scale6Selection.get() != '1.00':
                    width = int(frame.shape[1] * float(scale6Selection.get()))
                    height = int(frame.shape[0] * float(scale6Selection.get()))

                    dimensions = (width, height)

                    frame = cr6.core.cv.resize(frame, dimensions, interpolation = cr6.core.cv.INTER_AREA)

                    cr6.core.cv.imshow('Camera_1', frame)
                else:
                    cr6.core.cv.imshow('Camera_1', frame)

                if take_6_screenshot:
                    cr6.core.cv.imwrite('./Screenshot_Camera_1_' + str(screenshot6_count) + '.png', frame)
                    take_6_screenshot = False
            else:
                break

            if cr6.core.cv.waitKey(20) & 0xFF == ord('d') or app_closing or close_video_6_window:
                break
    except Exception as e:
        print(str(e))

    if not app_closing:
        popup_menu_source6['state'] = 'normal'
        popup_menu_scale6['state'] = 'normal'
        closeBtn6['state'] = 'disabled'
        screenshotBtn6['state'] = 'disabled'
        source6Selection.set('None')

    capture6.release()
    cr6.core.cv.destroyAllWindows()

def close_video_1():
    global close_video_1_window

    close_video_1_window = True

def close_video_2():
    global close_video_2_window

    close_video_2_window = True

def close_video_5():
    global close_video_5_window

    close_video_5_window = True

def close_video_6():
    global close_video_6_window

    close_video_6_window = True

def take_screenshot1():
    global take_1_screenshot
    global screenshot1_count

    take_1_screenshot = True
    screenshot1_count += 1

def take_screenshot2():
    global take_2_screenshot
    global screenshot2_count

    take_2_screenshot = True
    screenshot2_count += 1

def take_screenshot5():
    global take_5_screenshot
    global screenshot5_count

    take_5_screenshot = True
    screenshot5_count += 1

def take_screenshot6():
    global take_6_screenshot
    global screenshot6_count

    take_6_screenshot = True
    screenshot6_count += 1

def main():
    global root
    global video_file_1
    global video_file_2
    global closeBtn1
    global closeBtn2
    global closeBtn5
    global closeBtn6
    global screenshotBtn1
    global screenshotBtn2
    global screenshotBtn5
    global screenshotBtn6
    global screenshot1_count
    global screenshot2_count
    global screenshot5_count
    global screenshot6_count
    global take_1_screenshot
    global take_2_screenshot
    global take_5_screenshot
    global take_6_screenshot
    global close_video_1_window
    global close_video_2_window
    global close_video_5_window
    global close_video_6_window
    global source1Selection
    global source2Selection
    global source5Selection
    global source6Selection
    global scale1Selection
    global scale2Selection
    global scale5Selection
    global scale6Selection
    global popup_menu_source1
    global popup_menu_source2
    global popup_menu_source5
    global popup_menu_source6
    global popup_menu_scale1
    global popup_menu_scale2
    global popup_menu_scale5
    global popup_menu_scale6
    global checkVar1Loop
    global checkVar2Loop
    global chb1Loop
    global chb2Loop

    # create our window
    root = Tk()
    root.config(background='navy')
    root.title('CAER Video GUI - Python v' + pythonVersion)
    root.geometry('700x205')
    root.resizable(0,0)

    # the following works for a single screen setup
    # if using a multi-screen setup then see the following link:
    # Ref: https://stackoverflow.com/questions/3129322/how-do-i-get-monitor-resolution-in-python/56913005#56913005
    screenDPI = root.winfo_fpixels('1i')
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    video_file_1, video_file_2 = None, None

    take_1_screenshot, take_2_screenshot, take_5_screenshot, take_6_screenshot = False, False, False, False
    screenshot1_count, screenshot2_count, screenshot5_count, screenshot6_count = 0, 0, 0, 0

    # bind the 'q' keyboard key to quit
    root.bind('q', lambda event:root.destroy())

    close_video_1_window, close_video_2_window, close_video_5_window, close_video_6_window = False, False, False, False

    #-----------------------------------------------------------------------

    # add a frame to hold caer version and screen attributes labels
    frame0 = Frame(root, background='navy')
    frame0.pack(side=TOP, fill=X)

    lblScreen = Label(frame0, text='Screen : ' + str(screen_width) + ' x ' + str(screen_height) + '   dpi: ' + str(int(screenDPI)), fg='lightgrey', bg='navy', font='Helvetica 9')
    lblScreen.pack(side=LEFT, padx=5, pady=5)

    lblVersion = Label(frame0, text='caer  v' + caerVersion, fg='lightgrey', bg='navy', font='Helvetica 9')
    lblVersion.pack(side=RIGHT, padx=10, pady=5)

    #-----------------------------------------------------------------------

    # add a frame to hold file_1_video controls
    frame1 = Frame(root, background='navy')
    frame1.pack(side=TOP, fill=X)

    # create a label for the video source
    lblSource1 = Label(frame1, text='Video 1', fg='yellow', bg='navy', width=6, font='Helvetica 10')
    lblSource1.pack(side=LEFT, padx=5, pady=10)

    # create the video 1 source selection variable and choices
    source1Selection = StringVar()
    source1Choices = ['None', 'Open File >>']
    source1Selection.set('None')
    source1Selection.trace('w', select_video_1_file)

    # create the video 1 source selection popup menu
    popup_menu_source1 = OptionMenu(frame1, source1Selection, *source1Choices)
    popup_menu_source1['width'] = 10
    popup_menu_source1['font'] = 'Helvetica 10'
    popup_menu_source1['bg'] = 'lightgreen'
    popup_menu_source1.pack(side=LEFT, padx=5, pady=5)

    # create the video 1 scale selection variable and choices
    scale1Selection = StringVar()
    scale1Choices = ['2.00', '1.75', '1.50', '1.00', '0.75', '0.50', '0.25']
    scale1Selection.set('1.00')

    # create a label for the video 1 scaling
    lblScale1 = Label(frame1, text='Scale', fg='yellow', bg='navy', font='Helvetica 10')
    lblScale1.pack(side=LEFT, padx=5, pady=5)

    # create the video 1 selection popup menu
    popup_menu_scale1 = OptionMenu(frame1, scale1Selection, *scale1Choices)
    popup_menu_scale1['width'] = 3
    popup_menu_scale1['font'] = 'Helvetica 10'
    popup_menu_scale1['bg'] = 'lightgreen'
    popup_menu_scale1.pack(side=LEFT, padx=1, pady=5)

    # add Close Video button
    closeBtn1 = Button(frame1, text='Close', width=10, fg='blue', bg='lightgrey', state='disabled', relief=RAISED, command=close_video_1)
    closeBtn1.pack(side=LEFT, padx=10, pady=5)

    # add Screenshot button
    screenshotBtn1 = Button(frame1, text='Screenshot', width=10, fg='blue', bg='lightgrey', state='disabled', relief=RAISED, command=take_screenshot1)
    screenshotBtn1.pack(side=LEFT, padx=1, pady=5)

    # add Loop checkbox
    checkVar1Loop = IntVar()
    chb1Loop = Checkbutton(frame1, text='Loop', variable=checkVar1Loop, bg='lightgrey', fg='blue', font='Helvetica 8', state='disabled')
    checkVar1Loop.set(0)
    chb1Loop.pack(side=LEFT, padx=10, pady=5)

    #-----------------------------------------------------------------------

    # add a frame to hold file_2_video controls
    frame2 = Frame(root, background='navy')
    frame2.pack(side=TOP, fill=X)

    # create a label for the video 2 source
    lblSource2 = Label(frame2, text='Video 2', fg='yellow', bg='navy', width=6, font='Helvetica 10')
    lblSource2.pack(side=LEFT, padx=5, pady=5)

    # create the video 2 source selection variable and choices
    source2Selection = StringVar()
    source2Choices = ['None', 'Open File >>']
    source2Selection.set('None')
    source2Selection.trace('w', select_video_2_file)

    # create the video 2 source selection popup menu
    popup_menu_source2 = OptionMenu(frame2, source2Selection, *source2Choices)
    popup_menu_source2['width'] = 10
    popup_menu_source2['font'] = 'Helvetica 10'
    popup_menu_source2['bg'] = 'lightgreen'
    popup_menu_source2.pack(side=LEFT, padx=5, pady=5)

    # create the video 2 scale selection variable and choices
    scale2Selection = StringVar()
    scale2Choices = ['2.00', '1.75', '1.50', '1.00', '0.75', '0.50', '0.25']
    scale2Selection.set('1.00')

    # create a label for the video 2 scaling
    lblScale2 = Label(frame2, text='Scale', fg='yellow', bg='navy', font='Helvetica 10')
    lblScale2.pack(side=LEFT, padx=5, pady=5)

    # create the video 2 selection popup menu
    popup_menu_scale2 = OptionMenu(frame2, scale2Selection, *scale2Choices)
    popup_menu_scale2['width'] = 3
    popup_menu_scale2['font'] = 'Helvetica 10'
    popup_menu_scale2['bg'] = 'lightgreen'
    popup_menu_scale2.pack(side=LEFT, padx=1, pady=5)

    # add Close Video button
    closeBtn2 = Button(frame2, text='Close', width=10, fg='blue', bg='lightgrey', state='disabled', relief=RAISED, command=close_video_2)
    closeBtn2.pack(side=LEFT, padx=10, pady=5)

    # add Screenshot button
    screenshotBtn2 = Button(frame2, text='Screenshot', width=10, fg='blue', bg='lightgrey', state='disabled', relief=RAISED, command=take_screenshot2)
    screenshotBtn2.pack(side=LEFT, padx=1, pady=5)

    # add Loop checkbox
    checkVar2Loop = IntVar()
    chb2Loop = Checkbutton(frame2, text='Loop', variable=checkVar2Loop, bg='lightgrey', fg='blue', font='Helvetica 8', state='disabled')
    checkVar2Loop.set(0)
    chb2Loop.pack(side=LEFT, padx=10, pady=5)

    #-----------------------------------------------------------------------

    # add a frame to hold cam_0_video controls
    frame5 = Frame(root, background='navy')
    frame5.pack(side=TOP, fill=X)

    # create a label for the cam 0 source
    lblSource5 = Label(frame5, text='Cam 0', fg='yellow', bg='navy', width=6, font='Helvetica 10')
    lblSource5.pack(side=LEFT, padx=5, pady=5)

    # create the cam 0 source selection variable and choices
    source5Selection = StringVar()
    source5Choices = ['None', 'Camera_0']
    source5Selection.set('None')
    source5Selection.trace('w', select_camera_0_source)

    # create the cam 0 source selection popup menu
    popup_menu_source5 = OptionMenu(frame5, source5Selection, *source5Choices)
    popup_menu_source5['width'] = 10
    popup_menu_source5['font'] = 'Helvetica 10'
    popup_menu_source5['bg'] = 'lightgreen'
    popup_menu_source5.pack(side=LEFT, padx=5, pady=5)

    # create the cam 0 scale selection variable and choices
    scale5Selection = StringVar()
    scale5Choices = ['2.00', '1.75', '1.50', '1.00', '0.75', '0.50', '0.25']
    scale5Selection.set('1.00')

    # create a label for the cam 0 scaling
    lblScale5 = Label(frame5, text='Scale', fg='yellow', bg='navy', font='Helvetica 10')
    lblScale5.pack(side=LEFT, padx=5, pady=5)

    # create the cam 0 selection popup menu
    popup_menu_scale5 = OptionMenu(frame5, scale5Selection, *scale5Choices)
    popup_menu_scale5['width'] = 3
    popup_menu_scale5['font'] = 'Helvetica 10'
    popup_menu_scale5['bg'] = 'lightgreen'
    popup_menu_scale5.pack(side=LEFT, padx=1, pady=5)

    # add Close Video button
    closeBtn5 = Button(frame5, text='Close', width=10, fg='blue', bg='lightgrey', state='disabled', relief=RAISED, command=close_video_5)
    closeBtn5.pack(side=LEFT, padx=10, pady=5)

    # add Screenshot button
    screenshotBtn5 = Button(frame5, text='Screenshot', width=10, fg='blue', bg='lightgrey', state='disabled', relief=RAISED, command=take_screenshot5)
    screenshotBtn5.pack(side=LEFT, padx=1, pady=5)

    #-----------------------------------------------------------------------

    # add a frame to hold cam_1_video controls
    frame6 = Frame(root, background='navy')
    frame6.pack(side=TOP, fill=X)

    # create a label for the cam 0 source
    lblSource6 = Label(frame6, text='Cam 1', fg='yellow', bg='navy', width=6, font='Helvetica 10')
    lblSource6.pack(side=LEFT, padx=5, pady=5)

    # create the cam 1 source selection variable and choices
    source6Selection = StringVar()
    source6Choices = ['None', 'Camera_1']
    source6Selection.set('None')
    source6Selection.trace('w', select_camera_1_source)

    # create the cam 1 source selection popup menu
    popup_menu_source6 = OptionMenu(frame6, source6Selection, *source6Choices)
    popup_menu_source6['width'] = 10
    popup_menu_source6['font'] = 'Helvetica 10'
    popup_menu_source6['bg'] = 'lightgreen'
    popup_menu_source6.pack(side=LEFT, padx=5, pady=5)

    # create the cam 0 scale selection variable and choices
    scale6Selection = StringVar()
    scale6Choices = ['2.00', '1.75', '1.50', '1.00', '0.75', '0.50', '0.25']
    scale6Selection.set('1.00')

    # create a label for the cam 0 scaling
    lblScale6 = Label(frame6, text='Scale', fg='yellow', bg='navy', font='Helvetica 10')
    lblScale6.pack(side=LEFT, padx=5, pady=5)

    # create the cam 0 selection popup menu
    popup_menu_scale6 = OptionMenu(frame6, scale6Selection, *scale6Choices)
    popup_menu_scale6['width'] = 3
    popup_menu_scale6['font'] = 'Helvetica 10'
    popup_menu_scale6['bg'] = 'lightgreen'
    popup_menu_scale6.pack(side=LEFT, padx=1, pady=5)

    # add Close Video button
    closeBtn6 = Button(frame6, text='Close', width=10, fg='blue', bg='lightgrey', state='disabled', relief=RAISED, command=close_video_6)
    closeBtn6.pack(side=LEFT, padx=10, pady=5)

    # add Screenshot button
    screenshotBtn6 = Button(frame6, text='Screenshot', width=10, fg='blue', bg='lightgrey', state='disabled', relief=RAISED, command=take_screenshot6)
    screenshotBtn6.pack(side=LEFT, padx=1, pady=5)

    #-----------------------------------------------------------------------

    # add Exit button
    exitBtn = Button(frame6, text='Exit', width=10, fg='red', bg='lightgrey', relief=RAISED, command=root.destroy)
    exitBtn.pack(side=RIGHT, padx=10, pady=5)

    #-----------------------------------------------------------------------

    # set the minimum window size to the current size
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())

    root.mainloop()

if __name__=='__main__':
    main()
    app_closing = True
