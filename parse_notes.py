import re

import pdb

class Questions:
    def __init__(self, filename):
        self.filename = filename
        self.questions = self.parse_file(filename)

    def parse_file(self, filename):
        questions = []
        with open(filename, 'r') as f:
            full_path = '/'.join(f.name.split('/')[:-1])
            for line in f:
                question = {}
                if re.match('-\s(.+):', line):
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
