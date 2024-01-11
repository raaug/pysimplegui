import PySimpleGUI as sg
import sys, re
from io import StringIO
from string import Template
from slist import slist


WORD_LENGTH = 5
wc = len(slist)

green_tuple = tuple()   # Letter is in string and in correct position
yellow_tuple = tuple()  # Letter is in string but is out of position
gray_tuple = tuple()    # Letter is not in string

green_set = set()       # Set of green tuples
yellow_set = set()      # Set of yellow tuples
gray_set = set()        # Set of gray tuples

g_temp_set = set()      # Temp variable for assisting in building regex
y_temp_set = set()      # Temp variable for assisting in building regex
d_temp_set = set()      # Temp variable for assisting in building regex

# Instructions for assigning the color to the assosciated letter
inst_line1 = "The color code letters are: 'g' for GREEN, 'y' for YELLOW and 'd' for DarkGray."
inst_line2 = "For example: gyddg would be green-yellow-darkgray-darkgray-green."
inst_line3 = "Exit to refresh and play again\n"

sg.theme('GreenTan')
layout = [
    [sg.Text("WORDLE ASSISTANT", font='Times 24', expand_x=True, justification='center')],
    [sg.Text(inst_line1)],
    [sg.Text(inst_line2)],
    [sg.Text(inst_line3)],
    [sg.Text('Input a five-letter word:',font='Helvetica 14'), sg.InputText(key='-WORD-', font='Helvetica 14', size=(6))],
    [sg.Text('Input a five-letter code:',font='Helvetica 14'), sg.InputText(key='-CODE-', font='Helvetica 14', size=(6))],
    [sg.Button('Submit'), sg.Button('Exit'), sg.Text(f"Initial word count = {wc}", key="-WC-")],
    [sg.Multiline(' '.join(slist), size=(36, 12), key='-OUTPUT-', pad = 10, font=('Courier', 16, 'bold'))]
]

window = sg.Window('Wordle Assistant', layout)


while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'Submit':
        word = values['-WORD-'].lower()
        code = values['-CODE-'].lower()
    
    if not re.findall('^[a-z]{5}$', word):
        sg.popup("word must be 5 alpha characters only!")
        break
    
    if not re.findall('^[dgy]{5}$', code):
        sg.popup("code must be 5 letters and consists of 'g', 'y' and 'd' only!")
        break

        
    regex_string = ''
    yellow = ''
    green = ''
    gray = ''
    do_not_add_to_gray_set = set()
    gray_string = ''
    temp_set = set()

    output_list = []
    wc = len(output_list)
    window['-OUTPUT-'].update(output_list)  # Update the multiline element with the output list.

    # Color code each letter and its position so that we can begin to generate the regular expression filter.
    # Use sets for the storage to avoid repetition.
    # If a letter is gray the letter is added to the gray-list and those words will be filtered out.
    # Caution! If you guess a letter twice and the solution only has on occurance the second letter will show gray.
    # You do not want to add the second occurance to the gray-list as it will filter out an accepable word.
    for i in range(WORD_LENGTH):
        if code[i] == 'd':
            gray_tuple=(word[i], i)
            gray_set.add(gray_tuple)

        elif code[i] == 'y':
            yellow_tuple=(word[i], i)
            yellow_set.add(yellow_tuple)
            do_not_add_to_gray_set.add(word[i])
            #print(f"yellow_tuple = {yellow_tuple}")
            #print(f"yellow_set = {yellow_set}")
        elif code[i] == 'g':
            green_tuple=(word[i],i)
            green_set.add(green_tuple)
            do_not_add_to_gray_set.add(word[i])
            #print(f"green_tuple = {green_tuple}")
            #print(f"green_set = {green_set}")
    

    # If you repeat a letter and it occurs in the solution more than once the second occurance will show as gray.
    # You do not waht to add this letter to the gray-list as it will filter out all occurnaces of this letter.
    for letter, position in green_set:
        s = Template("(?=^.{$position}$letter)")
        g_temp_set.add(s.substitute(position=position, letter=letter))
    for item in g_temp_set:
        green += item

    # The same caution applies to yellow letter. Be careful what you add to the gray-set.
    # The yellow letter requires two entries:
        # One that finds the letter in the string
        # The other that excludes strings with that letter in the current position.
    for letter, position in yellow_set:
        s = Template("(?=.*$letter)(?!^.{$position}$letter)")
        y_temp_set.add(s.substitute(position=position, letter=letter))
    for item in y_temp_set:
        yellow += item

    for letter, position in gray_set:
        if letter not in do_not_add_to_gray_set:
            temp_set.add(letter)
        s = Template("(?!^.{$position}$letter)")
        d_temp_set.add(s.substitute(position=position, letter=letter))

    for item in d_temp_set: # The accumulation of all the positional dark gray letters.
        gray += item

    gray_string = ''.join(temp_set)     # gray_string is a stringafied version ot the set of the "do_not_add_letters".
    s = Template("^[^$gray_string]+$$") # This Template prepends "^[^" and postpends "]+$" Notice the escaped $ by $$.
    gray_string = s.substitute(gray_string=gray_string)

    # Final assembly of the regular expression string.
    regex_string = green + yellow + gray + gray_string
    
    # Compile the regex to assign it to concice variable.
    pattern = re.compile(regex_string)

    for item in slist:
        if pattern.match(item):
            output_list.append(item) # output list is a list of all the remaining elegible words.

    wc = len(output_list) # The word count of all the remaining elegible words.
    window['-OUTPUT-'].update(' '.join(output_list))  # remove the brackets and commas and pass the list to the display window.
    window['-WC-'].update(f'Remaining word count = {wc}') # Displays the remaining word count.

window.close()
