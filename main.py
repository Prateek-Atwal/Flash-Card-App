from tkinter import *
import pandas as pd
BACKGROUND = "#B1DDC6"


def remove_card():
    global df
    word = canvas.itemcget(cur_word, "text")
    print(word)
    df = df[df.English != word]
    df = df[df.Japanese != word]
    try:
        revision_card = pd.read_csv("./data/revision_words.csv")
    except pd.errors.EmptyDataError:
        revision_card = pd.DataFrame()
    else:
        if len(revision_card) > 1:
            print(df)
            df.to_csv("./data/revision_words.csv", index=False)
        else:
            pd.DataFrame().to_csv("./data/revision_words.csv", index=False)
    generate_card()


def generate_card():
    global df, flipper
    window.after_cancel(flipper)
    if len(df) == 0:
        df = pd.read_csv("./data/JP Words.csv")
    df = df.sample(frac=1)
    word = df["Japanese"].iloc[0]
    canvas.itemconfig(canvas_img, image=card_front)
    canvas.itemconfig(cur_word, text=word)
    canvas.itemconfig(cur_lang, text="日本語")
    flipper = window.after(3000, reveal_sol)


def reveal_sol():
    global df, flipper
    window.after_cancel(flipper)
    word = df["English"].iloc[0]
    canvas.itemconfig(cur_word, text=word)
    canvas.itemconfig(canvas_img, image=card_back)
    canvas.itemconfig(cur_lang, text="English")


def revise_card():
    global df
    add_to_revision()
    df = pd.concat([df.iloc[1:].sample(frac=1), df.iloc[:1]], axis="rows")
    print(len(df))
    generate_card()


def get_file():
    try:
        data = pd.read_csv("./data/revision_words.csv")
    except pd.errors.EmptyDataError:
        data = pd.read_csv("./data/JP Words.csv")
    else:
        if len(data) == 0:
            data = pd.read_csv("./data/JP Words.csv")
    return data


def add_to_revision():
    try:
        data = pd.read_csv("./data/revision_words.csv")
    except pd.errors.EmptyDataError:
        data = pd.DataFrame()
    finally:
        if len(data) > 0 and len(data[data.Japanese == df.Japanese.iloc[0]]) > 0:
            pass
        else:
            data = pd.concat([df.iloc[:1], data])
            data.to_csv("./data/revision_words.csv", index=False)


df = get_file()

window = Tk()
window.config(padx=50, pady=30, bg=BACKGROUND)
window.geometry("+0+0")

card_front = PhotoImage(file="./images/card_front.png")
card_back = PhotoImage(file="./images/card_back.png")

canvas = Canvas(width=800, height=526, bg=BACKGROUND, highlightthickness=0)
canvas_img = canvas.create_image(400, 270, image=card_front)
canvas.grid(row=0, column=0, columnspan=2)

wrong_img = PhotoImage(file="./images/wrong.png")
wrong_button = Button(width=100, height=100, image=wrong_img, command=revise_card, highlightthickness=0, bg=BACKGROUND)
wrong_button.grid(row=1, column=0)

right_img = PhotoImage(file="./images/right.png")
right_button = Button(width=75, height=75, image=right_img, command=remove_card, highlightthickness=0, bg=BACKGROUND)
right_button.grid(row=1, column=1)

cur_lang = canvas.create_text(400, 150, text="日本語", font=("Ariel", 40, "italic"))
cur_word = canvas.create_text(400, 263, text=df["Japanese"].iloc[0], font=("Ariel", 60, "bold"))

flipper = window.after(3000, reveal_sol)

window.mainloop()
