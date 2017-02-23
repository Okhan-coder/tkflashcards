import argparse


def get():
    parser = argparse.ArgumentParser()

    parser.add_argument("-f",
                        "--sourcefile",
                        type=str,
                        default=None,
                        help='If None then uses the clipboard')
    parser.add_argument("-l",
                        "--latex-header-file",
                        type=str,
                        default=None)
    parser.add_argument("-r",
                        "--shuffle",
                        type=int,
                        default=1)

    return parser.parse_args()