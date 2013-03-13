import sure
from datetime import datetime
from elasticfun import Query, ParsingException


def test_query_all():
    # When I query for all the objects
    querystr = str(Query())

    # Then I see that the right query was created
    querystr.should.equal('*:*')


def test_empty_query():
    # When I query for nothing
    querystr = str(Query(_empty=True))

    # Then I see that this query object won't return anything just yet
    querystr.should.be.empty


def test_empty_query_should_blowup_with_fields_or_query():
    # When I query for nothing
    Query.when.called_with('blah', _empty=True).should.throw(
        ParsingException,
        'You cannot pass fields or words to empty queries')

    Query.when.called_with(field='blah', _empty=True).should.throw(
        ParsingException,
        'You cannot pass fields or words to empty queries')


def test_mixing_words_and_fields():
    # When I try to filter by both words and fields in the same object,
    # Than I see that it actually raised an exception
    Query.when.called_with('stuff', field='val').should.throw(
        ParsingException,
        "You cannot use both words and fields in the same call. "
        "You should do something like this: qb('stuff') & qb(field='val')")


def test_passing_more_than_one_field():
    # When I try to filter with more than one field in the same object,
    # Than I see that it actually raised an exception
    Query.when.called_with(field1='a', field2='b').should.throw(
        ParsingException,
        "You cannot use more than one field the same call. "
        "You should do something like this: qb(field2='b') & qb(field1='a')")


def test_query_single_word():
    # When I filter by a certain word.
    query = Query('stuff')

    # Then I see that the right query was created
    str(query).should.equal('stuff')


def test_query_single_field():
    # When I filter by a certain field.
    query = Query(brand='blah')

    # Then I see that the right query was created
    str(query).should.equal('brand:blah')


def test_query_single_boolean_value():
    # When I filter by a boolean value
    query = Query(True)

    # Then I see that the right query was created
    str(query).should.equal('True')


def test_query_single_datetime_value():
    # When I filter by a boolean value.
    query = Query(datetime(2013, 3, 13, 1, 32))

    # Then I see that the right query was created with the date
    # converted to a string in the YYYY-mm-ddTHH:MM:SS format
    str(query).should.equal('2013-03-13T01:32:00')


def test_query_with_and():
    # When I filter by one word after another
    query = Query('ice') & Query('cream')

    # Then I see that the right query was created with the AND operator
    str(query).should.equal('(ice AND cream)')


def test_query_with_or():
    # When I filter by one word and then by another word with the OR
    # operator
    query = Query('ice') | Query('cream')

    # Then I see that the right query was created
    str(query).should.equal('(ice OR cream)')


def test_query_with_implicit_and():
    # When I filter by two words in the same filter
    query = Query('ice cream')

    # Then I see that the right query was created with an AND separating
    # the two words
    str(query).should.equal('(ice AND cream)')


def test_query_with_field_and():
    # When I filter by field with more than one value
    query = Query(brand='ice cream')

    # Then I see that the value of the field that contaiend two words
    # was evaluated to an expression
    str(query).should.equal('brand:(ice AND cream)')


def test_query_add_boost():
    # When I filter by one word and add a boost to a field
    query = Query('stuff', _boost=('field', 3))

    # Then I see that the query contains both, the field and the query
    # boosting
    str(query).should.equal('stuff field^3')
