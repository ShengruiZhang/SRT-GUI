import PySimpleGUI as sg
import sys
import time

if len(sys.argv) == 1:
    raise SystemExit("Fucked")
else:
    Timer = int(sys.argv[1])

#layout = [  [sg.T('Timer is running'), sg.T(size=(10, 10))]  ]
layout = [  [sg.T('Timer is running', size=(30, 1))],
            [sg.T('Timer', size=(30, 1), key='-TIME-', enable_events=True)]
        ]

window = sg.Window('Testing Window', layout, finalize=True)

while Timer < 5:
    window['-TIME-'].update(Timer)
    time.sleep(1)
    Timer += 1
    print(Timer)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

