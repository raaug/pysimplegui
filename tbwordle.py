import random

def Process_Guess(the_answer, the_guess):
	position = 0
	clue = ""
	for letter in the_guess:
		if letter == the_answer[position]:
			clue += 'G'
		elif letter in the_answer:
			clue += 'Y'
		else:
			clue += 'D'
		position += 1
	print(clue)
	return clue == "GGGGG"

# load words and store them in a list
word_list = []
with open("words.txt") as word_file:
    for word in word_file:
    	word_list.append(word.strip())

# pick a word
answer = random.choice(word_list)
#print(f"{answer}")

num_of_guesses = 0
guessed_correctly = False

while num_of_guesses < 6 and not guessed_correctly:
    # get guess from user
    guess = input("Input a guess: ")
    print(f"{guess}")
    num_of_guesses += 1

    guessed_correctly = Process_Guess(answer, guess)
    if guessed_correctly:
        print(f"Congrats, you guessed the correct word in {num_of_guesses} guesses")
    elif num_of_guesses < 6:
        continue
    else:
        print(f"You have used up your guesses, the answer was {answer}")
