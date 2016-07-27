import os
import random

from Tkinter import *
import Tkinter as tk

import sympy
from PIL import Image, ImageTk

from parse_notes import Questions

import pdb

h1 = ('Helvetica', 24)
h2 = ('Helvetica', 18)
p = ('Times', 16)

class Quiz(Frame):
    def __init__(self, master=None, sourcefile=None):
        Frame.__init__(self, master)
        self.pack()
        # window settings
        master.resizable(width=False, height=False)
        master.geometry('{}x{}'.format(700, 400))
        # get content
        qs = Questions(sourcefile).questions
        random.shuffle(qs)
        # quiz states
        self.idx = 0
        self.last_question = None # i.e. post next question if None
        self.num_questions = len(qs)
        self.qq = enumerate(qs) # question queue

        # graphical components
        self.title = tk.Label(master,text = 'Quiz (%i questions)' % self.num_questions, font=h1)
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
        if self.last_question:
            # show answer with latex
            qtxt = self.last_question['A']
            if self.last_question['type'] == 'flash-latex':
                sympy.preview(qtxt, viewer='file', filename='qtemp.jpg', euler=False)
                image = Image.open('qtemp.jpg')
                photo = ImageTk.PhotoImage(image)
                self.answer.image = photo
                self.answer.config(image = photo)
                self.answer.pack()
            else:
                self.answer.image = None
                self.answer.config(text = qtxt)
            # state maintenance
            self.status.config(text = 'Answer %i)' % (self.idx+1),
                font=h2)
            self.fbutton.config(text = 'Next Question')
            self.last_question = None
        else:
            # post new question
            self.idx, newq = self.qq.next()
            self.question.config(text = newq['Q'], font=p)
            # state maintenance
            self.status.config(text = 'Question %i) Define or state the theorem:' % (self.idx+1),
                font=h2)
            self.fbutton.config(text = 'See Answer')
            self.answer.image = None
            self.last_question = newq

if __name__ == '__main__':
    sf = '../test.md'
    if len(sys.argv) == 2:
        sf = sys.argv[1]

    root = Tk()
    # root = Toplevel
    app = Quiz(master=root, sourcefile=sf)
    # bring python window to front
    os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
    app.mainloop()
    root.destroy()