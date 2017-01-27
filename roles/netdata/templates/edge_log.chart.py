# -*- coding: utf-8 -*-
# Description: Edge log netdata python.d module


from base import LogService

priority = 60000
retries = 60

ORDER = ['documents']
CHARTS = {
    'documents': {
        'options': [None, 'Process documents', 'documents', 'Process documents', '', 'line'],
        'lines': [
            ['save', None, 'absolute', 1, 1],
            ['update', None, 'absolute', 1, 1]
        ]
    }
}


class Service(LogService):
    def __init__(self, configuration=None, name=None):
        LogService.__init__(self, configuration=configuration, name=name)
        self.log_path = configuration['path']
        if len(self.log_path) == 0:
            raise Exception('Invalid log path')
        self.order = ORDER
        self.definitions = CHARTS
        self.data = {
            'save': 0,
            'update': 0
        }

    def _get_data(self):
        self.data['save'] = 0
        self.data['update'] = 0
        try:
            raw = self._get_raw_data()
            if raw is None:
                return None
            elif not raw:
                return self.data
        except (ValueError, AttributeError):
            return None

        for line in raw:
            if 'Save' in line:
                self.data['save'] += 1
            elif 'Update' in line:
                self.data['update'] += 1

        return self.data
