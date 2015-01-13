#!/usr/bin/python
# *-* coding: utf-8 *-*
"""
Given a reference and one or more target xml files, replace the specified tags
of the target files with those from the reference file.

WARNING: At the moment some comments will be lost when using this script!
"""
import os
import io
import copy
from optparse import OptionParser
import xml.etree.ElementTree as xmlp
from allconf.xmlc import xmlio


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

    return options, targets


def update_xml_files(reffile, target_files, tags):
    # read reference file
    reftree = xmlp.ElementTree()
    reftree.parse(reffile)

    print('Reading target xml files')
    # read targets
    targettrees = []
    for filename in target_files:
        ttree = xmlp.ElementTree()
        ttree.parse(filename)
        targettrees.append(ttree)

    print('Updating settings')
    # now replace or insert each tag
    for index, ttree in enumerate(targettrees):
        print target_files[index]

        for tag in tags:
            # find ref tag
            reftag = reftree.getroot().find(tag)
            if reftag is None:
                raise Exception('Tag not round in reference: {0}'.format(tag))

            # find target tag
            ttag = ttree.getroot().find(tag)
            if ttag is not None:
                ttree.getroot().remove(ttag)

            # make a copy of the ref element
            copy_reftag = copy.deepcopy(reftag)

            ttree.getroot().append(copy_reftag)

    print('Saving files')
    # save to file
    for filename, ttree in zip(target_files, targettrees):
        print(filename)
        tree_string = xmlio.prettify(ttree.getroot())
        with io.open(filename, 'w', encoding='utf-8') as fid:
            fid.write(tree_string)


if __name__ == '__main__':
    options, targets = handle_cmd_options()
    update_xml_files(options.reference, targets, options.tags.split(';'))
