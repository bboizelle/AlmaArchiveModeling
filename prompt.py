from tkinter import messagebox as mb


def call():
    res = mb.askquestion('Satisfied?',
                         'Are you satisfied with the object fitting box?')
    if res == 'yes':
        return "y"

    else:
        return "n"


def main():
    call()


if __name__ == '__main__':
    main()
