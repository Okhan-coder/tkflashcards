import re

import pdb

class Questions:
    def __init__(self, filename):
        self.filename = filename
        self.questions = self.parse_file(filename)

    def parse_file(self, filename):
        questions = []
        with open(filename, 'r') as f:
            for line in f:
                question = {}
                if re.match('-\s(.+):', line):
                    ls = re.split('-\s([^:]+):', line, maxsplit=1)
                    # skip anything with latex in the question
                    if len(ls[1].split('$')) == 1:
                        question['Q'] = ls[1]
                        question['A'] = ls[2]
                        # re.match('\$', ls[2]) not working, who knows
                        if len(ls[2].split('$')) > 1:
                            question['type'] = 'flash-latex'
                        else:
                            question['type'] = 'flash'
                        questions.append(question)
        return questions

if __name__ == '__main__':
    qq = Questions('../test.md')
    pdb.set_trace()
