#   Team 21039: Radio Telescope
#
#   Graphical User Interface
#   TODO
#   1. [Verified]Input protection for coord. input
#   2. [Verified]Update the Target Position after an coord. is entered
#   3. [Verified]Add Restart button 
#   4. [Verified]Attach zeroing to calibration
#   5. [Verified]Swap alt jogging direction
#   6. [Verified]Set SW limit switch
#   7. [Verified]figure out how to update dial
#   8. [Verified]integrate alt/az dial
#   9. [Verified]Implement Stow button
#   10. [Verified]Check main additions
#   11. [Obsoleted]Change coord entry to Celestial
#   12. [Added, Need test]attach anemometer
#   13. attach brake to jogging
#   14. [Verified]fix stop indexerror
#   15. [Verified]disabled absPos logging, need to reduce file size


from time import sleep
import PySimpleGUI as sg
import Dials.Dial_AZ as daz
import Dials.Dial_ALT as dalt
import AnalogFrontEnd.AFE as afe
from datetime import datetime as dt

import sys
sys.path.append("~/SRT-GUI/")
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
                [sg.T('Azimuthal:',size=(15,1),font=("Helvetica 12")), sg.T(size=(12,1),key='-OUT-AZ-')],
                [sg.Input(key='-IN-AZ-',size=(20,1),justification='left')],
                [sg.T('Altitudinal:',size=(15,1),font=("Helvetica 12")), sg.T(size=(12,1),key='-OUT-ALT-')],
                [sg.Input(key='-IN-ALT-',size=(20,1),justification='left')],
                [sg.T('')],
                [sg.B('Read')],
                [sg.T('')],
                [sg.T('AZ range: 0\N{DEGREE SIGN} ~ +360\N{DEGREE SIGN}',font=("OpenSans 15"),justification='l')],
                [sg.T('ALT range: +13\N{DEGREE SIGN} ~ +130\N{DEGREE SIGN}',font=("OpenSans 15"),justification='l')]
                ]

