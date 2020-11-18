import PySimpleGUI as sg

sg.theme('Topanga')

layout = [
        [sg.T('I need you bank account and password')],
        [sg.T('account num ', size=(15, 1)), sg.In(key='-AccountNum-')],
        [sg.T('password', size=(15, 1)), sg.In(key='-PWD-')],
        [sg.T('phone', size=(15, 1)), sg.In(key='-Phone-')],
        [sg.Submit(), sg.Cancel()]
]

window = sg.Window('I steal bank account and password', layout)
event, values = window.read()
window.close()
print(event, values['-PWD-'])
