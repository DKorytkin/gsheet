
import trafaret as t
from trafaret_config import read_and_validate


CONFIG_TRAFARET = t.Dict({
    'google': t.Dict({
        'secret_file': t.String(),
        'services': t.List(t.String()),
    }),
})
