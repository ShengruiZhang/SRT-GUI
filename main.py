#   Team 21039: Radio Telescope
#
#   Graphical User Interface
#   TODO
#   1. Input protection for coord. input
#   2. Update the Target position after an coord. is entered


import PySimpleGUI as sg
import sys
from datetime import datetime as dt

sys.path.append("~/SRT-GUI/")
import AnalogFrontEnd.AFE
import Servomotor.MotorControl as mc

#sg.theme('LightGrey5')
sg.theme_input_background_color('ghost white')
sg.theme_background_color('maroon')
sg.theme_text_element_background_color('maroon')
sg.theme_text_color('ghost white')
#sg.theme_button_color('midnight blue')


#---------------------------------------------------------------------------------------------------
#----------------------------- Window Elements Definition ------------------------------------------
menu_def = [    ['&File', ['&Open', '&Save', 'Prope&rties', 'E&xit',] ],
                ['&Edit', ['Undo', 'Paste', ['Special', 'Normal']] ],
                ['&Help', '&About...']  ]

CoordEntry = [  [sg.T('Coordinate Entry:',font=("Helvetica 14 underline bold"))],
                [sg.T('Azimuthal:',size=(15,1),font=("Helvetica 12"))],
                [sg.In(key='-IN-AZ-',size=(20,1),justification='left')],
                [sg.T('Altitudinal:',size=(15,1),font=("Helvetica 12"))],
                [sg.In(key='-IN-ALT-',size=(20,1),justification='left')],
                [sg.T('')],
                [sg.B('Enter')] ]

Parameters = [  [sg.T('System Status:',font=("Helvetica 14 underline bold"))],
                [sg.T('Current Position:',font=("Helvetica 10"),size=(15,1),justification='l'),
                    sg.T('32 N, 10 W',size=(11,1),justification='l',key='-POS-CURRENT-')],
                [sg.T('Target Position:',font=("Helvetica 10"),size=(15,1),justification='l'),
                    sg.T('59 N, 64 W',size=(11,1),justification='l',key='-POS-TGT-')],
                [sg.T('Wind Speed:',font=("Helvetica 10"),size=(15,1),justification='l'),
                    sg.T('30 m/s',size=(11,1),justification='l',key='-WIND-')],
                [sg.T('AZ Servo Voltage:',font=("Helvetica 10"),size=(15,1),justification='l'),
                    sg.T('48.00 V',size=(11,0),justification='l',key='_voltAZ_')],
                [sg.T('ALT Servo Voltage:',font=("Helvetica 10"),size=(15,1),justification='l'),
                    sg.T('48.00 V',size=(11,0),justification='l',key='_voltALT_')],
                [sg.T('')],
                [sg.B('Update',key='-UPDATE-')]
                ]

Jogging = [     [sg.T('Jogging',font=('Helvetica 14 underline bold'))],
                [sg.T('Steps in degrees',justification='l',size=(30,1))],
                [sg.B('.5',size=(3,1),use_ttk_buttons=True,key='-STEP1-'),
                    sg.B('1',size=(3,1),use_ttk_buttons=True,button_color=('black','gray'),key='-STEP2-'),
                    sg.B('5',size=(3,1),use_ttk_buttons=True,button_color=('black','gray'),key='-STEP3-'),
                    sg.B('10',size=(3,1),use_ttk_buttons=True,button_color=('black','gray'),key='-STEP4-')],
                [sg.T(''),sg.T('')],
                [sg.B('Azimuth +',size=(10,1),key='_AZ+_'), sg.B('Azimuth -',size=(10,1),key='_AZ-_')],
                [sg.B('Altitude +',size=(10,1),key='_ALT+_'), sg.B('Altitude -',size=(10,1),key='_ALT-_')]
                ]

System = [      [sg.T('System Settings',font=('Helvetica 14 underline bold'))],
                [sg.Check('Enable Telescope',size=(20,1),default=False,enable_events=True,key='-EN-SRT-')],
                [sg.Check('Enable Servomotors',size=(20,1),default=False,enable_events=True,key='-EN-SERVO-')],
                [sg.Check('Enable AnalogFrontEnd',size=(20,1),default=False,enable_events=True,key='-EN-AFE-')],
                [sg.Check('Enable Jogging',size=(20,1),default=False,enable_events=True,key='-EN-JOG-')]
                ]

data_recording = [
                [sg.B('Start Recording Data',font=("Helvetica 10")),
                    sg.B('Stop Recording Data',font=("Helvetica 10"))],
                [sg.T('Choose A Folder to Save Your Graph To:',size=(35,1),font=("Helvetica 10"))],
                [sg.T('Save Path',size=(15,1),auto_size_text=False,justification='r'),
                    sg.In('Default Folder',font=("Helvetica 10")), sg.FolderBrowse()]
                ]

output =    [   [sg.T('Radio Telescope Control Output/Log')],
                [sg.Output(size=(50,10),key='-OUTPUT-')],
                [sg.B('Clear'), sg.B('Save Log'), sg.B('Quit')]
                ]

#---------------------------------------------------------------------------------------------------
#------------------------------------ Main Window Layout -------------------------------------------

