from mock import patch, Mock

from elasticfun import (
    ConfigMissingException,
    EmptyQuerySetException,
    ImproperlyConfigured,
    Query,
    QuerySet,
    Wrapper
)


def test_create_queryset_with_no_conf():
    QuerySet.when.called_with().should.throw(
        ConfigMissingException,
        'You cannot initialize a queryset without a configuration object.'
    )


def test_create_queryset_with_empty_conf():
    QuerySet.when.called_with({}).should.throw(
        ConfigMissingException,
        'You cannot initialize a queryset without a configuration object.'
    )


def test_searching_against_an_invalid_index():

    # Given that I create a Queryset with a conf with two indexes
    conf = Mock(indexes=['default', 'other_index'])
    queryset = QuerySet(conf=conf)

    # When I try to perform a search against an unexisting index, then I
    # receive a nice exception telling me what was wrong
    queryset.search.when.called_with('something', index='blah').should.throw(
        ImproperlyConfigured,
        "There's no index called `blah`, the available ones are: default, other_index.")


@patch('elasticfun.queryset.pyelasticsearch')
def test_search_api(pyelasticsearch):
    # Given that I want to query for something on elasticsearch, I need
    # to add some configuration to my settings file.
    connections = {
        'default': {'URL': 'http://localhost:9200'}
    }

    conf = Mock(connections=connections, indexes=connections.keys())
    queryset = QuerySet(conf=conf)

    pyelasticsearch.ElasticSearch.return_value.search.return_value = \
        'a lot of awesome stuff'

    # When I use the queryset.search() method
    results = queryset.search('something')

    # Then I see that behinde the scenes it uses the proper connection
    # declared in the django settings and also, the query was performed
    # against the right index
    pyelasticsearch.ElasticSearch.assert_called_once_with(
        'http://localhost:9200')
    pyelasticsearch.ElasticSearch.return_value.search.assert_called_once_with(
        'something', index='default')
    results.should.be.a('elasticfun.queryset.QuerySet')
    results.raw_results.should.equal('a lot of awesome stuff')


@patch('elasticfun.queryset.pyelasticsearch')
def test_connection_with_index_name(pyelasticsearch):
    # Given that we might want to name a connection with a different
    # string then the one used to identify my indexes
    connections = {
        'default': {'URL': 'http://localhost:9200'},
        'stuff': {'URL': 'http://localhost:9201'}
    }
    # When I query the available connections and indexes
    conf = Mock(connections=connections, indexes=connections.keys())
    queryset = QuerySet(conf=conf)

    # So, when I query for something using the API, I need to pass
    # the connection name or the index name, depending on how I declared
    # them in my settings.
    queryset.search('something', index='stuff')

    # Then I see that the pyelasticsearch API made the right calls
    pyelasticsearch.ElasticSearch.assert_called_once_with(
        'http://localhost:9201')
    pyelasticsearch.ElasticSearch.return_value.search.assert_called_once_with(
        'something', index='stuff')


@patch('elasticfun.queryset.pyelasticsearch')
def test_searching_with_query_objects(pyelasticsearch):

    connections = {
        'default': {'URL': 'http://localhost:9200'}}
    conf = Mock(connections=connections, indexes=connections.keys())
    queryset = QuerySet(conf=conf)

    # Given that I have a query object
    query = Query('ice') & Query('cream')

    # When I pass this query to the search function
    queryset.search(query)

    # Then I see that the pyelasticsearch function was called with a
    # string containing the evaluated query
    pyelasticsearch.ElasticSearch.return_value.search.assert_called_once_with(
        '("ice" AND "cream")', index='default')


@patch('elasticfun.queryset.pyelasticsearch')
def test_searching_with_dicts(pyelasticsearch):
    connections = {
        'default': {'URL': 'http://localhost:9200'}}
    conf = Mock(connections=connections, indexes=connections.keys())
    queryset = QuerySet(conf=conf)

    # Given that I have a query dict
    query = {'query': {'filtered': {'query': {'query_string': 'stuff'}}}}

    # When I pass this query to the search function
    queryset.search(query)

    # Then I see that the pyelasticsearch function was called with a
    # string containing the evaluated query
    pyelasticsearch.ElasticSearch.return_value.search.assert_called_once_with(
        query, index='default')


