# -*- coding: utf-8 -*-
# Description: Edge log netdata python.d module


from base import SimpleService
import json
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

priority = 60000
retries = 60
update_every = 10

ORDER = ['queues', 'workers', 'problem_docs', 'process_documents']
CHARTS = {
    'process_documents': {
        'options': [None, 'Processing', 'documents', 'Processing',
                    '', 'line'],
        'lines': [
            ['save', 'saved', 'absolute', 1, 1],
            ['update', 'updated', 'absolute', 1, 1],
            ['skiped', 'skiped', 'absolute', 1, 1],
            ['droped', 'droped', 'absolute', 1, 1],
            ['add_to_resource_items_queue', 'add to queue', 'absolute', 1, 1]
        ]
    },
    'workers': {
        'options': [None, 'Threads', 'threads', 'Threads', '', 'line'],
        'lines': [
            ['workers_count', 'main', 'absolute', 1, 1],
            ['retry_workers_count', 'retry', 'absolute', 1, 1],
            ['filter_workers_count', 'fill', 'absolute', 1, 1]
        ]
    },
    'problem_docs': {
        'options': [None, 'Documents', 'documents', 'Documents',
                    '', 'line'],
        'lines': [
            ['not_actual_docs_count', 'not actual', 'absolute', 1, 1],
            ['not_found_count', 'not found', 'absolute', 1, 1],
            ['add_to_retry', 'add to retry', 'absolute', 1, 1]
        ]
    },
    'queues': {
        'options': [None, 'Queue', 'items', 'Queues', '', 'line'],
        'lines': [
            ['resource_items_queue_size', 'main queue', 'absolute', 1, 1],
            ['retry_resource_items_queue_size', 'retry queue', 'absolute', 1, 1]
        ]
    }
}


class Service(SimpleService):
    def __init__(self, configuration=None, name=None):
        SimpleService.__init__(self, configuration=configuration, name=name)
        self.couch_url = configuration['couch_url']
        self.couch_url_args = '/_changes?descending=true&limit=20&include_docs=true'
        self.resource = configuration['resource']
        if len(self.couch_url) == 0:
            raise Exception('Invalid couch_url')
        self.order = ORDER
        self.definitions = CHARTS
        self.data = {
            'save': 0,
            'update': 0,
            'workers_count': 0,
            'resource_items_queue_size': 0,
            'free_api_clients': 0,
            'exceptions_count': 0,
            'add_to_resource_items_queue': 0,
            'skiped': 0,
            'droped': 0,
            'retry_resource_items_queue_size': 0,
            'filter_workers_count': 0,
            'not_found_count': 0,
            'add_to_retry': 0,
            'retry_workers_count': 0,
            'not_actual_docs_count': 0
        }
        self.seq = 0
        self.repeat_seq_count = 0

    def _get_data(self):
        self.data['save'] = 0
        self.data['update'] = 0
        self.data['workers_count'] = 0
        self.data['resource_items_queue_size'] = 0
        self.data['exceptions_count'] = 0
        self.data['add_to_resource_items_queue'] = 0
        self.data['skiped'] = 0
        self.data['droped'] = 0
        self.data['workers_count'] = 0
        self.data['retry_resource_items_queue_size'] = 0
        self.data['filter_workers_count'] = 0
        self.data['not_found_count'] = 0
        self.data['add_to_retry'] = 0
        self.data['retry_workers_count'] = 0
        self.data['not_actual_docs_count'] = 0

        try:
            response = urllib2.urlopen(self.couch_url +
                                       self.couch_url_args).read()
            docs = json.loads(response)['results']
            for d in reversed(docs):
                if d['doc']['resource'] == self.resource \
                        and d['seq'] > self.seq:
                    self.seq = d['seq']
                    doc = d['doc']
                    self.data['workers_count'] = doc['workers_count']
                    self.data['resource_items_queue_size'] \
                        = doc['resource_items_queue_size']
                    self.data['exceptions_count'] = doc['exceptions_count']
                    self.data['save'] = doc['save_documents']
                    self.data['add_to_resource_items_queue'] \
                        = doc['add_to_resource_items_queue']
                    self.data['skiped'] = doc['skiped']
                    self.data['droped'] = doc['droped']
                    self.data['workers_count'] = doc['workers_count']
                    self.data['retry_resource_items_queue_size'] \
                        = doc['retry_resource_items_queue_size']
                    self.data['filter_workers_count'] \
                        = doc['filter_workers_count']
                    self.data['not_found_count'] = doc['not_found_count']
                    self.data['update'] = doc['update_documents']
                    self.data['add_to_retry'] = doc['add_to_retry']
                    self.data['retry_workers_count'] \
                        = doc['retry_workers_count']
                    self.data['not_actual_docs_count'] \
                        = doc['not_actual_docs_count']
                    break
        except (ValueError, AttributeError):
            return self.data
        return self.data
