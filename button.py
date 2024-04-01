import PySimpleGUI as sg

layout = [[sg.Text('My Window')],
        [sg.Button('Go',key='-GO-',font=('Helvetica', 14),button_color = None),
        sg.B('Clear'), sg.Button('Exit', font=('Helvetica', 14))]]

window = sg.Window('Button color', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == '-GO-':
        window['-GO-'].update(button_color = ('black','yellow'))

window.close()