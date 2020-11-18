import PySimpleGUI as sg

#sg.theme('DarkAmber')

layout = [  [sg.Text('Some fuckshit 1', font='Courier 12', text_color='blue',
                                                        background_color='green')],
            [sg.Text('Enter some fuckshit here'), sg.InputText()],
            [sg.Button('Cancel'), sg.Button('Accept')]  ]

window = sg.Window('ENGR 498 Bull$hit', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    print('Nonsense ', values[0])

window.close()