Parameters = [  [sg.T('System Status:',font=("Helvetica 14 underline bold"))],

                [sg.T('Current AZ:',font=("Helvetica 10"),size=(16,1),justification='l'),
                    sg.T('N/A\N{DEGREE SIGN}',size=(7,1),justification='l',key='-POS-CURR-AZ-')],
                [sg.T('Current ALT:',font=("Helvetica 10"),size=(16,1),justification='l'),
                    sg.T('N/A\N{DEGREE SIGN}',size=(7,1),justification='l',key='-POS-CURR-ALT-')],

                [sg.T('Target AZ:',font=("Helvetica 10"),size=(16,1),justification='l'),
                    sg.T('N/A\N{DEGREE SIGN}',size=(7,1),justification='l',key='-POS-TGT-AZ-')],
                [sg.T('Target ALT:',font=("Helvetica 10"),size=(16,1),justification='l'),
                    sg.T('N/A\N{DEGREE SIGN}',size=(7,1),justification='l',key='-POS-TGT-ALT-')],

                [sg.T('Wind Speed:',font=("Helvetica 10"),size=(16,1),justification='l'),
                    sg.T('N/A',size=(7,1),justification='l',key='-WIND-')],

                [sg.T('AZ Servo Voltage:',font=("Helvetica 10"),size=(16,1),justification='l'),
                    sg.T('N/A',size=(7,1),justification='l',key='-voltAZ-')],

                [sg.T('ALT Servo Voltage:',font=("Helvetica 10"),size=(16,1),justification='l'),
                    sg.T('N/A',size=(7,1),justification='l',key='-voltALT-')],

                [sg.T('')],
                [sg.T('',font=("OpenSans 12 italic"),size=(30,1),justification='c',key='-SYS-')],
                [sg.T('',font=("OpenSans 12 italic"),size=(30,1),justification='c',key='-SYS2-')]
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
                    enable_events=True,disabled=False,key='-EN-SRT-')],

                [sg.Check('Enable Servomotors',size=(20,1),default=False,
                    enable_events=True,disabled=True,key='-EN-SERVO-')],

                [sg.Check('Enable AnalogFrontEnd',size=(20,1),default=False,
                    enable_events=True,disabled=True,key='-EN-AFE-')],

                [sg.Check('Enable Jogging',size=(20,1),default=False,
                    enable_events=True,disabled=True,key='-EN-JOG-')],

                [sg.Check('Advance Features',size=(20,1),default=False,
                    enable_events=True,disabled=True,key='-EN-ADV-')],

                [sg.T('')],
                [sg.B('Home AZ',size=(9,1),key='-HOME-AZ-',disabled=True,visible=False),
                    sg.B('Home ALT',size=(9,1),key='-HOME-ALT-',disabled=True,visible=False)],

                [sg.B('Restart',size=(9,1),key='-RESTART-',disabled=True,visible=False)]
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
                relief=sg.RELIEF_RAISED),sg.T('',font=("DejaVu 10"),size=(15,1),key='-datetime-')],

            [sg.T('')],
            [sg.B('Start Calibration',size=(15,1),font=("Helvetica 13"),key='-CALIB-'),
                sg.B('TELESCOPE STOP',size=(20,1),font=("Helvetica 20"),key='-ESTOP-'),
                sg.B('Stow Telescope',size=(15,1),font=("Helvetica 13"),key='-STOW-')],

            [sg.T('')],
            [sg.Col(CoordEntry, element_justification='c', vertical_alignment='top'),

                #sg.VSep(pad=((30,30),(0,0))),
                sg.VSep(pad=((0,0),(0,0))),

                sg.Col(Parameters, element_justification='c', vertical_alignment='top'),

                #sg.VSep(pad=((30,30),(0,0))),
                sg.VSep(pad=((0,30),(0,0))),

                sg.Col(Jogging, element_justification='c', vertical_alignment='top'),

                #sg.VSep(pad=((30,30),(0,0))),
                sg.VSep(pad=((30,30),(0,0))),

                sg.Col(System, pad=((0,30),(0,0)), element_justification='c', vertical_alignment='top')],

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
WindSpeed = 0

VAZ = 00.00
VALT = 00.00

azDial = daz.AZ()
altDial = dalt.ALT()

window.move(200,250)
azDial.Dial.move(1300,50)
altDial.Dial.move(1300,700)
Output2.move(2000,50)


# Abs Position of Servomotors
AbsAZ = 0
AbsALT = 0
absPosTimer = 0
SysTimer = 0

