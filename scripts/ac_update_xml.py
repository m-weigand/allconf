#!/usr/bin/python
# *-* coding: utf-8 *-*
"""
Given a reference and one or more target xml files, replace the specified tags
of the target files with those from the reference file.
"""
import os
from optparse import OptionParser


def handle_cmd_options():
    usage = 'usage: %prof [options] target1 target2 ...'
    parser = OptionParser(usage=usage)
    parser.add_option("-r", "--reference",
                      dest="reference",
                      type='string',
                      help="Reference XML file",
                      metavar="DIR",
                      default=None)

    parser.add_option("-t", "--tags",
                      dest="tags",
                      type='string',
                      help="Tags to update in targets (separate by ;)",
                      metavar="TAGS",
                      default=None)
    (options, targets) = parser.parse_args()

    # we need at least one positional argument (i.e. a target)
    if len(targets) == 0:
        print('You must specify at least one target xml file')
        exit()
    else:
        for filename in targets:
            if not os.path.isfile(filename):
                print('Filename not found: {0}'.format(filename))
                exit()

    if options.reference is None:
        print('You must specify a reference file')
        exit()

    return options


if __name__ == '__main__':
    options, targets = handle_cmd_options()
