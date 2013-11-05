# -*- coding: utf-8 -*-
from elasticfun import Query


def test_user_input_empty():
    query = Query.from_user_input('')

    str(query).should.equal('*:*')


def test_user_input_simple():
    query = Query.from_user_input('simple')

    str(query).should.equal('"simple"')


def test_user_input_with_spaces_around_it():
    query = Query.from_user_input(' simple ')

    str(query).should.equal('"simple"')


def test_user_input_two_words_and():
    query = Query.from_user_input('ice cream', default_op='AND')

    str(query).should.equal('("ice" AND "cream")')


def test_user_input_with_two_words_and_double_spaces_between_them():
    query = Query.from_user_input('ice  cream', default_op='AND')

    str(query).should.equal('("ice" AND "cream")')


def test_user_input_two_words_or():
    query = Query.from_user_input('ice cream', default_op='OR')

    str(query).should.equal('("ice" OR "cream")')