# GUI Status bits
#   bit7 - Stowed
#   bit6 - Calibrated
#   bit5 - ALT homed
#   bit4 - AZ homed
#   bit3 - Jogging Enabled
#   bit2 - Servomotor ALT Enabled
#   bit1 - Servomotor AZ Enabled
#   bit0 - AFE Enabled
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
#---------------------------------------------------------------------------------------------------
#------------------------------------ GUI Event Loop -----------------------------------------------
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
while True:

    # check every 35 ms
    #   The first values in event is the menu bar event
    event, values = window.read(timeout=35)

    # update time
    time = dt.now().strftime('%Y-%m-%d   %H:%M')
    window['-datetime-'].update(time)


    #TODO, be careful to use
    if event == '-CALIB-':

        print("Starting Calibration")
        #30 degrees past zenith/0.09 motor counts = 333 counts

        window['-CALIB-'].Update(button_color=('black', 'gray'))


    if event == sg.WIN_CLOSED or event == 'Exit':
        # GUI is closed either by using 'X', or the Exit button
        break

    if event == '-EN-SRT-' and values['-EN-SRT-'] == True:
        print('Enabling Telescope Control')

        window['-EN-SERVO-'].update(disabled=False)
        window['-EN-AFE-'].update(disabled=False)
        window['-EN-JOG-'].update(disabled=False)
        window['-EN-ADV-'].update(disabled=False)

    if event == '-EN-SRT-' and values['-EN-SRT-'] == False:
        print('Disabling Telescope Control')

        window['-EN-SERVO-'].update(disabled=True)
        window['-EN-AFE-'].update(disabled=True)
        window['-EN-JOG-'].update(disabled=True)
        window['-EN-ADV-'].update(disabled=True)


    if event == '-EN-SERVO-' and values['-EN-SERVO-'] == True:

        print('Enabling Servomotor Drive')

        try:
            Servo_AZ = mc.Init('/dev/ttyUSB0')
            GUIstatus |= 0b0010
            print('Servomotor AZ enabled')

        except Exception as e:
            print(str(e))

        try:
            Servo_ALT = mc.Init('/dev/ttyUSB1')
            GUIstatus |= 0b0100
            print('Servomotor ALT enabled')

        except Exception as e:
            print(str(e))

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


    if event == '-EN-AFE-' and values['-EN-AFE-'] == True:

        print('Enabling AnalogFrontEnd')

        #AFE = afe.Init('/dev/ttyUSB3', 57600)
        AFE = afe.Init('/dev/ttyUSB0', 57600)

        if AFE == None:
            print('Check AFE Connection')
            window['-EN-AFE-'].update(value=False)

        else:
            GUIstatus |= 0b00000001



    if event == '-EN-AFE-' and values['-EN-AFE-'] == False:

        print('Disabling AnalogFrontEnd')

        afe.CloseSerial(AFE)

        GUIstatus &= 0b11111110


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


    if event == '-EN-ADV-' and values['-EN-ADV-'] == True:

        window['-HOME-AZ-'].update(disabled=False, visible=True)
        window['-HOME-ALT-'].update(disabled=False, visible=True)
        window['-RESTART-'].update(disabled=False, visible=True)

    if event == '-EN-ADV-' and values['-EN-ADV-'] == False:

        window['-HOME-AZ-'].update(disabled=True, visible=False)
        window['-HOME-ALT-'].update(disabled=True, visible=False)
        window['-RESTART-'].update(disabled=True, visible=False)


    if event == 'Read':

        print('Received coordinates (AZ, ALT): ', values['-IN-AZ-'], ', ', values['-IN-ALT-'])
        window['-OUT-AZ-'].update(values['-IN-AZ-'])
        window['-OUT-ALT-'].update(values['-IN-ALT-'])
        window['-POS-TGT-AZ-'].update(str(values['-IN-AZ-']) + '\N{DEGREE SIGN}')
        window['-POS-TGT-ALT-'].update(str(values['-IN-ALT-']) + '\N{DEGREE SIGN}')


        if (GUIstatus & 0b0110) == 0b0110:

            if values['-IN-ALT-'] and values['-IN-AZ-']:
                mc.Entry(Servo_AZ, Servo_ALT, int(values['-IN-AZ-']), int(values['-IN-ALT-']))

            elif values['-IN-ALT-'] and not values['-IN-AZ-']:
                mc.Entry_ALT(Servo_ALT, int(values['-IN-ALT-']))

            elif values['-IN-AZ-'] and not values['-IN-ALT-']:
                mc.Entry_AZ(Servo_AZ, int(values['-IN-AZ-']))

            else:
                window['-POS-TGT-AZ-'].update('N/A')
                window['-POS-TGT-ALT-'].update('N/A')

        else:
            print('No servo motors are enabled.')


    if event == '-ESTOP-':

        print("Software E-Stop is pressed")

        if (GUIstatus & 0b0010) == 0b0010:
            mc.Stop(Servo_AZ)

        if (GUIstatus & 0b0100) == 0b0100:
            mc.Stop(Servo_ALT)

        if (GUIstatus & 0b0110) == 0b0000:
            print('No servo motors are enabled.')

        if (GUIstatus & 0b0001) == 0b0001:
            afe.EngageBrake(AFE)


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

        mc.Stow(Servo_AZ, 0, 2, 5)
        mc.Stow(Servo_ALT, 0, 1, 2)
        GUIstatus |= 0b10000000


    if event == '-RESTART-' and (GUIstatus & 0b0110) == 0b0110:

        mc.Restart(Servo_AZ)
        mc.Restart(Servo_ALT)

        GUI.JogDisable()

        window['-EN-JOG-'].update(value=False)
        window['-EN-SERVO-'].update(value=False)

        mc.CloseSerial(Servo_AZ)
        mc.CloseSerial(Servo_ALT)

        GUIstatus &= 0b11111001


    # -------------Polling Servo Data------------
    # Poll AZ Abs Position, and update AZ dial
    if (GUIstatus & 0b0010) == 0b0010:

        AbsAZ = mc.LimitAZ(Servo_AZ)
        azDial.Update(round((AbsAZ/(-9365)), 1))
        window['-POS-CURR-AZ-'].update(round((AbsAZ/9365), 1))

        # Update Voltage
        VAZ = mc.GetVoltage(Servo_AZ)
        window['-voltAZ-'].update(str(VAZ)+" V")

        # Set the HOMED bit if zero pos
        if AbsAZ == 0:
            GUIstatus |= 0b00010000
        else:
            GUIstatus &= 0b01101111

    else:
        window['-voltAZ-'].update("N/A")


    # Poll ALT Abs Position, and update ALT dial
    if (GUIstatus & 0b0100) == 0b0100:

        AbsALT = mc.LimitALT_zenith(Servo_ALT)
        altDial.Update(round((AbsALT/(-1857)) + 90, 1))
        window['-POS-CURR-ALT-'].update(round((AbsALT/(-1857)) + 90, 1))

        # Update Voltage
        VALT = mc.GetVoltage(Servo_ALT)
        window['-voltALT-'].update(str(VALT)+" V")

        # Set the HOMED bit if zero pos
        if AbsALT == 0:
            GUIstatus |= 0b00100000
        else:
            GUIstatus &= 0b01011111

    else:
        window['-voltALT-'].update("N/A")


    # If both axis are homed, set the Stowed bit
    if (GUIstatus & 0b00110000) == 0b00110000:
        GUIstatus |= 0b10110000


    # Get windspeed from AFE
    if (GUIstatus & 0b0001) == 0b0001:

        try:
            WindSpeed = int( afe.GetWind(AFE) )
            window['-SYS2-'].update('')

        except ValueError as e:
            afe.CloseSerial(AFE)
            window['-EN-AFE-'].update(value=False)
            window['-SYS2-'].update('AFE Disconnected')
            GUIstatus &= 0b11111110
            print('AFE disconnected... Check AFE Connection.')

            with open('gui.log','a') as log:
                log.writelines( dt.now().strftime('%Y-%m-%d %H:%M:%S\n') )
                log.writelines( 'AFE Disconnected\n' )

        window['-WIND-'].update( str(WindSpeed) + " m/s" )

        if WindSpeed > 5 and WindSpeed < 25:
            window['-SYS-'].update('Wind speed exceeds op. limit')
            window['-SYS2-'].update('Stowing telescope advised')

        elif WindSpeed >= 25:
            window['-SYS-'].update('Wind speed exceeds survival limit')
            window['-SYS2-'].update('Telescope must be stowed')

        else:
            window['-SYS-'].update('Wind speed normal')

    else:
        window['-WIND-'].update('N/A')
        window['-SYS-'].update('Enable AFE to update wind speed')


    # Save absolute Position externally every 2s
    absPosTimer += 1

    if absPosTimer == 57:

        with open('absPos.dat', 'a') as absPos:
            absPos.writelines( dt.now().strftime('%Y-%m-%d %H:%M:%S\n') )
            absPos.writelines( str(AbsAZ) + '\n' )
            absPos.writelines( str(AbsALT) + '\n' + '\n' )

        absPosTimer = 0

#----------------------------------------------------------------------------
# -----------------Dump some log---------------------------------------------
#----------------------------------------------------------------------------
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
    log.writelines( 'Last Detected Wind Speed: ' + str(WindSpeed) + '\n' )

    log.writelines(';GUI log ends here\n\n\n')

window.close()
