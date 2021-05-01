from tkinter import messagebox as mb


def call(question):
    res = mb.askquestion('Satisfied?',
                         question)
    if res == 'yes':
        return "y"

    else:
        return "n"
