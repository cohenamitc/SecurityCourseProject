import json
import os


class ConfigService(object):
    def __init__(self):
        self.config_types = os.listdir('../../config')

    def _get_config(self, type, field):
        if f'{type}.json' in self.config_types:
            with open(f'../../config/{type}.json', 'r') as f:
                return json.loads(f.read()).get(field, None)
        return None

    def get_main(self, field):
        return self._get_config('main', field)

    def get_messages(self, field):
        return self._get_config('messages', field)
