import PySimpleGUI as sg

layout = [  [sg.T('Radio Telescope Control',size=(70,1),font='FreeSans 24',justification='center')],
            [sg.T('Status: ')]
            ]

window = sg.Window('Radio Telescope Control Interface Version Beta v0.1', layout)

while True:
    event, values = window.read()
    print(event)
    if event == sg.WIN_CLOSED:
        break
