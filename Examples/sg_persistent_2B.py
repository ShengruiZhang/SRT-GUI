import PySimpleGUI as sg

sg.theme('BluePurple')

layout = [  [sg.T('Your bank password shows up here'), sg.T(size=(15,1), key='-OUTPUT-')],
            [sg.In(key='-IN-')],
            [sg.B('rEveAl', key='-OK-'), sg.B('Get the fuck out', key='-NO-')]    ]

window = sg.Window('Some dogshit', layout)


while True:
    event, values = window.read()
    print(event, values)
    #if event == sg.WIN_CLOSED or event == 'Get the fuck out':
    if event in (sg.WIN_CLOSED, '-NO-'):
        break
    if event == '-OK-':
        window['-OUTPUT-'].update(values['-IN-'])
        window['-OK-'].update('ThinkPad')
        window['-NO-'].update('/$/hit')

print('Program Exit')
window.close()