layout = [  [sg.Menu(menu_def, tearoff=True)],
            [sg.T('Student Radio Telescope Control',size=(30,1),justification='c',font=("Helvetica 25"),
                relief=sg.RELIEF_SOLID),sg.T('',font=("DejaVu 10"),size=(15,1),key='-datetime-')],
            [sg.T('')],
            [sg.B('Start Calibration',size=(15,1),font=("Helvetica 13"),key='-CALIB-'),
                sg.B('TELESCOPE STOP',size=(20,1),font=("Helvetica 20"),key='-ESTOP-'),
                sg.B('Stow Telescope',size=(15,1),font=("Helvetica 13"),key='-STOW-')],
            [sg.T('')],
            [sg.Col(CoordEntry, element_justification='c', vertical_alignment='top'),
                sg.VSep(pad=((30,30),(0,0))),
                sg.Col(Parameters, element_justification='c', vertical_alignment='top'),
                sg.VSep(pad=((30,30),(0,0))),
                sg.Col(Jogging, element_justification='c', vertical_alignment='top'),
                sg.VSep(pad=((30,30),(0,0))),
                sg.Col(System, element_justification='c', vertical_alignment='top')],
            [sg.T('')],
            [sg.Frame(layout=data_recording, title='Data Output:',
                font=("Helvetica 12"), title_color='white', relief=sg.RELIEF_RIDGE,
                background_color='maroon', element_justification='c'),
                sg.Output(size=(50,10),key='-OUTPUT-',echo_stdout_stderr=True)],
            [sg.Exit()]
            ]


# create window
window = sg.Window('Student Radio Telescope Control', layout, element_justification='c')

WindSpeed = 15

VAZ = 47.89
VALT = 46.78

JogStepAZ = 4683
JogStepALT = 929

# Serial connection to Analog Front-End Control
#AnalogControl = AFE.Init(9600)
#AFE.Activate(AnalogControl)

# Serial Connection to Servomotor
#motor_AZ = mc.Init('/dev/ttyUSB0')
#motor_ALT = mc.Init('/dev/ttyUSB0')

while True:  # Event Loop

    # check every 100 ms
    #   The first values in event is the menu bar event
    event, values = window.read(timeout=100)
    print(values)

    # update time
    time = dt.now().strftime('%Y-%m-%d   %H:%M')
    window['-datetime-'].update(time)


    if event == sg.WIN_CLOSED or event == 'Exit':
        # GUI is closed either by using 'X', or the Exit button
        break

    if event == '-EN-SRT-':
        print('Enabling Telescope Control')

    if event == '-EN-SERVO-':
        print('Enabling Servomotor Drive')

    if event == '-EN-AFE-':
        print('Enabling AnalogFrontEnd')

    if event == '-EN-JOG-':
        print('Enabling Jogging')


    if event == 'Enter':
        #TODO
        PosTarget = '32 N, 110 W'
        window['-POS-TGT-'].update(PosTarget)


    if event == '-ESTOP-':

        print("Software E-Stop is pressed")

        #mc.Stop(motor_AZ)
        #mc.Stop(motor_ALT)
        #AFE.EngageBrake(AnalogControl)


    if event == '-UPDATE-':

        # When Update button is pressed, retreive ADC value from AFE
        print("Updating System Status")

        #WindSpeed = AFE.GetWindRaw(AnalogControl)
        window['-WIND-'].update(str(WindSpeed)+" m/s")

        # Update voltge
        #VAZ = mc.GetVoltage(motor_AZ)
        #VALT = mc.GetVoltage(motor_ALT)

        window['_voltAZ_'].update(str(VAZ)+" V")
        window['_voltALT_'].update(str(VALT)+" V")


    if event == '-STEP1-':

        print("Set Jog Steps: 0.5 deg")

        JogStepAZ = 4683
        JogStepALT = 929

        window['-STEP1-'].Update(button_color=('ghost white','midnight blue'))
        window['-STEP2-'].Update(button_color=('black','gray'))
        window['-STEP3-'].Update(button_color=('black','gray'))
        window['-STEP4-'].Update(button_color=('black','gray'))

    if event == '-STEP2-':

        print("Set Jog Steps: 1 deg")

        JogStepAZ = 9365
        JogStepALT = 1857

        window['-STEP1-'].Update(button_color=('black','gray'))
        window['-STEP2-'].Update(button_color=('ghost white','midnight blue'))
        window['-STEP3-'].Update(button_color=('black','gray'))
        window['-STEP4-'].Update(button_color=('black','gray'))

    if event == '-STEP3-':

        print("Set Jog Steps: 5 deg")

        JogStepAZ = 46825
        JogStepALT = 9286

        window['-STEP1-'].Update(button_color=('black','gray'))
        window['-STEP2-'].Update(button_color=('black','gray'))
        window['-STEP3-'].Update(button_color=('ghost white','midnight blue'))
        window['-STEP4-'].Update(button_color=('black','gray'))

    if event == '-STEP4-':

        print("Set Jog Steps: 10 deg")

        JogStepAZ = 93651
        JogStepALT = 18571

        window['-STEP1-'].Update(button_color=('black','gray'))
        window['-STEP2-'].Update(button_color=('black','gray'))
        window['-STEP3-'].Update(button_color=('black','gray'))
        window['-STEP4-'].Update(button_color=('ghost white','midnight blue'))


    if event == '_AZ+_':

        print('Jogging Azimuth Clockwise')
        #mc.Jogging(motor_AZ, JogStepAZ)

    if event == '_AZ-_':

        print('Jogging Azimuth Counter-Clockwise')
        #mc.Jogging(motor_AZ, -JogStepAZ)

    if event == '_ALT+_':

        print('Jogging Altitude Clockwise')
        #mc.Jogging(motor_ALT, JogStepALT)

    if event == '_ALT-_':

        print('Jogging Altitude Counter-Clockwise')
        #mc.Jogging(motor_ALT, -JogStepALT)


# Close the Serial connection
#AFE.CloseSerial(AnalogControl)
#mc.CloseSerial(motor_AZ)

window.close()
