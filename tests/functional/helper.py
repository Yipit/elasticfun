import pyelasticsearch


conn = pyelasticsearch.ElasticSearch('http://localhost:9200')


def flush(index_name):
    conn.delete_index('test_{}'.format(index_name))


def refresh(index_name):
    conn.refresh('test_{}'.format(index_name))


def index(index_name, type_, data):
    conn.index('test_{}'.format(index_name), type_, data)


def search(query, index='test_default'):
    results = conn.search(str(query), index=index)
    if results:
        results = [x['_source'] for x in results['hits']['hits']]
    return results
