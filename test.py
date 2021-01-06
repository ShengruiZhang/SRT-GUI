import PySimpleGUI as sg

tab1_layout =  [[sg.T('Inside Tab 1')],
                [sg.T('Using this space to get input...')],
                [sg.T('Input Tab (Key) to switch to'),sg.In(key='_IN_')]]

tab2_layout = [[sg.T('Inside Tab2')]]
tab3_layout = [[sg.T('Inside Tab3')]]

tabgroup_layout = [[sg.Tab('Tab 1', tab1_layout, key='_TAB1_'),
                    sg.Tab('Tab 2', tab2_layout),
                    sg.Tab('Tab 3', tab3_layout, key='_TAB3_')]]

layout = [ [sg.T('', size=(45,1), key='_OUT_')],
            [sg.TabGroup(tabgroup_layout, key='_TABGROUP_')],
            [sg.Button('Read', bind_return_key=True)]]

window = sg.Window('My window with tabs', default_element_size=(12,1)).Layout(layout)

while True:
    event, values = window.Read()
    if event is None:           # always,  always give a way out!
        break
    try:        # Attempt to select the tab based on Input value
        window.Element(values['_IN_'], silent_on_error=True).Select()
    except: pass
    # Display on the first window line some useful information
    window.Element('_OUT_').Update(f'The selected tab was = {values["_TABGROUP_"]}, direct read = {window.Element("_TABGROUP_").Get()}')
