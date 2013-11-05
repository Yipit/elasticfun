# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import operator
import re
from six import text_type
from datetime import datetime
from functools import reduce

from .compat import UnicodeMixin
from .exceptions import ParsingException

LOOKUPS = ['lte', 'gte', 'lt', 'gt', 'in', 'range', 'startswith', 'endswith']

LOOKUP_OPS = {'in': 'OR', 'range': 'TO'}


class Query(UnicodeMixin):

    re_spaces = re.compile(r'\s+')

    def __init__(self, query=None, **kwargs):

        # Reading the special parameters
        self.boost = kwargs.pop('_boost', None)

        # Attributes that controls the beginning of a chain. Users were
        # not supposed to change them manually. Please refer to the
        # `Query.empty()` constructor.
        self._empty = kwargs.pop('_empty', False)
        self._cache = None

        # After cleaning up the kwargs we'll have just the plain field
        # declaration
        field = kwargs

        # Just formatting the fields to show a feedback for the caller
        # when he/she uses the API in a way we were not expecting
        fields_str = \
            ' & '.join("qb({}='{}')".format(k, v) for k, v in kwargs.items())

        # Hey we have a special case here, the user should _not_ use
        # both
        if query and field:
            msg = (
                "You cannot use both words and fields in the same call. "
                "Instead, you can do something like this: qb('{}') & {}"
            ).format(query, fields_str)
            raise ParsingException(msg)

        # If the user tries to query for more than one field in the same
        # object we also raise an exception
        if len(field) > 1:
            msg = (
                "You cannot use more than one field in the same call. "
                "Instead, you can do something like this: {}"
            ).format(fields_str)
            raise ParsingException(msg)

        self.field, self.lookup, self.query = None, None, query
        # The user wants to query by a specific field
        if field:
            self.field, self.lookup, self.query = self._process_field(field)

    @classmethod
    def empty(cls):
        return cls(_empty=True)

    @classmethod
    def from_user_input(cls, user_input='', default_op='AND'):
        user_input = user_input.strip()
        user_input = [cls(token) for token in cls.re_spaces.split(user_input)]
        op = operator.and_ if default_op == 'AND' else operator.or_
        query = reduce(op, user_input)
        return query

    def __unicode__(self):
        return self._cache or self._eval()

    def __and__(self, other):
        if self._empty:
            self._cache = text_type(other)
        else:
            self._cache = '({} AND {})'.format(self, other)
        self._empty = False
        return self

    def __or__(self, other):
        if self._empty:
            self._cache = text_type(other)
        else:
            self._cache = '({} OR {})'.format(self, other)
        self._empty = False
        return self

    def __invert__(self):
        self._cache = '(NOT {})'.format(self)
        return self

    def _process_field(self, field):
        field, val = list(field.items())[0]
        lookup = None
        if '__' in field:
            field, lookup = field.rsplit('__', 1)
            if not lookup in LOOKUPS:
                msg = (
                    "This is not a valid lookup argument."
                    "The valid lookups are: {}"
                ).format(', '.join(LOOKUPS))
                raise ParsingException(msg)
        return field, lookup, val

    def _escape(self, s):
        r = []
        for c in text_type(s):
            if c in '+-&|!(){}[]^"~*?:\\':
                r.append('\\')
            r.append(c)
        return ''.join(r)

    def _cast(self, val, lookup=None):
        if isinstance(val, bool):
            return '"{}"'.format(text_type(val).lower())
        if isinstance(val, datetime):
            return '"{}"'.format(val.isoformat())
        if isinstance(val, (list, set)):
            op = ' {} '.format(lookup and LOOKUP_OPS.get(lookup) or 'OR')
            return op.join(map(self._cast, val))
        if isinstance(val, Query):
            return text_type(val)

        val = self._escape(val)

        if lookup == 'startswith':
            val = '{}*'.format(val)
        elif lookup == 'endswith':
            val = '*{}'.format(val)

        return '"{}"'.format(val)

    def _process_lookup(self, lookup, value):
        if lookup == 'lte':
            value = '[* TO {}]'.format(value)
        elif lookup == 'gte':
            value = '[{} TO *]'.format(value)
        elif lookup == 'lt':
            value = '{{* TO {}}}'.format(value)
        elif lookup == 'gt':
            value = '{{{} TO *}}'.format(value)
        elif lookup in ['in', 'range']:
            # In this case the logic to handle in iterables
            # is in the cast method
            pass
        return '({})'.format(value)

    def _eval(self):
        # This query is empty, let's return nothing
        if self._empty:
            return ''

        # No specific query was received, let's return everything
        if not self.field and \
                not self.query and \
                not isinstance(self.query, bool):
            return '*:*'

        # Start out with a blank field, and the query specified
        field, val = '', self.query
        # If a field was specified add appropriate formatting
        if self.field:
            field = '{}:'.format(self.field)

        val = self._cast(val, lookup=self.lookup)

        # Update the value with appropriate formatting if there
        # are any lookups
        if self.lookup:
            val = self._process_lookup(self.lookup, val)

        # If the user needs to boost any fields!
        if self.boost:
            val = '{} {}^{}'.format(val, *self.boost)

        return '{}{}'.format(field, val)
