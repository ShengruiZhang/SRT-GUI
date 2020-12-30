# import the time module
# TODO variable windSpeed needs to be changed so it is coming from analog output instead of set variable
import time

windSpeed = 6

MAX_WIND_SPEED = 4

MAX_TIME = 120

def WindSpeed(windSpeed):
    if windSpeed > MAX_WIND_SPEED:
        print('Start timer')
        WindTimer(MAX_TIME)


def WindTimer(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1

    print('Stowing Telescope Due to High Winds')


# function calls
# WindTimer(int(t))

WindSpeed(windSpeed)
