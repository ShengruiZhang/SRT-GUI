import PySimpleGUI as sg
import math

class AZ:

    def __init__(self):

        self.layout = [ [sg.Graph(canvas_size=(500,500),
            graph_bottom_left=(-700,-700),
            graph_top_right=(700,700),
            background_color='black',
            key='DIAL-AZ',
            tooltip='Azimuth Position')
            ]
            ]

        self.Dial = sg.Window('Radio Telescope Dials',
                self.layout,
                grab_anywhere=True,
                finalize=True)

        self.Dial['DIAL-AZ'].DrawCircle( (0,100),
                500,
                fill_color=None,
                line_color='gold',
                line_width=2)

        self.Dial['DIAL-AZ'].DrawPoint( (0,100),
                size=25,
                color='gold')

        self.Dial['DIAL-AZ'].DrawText(  "0",
                (0,650),
                color='gold',
                font=("OpenSans 20"),
                angle=0,
                text_location="center")

        self.Dial['DIAL-AZ'].DrawText(  "90",
                (550,100),
                color='gold',
                font=("OpenSans 20"),
                angle=270,
                text_location="center")

        self.Dial['DIAL-AZ'].DrawText(  "180",
                (0,-450),
                color='gold',
                font=("OpenSans 20"),
                angle=0,
                text_location="center")

        self.Dial['DIAL-AZ'].DrawText(  "270",
                (-550,100),
                color='gold',
                font=("OpenSans 20"),
                angle=90,
                text_location="center")

        self.Dial['DIAL-AZ'].DrawText(  "N",
                (0,530),
                color='gold',
                font=("OpenSans 28"),
                angle=0,
                text_location="center")

        self.Dial['DIAL-AZ'].DrawText(  "S",
                (0,-330),
                color='gold',
                font=("OpenSans 28"),
                angle=0,
                text_location="center")

        self.Dial['DIAL-AZ'].DrawText(  "W",
                (430,100),
                color='gold',
                font=("OpenSans 28"),
                angle=0,
                text_location="center")

        self.Dial['DIAL-AZ'].DrawText(  "E",
                (-430,100),
                color='gold',
                font=("OpenSans 28"),
                angle=0,
                text_location="center")

        self.line = self.Dial['DIAL-AZ'].DrawLine(
                (0,100),
                (0,600),
                color='gold',
                width=3)

        self.point = self.Dial['DIAL-AZ'].DrawPoint(
                (0,600),
                size=25,
                color='lime green')

        self.txt = self.Dial['DIAL-AZ'].DrawText(
                "AZ Position = ???\N{DEGREE SIGN}",
                (0,-600),
                color='gold',
                font=("OpenSans 30"),
                angle=0,
                text_location="center")


    def DelHand(self):

        self.Dial['DIAL-AZ'].delete_figure(self.line)
        self.Dial['DIAL-AZ'].delete_figure(self.point)
        self.Dial['DIAL-AZ'].delete_figure(self.txt)


    def Update(self, degree):

        self.DelHand()

        y = 500 * math.cos( abs(degree) * math.pi / 180 )
        x = 500 * math.sin( abs(degree) * math.pi / 180 )

        self.line = self.Dial['DIAL-AZ'].DrawLine(   (0,100),
                (x, y+100),
                color='gold',
                width=3)

        self.point = self.Dial['DIAL-AZ'].DrawPoint( (x, y+100),
                size=25,
                color='lime green')

        self.txt = self.Dial['DIAL-AZ'].DrawText(
                f'AZ Position = {abs(degree)}\N{DEGREE SIGN}',
                (0,-600),
                color='gold',
                font=("OpenSans 30"),
                angle=0,
                text_location="center")
