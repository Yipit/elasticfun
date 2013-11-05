# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class Wrapper(object):

    @classmethod
    def get_key(cls, obj):
        return '{}:{}'.format(obj['_type'], obj['_id'])

    @classmethod
    def match(cls, obj):
        raise NotImplementedError

    @classmethod
    def wrap(cls, obj):
        raise NotImplementedError
