# -*- coding: utf-8 -*-
import pyelasticsearch
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from .. import Query

__all__ = 'elasticfun',


class ConfManager(object):
    @property
    def connections(self):
        return settings.ELASTICFUN_CONNECTIONS

    @property
    def indexes(self):
        return settings.ELASTICFUN_CONNECTIONS.keys()


class ElasticFun(object):

    conf = ConfManager()

    def search(self, query, index='default'):
        # Looking up the index
        if index not in self.conf.indexes:
            raise ImproperlyConfigured((
                "There's no index called `{}`, the available ones are: {}. "
                "Check the ELASTICFUN_CONNECTIONS variable in your settings "
                "file."
            ).format(index, ', '.join(self.conf.indexes)))

        # Calling the backend search method
        esurl = self.conf.connections[index]['URL']
        esinst = pyelasticsearch.ElasticSearch(esurl)
        query = isinstance(query, Query) and str(query) or query
        return esinst.search(query, index=index)

elasticfun = ElasticFun()
