import re
import random
import os
import sys

import sympy

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

    # Caption - Word Wrapped Label, from: http://www.imagemagick.org/Usage/text/#label
    def export_flashcard_text(self, text, filename):
        cmd = 'convert -background White -pointsize 35 -size 667x375 -gravity Center caption:"%s" %s'  % (text, filename)
        os.system(cmd)
        return 1

    def export_flashcard_image(self, imgfile, filename):
        # just pad it
        cmd = 'convert %s -gravity center -background white -extent 667x375 %s' % (imgfile, filename)
        os.system(cmd)
        return 1

    # overwrites!
    # use this on every answer so it is easy to tell which is the question and which is the answer
    # http://www.imagemagick.org/Usage/annotating/
    def add_text_to_image(self, text, imgfile):
        cmd2 = 'convert -background "#0008" -fill white -gravity center -pointsize 25 -size 667x caption:" %s " %s +swap -gravity north -composite  %s' % (text, imgfile, imgfile)
        os.system(cmd2)
        return 1

    def export_flashcards(self, outpdf):
        qs = self.questions
        # random.shuffle(qs)

        os.system('rm flash_export_tmp/*.png')

        dr = 'flash_export_tmp/'
        i = 0;
        tmpfile = ('%sqtemp.png' % dr)
        for q in qs:
            if q['type'] == 'text':
                # question
                i += self.export_flashcard_text(q['Q'], "%s%03i.png" % (dr, i))

                self.export_flashcard_text(q['A'], "%s%03i.png" % (dr, i))
                i += self.add_text_to_image(q['Q'], "%s%03i.png" % (dr, i))
            elif q['type'] == 'latex':
                try:
                    sympy.preview(q['A'], viewer='file', filename=tmpfile, euler=False)
                    i += self.export_flashcard_text(q['Q'], "%s%03i.png" % (dr, i))

                    self.export_flashcard_image(tmpfile, "%s%03i.png" % (dr, i))
                    i += self.add_text_to_image(q['Q'], "%s%03i.png" % (dr, i))
                except:
                    print 'bad question answer:\n%s\n%s' % (q['Q'], q['A'])
        os.system('rm %s' % tmpfile)
        # combine into pdf
        pdf_cmd = 'convert %s/*.png %s' % (dr, outpdf)
        os.system(pdf_cmd)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        qq = Questions('../test.md')
    elif len(sys.argv) == 3:
        infile = sys.argv[1]
        outfile = sys.argv[2]
        qq = Questions(infile)
        qq.export_flashcards(outfile)
    # pdb.set_trace()
