import time
import PySimpleGUI as sg

#import wind speed from arduino nano
windSpeed = 6

MAX_WIND_SPEED = 4.5 # in m/s

MAX_TIME = 30 # in seconds

# Delay for 1 minute after high wind is detected
#
# Input: Wind speed in m/s from AFE
# Output:
#
def WindSpeed(windSpeed):
    if windSpeed > MAX_WIND_SPEED:
         print('Start timer')
         #auto closes after 3 seconds
         sg.popup_no_buttons('Wind Speed Exceeds Mechanical Limit! \n                   Starting timer',title='High Wind Speed',auto_close=True)
         WindTimer(MAX_TIME)


# 1 minute Delay timer
#
# Input: Compare value
# Output: 1 if time is up, otherwise 0
#
def WindTimer(Thres):

    begin = time.time()

    while True:
        end = time.time()
        print(end)
        if (int(end-begin)) >= Thres:
            print("Times up")
            #sg.popup_no_buttons('Stowing Telescope Due to High Winds')
            #sg.popup_non_blocking_no_buttons("Test")
            sg.popup('Telescope is being stowed because wind speed exceeds mechanical limit.',
                        title='Radio Telescope: High Wind Speed',auto_close=True,auto_close_duration=15,non_blocking=True,
                        line_width=50,font="OpenSans 15",keep_on_top=True)
            print('Telescope is being stowed because wind speed exceeds mechanical limit.')
            return 1

    return 0


#move telescope back to stow position


# # function calls

#WindSpeed(windSpeed)
