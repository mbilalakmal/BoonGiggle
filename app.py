# -----------------------------------------------------------
# This module displays a window containing a search bar.
#
#
# (C) 2020 Muhammad Bilal Akmal, 17K-3669
# -----------------------------------------------------------

import PySimpleGUI as sg

from index_builder import generate_index_file
from query_dispatcher import dispatch_query

sg.theme('DarkBlue')

layout = [  [sg.Text('')],
            [sg.Image(r'resources\icon.png'), sg.Text('BoonGiggle', font=('Helvetica', 18))],
            [sg.Text('A Search Engine For Trump\'s Speeches.', font=('Helvetica', 9))],
            [sg.Input(key='_QUERY_'), sg.Button('SEARCH')],
            [sg.Text('')],
            [sg.Text(size=(48,6), key='_DOCS_')],
            [sg.Text('')],
            [sg.Text(size=(4, 1), key='_SIZE_')],
            [sg.Button('Build Index')],
            [sg.Text('')]
        ]

window = sg.Window(
    title='Information Retreival - Assignment 1',
    layout=layout,
    resizable=True,
    element_padding=(4, 4),
    element_justification='center'
    )

while True:
    event, values = window.read()
    print(event, values)
    if event is None:
        break
    if event == 'SEARCH':
        
        query = values['_QUERY_']

        if not query:
            continue

        result = dispatch_query(query)
        if result == None:
            display = 'No relevant speeches.'
            size = 0
        else:
            display = ', '.join(result[0])
            size = len(result[0])

        print(f'Relevant speeches: {display}')
        print(f'Number of relevant documents: {size}')
        window['_DOCS_'].update(display)
        window['_SIZE_'].update(size)
        
    elif event == 'Build Index':
        generate_index_file()

window.close()
