#   Team 21039: Radio Telescope
#
#   Graphical User Interface
#   TODO
#   1. Input protection for coord. input
#   2. Update the Target Position after an coord. is entered
#   3. [Verified]Add Restart button 
#   4. [fixed, not tested]Attach zeroing to calibration
#   5. [Verified]Swap alt jogging direction
#   6. [Need work]Set SW limit switch
#   7. figure out how to update dial
#   8. integrate alt/az dial
#   9. [Verified]Implement Stow button
#   10. Check main additions
#   11. Change coord entry to Celestial
#   12. attach anemometer
#   13. attach brake to jogging
#   14. [Verified]fix stop indexerror
#   15. [Verified]disabled absPos logging, need to reduce file size


from time import sleep
import PySimpleGUI as sg
import Dials.Dial_AZ as daz
import Dials.Dial_ALT as dalt
from datetime import datetime as dt

import sys
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
                [sg.T('Current Position:',font=("Helvetica 10"),size=(16,1),justification='l'),
                    sg.T('32 N, 10 W',size=(11,1),justification='l',key='-POS-CURRENT-')],

                [sg.T('Target Position:',font=("Helvetica 10"),size=(16,1),justification='l'),
                    sg.T('59 N, 64 W',size=(11,1),justification='l',key='-POS-TGT-')],

                [sg.T('Wind Speed:',font=("Helvetica 10"),size=(16,1),justification='l'),
                    sg.T('30 m/s',size=(11,1),justification='l',key='-WIND-')],

                [sg.T('AZ Servo Voltage:',font=("Helvetica 10"),size=(16,1),justification='l'),
                    sg.T('48.00 V',size=(11,0),justification='l',key='-voltAZ-')],

                [sg.T('ALT Servo Voltage:',font=("Helvetica 10"),size=(16,1),justification='l'),
                    sg.T('48.00 V',size=(11,0),justification='l',key='-voltALT-')],

                [sg.T('')],
                [sg.B('Update',key='-UPDATE-')]
                ]

Jogging = [     [sg.T('Jogging',font=('Helvetica 14 underline bold'))],
                [sg.T('Steps in degrees',justification='l',size=(30,1))],

                [sg.B('.5',size=(3,1),use_ttk_buttons=True,disabled=True,key='-STEP1-'),
                    sg.B('1',size=(3,1),use_ttk_buttons=True,disabled=True,button_color=('black','gray'),key='-STEP2-'),
                    sg.B('5',size=(3,1),use_ttk_buttons=True,disabled=True,button_color=('black','gray'),key='-STEP3-'),
                    sg.B('10',size=(3,1),use_ttk_buttons=True,disabled=True,button_color=('black','gray'),key='-STEP4-')],

                [sg.T(''),sg.T('')],
                [sg.B('Azimuth +',size=(10,1),disabled=True,key='_AZ+_'),
                    sg.B('Azimuth -',size=(10,1),disabled=True,key='_AZ-_')],
                [sg.B('Altitude +',size=(10,1),disabled=True,key='_ALT+_'),
                    sg.B('Altitude -',size=(10,1),disabled=True,key='_ALT-_')]
                ]

System = [      [sg.T('System Settings',font=('Helvetica 14 underline bold'))],

                [sg.Check('Enable Telescope',size=(20,1),default=False,
                    enable_events=True,key='-EN-SRT-')],

                [sg.Check('Enable Servomotors',size=(20,1),default=False,
                    enable_events=True,key='-EN-SERVO-')],

                [sg.Check('Enable AnalogFrontEnd',size=(20,1),default=False,
                    enable_events=True,key='-EN-AFE-')],

                [sg.Check('Enable Jogging',size=(20,1),default=False,
                    enable_events=True,key='-EN-JOG-')],

                [sg.B('Home AZ',size=(9,1),key='-HOME-AZ-'),sg.B('Home ALT',size=(9,1),key='-HOME-ALT-')],

                [sg.B('[DEBUG]Restart',key='-RESTART-')]
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
#------------------------------------ Main Window layout -------------------------------------------

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
                #sg.Output(size=(50,10),key='-OUTPUT-',echo_stdout_stderr=True)],
                ],

            [sg.Exit()]
            ]

layout_output = [ [sg.Output(size=(90,50),key='-OUT2-',echo_stdout_stderr=True)]  ]


#---------------------------------------------------------------------------------------------------
#------------------------------------ Creating Window ----------------------------------------------
window = sg.Window('Student Radio Telescope Control', layout, element_justification='c')
Output2 = sg.Window('Student Radio Telescope Control Output', layout_output, finalize=True)


#---------------------------------------------------------------------------------------------------
#------------------------------------ System Init --------------------------------------------------

# FOR TESTING, making up numbers here
WindSpeed = 55

VAZ = 00.00
VALT = 00.00

azDial = daz.AZ()
altDial = dalt.ALT()

