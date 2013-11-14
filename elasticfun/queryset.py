# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from collections import defaultdict
import pyelasticsearch

from .exceptions import (
    ImproperlyConfigured,
    ConfigMissingException,
    EmptyQuerySetException
)
from .query import Query


class QuerySet(object):

    def __init__(self, conf=None):
        if not conf:
            raise ConfigMissingException(
                    'You cannot initialize a queryset without a configuration object.'
                    )

        self.conf = conf
        self.raw_results = None
        self.wrappers = []

    def raise_improperly_configured(self, index=None):
        raise ImproperlyConfigured((
            "There's no index called `{}`, the available ones are: {}."
        ).format(index, ', '.join(self.conf.indexes)))

    def search(self, query, index='default', **kwargs):
        """
        kwargs supported are the parameters listed at:
            http://www.elasticsearch.org/guide/reference/api/search/request-body/
        Namely: timeout, from, size and search_type.
        IMPORTANT: prepend ALL keys with "es_" as pyelasticsearch requires this
        """
        # Looking up the index
        if index not in self.conf.indexes:
            self.raise_improperly_configured(index=index)

        # Calling the backend search method
        esurl = self.conf.connections[index]['URL']
        esinst = pyelasticsearch.ElasticSearch(esurl)

        query = isinstance(query, Query) and str(query) or query
        self.raw_results = esinst.search(query, index=index, **kwargs)

        return self

    def count(self):
        if not self.raw_results:
            return 0
        return self.raw_results['hits']['total']

    def max_score(self):
        if not self.raw_results:
            return 0
        return self.raw_results['hits']['max_score']

    def wrap(self, wrapper):
        self.wrappers.append(wrapper)
        return self

    def items(self, clean=True):
        if self.raw_results is None:
            raise EmptyQuerySetException(
                'This QuerySet object is empty. Make sure a search has '
                'been made before calling the items() method.'
            )

        hits = self.raw_results['hits']['hits'][:]
        if not self.wrappers:
            return hits

        _order_dict = {}
        _type_dict = defaultdict(list)

        for wrapper in self.wrappers:
            for hit_order, hit in enumerate(hits):
                if wrapper.match(hit):
                    _type_dict[wrapper].append(hit)
                    _order_dict[wrapper.get_key(hit)] = hit_order

        # Creating a list of None items of length == len(hits)
        # This will be useful for correctly placing the wrapped object
        # in the sorted order, as well as gives us an indication of
        # what objects did not get wrapped correctly due to database / ES
        # index inconsistencies
        processed_results = [None] * len(hits)
        for wrapper, typed_results in _type_dict.items():
            wrapped_hits = wrapper.wrap(typed_results)
            for hit in wrapped_hits:
                index = _order_dict[wrapper.get_key(hit)]
                processed_results[index] = hit

        if clean:
            processed_results = list(filter(lambda val: val is not None, processed_results))

        return processed_results
