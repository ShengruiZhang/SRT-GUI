import PySimpleGUI as sg

layout = [  [sg.T('Enter only float')],
            [sg.In(key='-IN-', enable_events=True)],
            [sg.B('GTFO')]  ]

window = sg.Window('Check Float', layout)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'GTFO'):
        break
    if event == '-IN-' and values['-IN-']:
        try:
            in_as_float = float(values['-IN-'])
        except:
            if len(values['-IN-']) == 1 and values['-IN-'][0] == '-':
                continue
            window['-IN-'].update(values['-IN-'][:-1])

window.close()
