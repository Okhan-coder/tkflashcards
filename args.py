import argparse


def get():
    parser = argparse.ArgumentParser()

    parser.add_argument("-f",
                        "--sourcefile",
                        type=str,
                        default='../test.md')
    parser.add_argument("-l",
                        "--latex-header-file",
                        type=str,
                        default=None)
    parser.add_argument("-r",
                        "--shuffle",
                        type=int,
                        default=1)

    return parser.parse_args()