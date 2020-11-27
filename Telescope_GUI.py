import PySimpleGUI as sg

layout = [  [sg.T('Radio Telescope Control',size=(70,1),font='FreeSans 24',justification='center')],
            [sg.T('Telescope Status: ',font='FreeSans 16',justification='left',pad=((10,0),(0,0)))],
            [sg.T('')],
            [sg.T('Current Alt Position: ',font='FreeSans 14'), sg.T('',font='FreeSans 16',key='_ALT-POS_')],
            [sg.T('Current Az Position: ',font='FreeSans 14')],
            [sg.B('Commit')]
            ]

window = sg.Window('Radio Telescope Control Interface Version Beta v0.1', layout)

while True:
    event, values = window.read()
    print(event)
    if event == sg.WIN_CLOSED:
        break
    if event == 'Commit':
        window['_ALT-POS_'].update(1)
