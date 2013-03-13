from datetime import datetime
from elasticfun import QueryBuilder


def test_query_all():
    # Given that I have an instance of the query builder
    qb = QueryBuilder()

    # When I query for all the objects
    querystr = str(qb)

    # Then I see that the right query was created
    querystr.should.equal('*:*')


def test_query_single_word():
    # Given that I have an instance of the query builder
    qb = QueryBuilder()

    # When I filter by a certain word
    qb.filter('stuff')

    # Then I see that the right query was created
    str(qb).should.equal('(stuff)')


def test_query_single_field():
    # Given that I have an instance of the query builder
    qb = QueryBuilder()

    # When I filter by a certain field
    qb.filter(brand='blah')

    # Then I see that the right query was created
    str(qb).should.equal('brand:blah')


def test_query_single_boolean_value():
    # Given that I have an instance of the query builder
    qb = QueryBuilder()

    # When I filter by a boolean value
    qb.filter(True)

    # Then I see that the right query was created
    str(qb).should.equal('(True)')


def test_query_single_datetime_value():
    # Given that I have an instance of the query builder
    qb = QueryBuilder()

    # When I filter by a boolean value
    qb.filter(datetime(2013, 3, 13, 1, 32))

    # Then I see that the right query was created with the date
    # converted to a string in the YYYY-mm-ddTHH:MM:SS format
    str(qb).should.equal('(2013-03-13T01:32:00)')


def test_query_with_and():
    # Given that I have an instance of the query builder
    qb = QueryBuilder()

    # When I filter by one word after another
    qb.filter('ice').filter('cream')

    # Then I see that the right query was created with the AND operator
    str(qb).should.equal('((ice) AND (cream))')


def test_query_with_or():
    # Given that I have an instance of the query builder
    qb = QueryBuilder()

    # When I filter by one word and then by another word with the OR
    # operator
    qb.filter('ice').filter_or('cream')

    # Then I see that the right query was created
    str(qb).should.equal('((ice) OR (cream))')


def test_query_with_implicit_and():
    # Given that I have an instance of the query builder
    qb = QueryBuilder()

    # When I filter by two words in the same filter
    qb.filter('ice cream')

    # Then I see that the right query was created with an AND separating
    # the two words
    str(qb).should.equal('((ice) AND (cream))')


def test_query_add_boost():
    # Given that I have an instance of the query builder
    qb = QueryBuilder()

    # When I filter by one word and add a boost to a field
    qb.filter('stuff')
    qb.boost('field', 3)

    # Then I see that the query contains both, the field and the query
    # boosting
    str(qb).should.equal('(stuff) field^3')
