import re
import random
import os
import sys

import sympy

import pdb

class Questions:
    def __init__(self, sourcefp, latexheaderfile=None):
        self.questions = self.parse_file(sourcefp, latexheaderfile)
        sourcefp.close()

    def parse_file(self, f, latex_headers=None):
        if latex_headers:
            with open(latex_headers, 'rU') as lh:
                lines = lh.readlines()
                latex_headers = (''.join(lines)).replace('\n','')
        questions = []
        full_path = '/'.join(f.name.split('/')[:-1])
        for line in f:
            question = {}
            if re.search('-\s(.+):', line):
                ls = re.split('-\s([^:]+):', line, maxsplit=1)
                # skip anything with latex in the question
                if not re.search('\$', ls[1]):
                    question['Q'] = ls[1]
                    question['A'] = ls[2]
                    if re.search('\!\[.*\]\((.+)\)', ls[2]): # md image
                        photo_loc = re.search('!\[.*\]\((.+)\)', ls[2]).groups()[0]
                        question['A+'] = '%s/%s' % (full_path, photo_loc)
                        no_image_cite_q = re.sub('!\[.*\]\((.+)\)', '(figure)', ls[2])
                        question['A'] = no_image_cite_q
                        # note the image goes in A+ and the other text in A
                        if re.search('\$', question['A']):
                            question['type'] = 'image-latex'
                        else:
                            question['type'] = 'image-text'
                    elif re.search('\$', ls[2]):
                        question['type'] = 'latex'
                    else:
                        question['type'] = 'text'
                    # insert headers
                    if latex_headers and re.search('latex', question['type']):
                        question['A'] = '%s %s' % (latex_headers, question['A'])
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
        os.system('rm -f flash_export_tmp/*.png')

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
                latex_image = self.latex_to_image(q['A'], tmpfile)
                if latex_image == tmpfile:
                    i += self.export_flashcard_text(q['Q'], "%s%03i.png" % (dr, i))

                    self.export_flashcard_image(tmpfile, "%s%03i.png" % (dr, i))
                    i += self.add_text_to_image(q['Q'], "%s%03i.png" % (dr, i))
        if i > 0:
            os.system('rm %s' % tmpfile)
            # combine into pdf
            pdf_cmd = 'convert %s/*.png %s' % (dr, outpdf)
            os.system(pdf_cmd)
        print '---\n%i flash cards created' % i

    def latex_to_image(self, text, filename='qtemp.jpg'):
        try:
            sympy.preview(text, viewer='file', filename=filename, euler=False)
            return filename
        except Exception,e:
            print '--- Failed to render latex for ---\n%s\n---\n' % text
            print e
            return 'latex_error.jpg'

if __name__ == '__main__':
    if len(sys.argv) == 4:
        infile = sys.argv[1]
        headerfile = sys.argv[2]
        outfile = sys.argv[3]
        fp = open(infile)
        qq = Questions(fp, headerfile)
        qq.export_flashcards(outfile)
    elif len(sys.argv) == 3:
        print 'No latex headers given... Creating flash cards'
        infile = sys.argv[1]
        outfile = sys.argv[2]
        fp = open(infile)
        qq = Questions(fp)
        qq.export_flashcards(outfile)
    else:
        print 'Nothing to do with %i input arguments' % len(sys.argv)
    # pdb.set_trace()
