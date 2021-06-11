from tkinter import messagebox as mb


# Uses tkinter for message box, for any "yes / no" question
def call(question):
    res = mb.askquestion('Satisfied?',
                         question)
    if res == 'yes':
        return "y"

    else:
        return "n"
