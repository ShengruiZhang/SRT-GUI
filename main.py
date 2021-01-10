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


# ------ Menu Definition ------ #
menu_def = [    ['&File', ['&Open', '&Save', 'Prope&rties', 'E&xit',] ],
                ['&Edit', ['Undo', 'Paste', ['Special', 'Normal']] ],
                ['&Help', '&About...']  ]

#   Making the background Gray for debugging
CoordEntry = [  [sg.T('Coordinate Entry:',font=("Helvetica 14 underline bold"),background_color='gray')],
                [sg.T('Altitudinal:',size=(15,1),font=("Helvetica 12"),background_color='gray')],
                [sg.In(key='-IN-ALT-',size=(20,1),justification='left',background_color='gray')],
                [sg.T('Azimuthal:',size=(15,1),font=("Helvetica 12"),background_color='gray')],
                [sg.In(key='-IN-AZ-',size=(20,1),justification='left',background_color='gray')],
                [sg.T('',background_color='gray')],
                [sg.B('Enter')] ]

#   Making the background Black for debugging
Parameters = [  [sg.T('Parameters:',font=("Helvetica 14 underline bold"),background_color='black')],
                [sg.T('Current Position:',font=("Helvetica 10"),background_color='black')],
                [sg.T('32 degree N, 10 degree W',font=("Helvetica 10"),background_color='black')],
                [sg.T('Target Position:',font=("Helvetica 10"),background_color='black')],
                [sg.T('59 degree N, 64 degree W',key='-POS-TGT-',background_color='black')],
                [sg.T('Wind Speed:',font=("Helvetica 10"),background_color='black',)],
                [sg.T('2 m/s',size=(10,1),justification='l',background_color='black',key='-WIND-')],
                [sg.B('Update',key='-UPDATE-')]
                ]

Jogging = [     [sg.T('Jogging',font=('Helvetica 14 underline bold'),background_color='blue')],
                [sg.B('1 degree')],
                [sg.B('Azimuth +',size=(10,1),key='_AZ+_'), sg.B('Azimuth -',size=(10,1),key='_AZ-_')],
                [sg.B('Altitude +',size=(10,1),key='_ALT+_'), sg.B('Altitude -',size=(10,1),key='_ALT-_')]
                ]

motor_status_az = [
                #[sg.T('Azimuthal Motor Status:',font=("Helvetica 11 underline bold")),sg.T('        ')],
                [sg.T('Azimuthal Motor Status:',font=("Helvetica 11 underline bold"))],
                [sg.T('Voltage:',font=("Helvetica 10")), sg.T(key='_voltAZ_',size=(10,1),justification='l')],
                [sg.T('Temperature:',font=("Helvetica 10"))],
                ]

motor_status_alt = [
                #[sg.T('Altitudinal Motor Status:',font=("Helvetica 11 underline bold")),sg.T('        ')],
                [sg.T('Altitudinal Motor Status:',font=("Helvetica 11 underline bold"))],
                [sg.T('Voltage:',font=("Helvetica 10")), sg.T(key='_voltALT_',size=(10,1),justification='l')],
                [sg.T('Temperature:',font=("Helvetica 10"))],
                ]

data_recording = [
                [sg.B('Start Recording Data',font=("Helvetica 10")),
                    sg.B('Stop Recording Data',font=("Helvetica 10"))],
                [sg.T('Choose A Folder to Save Your Graph To:',size=(35,1),font=("Helvetica 10"))],
                [sg.T('Save Path',size=(15,1),auto_size_text=False,justification='r'),
                    sg.In('Default Folder',font=("Helvetica 10")), sg.FolderBrowse()]
                ]
# layout
layout = [  [sg.Menu(menu_def, tearoff=True)],
            [sg.T('Student Radio Telescope Control',size=(30,1),justification='c',font=("Helvetica 25"),
                relief=sg.RELIEF_GROOVE)],
            #[sg.T(" ")],
            [sg.T('',font=("DejaVu 10"),size=(15,1),key='-datetime-')],
            [sg.B('Start Calibration',size=(15,1),font=("Helvetica 13"),key='-CALIB-'),
                sg.B('TELESCOPE STOP',size=(20,1),font=("Helvetica 20"),key='-ESTOP-'),
                sg.B('Stow Telescope',size=(15,1),font=("Helvetica 13"),key='-STOW-')],
            [sg.T(" ")],
            [sg.Col(CoordEntry, element_justification='c', vertical_alignment='top'),
                sg.VSep(pad=((30,30),(0,0))),
                sg.Col(Parameters, element_justification='c', vertical_alignment='top'),
                sg.VSep(pad=((30,30),(0,0))),
                sg.Col(Jogging, element_justification='c', vertical_alignment='top')],
            [sg.T(" ")],
            [sg.Col(motor_status_az, element_justification = 'l'),
                sg.VSep(),
                sg.Col(motor_status_alt, element_justification='l')],
            #[sg.T(" ")],
            [sg.Frame(layout=data_recording, title='Data Output:',
                font=("Helvetica 12"), title_color='white', relief=sg.RELIEF_RIDGE,
                background_color='maroon', element_justification='c')],
            [sg.Exit()]
            ]

# create window
window = sg.Window('Student Radio Telescope Control', layout, element_justification='c')

WindSpeed = -99
WindSpeedstr = str(WindSpeed) + ' m/s'

# Serial connection to Analog Front-End Control
#AnalogControl = AFE.Init(9600)
#AFE.Activate(AnalogControl)

# Serial Connection to Servomotor
#motor_AZ = mc.Init('/dev/ttyUSB0')
#motor_ALT = mc.Init('/dev/ttyUSB0')

while True:  # Event Loop

    # check every 100 ms
    event, values = window.read(timeout=100)

    # update time
    time = dt.now().strftime('%Y-%m-%d   %H:%M')
    window['-datetime-'].update(time)

    #print(event, values)

    if event == sg.WIN_CLOSED or event == 'Exit':
        # GUI is closed either by using 'X', or the Exit button
        break

    if event == 'Enter':

        #TODO
        window['-POS-TGT-'].update(9999)

    if event == '-ESTOP-':
        print("Software E-Stop is pressed")

        mc.Stop(motor_AZ)
        #mc.Stop(motor_ALT)
        AFE.ReleaseBrake(AnalogControl)

    if event == '-UPDATE-':
        # When Update is pressed, retreive ADC value from AFE
        print('Manually update parameters')

        #WindSpeed = AFE.GetWindRaw(AnalogControl)
        window['-WIND-'].update(value=WindSpeed)

        # TODO Update voltge
        _VAZ_ = mc.GetVoltage(motor_AZ)
        #_VALT_ = mc.GetVoltage(motor_ALT)

        window['_voltAZ_'].update(value=_VAZ_)
        #window['_voltALT_'].update(value=_VALT_)

    if event == '_AZ+_':
        print('Jog AZ +')
        mc.Jogging(motor_AZ, 0)

    if event == '_AZ-_':
        print('Jog AZ -')
        mc.Jogging(motor_AZ, 1)

    if event == '_ALT+_':
        print('Jog ALT +')
        mc.Jogging(motor_AZ, 0)

    if event == '_ALT-_':
        print('Jog ALT -')
        mc.Jogging(motor_AZ, 1)


# Close the Serial connection
#AFE.CloseSerial(AnalogControl)
#mc.CloseSerial(motor_AZ)

window.close()
