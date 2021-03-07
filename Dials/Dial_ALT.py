import PySimpleGUI as sg
import math

class ALT:

    def __init__(self):

        self.layout = [  [sg.Graph(canvas_size=(700,700),
            graph_bottom_left=(-700,-700),
            graph_top_right=(700,700),
            background_color='black',
            key='DIAL-ALT',
            tooltip='Altitude Position')
            ]
            ]

        self.Dial = sg.Window('Radio Telescope Dials',
                self.layout,
                grab_anywhere=True,
                finalize=True)

        self.Dial['DIAL-ALT'].DrawArc(   (-500,-400),
                (500,600),
                135,
                0,
                style='arc',
                arc_color='gold',
                line_width=None)

        self.Dial['DIAL-ALT'].DrawText(  "0",
                (550,100),
                color='gold',
                font=("OpenSans 20"),
                angle=0,
                text_location='center')

        self.Dial['DIAL-ALT'].DrawText(  "45",
                (394,494),
                color='gold',
                font=("OpenSans 20"),
                angle=0,
                text_location='center')

        self.Dial['DIAL-ALT'].DrawText(  "90",
                (0,650),
                color='gold',
                font=("OpenSans 20"),
                angle=0,
                text_location='center')

        self.Dial['DIAL-ALT'].DrawText(  "135",
                (-394,494),
                color='gold',
                font=("OpenSans 20"),
                angle=0,
                text_location='center')

        self.Dial['DIAL-ALT'].DrawPoint( (0,100),
                size=25,
                color='gold')

        self.line = self.Dial['DIAL-ALT'].DrawLine(
                (0,100),
                (500,100),
                color='gold',
                width=3)

        self.point = self.Dial['DIAL-ALT'].DrawPoint(
                (510,100),
                size=25,
                color='lime green')

        self.txt = self.Dial['DIAL-ALT'].DrawText(
                "ALT Position = ???\N{DEGREE SIGN}",
                (0,-600),
                color='gold',
                font=("OpenSans 36"),
                angle=0,
                text_location="center")


    def DelHand(self):

        self.Dial['DIAL-ALT'].delete_figure(self.line)
        self.Dial['DIAL-ALT'].delete_figure(self.point)
        self.Dial['DIAL-ALT'].delete_figure(self.txt)


    def Update(self, degree):

        self.DelHand()

        x = 500 * math.cos( abs(degree) * math.pi / 180 )
        y = 500 * math.sin( abs(degree) * math.pi / 180 )
        xpt = 510 * math.cos( abs(degree) * math.pi / 180 )
        ypt = 510 * math.sin( abs(degree) * math.pi / 180 )

        self.line = self.Dial['DIAL-ALT'].DrawLine( (0,100),
                (x, y+100), color='gold', width=3)

        self.point = self.Dial['DIAL-ALT'].DrawPoint(
                (xpt, ypt+100), size=25, color='lime green')

        self.DrawTx(degree)

    def DrawTx(self, degree):

        self.txt = self.Dial['DIAL-ALT'].DrawText(
                f'ALT Position = {abs(degree)}\N{DEGREE SIGN}',
                (0,-600),
                color='gold',
                font=("OpenSans 36"),
                angle=0,
                text_location="center")
