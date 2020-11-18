import PySimpleGUI as sg
import time

sg.theme('Dark Blue 8')

for i in range(10):   # this is your "work loop" that you want to monitor
    sg.OneLineProgressMeter('One Line Meter Example', i + 1, 10, 'key')
    time.sleep(1);

#window.close()
