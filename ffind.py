#!/usr/bin/env python
''' Search for a file name in the specified dir (default current one) '''
import os
import argparse
import re

# Define colors
RED_CHARACTER = '\x1b[31m'
GREEN_CHARACTER = '\x1b[32m'
YELLOW_CHARACTER = '\x1b[33m'
BLUE_CHARACTER = '\x1b[36m'
PURPLE_CHARACTER = '\x1b[35m'
NO_COLOR = '\x1b[0m'


def search(directory, file_pattern, path_match, output=True, colored=True):
    ''' Search the files matching the pattern.
        The files will be returned, and can be optionally printed '''

    pattern = re.compile(file_pattern)

    results = []

    for root, sub_folders, files in os.walk(directory):
        for filename in files:
            full_filename = os.path.join(root, filename)
            to_match = full_filename if path_match else filename
            match = re.search(pattern, to_match)
            if match:
                # Split the match to be able to colorize it
                # prefix, matched_pattern, sufix
                smatch = [to_match[:match.start()],
                          to_match[match.start(): match.end()],
                          to_match[match.end():]]
                if not path_match:
                    smatch[0] = os.path.join(root, smatch[0])

                if output:
                    print_match(smatch, colored)

                results.append(full_filename)

    return results


def print_match(splitted_match, colored, color=RED_CHARACTER):
    ''' Output a match on the console '''
    if colored:
        a, b, c = splitted_match
        colored_output = (a, color, b, NO_COLOR, c)
    else:
        colored_output = splitted_match

    print ''.join(colored_output)


def main():
    parser = argparse.ArgumentParser(
        description='Search file name in dir tree'
    )
    parser.add_argument('-d', metavar='dir', default='.', required=False)
    parser.add_argument('-p',
                        action='store_true',
                        help='match path',
                        default=False)
    parser.add_argument('-c --no_color',
                        action='store_false',
                        dest='colored',
                        help='Do not display color',
                        default=True)
    parser.add_argument('filepattern')
    args = parser.parse_args()

    search(directory=args.d, file_pattern=args.filepattern,
           path_match=args.p, colored=args.colored)

if __name__ == '__main__':
    main()