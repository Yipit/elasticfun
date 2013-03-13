from datetime import datetime


class ParsingException(ValueError):
    pass


class Query(object):
    def __init__(self, query=None, **kwargs):

        # Reading the special parameters
        self.empty = kwargs.pop('_empty', None)
        self.boost = kwargs.pop('_boost', None)

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
                "You should do something like this: qb('{}') & {}"
            ).format(query, fields_str)
            raise ParsingException(msg)

        # If the user tries to query for more than one field in the same
        # object we also raise an exception
        if len(field) > 1:
            msg = (
                "You cannot use more than one field the same call. "
                "You should do something like this: {}"
            ).format(fields_str)
            raise ParsingException(msg)

        # Empty queries should NOT have fields or queries
        if self.empty and (field or query):
            raise ParsingException(
                'You cannot pass fields or words to empty queries')

        self.query = query
        self.field = field
        self.evaluated = False
        self.cache = None

    def __str__(self):
        return self.cache if self.evaluated else self._eval()

    def __and__(self, other):
        if self.empty:
            self.cache = str(other)
        else:
            self.cache = '({} AND {})'.format(self, other)
        self.evaluated = True
        self.empty = False
        return self

    def __or__(self, other):
        if self.empty:
            self.cache = str(other)
        else:
            self.cache = '({} OR {})'.format(self, other)
        self.evaluated = True
        self.empty = False
        return self

    def _cast(self, val):
        if isinstance(val, datetime):
            return val.isoformat()
        return str(val)

    def _eval(self):
        # This query is empty, let's return nothing
        if self.empty:
            return ''

        # No specific query was received, let's return everything
        if not self.field and not self.query:
            return '*:*'

        # The user wants to query by a specific field
        if self.field:
            field, val = self.field.items()[0]
            field = '{}:'.format(field)
        else:
            field, val = '', self.query

        # Taking care of values with spaces
        subvalues = self._cast(val).split(' ')
        if len(subvalues) == 1:
            # If we only have one case, it's time to return with the
            # right value
            val = subvalues[0]
            result = field + self._cast(val)

            # If the user needs to boost any fields!
            if self.boost:
                return '{} {}^{}'.format(result, *self.boost)
            return result
        else:
            # If we have more values to handle, we'll use some recursion
            subquery = Query(_empty=True)
            for subvalue in subvalues:
                subquery &= Query(self._cast(subvalue))

        return '{}{}'.format(field, subquery)