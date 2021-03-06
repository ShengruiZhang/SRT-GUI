import PySimpleGUI as sg

layout = [  [sg.Graph(canvas_size=(700,700),
                        graph_bottom_left=(-700,-700),
                        graph_top_right=(700,700),
                        background_color='black',
                        key='graph',
                        tooltip='This is a cool graph!')],
        ]

window = sg.Window('Graph of a Circle', layout, grab_anywhere=True, finalize=True)

graph = window['graph']

graph.DrawCircle((0,40),600,fill_color=None,line_color="red",line_width=2)

event, values= window.read()
