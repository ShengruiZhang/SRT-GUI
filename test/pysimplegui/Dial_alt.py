import PySimpleGUI as sg

layout = [  [sg.Graph(canvas_size=(700,700),
                        graph_bottom_left=(-700,-700),
                        graph_top_right=(700,700),
                        background_color='black',
                        key='DIAL-ALT',
                        tooltip='Altitude Position')
            ],
        ]

window = sg.Window('Radio Telescope Dials',
                    layout,
                    grab_anywhere=True,
                    finalize=True)

Dial_alt = window['DIAL-ALT']

#Dial_alt.DrawCircle((0,100),
#                    500,
#                    fill_color=None,
#                    line_color='gold',
#                    line_width=2)

#Dial_alt.DrawRectangle(
#                    (-500,-400),
#                    (500,600),
#                    fill_color=None,
#                    line_color='gold',
#                    line_width=2)

Dial_alt.DrawArc(   (-500,-400),
                    (500,600),
                    135,
                    0,
                    style='arc',
                    arc_color='gold',
                    line_width=None)

Dial_alt.DrawText(  "0",
                    (550,100),
                    color='gold',
                    font=("OpenSans 20"),
                    angle=0,
                    text_location='center')

Dial_alt.DrawText(  "45",
                    (394,494),
                    color='gold',
                    font=("OpenSans 20"),
                    angle=0,
                    text_location='center')

Dial_alt.DrawText(  "90",
                    (0,650),
                    color='gold',
                    font=("OpenSans 20"),
                    angle=0,
                    text_location='center')

Dial_alt.DrawText(  "135",
                    (-394,494),
                    color='gold',
                    font=("OpenSans 20"),
                    angle=0,
                    text_location='center')

Dial_alt.DrawPoint( (0,100),
                    size=25,
                    color='gold')

line = Dial_alt.DrawLine(
                    (0,100),
                    (500,100),
                    color='gold',
                    width=3)

point = Dial_alt.DrawPoint(
                    (510,100),
                    size=25,
                    color='lime green')

while True:

        event, values = window.read(timeout=50)

        if event == sg.WIN_CLOSED:
            break

window.close()
