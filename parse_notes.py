import re

import pdb


class Line(object):
    # a Line is either a heading, or not.
    # if it is not a heading, it will have no children
    def __init__(self, parent, txt):
        self.parent = parent
        self.parent.children.append(self)
        self.line = txt
        self.children = []

    def is_heading(self):
        return (True if len(children)>0 else False)

class Questions:
    def __init__(self, filename):
        self.filename = filename
        self.questions = self.extract_all_questions(filename)

    def extract_all_questions(self, filename):
        head = Line(None,None)
        last_line = head
        last_level = 0

        questions = []
        with open(filename, 'r') as f:
            full_path = '/'.join(f.name.split('/')[:-1])
            for line in f:
                question = {}
                if re.match('#+\s(.+):', line): # heading
                    poundsigns = re.split('(#+).*', line)[1]
                    level = len(poundsigns)
                    d_level = level - last_level # positive means number to move down
                    # if d_level > 1, add empty levels in between just to
                    # keep things predictable


                elif re.match('-\s(.+):', line): # list item
                    ls = re.split('-\s([^:]+):', line, maxsplit=1)
                    # skip anything with latex in the question
                    if not re.search('\$', ls[1]):
                        question['Q'] = ls[1]
                        question['A'] = ls[2]
                        if re.search('\!\[.*\]\((.+)\)', ls[2]): # md image
                            photo_loc = re.search('!\[.*\]\((.+)\)', ls[2]).groups()[0]
                            question['A'] = '%s/%s' % (full_path, photo_loc)
                            no_image_cite_q = re.sub('!\[.*\]\((.+)\)', '(figure)', ls[2])
                            question['A+'] = no_image_cite_q
                            if re.search('\$', question['A+']):
                                question['type'] = 'image-latex'
                            else:
                                question['type'] = 'image-text'
                        elif re.search('\$', ls[2]):
                            question['type'] = 'latex'
                        else:
                            question['type'] = 'text'
                        questions.append(question)
        return questions

if __name__ == '__main__':
    qq = Questions('../test.md')
    pdb.set_trace()
