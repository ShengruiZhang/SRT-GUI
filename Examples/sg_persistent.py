import PySimpleGUI as sg

sg.theme('DarkAmber')

layout = [  [sg.T('360 Baidu Ali Tencent is watching you')],
            [sg.In(key='-FilePath-')],
            [sg.B('Read'), sg.Exit()]  ]

window = sg.Window('Window that fucks u up', layout)

while True:
    event, values = window.read()
    FilePath = values['-FilePath-']
    print(event, values)
    print('Bank Account: ', FilePath)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break



window.close()
