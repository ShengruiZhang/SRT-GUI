import PySimpleGUI as sg
import sys

if len(sys.argv) < 2:
    raise SystemExit("Fucked")
else:
    Timer = int(sys.argv[1])

layout = [  [sg.T('Timer is running'), sg.T(size=(15, 1), key='-00-')],
            [sg.T('1', key='-TIMER-')],
            [sg.B('Count Up')]
]

window = sg.Window('Simple Timer', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == 'Count Up':
        Timer += 1
        window['-TIMER-'].update(Timer)

window.close()
