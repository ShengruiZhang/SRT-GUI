import PySimpleGUI as sg
import sys

if len(sys.argv) == 1:
    print('Only one argument is provided.')
    event, values = sg.Window('Choose input file',
                [   [sg.T('Select you credit card')],
                    [sg.In(key='-CCard-'), sg.FileBrowse()],
                    [sg.Open(), sg.Cancel()]
                    ]   ).read(close=True)
    fname = values['-CCard-']
else:
    fname = sys.argv[1]


if not fname:
    sg.popup("Cancel", "You didn't give me your CC number")
    raise SystemExit("Canceling: I want your CC number")
else:
    sg.popup('you cc number is ', fname)

print("Debug: ", fname)
