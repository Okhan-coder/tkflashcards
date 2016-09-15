import os
import re
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

        self.master = master
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

        self.txtanswer = tk.Label(master, text = '', wraplength = 600) # wrap in pixels
        self.txtanswer.pack()
        self.ltximganswer = tk.Label(master, text = '')
        self.ltximganswer.pack()
        self.imganswer = tk.Label(master, text = '')
        self.imganswer.pack()

        self.fbutton = tk.Button(master, text = '', command = self.next_frame)
        self.fbutton.pack()


        self.next_frame()

    def update_attr_label_w_image(self, attr_label_name, image_filename):
        tk_label = getattr(self, attr_label_name)
        image = Image.open(image_filename)
        photo = ImageTk.PhotoImage(image)

        tk_label.image = photo
        tk_label.config(image = photo)
        tk_label.pack()

    def next_frame(self):
        if self.last_question: # show answer
            qtxt = self.last_question['A']
            if self.last_question['type'] == 'latex':
                try:
                    sympy.preview(qtxt, viewer='file', filename='qtemp.jpg', euler=False)
                    self.update_attr_label_w_image('ltximganswer', 'qtemp.jpg')
                except:
                    self.txtanswer.config(text = 'FAILED TO RENDER LATEX FOR: %s' % qtxt)
            # or show answer with an image
            elif re.search('image', self.last_question['type']):
                self.update_attr_label_w_image('imganswer', qtxt)
                # then also display the leftover latex or txt
                qtxt2 = self.last_question['A+']
                if self.last_question['type'] == 'image-text':
                    self.txtanswer.config(text = qtxt2)
                elif self.last_question['type'] == 'image-latex':
                    sympy.preview(qtxt2, viewer='file', filename='qtemp.jpg', euler=False)
                    self.update_attr_label_w_image('ltximganswer', 'qtemp.jpg')
            else:
                self.txtanswer.config(text = qtxt)
            # state maintenance
            self.status.config(text = 'Answer %i)' % (self.idx+1),
                font=h2)
            self.last_question = None
            # if the last question's answer was just displayed, prep for closing
            if (self.idx + 1) == self.num_questions:
                self.title.config(text = 'Done!')
                self.fbutton.config(text = 'Close Quiz', command = self.master.destroy)
            else:
                self.fbutton.config(text = 'Next Question')
        else: # show new question
            self.idx, newq = self.qq.next()
            self.question.config(text = newq['Q'], font=p)
            # state maintenance
            self.status.config(text = 'Question %i) Define or state the theorem:' % (self.idx+1),
                font=h2)
            self.fbutton.config(text = 'See Answer')
            # erase answers
            self.txtanswer.config(text = '')

            # erase latex and image
            self.update_attr_label_w_image('ltximganswer', 'blank.jpg')
            self.update_attr_label_w_image('imganswer', 'blank.jpg')

            self.last_question = newq

if __name__ == '__main__':
    # sf = '../test.md'
    sf = '../fitzpatrick_outline.md'
    if len(sys.argv) == 2:
        sf = sys.argv[1]

    root = Tk()
    # root = Toplevel
    app = Quiz(master=root, sourcefile=sf)
    # bring python window to front
    os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
    app.mainloop()
