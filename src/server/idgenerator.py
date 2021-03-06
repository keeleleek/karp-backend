import elasticsearch
from elasticsearch_dsl import Index, Mapping
import logging
import src.server.helper.configmanager as configM


# SAOL stopped at 508133 when imported to Karp (set start to that number)
def create_sequence_index(index_name='', start=''):
    es = configM.elastic(mode=index_name)
    sequence_index = Index("sequence", using=es)
    if sequence_index.exists():
        logging.debug('sequence id %s already exists' % index_name)

    else:
        logging.debug('create sequence id %s starting at %s' % (index_name, start or 0))
        sequence_index.settings(
            number_of_shards=1,
            number_of_replicas=0
        )
        sequence_index.create()

        m = Mapping("sequence")
        m.meta("_all", enabled=False)
        m.meta("_source", enabled=False)
        m.save("sequence", using=es)

    if start:
        tasks = ('{"index": {"_index": "sequence", "_type": "sequence", "_id": "%s", "version": "%s", "version_type": "external"}}\n{}\n' %
                 (index_name, start))
        result = es.bulk(body=tasks)
        logging.debug('sequence id starting at %s: %s' % (start, result))
        return result


def reset_sequence(index_name):
    es = configM.elastic(mode=index_name)
    try:
        es.delete(index="sequence", doc_type="sequence", id=index_name)
    except elasticsearch.exceptions.NotFoundError:
        pass


def get_id_sequence(index_name, size):
    tasks = "".join(['{"index": {"_index": "sequence", "_type": "sequence", "_id": "' + index_name + '"}}\n{}\n' for _ in range(0, size)])
    es = configM.elastic(mode=index_name)
    result = es.bulk(body=tasks)
    for item in result['items']:
        yield item["index"]["_version"]


# if __name__ == '__main__':
#     #create_sequence_index('saol', 508133)
#     for _id in get_id_sequence('saol', 5):
#         print _id
