import PySimpleGUI as sg

#
# An Async Demonstration of a media player
# Uses button images for a super snazzy look
# See how it looks here:
# https://user-images.githubusercontent.com/13696193/43159403-45c9726e-8f50-11e8-9da0-0d272e20c579.jpg
#
def MediaPlayerGUI():
    #background = '#F0F0F0'
    # Set the backgrounds the same as the background on the buttons
    #sg.SetOptions(background_color=background, element_background_color=background)

    # Images are located in a subfolder in the Demo Media Player.py folder
    #image_pause = './ButtonGraphics/Pause.png'
    #image_restart = './ButtonGraphics/Restart.png'
    #image_next = './ButtonGraphics/Next.png'
    #image_exit = './ButtonGraphics/Exit.png'

    # A text element that will be changed to display messages in the GUI


    # define layout of the rows
    layout = [
            [sg.Text('This is the GUI Front-End for the SRT',auto_size_text=True,font=("FreeSans", 25))],
            [sg.Text(size=(15, 2), font=("Helvetica", 14), key='output')],
            [sg.Text('_'*20)],
            [sg.Text(' '*30)],
            [
                    sg.Slider(range=(-10, 10), default_value=0, size=(10, 20), orientation='vertical', font=("Helvetica", 15)),
                    sg.Text(' ' * 2),
                    sg.Slider(range=(-10, 10), default_value=0, size=(15, 20), orientation='vertical', font=("Helvetica", 15)),
                    sg.Text(' ' * 2),
                    sg.Slider(range=(-10, 10), default_value=0, size=(10, 20), orientation='vertical', font=("Helvetica", 15),pad=((100,20),(10,10)) )],
                [   sg.Text('   Velocity', font=("Helvetica", 15), size=(9, 1)),
                    sg.Text('Acceleration', font=("Helvetica", 15), size=(15, 1)),
                    sg.Text('Abs. Position', font=("Helvetica", 15), size=(7, 1))]
                ]

    # Open a form, note that context manager can't be used generally speaking for async forms
    window = sg.Window('Media File Player', layout, default_element_size=(20, 1),
            font=("Helvetica", 25))
    # Our event loop
    while(True):
        event, values = window.read(timeout=100)        # Poll every 100 ms
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break
        # If a button was pressed, display it on the GUI by updating the text element
        if event != sg.TIMEOUT_KEY:
            window['output'].update(event)

MediaPlayerGUI()
