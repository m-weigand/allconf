import os
import xml.etree.ElementTree as xmlp
from xml.dom import minidom


class xmlio(object):
    """Read or write to xml files
    """
    def __init__(self, option_class):
        self.target = option_class
        self.target_name = type(self.target).__name__

    @staticmethod
    def prettify(element):
        """Return a pretty-printed XML string for the Element.
        """
        rough_string = xmlp.tostring(element, encoding='utf-8')
        reparsed = minidom.parseString(rough_string)
        pretty_string = reparsed.toprettyxml(indent="  ", encoding='utf-8')
        pretty_str_utf8 = unicode(pretty_string, encoding='utf-8')
        # remove empty lines
        ps_no_empty_lines = u'\n'.join(
            [x for x in pretty_str_utf8.splitlines() if x.strip() != u''])

        return ps_no_empty_lines

    def write_to_file(self, filename, merge=True):
        existing_tags = []
        if os.path.isfile(filename) and merge:
            # read in all elements
            tree = xmlp.ElementTree()
            tree.parse(filename)

            # childs
            for i in tree.getroot():
                if i.tag != self.target_name:
                    existing_tags.append(i)

        root = xmlp.Element('settings')
        global_comment = ''.join(('Do not edit any comments in this file, it',
                                  ' is possible that they will be',
                                  ' overwritten!',
                                  '\n    ',
                                  'Do not use the word "None" as a value ',
                                  'expect to indicate that no value is ',
                                  'provided'))
        root.append(xmlp.Comment(global_comment))

        primary_subelm = xmlp.SubElement(root, self.target_name)

        for key, item in vars(self.target).iteritems():
            if item.comment is not None:
                comment = xmlp.Comment(item.comment)
                primary_subelm.append(comment)
            new_elm = xmlp.SubElement(primary_subelm, key)
            new_elm.text = '{0}'.format(item.value)

        # add other settings back
        for element in existing_tags:
            root.append(element)

        human_readable = self.prettify(root)
        with open(filename, 'w') as fid:
            fid.write(human_readable)

    def read_from_file(self, filename):
        """Parse a given xml file and write the contents to self.target.

        Only parse the subelements of target
        """
        if not os.path.isfile(filename):
            raise Exception('File not found: {0}'.format(filename))

        tree = xmlp.ElementTree()
        tree.parse(filename)

        for item in tree.find(self.target_name):
            obj = getattr(self.target, item.tag)
            # we always get string, so we need to convert the strings
            obj.set(item.text.strip(), convert=True)
