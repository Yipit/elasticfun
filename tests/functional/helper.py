import pyelasticsearch


conn = pyelasticsearch.ElasticSearch('http://localhost:9200')


def flush(index_name):
    try:
        conn.delete_index('test_{}'.format(index_name))
    except (pyelasticsearch.ElasticHttpNotFoundError,
        pyelasticsearch.ConnectionError):
        pass


def refresh(index_name):
    conn.refresh('test_{}'.format(index_name))


def index(index_name, type_, data):
    conn.index('test_{}'.format(index_name), type_, data)


def search(query, index='test_default', sort_func=None):
    results = conn.search(str(query), index=index)

    # Making it simpler to test the results. We don't care about the
    # other metadata that elasticsearch returns
    if results:
        results = [x['_source'] for x in results['hits']['hits']]

    # The user can sort the results by providing a sort function
    if sort_func:
        results.sort(key=sort_func)
    return results
