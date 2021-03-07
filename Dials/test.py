import PySimpleGUI as sg

import sys
import Dial_Az
import Dial_Alt

layout = [  [sg.B('Open Dials',key='POP')]    ]

window_main = sg.Window('Wrapper', layout, finalize=True)

while True:
    window, event, values = sg.read_all_windows()

    if window == sg.WIN_CLOSED:
        break

    if event == 'POP':
        print('Opening dials')

window_main.close()
