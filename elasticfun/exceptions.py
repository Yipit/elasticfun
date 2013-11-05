# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class ImproperlyConfigured(Exception):
    pass


class ConfigMissingException(Exception):
    pass


class ParsingException(ValueError):
    pass


class EmptyQuerySetException(Exception):
    pass
