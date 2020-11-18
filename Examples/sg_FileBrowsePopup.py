import PySimpleGUI as sg
import sys

if len(sys.argv) == 1:
    fname = sg.popup_get_file('Gimme your cc number')
else:
    fname = sys.argv[1]

if not fname:
    sg.popup("Fuck", "You didn't give me ur cc")
    raise SystemExit("Cancelling, I need ur cc")
else:
    sg.popup('Ur cc number is ', fname)
