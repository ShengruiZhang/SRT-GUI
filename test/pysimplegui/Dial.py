import time
import math
import PySimpleGUI as sg

layout = [
            [sg.Graph(canvas_size=(700,700),
                        graph_bottom_left=(-700,-700),
                        graph_top_right=(700,700),
                        background_color='black',
                        key='DIAL',
                        tooltip='Testing Dial 1')
            ],
        ]

window = sg.Window('Radio Telescope Dials', layout,
                    grab_anywhere=True,
                    finalize=True)

Dial = window['DIAL']

Dial.DrawCircle( (0,100), 500,
                    fill_color=None,
                    line_color='gold',
                    line_width=2)

Dial.DrawPoint( (0,100),
                size=25,
                color='gold')

Dial.DrawText(  "0",
                (0,650),
                color='gold',
                font=("OpenSans 20"),
                angle=0,
                text_location="center")

Dial.DrawText(  "90",
                (550,100),
                color='gold',
                font=("OpenSans 20"),
                angle=270,
                text_location="center")

Dial.DrawText(  "180",
                (0,-450),
                color='gold',
                font=("OpenSans 20"),
                angle=0,
                text_location="center")

Dial.DrawText(  "270",
                (-550,100),
                color='gold',
                font=("OpenSans 20"),
                angle=90,
                text_location="center")

Dial.DrawText(  "N",
                (0,530),
                color='gold',
                font=("OpenSans 28"),
                angle=0,
                text_location="center")

Dial.DrawText(  "S",
                (0,-330),
                color='gold',
                font=("OpenSans 28"),
                angle=0,
                text_location="center")

Dial.DrawText(  "W",
                (430,100),
                color='gold',
                font=("OpenSans 28"),
                angle=0,
                text_location="center")

Dial.DrawText(  "E",
                (-430,100),
                color='gold',
                font=("OpenSans 28"),
                angle=0,
                text_location="center")

line = Dial.DrawLine(   (0,100),
                        (0,600),
                        color='gold',
                        width=3)

point = Dial.DrawPoint( (0,600),
                        size=25,
                        color='lime green')

degree = Dial.DrawText("AZ Position = 0\N{DEGREE SIGN}",
                        (0,-600),
                        color='gold',
                        font=("OpenSans 36"),
                        angle=0,
                        text_location="center")

input_deg = 0

while True:

    event, values = window.read(timeout=50)

    if event == sg.WIN_CLOSED:
        break

    dial_y = 500 * math.cos(abs(input_deg)*math.pi/180)
    dial_x = 500 * math.sin(abs(input_deg)*math.pi/180)

    Dial.delete_figure(line)
    Dial.delete_figure(point)
    Dial.delete_figure(degree)

    line = Dial.DrawLine(   (0,100),
                            (dial_x,dial_y+100),
                            color='gold',
                            width=3)

    point = Dial.DrawPoint( (dial_x,dial_y+100),
                            size=25,
                            color='lime green')

    degree = Dial.DrawText(f'AZ Position = {abs(input_deg)}\N{DEGREE SIGN}',
                        (0,-600),
                        color='gold',
                        font=("OpenSans 36"),
                        angle=0,
                        text_location="center")

    if input_deg <= 360:
        input_deg += 1
    else:
        input_deg = -360

window.close()
