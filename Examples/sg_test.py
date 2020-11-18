import PySimpleGUI as sg

layout = [  [sg.Text('Enter Save File Path')],
            [sg.InputText(key='-IN-')],
            [sg.Submit(), sg.Cancel()]  ]

window = sg.Window('Some bullshit Window', layout)

event, values = window.read()
window.close()

text_input = values['-IN-']
sg.popup_ok_cancel('Shit just collected: ', text_input)
print("Debug: ", text_input)



#############################################################
sg.popup_ok('Switching to next styles: Pattern 1B')

event, values = sg.Window('Hacking Window', [
            [sg.T('Enter your credit card number'), sg.In(key='-ID-')],
            [sg.B('OK'), sg.B('Cancel')]    ]
            ).read(close=True)

Credit_Card = values['-ID-']
sg.popup_ok('Fucked, Credit card number is ', Credit_Card)
