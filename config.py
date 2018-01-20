
import os

import trafaret as t
from trafaret_config import read_and_validate


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, 'config.yml')

CONFIG_TRAFARET = t.Dict({
    'google': t.Dict({
        'secret_file': t.String(),
        'services': t.List(t.String()),
        'doc_template': t.Dict({
            'sheets': t.List(t.Null),
            'properties': t.Dict({
                'title': t.String(),
                'locale': t.String()
            })
        })
    }),
})


def parse_config():
    app_config = read_and_validate(CONFIG_PATH, CONFIG_TRAFARET)
    config = app_config.copy()
    return config
