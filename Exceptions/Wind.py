import time
import PySimpleGUI as sg

#import wind speed from arduino nano
windSpeed = 6

MAX_WIND_SPEED = 4.5

MAX_TIME = 57 #in seconds - to account for first autoclose popup

def WindSpeed(windSpeed):
    if windSpeed > MAX_WIND_SPEED:
         print('Start timer')
         #auto closes after 3 seconds
         sg.popup_no_buttons('Wind Speed Exceeds Mechanical Limit! \n                   Starting timer',title='High Wind Speed',  auto_close= True)
         WindTimer(MAX_TIME)

#
def WindTimer(t):
     while t:
         mins, secs = divmod(t, 60)
         timer = '{:02d}:{:02d}'.format(mins, secs)
         print(timer)
         time.sleep(1)
         t -= 1

     sg.popup_no_buttons('Stowing Telescope Due to High Winds')

#move telescope back to stow position


# # function calls

WindSpeed(windSpeed)