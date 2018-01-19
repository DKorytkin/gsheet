
import trafaret as t
from trafaret_config import read_and_validate


CONFIG_TRAFARET = t.Dict({
    'google': t.Dict({
        'secret_file': t.String(),
        'services': t.List(t.String()),
        'doc_template': t.Dict({
            'properties': t.Dict({
                'title': t.String(),
                'locale': t.String(),
                'sheets': t.List(t.Null)
            })
        })
    }),
})


def parse_config():
    app_config = read_and_validate('config.yml', CONFIG_TRAFARET)
    config = app_config.copy()
    return config