window.move(200,250)
azDial.Dial.move(1300,50)
altDial.Dial.move(1300,700)
Output2.move(2000,50)

# Serial connection to Analog Front-End Control
#AnalogControl = AFE.Init(9600)
#AFE.Activate(AnalogControl)


# Abs Position of Servomotors
AbsAZ = 0
AbsALT = 0
absPosTimer = 0

# GUI Status bits
#   bit7 - Stowed
#   bit6 - Calibrated
#   bit5 - ALT homed
#   bit4 - AZ homed
#   bit3 - Jogging Enabled
#   bit2 - Servomotor ALT Enabled
#   bit1 - Servomotor AZ Enabled
#   bit0 - GUI opened
GUIstatus = 0b00000000

# Is there a better way doing this?
# Using class here so that modules can be re-used
class GUI():

    def JogDisable():

        window['_AZ+_'].update(disabled=True)
        window['_AZ-_'].update(disabled=True)
        window['_ALT+_'].update(disabled=True)
        window['_ALT-_'].update(disabled=True)
        window['-STEP1-'].update(disabled=True)
        window['-STEP2-'].update(disabled=True)
        window['-STEP3-'].update(disabled=True)
        window['-STEP4-'].update(disabled=True)


    def JogEnable():

        window['_AZ+_'].update(disabled=False)
        window['_AZ-_'].update(disabled=False)
        window['_ALT+_'].update(disabled=False)
        window['_ALT-_'].update(disabled=False)
        window['-STEP1-'].update(disabled=False)
        window['-STEP2-'].update(disabled=False)
        window['-STEP3-'].update(disabled=False)
        window['-STEP4-'].update(disabled=False)


