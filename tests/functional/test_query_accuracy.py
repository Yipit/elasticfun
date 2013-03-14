from . import helper

from elasticfun import Query


def test_query_all():
    # Given that we have a list of indexed documents saved on an empty
    # elasticsearch instance
    helper.flush('default')
    helper.index('default', 'person', {"name": "Joe Tester"})
    helper.index('default', 'person', {"name": "Jessica Coder"})
    helper.refresh('default')

    # When I search for Joe
    results = helper.search(Query())

    # Then I see that the results matched our expectation
    results.should.equal([
        {"name": "Joe Tester"},
        {"name": "Jessica Coder"}
    ])


def test_query_single_word_no_results():
    # Given that we have a list of indexed documents saved on an empty
    # elasticsearch instance
    helper.flush('default')
    helper.index('default', 'person', {"name": "Joe Tester"})
    helper.index('default', 'person', {"name": "Jessica Coder"})
    helper.refresh('default')

    # When I search for something that does NOT exist in ES
    results = helper.search(Query('something'))

    # Then I see that the results are empty
    results.should.be.empty


def test_query_single_word():
    # Given that we have a list of indexed documents saved on an empty
    # elasticsearch instance
    helper.flush('default')
    helper.index('default', 'person', {"name": "Joe Tester"})
    helper.index('default', 'person', {"name": "Jessica Coder"})
    helper.refresh('default')

    # When I search for Joe
    results = helper.search(Query('joe'))

    # Then I see that the results matched our expectation
    results.should.equal([{"name": "Joe Tester"}])


def test_query_single_field_no_results():
    # Given that we have a list of indexed documents saved on an empty
    # elasticsearch instance
    helper.flush('default')
    helper.index('default', 'person', {"name": "Joe Tester"})
    helper.index('default', 'person', {"name": "Jessica Coder"})
    helper.refresh('default')

    # When I search for something that does NOT exist
    results = helper.search(Query(name='something'))

    # Then I see that the results were empty
    results.should.be.empty


def test_query_single_field():
    # Given that we have a list of indexed documents saved on an empty
    # elasticsearch instance
    helper.flush('default')
    helper.index('default', 'person', {"name": "Joe Tester"})
    helper.index('default', 'person', {"name": "Jessica Coder"})
    helper.refresh('default')

    # When I search for Joe
    results = helper.search(Query(name='jessica'))

    # Then I see that the results matched our expectation
    results.should.equal([{"name": "Jessica Coder"}])


def test_query_single_correct_field():
    # Given that we have a list of indexed documents saved on an empty
    # elasticsearch instance
    helper.flush('default')
    helper.index(
        'default', 'person',
        {"name": "Joe Tester", 'sister': "Jessica Noncoder"})
    helper.index(
        'default', 'person',
        {"name": "Jessica Coder", 'sister': "Lincoln Worker"})
    helper.refresh('default')

    # When I search for Joe
    results = helper.search(Query(name='jessica'))

    # Then I see that the results matched our expectation
    results.should.equal([
        {"name": "Jessica Coder", 'sister': "Lincoln Worker"}
    ])

    # When I search for Joe
    results = helper.search(Query(name='jessica'))

    # Then I see that the results matched our expectation
    results.should.equal([{
        "name": "Jessica Coder", 'sister': 'Lincoln Worker'}])


def test_query_with_and():
    # Given that we have a list of indexed documents saved on an empty
    # elasticsearch instance
    helper.flush('default')
    helper.index('default', 'person', {"name": "Joe Tester"})
    helper.index('default', 'person', {"name": "Jessica Coder"})
    helper.refresh('default')

    # When I search for Joe
    results = helper.search(Query('jessica') & Query('coder'))

    # Then I see that the results matched our expectation
    results.should.equal([{"name": "Jessica Coder"}])


def test_query_with_and_all_words_crossfield():
    # Given that we have a list of indexed documents saved on an empty
    # elasticsearch instance
    helper.flush('default')
    helper.index(
        'default', 'person',
        {"name": "Joe Tester", 'sister': "Jessica Noncoder"})
    helper.index(
        'default', 'person',
        {"name": "Jessica Coder", 'sister': "Lincoln Worker"})
    helper.refresh('default')

    # When I search for Joe
    results = helper.search(Query('jessica') & Query('coder'))

    # Then I see that the results matched our expectations
    # This is the only result since all are single values
    # enclosed within quotes
    results.should.equal([
        {"name": "Jessica Coder", 'sister': "Lincoln Worker"}
    ])


def test_query_with_and_across_fields():
    # Given that we have a list of indexed documents saved on an empty
    # elasticsearch instance
    helper.flush('default')
    helper.index(
        'default', 'person',
        {"name": "Joe Tester", 'sister': "Jessica Noncoder"})
    helper.index(
        'default', 'person',
        {"name": "Jessica Coder", 'sister': "Lincoln Worker"})
    helper.refresh('default')

    # When I search for Joe
    results = helper.search(Query('jessica') & Query('Worker'))

    # Then I see that the results matched our expectation
    results.should.equal([
        {"name": "Jessica Coder", 'sister': "Lincoln Worker"}
    ])
