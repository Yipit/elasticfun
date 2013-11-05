# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import six


# code from
# http://docs.python.org/3/howto/pyporting.html#str-unicode
class UnicodeMixin(object):
    """Mixin class to handle defining the proper __str__/__unicode__
    methods in Python 2 or 3."""

    if six.PY3:
        def __str__(self):
            return self.__unicode__()
    else:  # Python 2
        def __str__(self):
            return self.__unicode__().encode('utf8')
