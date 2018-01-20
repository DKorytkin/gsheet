
import os

import httplib2
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

from config import BASE_DIR


class GoogleAuth(object):

    def __init__(self, config):
        self.config = config.get('google')
        self._credentials = ServiceAccountCredentials.from_json_keyfile_name(
            filename=os.path.join(BASE_DIR, self.config.get('secret_file')),
            scopes=self.config.get('services')
        )
        self._http_auth = self._credentials.authorize(httplib2.Http())

    def sheet(self):
        return discovery.build('sheets', 'v4', http=self._http_auth)

    def drive(self):
        return discovery.build('drive', 'v3', http=self._http_auth)