def test_queryset_wrap():
    connections = {
        'default': {'URL': 'http://localhost:9200'}}
    conf = Mock(connections=connections, indexes=connections.keys())
    queryset = QuerySet(conf=conf)

    queryset.wrap('a wrapper')
    queryset.wrap('another wrapper')

    queryset.wrappers.should.be.length_of(2)
    queryset.wrappers.should.equal(['a wrapper', 'another wrapper'])


@patch('elasticfun.queryset.pyelasticsearch')
def test_get_items_without_searching_before(pyelasticsearch):
    # Given that we have a well configured queryset object
    connections = {
        'default': {'URL': 'http://localhost:9200'}}
    conf = Mock(connections=connections, indexes=connections.keys())
    queryset = QuerySet(conf=conf)

    # when the queryset.items() method is called
    # without first calling search
    # it should raise an exception
    queryset.items.when.called_with().should.throw(
        EmptyQuerySetException,
            'This QuerySet object is empty. Make sure a search has '
            'been made before calling the items() method.'
        )


@patch('elasticfun.queryset.pyelasticsearch')
def test_get_items_without_wrap_before(pyelasticsearch):
    # Given that we have a well configured queryset object
    connections = {
        'default': {'URL': 'http://localhost:9200'}}
    conf = Mock(connections=connections, indexes=connections.keys())
    queryset = QuerySet(conf=conf)
    queryset.raw_results = {'hits': {'hits': ['hit1', 'hit2']}}

    # it should return a list of hits
    queryset.items().should.equal(['hit1', 'hit2'])


def test_get_items_after_wrap_calls_match():

    # Given that we have a well configured queryset object
    connections = {
        'default': {'URL': 'http://localhost:9200'}}
    conf = Mock(connections=connections, indexes=connections.keys())
    queryset = QuerySet(conf=conf)
    queryset.raw_results = {'hits': {'hits': ['hit1', 'hit2']}}

    wrapper = Mock()
    wrapper.wrap.return_value = []

    queryset.wrap(wrapper).items()

    wrapper.match.call_count.should.equal(2)
    wrapper.match.assert_any_call('hit1')
    wrapper.match.assert_any_call('hit2')


def test_get_items_after_wrap_calls_wrap():

    # Given that we have a well configured queryset object
    connections = {
        'default': {'URL': 'http://localhost:9200'}}
    conf = Mock(connections=connections, indexes=connections.keys())
    queryset = QuerySet(conf=conf)
    queryset.raw_results = {'hits': {'hits': ['hit1', 'hit2']}}

    wrapper = Mock()
    wrapper.wrap.return_value = []

    queryset.wrap(wrapper).items()

    wrapper.wrap.assert_called_once_with(['hit1', 'hit2'])


def test_get_items_after_wrap_with_more_wrappers():

    # Given that we have a well configured queryset object
    connections = {
        'default': {'URL': 'http://localhost:9200'}}
    conf = Mock(connections=connections, indexes=connections.keys())
    queryset = QuerySet(conf=conf)
    queryset.raw_results = {'hits': {'hits': ['hit1', 'hit2']}}

    wrapper = Mock()
    wrapper.wrap.return_value = []
    wrapper.match = lambda obj: obj == 'hit1'

    wrapper2 = Mock()
    wrapper2.wrap.return_value = []
    wrapper2.match = lambda obj: obj == 'hit2'

    queryset.wrap(wrapper).wrap(wrapper2).items()

    wrapper.wrap.assert_called_once_with(['hit1'])
    wrapper2.wrap.assert_called_once_with(['hit2'])


def test_get_items_ordered_results():

    # Given that we have a well configured queryset object
    connections = {
        'default': {'URL': 'http://localhost:9200'}}
    conf = Mock(connections=connections, indexes=connections.keys())
    queryset = QuerySet(conf=conf)

    hit1 = {'_type': 'type1', '_id': 'some_id', 'value': 'hit1'}
    hit2 = {'_type': 'type2', '_id': 'another_id', 'value': 'hit2'}
    hit3 = {'_type': 'type1', '_id': 'last_id', 'value': 'hit3'}

    queryset.raw_results = {'hits': {'hits': [hit1, hit2, hit3]}}

    wrapper = Wrapper()
    wrapper.wrap = lambda obj: obj
    wrapper.match = lambda obj: obj['_type'] == 'type1'

    wrapper2 = Wrapper()
    wrapper2.wrap = lambda obj: obj
    wrapper2.match = lambda obj: obj['_type'] == 'type2'

    results = queryset.wrap(wrapper).wrap(wrapper2).items()

    results.should.equal([hit1, hit2, hit3])
