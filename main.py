import PySimpleGUI as sg

sg.theme('LightGrey5')

# layout
layout = [ [sg.Text('Student Radio Telescope')],
           [sg.Button('Start Calibration')],
           [sg.Text('Manual Coordinate Entry:')],
           [sg.Text('Altitudinal:'), sg.Text(size=(15,1), key='-OUTPUT-')],
           [sg.Input(key='-IN-')],
           [sg.Text('Azimuthal:'), sg.Text(size=(15,1), key='-OUTPUT2-')],
           [sg.Input(key='-IN2-')],
           [sg.OK()],
           [sg.Text('Emergency Stop Button:')],
           [sg.Button('STOP!!!!')],
           [sg.Text('Current Position:')],
           [sg.Text('32 degree N, 12 degree W')],
           [sg.Text('Target Position:')],
           [sg.Text('59 degree N, 64 degree W')],
           #  [sg.Text('Start Calibration Routine:')],
           [sg.Button('Output Graph')],
          # [sg.Graph(canvas_size= 100, graph_top_right=10, graph_bottom_left=10)],
           [sg.Text('Choose A Folder to Save Your Graph To:', size=(35, 1))],
           [sg.Text('Your Folder', size=(15, 1), auto_size_text=False, justification='right'),
            sg.InputText('Default Folder'), sg.FolderBrowse()],
           [sg.Exit()]]
          # [sg.OK(), sg.Cancel()]]

# create window
window = sg.Window('Student Radio Telescope').Layout(layout)
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
    if button == 'STOP':
        break

window.close()