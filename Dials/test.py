import PySimpleGUI as sg
import Dial_ALT as d

import sys

layout = [  [sg.B('Open Dials',key='POP')],
            [sg.B('Track',key='TRK')]
        ]

window_main = sg.Window('Wrapper', layout, finalize=True)

while True:

    window, event, values = sg.read_all_windows(timeout=1000)

    if event == sg.WIN_CLOSED:
        break

    if event == 'POP':

        print('Opening dials')
        a = d.ALT()

    if event == 'TRK':

        print('Start Tracking')
        a.Update(120)

    #print(window, event, values)

window_main.close()
