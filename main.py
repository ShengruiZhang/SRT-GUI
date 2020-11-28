import PySimpleGUI as sg

#sg.theme('LightGrey5')
sg.theme_input_background_color('ghost white')
sg.theme_background_color('maroon')
sg.theme_text_element_background_color('maroon')
sg.theme_text_color('ghost white')
#sg.theme_button_color('midnight blue')



# ------ Menu Definition ------ #
menu_def = [['&File', ['&Open', '&Save', 'E&xit', 'Properties']],
            ['&Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],
            ['&Help', '&About...'], ]

# layout
layout = [ [sg.Menu(menu_def, tearoff=True)],
           [sg.Text('Student Radio Telescope', size=(30,1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_FLAT)],
           [sg.Text(" ")],
           [sg.Button('Start Calibration', size=(20,1), font=("Helvetica", 15)) ],
          # [sg.Text(" ")],
           [sg.Frame(layout=[
          # [sg.Text('Manual Coordinate Entry:')],
           [sg.Text('Altitudinal:'), sg.Text(size=(15,1), font=("Helvetica", 10), key='-OUTPUT-')],
           [sg.Input(key='-IN-')],
           [sg.Text('Azimuthal:'), sg.Text(size=(15,1), font=("Helvetica", 10), key='-OUTPUT2-')],
           [sg.Input(key='-IN2-')],
           [sg.OK()]], title= 'Manual Coordinate Entry: ', font=("Helvetica", 12), title_color='white', relief=sg.RELIEF_RIDGE, background_color='maroon')],
           [sg.Frame(layout=[
           [sg.Button('STOP!!!!', size=(20,1), font=("Helvetica", 15))]], title= 'Emergency Stop: ', font=("Helvetica", 12), title_color='white', relief=sg.RELIEF_RIDGE, background_color='maroon')],
           [sg.Frame(layout=[
           [sg.Text('Current Position:', font=("Helvetica", 10, 'underline bold'))],
           [sg.Text('32 degree N, 10 degree W', font=("Helvetica", 10))],
           [sg.Text('Target Position:', font=("Helvetica", 10, 'underline bold'))],
           [sg.Text('59 degree N, 64 degree W')]], title= 'Positioning: ', font=("Helvetica", 12), title_color='white', relief=sg.RELIEF_RIDGE, background_color='maroon')],
           #  [sg.Text('Start Calibration Routine:')],
           [sg.Frame(layout=[
           [sg.Radio('Amplitude vs. Time', "RADIO1", default=True, background_color='maroon', font=("Helvetica", 10))],
           [sg.Radio('Amplitude vs. Position', "RADIO1", background_color='maroon', font=("Helvetica", 10))],
           [sg.Button('Output Graph')]], title= 'Graphing Options: ', font=("Helvetica", 12), title_color='white', relief=sg.RELIEF_RIDGE, background_color='maroon', element_justification='c')],
          # [sg.Graph(canvas_size= 100, graph_top_right=10, graph_bottom_left=10)],
           [sg.Frame(layout=[
           [sg.Text('Choose A Folder to Save Your Graph To:', size=(35, 1), font=("Helvetica", 10))],
           [sg.Text('Your Folder', size=(15, 1), auto_size_text=False, justification='right'),
            sg.InputText('Default Folder', font=("Helvetica", 10)), sg.FolderBrowse()]], title= 'Save Data: ', font=("Helvetica", 12), title_color='white', relief=sg.RELIEF_RIDGE, background_color='maroon', element_justification='c')],
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
    if button == 'STOP':
        break

window.close()