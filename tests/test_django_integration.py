from django.core.exceptions import ImproperlyConfigured
from mock import patch

from elasticfun.django import elasticfun
from elasticfun import Query


@patch('elasticfun.django.settings')
def test_connection_settings(settings):
    # Given that I have my settings object with two connections
    settings.ELASTICFUN_CONNECTIONS = {
        'default': {'URL': 'http://localhost:9200'},
        'other_connection': {'URL': 'http://localhost:9200'},
    }

    # When I query the available connections and indexes
    connections = elasticfun.conf.connections.keys()
    indexes = elasticfun.conf.indexes

    # Then I see that it matches exactly what we have in the settings
    # file
    connections.should.equal(settings.ELASTICFUN_CONNECTIONS.keys())
    connections.should.equal(indexes)
    indexes.should.equal(['default', 'other_connection'])


@patch('elasticfun.django.settings')
def test_searching_against_an_invalid_index(settings):
    # Given that I want to query for something on elasticsearch, I need
    # to add some configuration to my settings file.
    settings.ELASTICFUN_CONNECTIONS = {
        'default': {'URL': 'http://localhost:9200'}
    }

    # When I try to perform a search against an unexisting index, then I
    # receive a nice exception telling me what was wrong
    elasticfun.search.when.called_with('something', index='blah').should.throw(
        ImproperlyConfigured,
        "There's no index called `blah`, the available ones are: default. "
        "Check the ELASTICFUN_CONNECTIONS variable in your settings file.")


@patch('elasticfun.django.settings')
@patch('elasticfun.django.pyelasticsearch')
def test_search_api(pyelasticsearch, settings):
    # Given that I want to query for something on elasticsearch, I need
    # to add some configuration to my settings file.
    settings.ELASTICFUN_CONNECTIONS = {
        'default': {'URL': 'http://localhost:9200'}
    }
    pyelasticsearch.ElasticSearch.return_value.search.return_value = \
        'a lot of awesome stuff'

    # When I use the elasticfun.search() method
    results = elasticfun.search('something')

    # Then I see that behinde the scenes it uses the proper connection
    # declared in the django settings and also, the query was performed
    # against the right index
    pyelasticsearch.ElasticSearch.assert_called_once_with(
        'http://localhost:9200')
    pyelasticsearch.ElasticSearch.return_value.search.assert_called_once_with(
        'something', index='default')
    results.should.equal('a lot of awesome stuff')


@patch('elasticfun.django.settings')
@patch('elasticfun.django.pyelasticsearch')
def test_connection_with_index_name(pyelasticsearch, settings):
    # Given that we might want to name a connection with a different
    # string then the one used to identify my indexes
    settings.ELASTICFUN_CONNECTIONS = {
        'default': {'URL': 'http://localhost:9200'},
        'stuff': {'URL': 'http://localhost:9201'}
    }

    # When I query the available connections and indexes
    connections = elasticfun.conf.connections.keys()
    indexes = elasticfun.conf.indexes

    # Then I see that it matches exactly what we have in the settings
    # file, but the indexes are now different, cause we customized the
    # name of the second one.
    connections.should.equal(settings.ELASTICFUN_CONNECTIONS.keys())
    indexes.should.equal(['default', 'stuff'])

    # So, when I query for something using the fun API, I need to pass
    # the connection name or the index name, depending on how I declared
    # them in my settings.
    elasticfun.search('something', index='stuff')

    # Then I see that the pyelasticsearch API made the right calls
    pyelasticsearch.ElasticSearch.assert_called_once_with(
        'http://localhost:9201')
    pyelasticsearch.ElasticSearch.return_value.search.assert_called_once_with(
        'something', index='stuff')


@patch('elasticfun.django.settings')
@patch('elasticfun.django.pyelasticsearch')
def test_searching_with_query_objects(pyelasticsearch, settings):
    settings.ELASTICFUN_CONNECTIONS = {
        'default': {'URL': 'http://localhost:9200'}}

    # Given that I have a query object
    query = Query('ice') & Query('cream')

    # When I pass this query to the search function
    elasticfun.search(query)

    # Then I see that the pyelasticsearch function was called with a
    # string containing the evaluated query
    pyelasticsearch.ElasticSearch.return_value.search.assert_called_once_with(
        '("ice" AND "cream")', index='default')


@patch('elasticfun.django.settings')
@patch('elasticfun.django.pyelasticsearch')
def test_searching_with_dicts(pyelasticsearch, settings):
    settings.ELASTICFUN_CONNECTIONS = {
        'default': {'URL': 'http://localhost:9200'}}

    # Given that I have a query dict
    query = {'query': {'filtered': {'query': {'query_string': 'stuff'}}}}

    # When I pass this query to the search function
    elasticfun.search(query)

    # Then I see that the pyelasticsearch function was called with a
    # string containing the evaluated query
    pyelasticsearch.ElasticSearch.return_value.search.assert_called_once_with(
        query, index='default')
