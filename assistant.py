import PySimpleGUI as sg
import sys, re
from io import StringIO
from string import Template
from slist import slist


WORD_LENGTH = 5
MAX_GUESSES = 6

green_tuple = tuple()   # Letter is in string and in correct position
yellow_tuple = tuple()  # Letter is in string but is out of position
black_tuple = tuple()   # Letter is not in string

g_temp_set = set()      # Temp variable for assisting in building regex
y_temp_set = set()      # Temp variable for assisting in building regex
green_set = set()
yellow_set = set()
black_set = set()
do_not_add_to_black = set()

BS = '^[^'              # Start of the black set
BE = ']+$'              # End of the black set

# Instructions for assigning the color to the assosciated letter
inst_line1 = "The color code letters are: 'g' for GREEN, 'y' for YELLOW and 'b' for GRAY."
inst_line2 = "For example: gybbg would be green-yellow-gray-gray-green."
inst_line3 = " "

layout = [
    [sg.Text(inst_line1)],
    [sg.Text(inst_line2)],
    [sg.Text(inst_line3)],
    [sg.Text('Input a five-letter word:',font='Helvetica 14'), sg.InputText(key='-WORD-', font='Helvetica 14')],
    [sg.Text('Input a five-letter code:',font='Helvetica 14'), sg.InputText(key='-CODE-', font='Helvetica 14')],
    [sg.Button('Submit'), sg.Button('Exit')],
    [sg.Multiline('', size=(40, 10), key='-OUTPUT-', font=('Courier', 16, 'bold'))]
]

window = sg.Window('Word and Code Input', layout)


while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'Submit':
        word = values['-WORD-'].lower()
        code = values['-CODE-'].lower()
    elif event == 'Flush':
        flush()

        
    regex_string = ''
    yellow = ''
    green = ''
    black = ''


    output_list = []
    window['-OUTPUT-'].update(output_list)  # Update the multiline element with the output

    # Color code each letter and its position so that we can begin to generate the regular expression filter.
    # Use sets for the storage to avoid repetition.
    # If a letter is gray the letter is added to the black-list and those words will be filtered out.
    # Caution! If you guess a letter twice and the solution only has on occurance the second letter will show gray.
    # You do not want to add the second occurance to the black-list as it will filter out an accepable word.
    for i in range(WORD_LENGTH):
        if code[i] == 'b':
            black_tuple=(word[i], i)
            black_set.add(black_tuple)
        elif code[i] == 'y':
            yellow_tuple=(word[i], i)
            yellow_set.add(yellow_tuple)
        elif code[i] == 'g':
            green_tuple=(word[i],i)
            green_set.add(green_tuple)
    

    # If you repeat a letter and it occurs in the solution more than once the second occurance will show as gray.
    # You do not waht to add this letter to the black-list as it will filter out all occurnaces of this letter.
    for letter, position in green_set:
        do_not_add_to_black.add(letter)
        s = Template("(?=^.{$position}$letter)")
        g_temp_set.add(s.substitute(position=position, letter=letter))
    for item in g_temp_set:
        green += item

    # The same caution applies to yellow letter. Be careful what you add to the black-set
    # The yellow letter requires two entries:
        # One that finds the letter in the string
        # The other that excludes strings with that letter in the current position.
    for letter, position in yellow_set:
        do_not_add_to_black.add(letter)
        s = Template("(?=.*$letter)(?!^.{$position}$letter)")
        y_temp_set.add(s.substitute(position=position, letter=letter))
    for item in y_temp_set:
        yellow += item

    for letter, position in black_set:
        if letter not in do_not_add_to_black:
            black += letter
    
    # Final assembly of the regular expression filter
    regex_string = green + yellow + BS + black + BE
    # ic(regex_string)
    
    # Compile the regex to assign it to concice variable
    pattern = re.compile(regex_string)

    for item in slist:
        if pattern.match(item):
            output_list.append(item)
#            output_list += (item + ' ')

    window['-OUTPUT-'].update(' '.join(output_list))  # Update the contents of the multiline element, removing the brackets and the commas

window.close()
