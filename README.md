# elasticfun

A small set of tools to make it easier and fun to use pyelasticsearch.
Our main goals here are:

 * Provide an easy and consistent way to build queries
 * Hook up a connection manager to the django settings system
 
Some of our long term goals

 * An API to declare indexes and fields
 * A set of commands to manage (update, rebuild, clean) indexes

## The Query object

This API aims to give you a pleasant way to build even complex queries
for elasticsearch. The following snippet demonstrates how it works:

```python
>>> query = (Query('fitness') & (Query(category='Accessories') | Query(category='Sport Wear')))
>>> str(query)
'(fitness AND (category:Accessories OR category:(Sport AND Wear)))')
```

## Test coverage

The very first line of this library was a unit-test, it was completely
written under the TDD concepts and we're planning to keep it that way.
If you're willing to send a patch to our humble project, please ensure
that the coverage won't decrease at all.

Also, I strongly suggest you to start your proposed feature or bug fix
by writing the tests. It will certainly decrease the complexibility of
the actual and thus improve it's quality.