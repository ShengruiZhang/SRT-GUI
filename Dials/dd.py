import Dial_ALT as Dial
import PySimpleGUI as sg

altDial = Dial.ALT()

while True:
    event, values = altDial.Dial.read(timeout=100)
    if event == sg.WIN_CLOSED:
        break
altDial.Dial.close()
