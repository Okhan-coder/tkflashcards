from Tkinter import *
import Tkinter as tk

from parse_notes import Questions

import pdb

class Quiz(Frame):
    def __init__(self, master=None, sourcefile=None):
        Frame.__init__(self, master)
        self.pack()

        self.last_question = None # i.e. post next question if None
        self.qq = iter(Questions(sourcefile).questions) # question queue

        # graphical components
        self.title = tk.Label(master,text = "Quiz")
        self.title.pack()

        self.status = tk.Label(master,text = '')
        self.status.pack()

        self.question = tk.Label(master, text = '')
        self.question.pack()

        self.answer = tk.Label(master, text = '')
        self.answer.pack()

        self.fbutton = tk.Button(master, text = '', command = self.next_frame)
        self.fbutton.pack()


        self.next_frame()

    def next_frame(self):
        if self.last_question: # show answer
            self.status.config(text = 'Answer:')
            self.fbutton.config(text = 'Next Question')
            self.answer.config(text = self.last_question['A'])

            self.last_question = None
        else: # post new question
            self.status.config(text = 'Question:')
            self.fbutton.config(text = 'See Answer')
            newq = self.qq.next()
            self.question.config(text = newq['Q'])
            self.answer.config(text = '')

            self.last_question = newq

if __name__ == '__main__':
    sf = '../fitzpatrick_outline.md'

    root = Tk()
    app = Quiz(master=root, sourcefile=sf)
    app.mainloop()
    root.destroy()