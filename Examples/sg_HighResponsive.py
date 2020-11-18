import PySimpleGUI as sg

choices = ('Red', 'Green', 'Blue', 'Yellow', 'Orange', 'Purple', 'Chartreuse')

layout = [  [sg.T('Find bank account')],
            [sg.Listbox(choices,
                size=(15, len(choices)),
                key='-COLOR-',
                enable_events=True)],
            [sg.T('You chose', key='-OUT-')]
         ]

window = sg.Window('Hacked', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if values['-COLOR-']:
        #sg.popup(f"This is {values['-COLOR-'][0]}")
        window['-OUT-'].update(values['-COLOR-'][0])

window.close()
