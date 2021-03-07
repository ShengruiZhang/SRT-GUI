import PySimpleGUI as sg
import Dial_ALT as d

import sys

layout = [  [sg.B('Open Dials',key='POP')],
            [sg.B('Track',key='TRK')]
        ]

window_main = sg.Window('Wrapper', layout, finalize=True)

input = 0

a = d.ALT()
while True:

    window, event, values = sg.read_all_windows(timeout=100)

    if event == sg.WIN_CLOSED:
        break

    if event == 'POP':

        print('Opening dials')
        a = d.ALT()

    if event == 'TRK':

        print('Start Tracking')
        a.Update(input)

    a.Update(input)

    if input <= 130:
        input += 1
    else:
        input = -130

    #print(window, event, values)

window_main.close()
