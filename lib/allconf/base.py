#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Use a class to define some options to be read/written from/to xml files, and
displayed using html forms

Common use cases
----------------

* create a new configuration file:
    wa_create_config "profil" "profil.xml" [--web]
    The --web option starts a webserver and shows a html edit mask
* edit an existing configuration file:
    * wa_config "profil.xml"
   Same as --web option before.
* import a configuration file from within python

  import wa_xml_config as wac
  profile = wac.read_from_file('profile.xml', wac.profil)

* save from python to file

    wac.save_to_file('profile_new.xml', profile)

* get options as dict

    options = wac.get_dict(profile)
    for key, item in options.iteritems():
        print key, item

notes/todo
----------

* show long descriptions of settings if requested (how do we do this in flask?)
* for certain settings we want to restrict possible values to a list of choices
* Could we implement cross-setting requirements? I.e., if 2D mode is on, then we
  need fictious sink nodes.
* multiple settings can be stored in a file, only the class names must be unique
* what about the level merging? If we keep this, we need some way to add and
  remove the settings (or just set them to None?). We have to distinguish
  between settings we do not want to touch at a specific level, and those we
  want to clear (i.e. reset to defaults)

  'None' - no setting
  '*' - use default

Argument description
--------------------

value : The initial value of the option
comment: the description
selection:
dtype: the type of the option
instances: types also recognized, wenn be converted to dtype. For example, int
           can be converted to float, so a dtype=float can convert an instance
           int types also recognized, wenn be converted to dtype. For example,
           int can be converted to float, so a dtype=float can convert an
           instance int.

"""


class OptionBase(object):
    """This is the base class for each configuration object
    """

    def __init__(self, **kwargs):
        # check for required keys
        for key in ('selection', 'value', 'comment'):
            if key not in kwargs:
                kwargs[key] = None

        self.dtype = kwargs['dtype']
        self.instances = kwargs['instances']
        self.selection = kwargs['selection']
        self.value = None
        self.comment = kwargs['comment']
        self.set(kwargs['value'])

    @property
    def get(self):
        return self.value

    def set(self, value, convert=False):
        """
        Parameters
        ----------
        value : value to store
        convert : [T|F] convert to correct type or raise error
        """
        if(value is None or
           value == 'None' or
           value == ''):
            self.value = None
        elif isinstance(value, self.instances) or convert:
            try:
                converted_value = self.dtype(value)
            except ValueError, e:
                print('There was an error converting the value "{0}"'.format(
                    value))
                print(e)
            else:
                # check against allowed values
                if self.selection is not None:
                    if converted_value not in self.selection:
                        raise Exception(
                            'Value {0} not in allowed values {1}'.format(
                                converted_value, self.selection))
                self.value = converted_value

        else:
            raise TypeError('Wrong data type')


class StrOpt(OptionBase):
    def __init__(self, **kwargs):
        kwargs['dtype'] = str
        kwargs['instances'] = (str, )
        super(StrOpt, self).__init__(**kwargs)


class IntOpt(OptionBase):
    def __init__(self, **kwargs):
        kwargs['dtype'] = int
        kwargs['instances'] = (int, )
        super(IntOpt, self).__init__(**kwargs)


class FloatOpt(OptionBase):
    def __init__(self, **kwargs):
        kwargs['dtype'] = float
        kwargs['instances'] = (int, float)
        super(FloatOpt, self).__init__(**kwargs)
