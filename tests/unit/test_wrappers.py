# -*- coding: utf-8 -*-
from elasticfun import Wrapper


def test_wrapper_get_key():

    hit1 = {'_type': 'type1', '_id': 'some_id', 'value': 'hit1'}

    Wrapper.get_key(hit1).should.equal('type1:some_id')


def test_wrapper_match():

    hit1 = {'_type': 'type1', '_id': 'some_id', 'value': 'hit1'}

    Wrapper.match.when.called_with(hit1).should.throw(NotImplementedError)


def test_wrapper_wrap():

    hit1 = {'_type': 'type1', '_id': 'some_id', 'value': 'hit1'}

    Wrapper.wrap.when.called_with(hit1).should.throw(NotImplementedError)
