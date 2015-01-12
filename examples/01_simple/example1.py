#!/usr/bin/python
# *-* coding: utf-8 *-*
from allconf.xmlc import xmlio
from allconf.base import FloatOpt, StrOpt, IntOpt


class profil(object):
    def __init__(self):
        # should be floats
        self.cb_mag_min = FloatOpt(value=1.0,
                                   comment='colorbar magnitude minimum')
        self.cb_mag_max = FloatOpt()

        # should be string
        self.description = StrOpt(value='Nice profile')

        # should be int
        self.total_nr = IntOpt(value=3)


if __name__ == '__main__':
    profil1 = profil()

    X = xmlio(profil1)
    X.write_to_file('test.xml')
    X.read_from_file('test.xml')
    X.write_to_file('test2.xml')
