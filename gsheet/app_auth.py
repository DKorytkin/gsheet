
import httplib2
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials


SERVICES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]


class GoogleAuth(object):

    def __init__(self, file_path):
        self._credentials = ServiceAccountCredentials.from_json_keyfile_name(
            filename=file_path,
            scopes=SERVICES
        )
        self._http_auth = self._credentials.authorize(httplib2.Http())

    def sheet(self):
        return discovery.build('sheets', 'v4', http=self._http_auth)

    def drive(self):
        return discovery.build('drive', 'v3', http=self._http_auth)
