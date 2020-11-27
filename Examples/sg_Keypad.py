import PySimpleGUI as sg

layout = [  [sg.T('Student Radio Telescope by Steward Observatory')],
            [sg.In(size=(20,1), justification='right', key='input')],
            [sg.B('1'), sg.B('2'), sg.B('3')],
            [sg.B('Commit'), sg.B('Clear')],
            [sg.T(size=(15,1), font=('Helvetica', 18), text_color='yellow', key='out')]
            ]

window = sg.Window('Telescope Control', layout, default_button_element_size=(5,2),
                    auto_size_buttons=False)

keys_entered = ''
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == 'Clear':
        keys_entered = ''
    elif event in '1234567890':
        keys_entered = values['input']
        keys_entered += event
        print(event);
        print('Key value: ', keys_entered)
    elif event == 'Commit':
        keys_entered = values['input']
        window['out'].update(keys_entered)
    window['input'].update(keys_entered)
