# Import
import tkinter
from tkinter import*
import random
import time
from PIL import ImageTk

#Background
width = 1100 
height = 700

canvas = Canvas(width=  width, height = height)
canvas.pack()

image = ImageTk.PhotoImage(file = "west.png")
canvas.create_image(0, 0, image=image, anchor=NW)


#Game body
def draw_gallow(x,y): #gallow structure
    gallows = x,y-50, x,y-100, x-200, y-170, x-200,y+250
    canvas.create_line(gallows, width = 10,fill = "#723900")
    canvas.create_line(x-300, y+290, x-0, y+290, width = 90, fill = "#723900")

def draw_hangman(x,y): # Hangman drawing
    head = canvas.create_oval(x-35, y-50, x+40, y+20, width = 5, state = tkinter.HIDDEN)
    torso = canvas.create_line(x,y+20,x, y+130, width = 5, state = tkinter.HIDDEN)
    larm = canvas.create_line(x-90,y+60, x, y+60, width = 5, state = tkinter.HIDDEN)
    rarm = canvas.create_line(x+90,y+60, x, y+60, width = 5, state = tkinter.HIDDEN)
    lleg = canvas.create_line(x,y+125, x-50, y+230, width = 5, state = tkinter.HIDDEN)
    rleg = canvas.create_line(x,y+125, x+50, y+230, width = 5, state = tkinter.HIDDEN)
    return head, torso, larm,rarm, lleg, rleg

def draw_letters(letters): # letters
    start = 0
    letter_ids = {letter:[] for letter in letters if letter !=" " }
    for letter in letters:
        if letter ==" ":
            start += 10
            continue
        canvas.create_line(start+2, 55, start+18, 55,width = 5,fill = "red")
        idx = canvas.create_text(start+10, 35, text = letter.upper(), 
                                font = "arial 20", fill = "red", state = tkinter.HIDDEN)
    
        letter_ids[letter].append(idx)
        start += 22

    return letter_ids

def load_world(file_name): # Ger random word from the database
    with open(file_name,"r") as fp:
        word_list = fp.read().splitlines() 
    random_word = random.choice(word_list)
    return random_word

# Game mechanics
def update_letters (letter_ids, already_guessed):  # Unhide guessed letters
    for letter, ids in letter_ids.items():
        if letter in already_guessed:
            for idx in  ids:
                canvas.itemconfig(idx, state = tkinter.NORMAL)
            

def update_hangman (wrong_guesses, hangman_ids): # Unhide part of the hangman
    for i in range(0,wrong_guesses):
        canvas.itemconfig(hangman_ids[i], state = tkinter.NORMAL)


def good_guess(letter):
    already_guessed.append(letter)
    update_letters (letter_ids, already_guessed)

def bad_guess(letter):
    global wrong_guesses
    already_guessed.append(letter)
    wrong_guesses += 1
    update_hangman(wrong_guesses, hangman_ids)

def is_winner (letter_ids, already_guessed):
    for letter in letter_ids:
        if letter not in already_guessed:
            return False
    return True

def check_game_state():
    global game_state
    if is_winner (letter_ids, already_guessed):
        game_state = "WIN"
    elif wrong_guesses > 5:
        game_state = "LOSE"

def game_over(state):
    if state == "WIN":
        canvas.create_text(320,240, text = "CONGRATULATIONS",
                           font = "arial 40", fill = "GREEN" )
    else:
        canvas.create_text(700,300, text = "Movie: "+the_word,
                           font = "arial 30", fill = "RED")
        canvas.create_text(320,240, text = "LOSE",
                           font = "arial 40", fill = "RED" ) 


    canvas.update()
    time.sleep(5)

draw_gallow(300,240)
hangman_ids = draw_hangman(300,240)
the_word = load_world("data-movies.txt")# We can use any type of database
letter_ids = draw_letters(the_word.upper())
game_state = "RUNNING"
already_guessed = []
wrong_guesses = 0

while game_state == "RUNNING":
    guess = input("guess letter:").upper()
    if guess in already_guessed:
        continue
    elif guess in letter_ids:
        print("OK")
        good_guess(guess)
    else:
        print("bad")
        bad_guess(guess)
    
    check_game_state()
    canvas.update()

game_over(game_state)
canvas.mainloop()







        

        
        