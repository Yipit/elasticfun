# -*- coding: utf-8 -*-
from django.core.exceptions import ImproperlyConfigured
from mock import patch, Mock

from elasticfun.django import QuerySet, ConfManager


@patch('elasticfun.django.settings')
def test_connection_settings(settings):
    # Given that I have my settings object with two connections
    settings.ELASTICFUN_CONNECTIONS = {
        'default': {'URL': 'http://localhost:9200'},
        'other_connection': {'URL': 'http://localhost:9200'},
    }

    # When I query the available connections and indexes
    conf = ConfManager()

    # Then I see that it matches exactly what we have in the settings
    # file
    conf.connections.should.equal(settings.ELASTICFUN_CONNECTIONS)
    set(conf.indexes).should.equal({'default', 'other_connection'})


def test_django_search_against_an_invalid_index():

    # Given that I create a Queryset with a conf with two indexes
    conf = Mock(indexes=['default', 'other_index'])
    queryset = QuerySet(conf=conf)

    # When I try to perform a search against an unexisting index, then I
    # receive a nice exception telling me what was wrong
    queryset.search.when.called_with('something', index='blah').should.throw(
        ImproperlyConfigured,
        "There's no index called `blah`, the available ones are: default, other_index. "
        "Check the ELASTICFUN_CONNECTIONS variable in your settings file."
    )
