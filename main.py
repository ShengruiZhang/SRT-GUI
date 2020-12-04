#   TODO
#   1. Input protection for coord. input
#   2. Update the Target position after an coord. is entered
import PySimpleGUI as sg

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
coord_entry = [ [sg.T('Coordinate Entry:',font=("Helvetica 12 underline bold"),background_color='gray')],
                [sg.T('Altitudinal:',size=(15,1),font=("Helvetica 10"),background_color='gray')],
                [sg.In(key='-IN-ALT-', size=(15,1),background_color='gray')],
                [sg.T('Azimuthal:',size=(15,1),font=("Helvetica 10"),background_color='gray')],
                [sg.In(key='-IN-AZ-',size=(15,1),background_color='gray')],
                [sg.Text('',background_color='gray')],
                [sg.B('Enter')]   ]

parameters = [  [sg.T('Parameters:',font=("Helvetica 12 underline bold"),background_color='black')],
                [sg.T('Current Position:',font=("Helvetica 10 underline"),background_color='black')],
                [sg.T('32 degree N, 10 degree W',font=("Helvetica 10"),background_color='black')],
                [sg.T('Target Position:',font=("Helvetica 10 underline"),background_color='black')],
                [sg.T('59 degree N, 64 degree W',key='-POS-TGT-',background_color='black')],
                [sg.T('Wind Speed:',font=("Helvetica 10 underline"),background_color='black')],
                [sg.T('2 m/s',justification='l',background_color='black')] ]

motor_status_az = [
                #[sg.T('Azimuthal Motor Status:',font=("Helvetica 11 underline bold")),sg.T('        ')],
                [sg.T('Azimuthal Motor Status:',font=("Helvetica 11 underline bold"))],
                [sg.T('Voltage:',font=("Helvetica 10 underline"))],
                [sg.T('Temperature:',font=("Helvetica 10 underline"))],
                ]

motor_status_alt = [
                #[sg.T('Altitudinal Motor Status:',font=("Helvetica 11 underline bold")),sg.T('        ')],
                [sg.T('Altitudinal Motor Status:',font=("Helvetica 11 underline bold"))],
                [sg.T('Voltage:',font=("Helvetica 10 underline"))],
                [sg.T('Temperature:',font=("Helvetica 10 underline"))],
                ]
# layout
layout = [
            [sg.Menu(menu_def, tearoff=True)],
            [sg.T('Student Radio Telescope Control',size=(30,1),justification='c',font=("Helvetica 25"),
                relief=sg.RELIEF_GROOVE)],
            [sg.T(" ")],
            [sg.B('Start Calibration',size=(15,1),font=("Helvetica 13")),
                sg.B('EMERGENCY STOP',size=(20,3),font=("Helvetica 20"),key='-ESTOP-'),
                sg.B('Stow Telescope',size=(15,1),font=("Helvetica 13"))],
            [sg.T(" ")],
            [sg.Col(coord_entry, element_justification='l'),
                sg.VSep( pad=( (50,50),(0,0) ) ),
                sg.Col(parameters, element_justification='c')],
            [sg.T(" ")],
            [sg.Col(motor_status_az, element_justification = 'l'),
                sg.VSep(),
                sg.Col(motor_status_alt, element_justification='l')],
            [sg.T(" ")],
            [sg.Frame(  layout=[
                [sg.B('Start Recording Data',font=("Helvetica 10")),
                    sg.B('Stop Recording Data',font=("Helvetica 10"))],
                [sg.T('Choose A Folder to Save Your Graph To:',size=(35,1),font=("Helvetica 10"))],
                [sg.T('Save Path',size=(15,1),auto_size_text=False,justification='r'),
                    sg.In('Default Folder',font=("Helvetica 10")), sg.FolderBrowse()]
                ], title='Data Output:', font=("Helvetica 12"), title_color='white', relief=sg.RELIEF_RIDGE,
                    background_color='maroon', element_justification='c')],
            [sg.Exit()]
            ]

# create window
window = sg.Window('Student Radio Telescope Control', layout, element_justification='c')

_TGT_POS = 0

while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        # GUI is closed either by using 'X', or Exit button is clicked
        break
    if event == 'Enter':
        _TGT_POS = values['-IN-ALT-'] + values['-IN-AZ-']
        window['-POS-TGT-'].update(_TGT_POS)
    if event == '-ESTOP-':
        # If SW Stop is pressed, interrupt motor motions
        print("Softeare E-Stop is pressed")

window.close()
