import sure
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

    # When I filter by a certain word.
    query = qb('stuff')

    # Then I see that the right query was created
    str(query).should.equal('stuff')


def test_query_single_field():
    # Given that I have an instance of the query builder
    qb = QueryBuilder()

    # When I filter by a certain field.
    query = qb(brand='blah')

    # Then I see that the right query was created
    str(query).should.equal('brand:blah')


def test_query_single_boolean_value():
    # Given that I have an instance of the query builder
    qb = QueryBuilder()

    # When I filter by a boolean value
    query = qb(True)

    # Then I see that the right query was created
    str(query).should.equal('True')


def test_query_single_datetime_value():
    # Given that I have an instance of the query builder
    qb = QueryBuilder()

    # When I filter by a boolean value.
    query = qb(datetime(2013, 3, 13, 1, 32))

    # Then I see that the right query was created with the date
    # converted to a string in the YYYY-mm-ddTHH:MM:SS format
    str(query).should.equal('2013-03-13T01:32:00')


def test_query_with_and():
    # Given that I have an instance of the query builder
    qb = QueryBuilder()

    # When I filter by one word after another
    query = qb('ice') & qb('cream')

    # Then I see that the right query was created with the AND operator
    str(query).should.equal('ice AND cream')


def test_query_with_or():
    # Given that I have an instance of the query builder
    qb = QueryBuilder()

    # When I filter by one word and then by another word with the OR
    # operator
    query = qb('ice') | ('cream')

    # Then I see that the right query was created
    str(query).should.equal('ice OR cream')


def test_query_with_implicit_and():
    # Given that I have an instance of the query builder
    qb = QueryBuilder()

    # When I filter by two words in the same filter
    query = qb('ice cream')

    # Then I see that the right query was created with an AND separating
    # the two words
    str(query).should.equal('ice AND cream')


def test_query_add_boost():
    # Given that I have an instance of the query builder
    qb = QueryBuilder()

    # When I filter by one word and add a boost to a field
    query = qb('stuff', boost=('field', 3))

    # Then I see that the query contains both, the field and the query
    # boosting
    str(query).should.equal('stuff field^3')
