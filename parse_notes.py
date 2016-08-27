import re

import pdb


class Line(object):
    """
    All the lines in the markdown file are considered to be in a heirarchy
    of headings, and list items
    """
    def __init__(self, parent, data):
        self.parent = parent
        self.parent.children.append(self)
        self.data = data
        self.children = []
        return self

class Questions:
    def __init__(self, filename):
        self.filename = filename
        self.questions = self.extract_all_questions(filename)

    def extract_all_questions(self, filename):
        head = Line(None, {'type': 'heading', 'heading': ''})
        last_line = head
        last_line_level = 0

        with open(filename, 'r') as f:
            full_path = '/'.join(f.name.split('/')[:-1])
            for line_txt in f:
                if re.match('#+\s(.+):', line_txt): # heading
                    line_wo_poundsigns = re.split('(#+)(.*)', line_txt)[2]
                    poundsigns = re.split('(#+).*', line_txt)[1]
                    level = len(poundsigns)
                    d_level = level - last_line_level # positive means number to move down

                    # now we go looking for the immediate parent from a starting point:
                    immediate_parent = last_line
                    if (d_level > 0): # last line is a parent, or grand-parent,
                        # or great-grand-parent, or ... etc.
                        for i in range(d_level - 1): # if d_level > 1, add empty
                            #levels in between (just to keep things predictable)
                            immediate_parent = Line(immediate_parent,None)
                    elif (d_level < 0): # last line is deeper than current line,
                        # but they share a parent eventually
                        for i in range(abs(d_level) + 1):
                            immediate_parent = immediate_parent.parent
                    else: # the last line is a sibling, jump up just once.
                        # this naturally merges into the previous elif case,
                        # but the code is more readable this way.
                        immediate_parent = immediate_parent.parent

                    # with a parent at hand, add the line and maintain state
                    data = {'type': 'heading', 'heading': line_wo_poundsigns}
                    last_line = Line(immediate_parent, data)
                    last_line_level = level
                elif re.match('-\s(.+):', line_txt): # list item
                    # we do not care about nested lists, we only care under which
                    # headings the list items are nested under
                    level = last_line_level
                    if last_line.parent['type'] == 'heading':
                        level += 1
                    else: # previous item is also a list item, i.e. a sibling
                        pass
                    question_data = {}
                    ls = re.split('-\s([^:]+):', line_txt, maxsplit=1)

                    # skip anything with latex in the question
                    if not re.search('\$', ls[1]):
                        question_data['Q'] = ls[1]
                        question_data['A'] = ls[2]
                        if re.search('\!\[.*\]\((.+)\)', ls[2]): # md image
                            photo_loc = re.search('!\[.*\]\((.+)\)', ls[2]).groups()[0]
                            question_data['A'] = '%s/%s' % (full_path, photo_loc)
                            no_image_cite_q = re.sub('!\[.*\]\((.+)\)', '(figure)', ls[2])
                            question_data['A+'] = no_image_cite_q
                            if re.search('\$', question_data['A+']):
                                question_data['type'] = 'image-latex'
                            else:
                                question_data['type'] = 'image-text'
                        elif re.search('\$', ls[2]):
                            question_data['type'] = 'latex'
                        else:
                            question_data['type'] = 'text'
                        # now add the question to the tree
                        last_line = Line(immediate_parent, question_data)
                        last_line_level = level
                else: # any non-heading, and non-list item line is ignored
                    pass
        return head

if __name__ == '__main__':
    qq = Questions('../test.md')
    pdb.set_trace()
