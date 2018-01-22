
import os

import trafaret as t
from trafaret_config import read_and_validate


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SECRET_FILE_PATH = os.path.join(BASE_DIR, 'secret_key.json')