#---------------------------------------------------------------------------------------------------
#------------------------------------ GUI Event Loop -----------------------------------------------
while True:

    # check every 100 ms
    #   The first values in event is the menu bar event
    event, values = window.read(timeout=100)

    # update time
    time = dt.now().strftime('%Y-%m-%d   %H:%M')
    window['-datetime-'].update(time)


    if event == sg.WIN_CLOSED or event == 'Exit':
        # GUI is closed either by using 'X', or the Exit button
        break

    if event == '-EN-SRT-' and values['-EN-SRT-'] == True:
        print('Enabling Telescope Control')
        #TODO

    if event == '-EN-SRT-' and values['-EN-SRT-'] == False:
        print('Disabling Telescope Control')
        #TODO

    if event == '-EN-SERVO-' and values['-EN-SERVO-'] == True:

        print('Enabling Servomotor Drive')

        try:
            Servo_AZ = mc.Init('/dev/ttyUSB0')
            GUIstatus |= 0b0010
            print('Servomotor AZ enabled')

        except Exception as e:
            print('Error: Cannot open serial port for AZ servo.')
            print(str(e))
            print('Error: Cannot enable AZ servo.')

        try:
            Servo_ALT = mc.Init('/dev/ttyUSB1')
            GUIstatus |= 0b0100
            print('Servomotor ALT enabled')

        except Exception as e:
            print('Error: Cannot open serial port for ALT servo.')
            print(str(e))
            print('Error: Cannot enable ALT servomotor.')

        if (GUIstatus & 0b0110) == 0:
            window['-EN-SERVO-'].update(value=False)

    if event == '-EN-SERVO-' and values['-EN-SERVO-'] == False:

        print('Disabling Servomotor Drive')

        GUI.JogDisable()

        window['-EN-JOG-'].update(value=False)

        if (GUIstatus & 0b0010) == 0b0010:
            mc.CloseSerial(Servo_AZ)

        if (GUIstatus & 0b0100) == 0b0100:
            mc.CloseSerial(Servo_ALT)

        GUIstatus &= 0b1001


    if event == '-EN-AFE-':
        print('Enabling AnalogFrontEnd')
        #TODO


    # Is there a better way to do this?
    if event == '-EN-JOG-' and values['-EN-JOG-'] == True:

        print('Enabling Jogging')

        JogStepAZ = 4683
        JogStepALT = 929

        if (GUIstatus & 0b0110) != 0b0110:
            print('Jogging Disabled: Servo motors are not enabled.')
            window['-EN-JOG-'].update(value=False)

        else:
            GUI.JogEnable()

        GUIstatus |= 0b1000

    if event == '-EN-JOG-' and values['-EN-JOG-'] == False:

        print('Disabling Jogging')

        GUI.JogDisable()

        GUIstatus &= 0b0111


    if event == 'Enter':
        #TODO
        PosTarget = '32 N, 110 W'
        window['-POS-TGT-'].update(PosTarget)


    if event == '-ESTOP-':

        print("Software E-Stop is pressed")

        if (GUIstatus & 0b0010) == 0b0010:
            mc.Stop(Servo_AZ)

        if (GUIstatus & 0b0100) == 0b0100:
            mc.Stop(Servo_ALT)

        if (GUIstatus & 0b0110) == 0b0000:
            print('No servo motors are enabled.')

        #TODO, need to check how brake engages
        #AFE.EngageBrake(AnalogControl)


    if event == '-UPDATE-':

        # When Update button is pressed, retreive ADC value from AFE
        print("Updating System Status")

        #WindSpeed = AFE.GetWindRaw(AnalogControl)
        window['-WIND-'].update(str(WindSpeed)+" m/s")

        if (GUIstatus & 0b0010) == 0b0010:
            VAZ = mc.GetVoltage(Servo_AZ)

        if (GUIstatus & 0b0100) == 0b0100:
            VALT = mc.GetVoltage(Servo_ALT)

        if (GUIstatus & 0b0110) == 0b0000:
            print('No servomotors are enabled.')

        window['-voltAZ-'].update(str(VAZ)+" V")
        window['-voltALT-'].update(str(VALT)+" V")


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
        mc.Jogging(Servo_AZ, JogStepAZ, 2, 5)

    if event == '_AZ-_':

        print('Jogging Azimuth Counter-Clockwise')
        mc.Jogging(Servo_AZ, -JogStepAZ, 2, 5)

    if event == '_ALT+_':

        print('Jogging Altitude Positive')
        mc.Jogging(Servo_ALT, -JogStepALT, 2, 2)

    if event == '_ALT-_':

        print('Jogging Altitude Negative')
        mc.Jogging(Servo_ALT, JogStepALT, 2, 2)


    # ------------------!!! Place Holder as written, need future work !!!----------------
    if event == '-CALIB-'and (GUIstatus & 0b0110) == 0b0110:

        print('Homing AZ and ALT')
        print(mc.Zero(Servo_AZ))
        print(mc.Zero(Servo_ALT))
        GUIstatus |= 0b00110000


    if event == '-HOME-AZ-' and (GUIstatus & 0b0010) == 0b0010:

        print('Setting current position as AZ home')
        print(mc.Zero(Servo_AZ))
        AbsAZ = 0
        GUIstatus |= 0b00010000

    if event == '-HOME-ALT-' and (GUIstatus & 0b0100) == 0b0100:

        print('Setting current position as ALT home')
        print(mc.Zero(Servo_ALT))
        AbsALT = 0
        GUIstatus |= 0b00100000


    if event == '-STOW-' and (GUIstatus & 0b10000110) == 0b00000110:

        mc.Stow(Servo_AZ, 0, 2, 3)
        mc.Stow(Servo_ALT, 0, 1, 2)
        GUIstatus |= 0b10000000


    if event == '-RESTART-' and (GUIstatus & 0b0110) == 0b0110:

        mc.Restart(Servo_AZ)
        mc.Restart(Servo_ALT)


    # Poll Abs Position, and update dials
    if (GUIstatus & 0b0010) == 0b0010:

        AbsAZ = mc.LimitAZ(Servo_AZ)
        azDial.Update(round((AbsAZ/(-9365)), 1))

    if (GUIstatus & 0b0100) == 0b0100:

        AbsALT = mc.LimitALT_zenith(Servo_ALT)
        altDial.Update(round((AbsALT/(-1857)) + 90, 1))


    # if pos is zero, set the HOMED bit
    if AbsAZ == 0:
        GUIstatus |= 0b00010000
    else:
        GUIstatus &= 0b01101111

    if AbsALT == 0:
        GUIstatus |= 0b00100000
    else:
        GUIstatus &= 0b01011111


    # Software limit switch
    absPosTimer += 1

    # Save absolute Position externally every 2s
    if absPosTimer == 20:

        with open('absPos.dat', 'a') as absPos:
            absPos.writelines( dt.now().strftime('%Y-%m-%d %H:%M:%S\n') )
            absPos.writelines( str(AbsAZ) + '\n' )
            absPos.writelines( str(AbsALT) + '\n' + '\n' )

        absPosTimer = 0


# Close the Serial connection
#AFE.CloseSerial(AnalogControl)

# Dump some log
with open('gui.log', 'a') as log:

    print('Saving logs before exiting')

    log.writelines( dt.now().strftime('%Y-%m-%d %H:%M:%S\n') )
    log.writelines( str(event) + '\n' )

    try:
        for key in values:
            log.writelines( str(key) + ' : ' + str(values[key]) + '\n')

    except TypeError as te:
        log.writelines('Window closed by X \n')
        print('Error message: ', te)
        print('Please use Exit button to close GUI.')

    log.writelines( 'Last GUIstatus: ' + str(bin(GUIstatus)) + '\n' )
    log.writelines( 'Last AZ Position: ' + str(AbsAZ) + '\n' )
    log.writelines( 'Last ALT Position: ' + str(AbsALT) + '\n' )

    log.writelines(';GUI log ends here\n\n\n')

window.close()
