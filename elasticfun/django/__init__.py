# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from ..queryset import QuerySet as ElasticFunQuerySet


class ConfManager(object):
    @property
    def connections(self):
        return settings.ELASTICFUN_CONNECTIONS

    @property
    def indexes(self):
        return list(self.connections.keys())


class QuerySet(ElasticFunQuerySet):

    def __init__(self, conf=None):
        conf = conf or ConfManager()
        super(QuerySet, self).__init__(conf=conf)

    def raise_improperly_configured(self, index=None):
        raise ImproperlyConfigured((
            "There's no index called `{}`, the available ones are: {}. "
            "Check the ELASTICFUN_CONNECTIONS variable in your settings "
            "file."
        ).format(index, ', '.join(self.conf.indexes)))
