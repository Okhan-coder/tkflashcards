import itertools
import random

import unittest
import pdb

from parse_notes import Line, Questions

class TraditionalMarkdownFile(unittest.TestCase):
    """
    """

    def getListItems(self, n):
        return "- list item\n"*n

    def getHeading(self, level):
        return "\n%s h%d heading\n\n" % ("#"*level, level)

    def setUp(self):
        self.filename = 'rand.md'
        perms = list(itertools.permutations([2,3,4,5]))
        self.groups_of_headings = perms
        flat_perms = [item for sublist in perms for item in sublist]
        self.heading_levels = [1] + flat_perms
        self.n_list_items_per_heading = [1] + flat_perms
        random.shuffle(self.n_list_items_per_heading)
        self.level_of_each_line = []

        with open(filename) as f:
            f.write("\n# only one h1\n\n")
            self.level_of_each_line += [1]
            i = 0
            f.write(self.getListItems(self.n_list_items_per_heading[i]))
            self.level_of_each_line += ([2] * self.n_list_items_per_heading[i])
            for perm in self.groups_of_headings:
                for level in perm:
                    i += 1
                    f.write(self.getHeading(level))
                    self.level_of_each_line += [level]
                    f.write(self.getListItems(self.n_list_items_per_heading[i]))
                    self.level_of_each_line += ([level+1] * self.n_list_items_per_heading[i])

    def testHeirarchyRecordedLevel(self):
        qq = Questions(self.filename)
        i = 0
        for node in qq.iterate_tree().next():
            self.failUnless(node.level == self.level_of_each_line[i])

    def testHeirarchyLevel(self):
        qq = Questions(self.filename)
        i = 0
        for node in qq.iterate_tree().next():
            self.failUnless(node.level() == self.level_of_each_line[i])

    def tearDown(self):
        pass

def main():
    unittest.main()

if __name__ == '__main__':
    main()
