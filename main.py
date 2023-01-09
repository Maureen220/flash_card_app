from tkinter import *
import pandas as pd
import random

# ---------------------------- CONSTANTS ------------------------------- #
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
df_dict = {}

try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    df = pd.read_csv("data/spanish_vocab.csv")
    df_dict = df.to_dict(orient="records")
else:
    df_dict = data.to_dict(orient="records")


# ---------------------------- GENERATE WORDS ------------------------------- #
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(df_dict)
    canvas.itemconfig(card_title, text="Spanish", fill="black")
    canvas.itemconfig(card_word, text=current_card["Spanish"], fill="black")
    canvas.itemconfig(canvas_image, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


def is_known():
    df_dict.remove(current_card)
    known_data = pd.DataFrame(df_dict)
    known_data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# ---------------------------- GENERATE WORDS ------------------------------- #
def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(canvas_image, image=card_back_img)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)

# Canvas image
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front_img)


# Canvas Text
card_title = canvas.create_text(400, 150, text="", fill="black", font=("Ariel", 30, "italic"))
card_word = canvas.create_text(400, 263, text="", fill="black", font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

# Buttons
wrong_img = PhotoImage(file="images/wrong.png")
button = Button(image=wrong_img, highlightthickness=0, command=next_card)
button.grid(column=0, row=1, columnspan=1)

right_img = PhotoImage(file="images/right.png")
button = Button(image=right_img, highlightthickness=0, command=is_known)
button.grid(column=1, row=1, columnspan=1)


next_card()

window.mainloop()
