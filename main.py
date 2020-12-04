import PySimpleGUI as sg
import serial

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

coord_entry = [ [sg.T('Coordinate Entry:',font=("Helvetica 12 underline bold"))],
                [sg.T('Altitudinal:',size=(15,1),font=("Helvetica 10"))],
                [sg.In(key='-IN-ALT-', size=(15,1))],
                [sg.T('Azimuthal:',size=(15,1),font=("Helvetica 10"))],
                [sg.In(key='-IN-AZ-',size=(15,1))],
                [sg.Text('')],
                [sg.B('Enter')]  ]

parameters = [  [sg.T('Parameters:',font=("Helvetica 12 underline bold"))],
                [sg.T('Current Position:',font=("Helvetica 10 underline"))],
                [sg.T('32 degree N, 10 degree W',font=("Helvetica 10"))],
                [sg.T('Target Position:',font=("Helvetica 10 underline"))],
                [sg.T('59 degree N, 64 degree W')],
                [sg.T('Wind Speed:',font=("Helvetica 10 underline"))],
                [sg.T('2 m/s',justification='l')] ]

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
                relief=sg.RELIEF_FLAT)],
            [sg.T(" ")],
            [sg.B('Start Calibration',size=(15,1),font=("Helvetica 13")),
                sg.B('EMERGENCY STOP',size=(20,1),font=("Helvetica 15")),
                sg.B('Stow Telescope',size=(15,1),font=("Helvetica 13"))],
            [sg.T(" ")],
            [sg.Column(coord_entry, element_justification='c'), sg.VSeparator(), sg.Column(parameters, element_justification='c')],
           [sg.Text(" ")],
           [sg.Column(motor_status_az, element_justification = 'l'), sg.VSeparator(), sg.Column(motor_status_alt, element_justification='l')],
         [sg.Text(" ")],
          # [sg.Frame(layout=[
          # [sg.Text('Manual Coordinate Entry:')],
         #  [sg.Text('Altitudinal:'), sg.Text(size=(15,1), font=("Helvetica", 10), key='-OUTPUT-')],
         #  [sg.Input(key='-IN-', size=(15,1))],
         #  [sg.Text('Azimuthal:'), sg.Text(size=(15,1), font=("Helvetica", 10), key='-OUTPUT2-')],
         #  [sg.Input(key='-IN2-', size=(15,1))],
        #   [sg.OK()]], title= 'Coordinate Entry: ', font=("Helvetica", 12), size=(25, 25), title_color='white', relief=sg.RELIEF_RIDGE, background_color='maroon')],
         #  [sg.Frame(layout=[
         #  [sg.Button('EMERGENCY STOP!!', size=(20,1), font=("Helvetica", 15))]], title= 'Emergency Stop: ', font=("Helvetica", 12), title_color='white', relief=sg.RELIEF_RIDGE, background_color='maroon')],
         #  [sg.Frame(layout=[
         #  [sg.Text('Current Position:', font=("Helvetica", 10, 'underline bold'))],
         #  [sg.Text('32 degree N, 10 degree W', font=("Helvetica", 10))],
         #  [sg.Text('Target Position:', font=("Helvetica", 10, 'underline bold'))],
         #  [sg.Text('59 degree N, 64 degree W')],
         #  [sg.Text('Motor Status: ', font=("Helvetica", 10, 'underline bold'))],
         #      [sg.Text('Voltage:     ')],
          #     [sg.Text('Temperature:     ')],
         #      [sg.Text('Current:     ')],
         #  ], title= 'Parameters: ', font=("Helvetica", 12), title_color='white', relief=sg.RELIEF_RIDGE, background_color='maroon')],
           #  [sg.Text('Start Calibration Routine:')],
          # [sg.Graph(canvas_size= 100, graph_top_right=10, graph_bottom_left=10)],
           [sg.Frame(layout=[
           [sg.Button('Start Recording Data', font=("Helvetica", 10)), sg.Button('Stop Recording Data', font=("Helvetica", 10))],
           [sg.Text('Choose A Folder to Save Your Graph To:', size=(35, 1), font=("Helvetica", 10))],
           [sg.Text('Your Folder', size=(15, 1), auto_size_text=False, justification='right'),
            sg.InputText('Default Folder', font=("Helvetica", 10)), sg.FolderBrowse()]], title= 'Data Output: ', font=("Helvetica", 12), title_color='white', relief=sg.RELIEF_RIDGE, background_color='maroon', element_justification='c')],
           [sg.Exit()]]
          # [sg.OK(), sg.Cancel()]]

# create window
window = sg.Window('Student Radio Telescope', layout, element_justification='c')
#my_windows_size = window.Size
# read window

while True:  # Event Loop
    button, values = window.read()
    print(button, values)
    if button == sg.WIN_CLOSED or button == 'Exit':
        break
    if button == 'OK':
        # Update the "output" text element to be the value of "input" element
        window['-OUTPUT-'].update(values['-IN-'])
        window['-OUTPUT2-'].update(values['-IN2-'])
  #  if button == 'Calibration':
   #     calibrate()
    if button == 'STOP':
        break

window.close()
