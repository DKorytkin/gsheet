
import logging

from gsheet.app_auth import GoogleAuth
from gsheet.drive import Drive
from gsheet.actions.format import SheetFormat
from gsheet.actions.value import SheetValue
from gsheet.actions.chart import SheetCharts
from gsheet.exceptions import NotExistSpreadsheet, RequiredSheet


log = logging.getLogger(__name__)


DOC_TEMPLATE = {
    'properties': {
        'title': 'Example title',
        'locale': 'ru_RU'
    },
    'sheets': []
}


def create_sheet(title):
    sheet_template = {
        'properties': {
            'sheetType': 'GRID',
            'sheetId': 0,
            'title': title,
        }
    }
    return sheet_template


def get_sheet_body(doc_title, sheet_title):
    """
    :param str doc_title:
    :param str sheet_title:
    :return: dict
    """
    doc = DOC_TEMPLATE.copy()
    doc['properties']['title'] = doc_title
    doc['sheets'].append(create_sheet(sheet_title))
    return doc


class Sheet(object):

    def __init__(self, secret_file_path):
        """
        example: {
            "type": "service_account",
            "project_id": "blahblah",
            "private_key_id": "",
            "private_key": "",
            "client_email": "",
            "client_id": "666",
            "auth_uri": ".../oauth2/auth",
            "token_uri": ".../oauth2/token",
            "auth_provider_x509_cert_url": "...certs",
            "client_x509_cert_url": "...."
        }

        :param secret_file_path:
        """
        self.secret = secret_file_path
        auth = GoogleAuth(self.secret)
        self.drive = Drive(auth.drive())
        self.spreadsheet_service = auth.sheet().spreadsheets()
        self.spreadsheet = None
        self.sheet_id = None
        self.sheet_title = None

    def create(self, doc_title, sheet_title):
        self.spreadsheet = self.spreadsheet_service.create(
            body=get_sheet_body(doc_title, sheet_title)
        ).execute()
        if not self.spreadsheet.get('spreadsheetId'):
            raise NotExistSpreadsheet('Something wrong not created')
        self.sheet_title = sheet_title
        self.shared()
        log.debug('[SHEET] created new google doc {}'.format(doc_title))
        return self.spreadsheet

    def get_spreadsheet(self, spreadsheet_id):
        self.spreadsheet = self.spreadsheet_service.get(
            spreadsheetId=spreadsheet_id
        ).execute()
        if not self.spreadsheet.get('spreadsheetId'):
            raise NotExistSpreadsheet('Not find by {}'.format(spreadsheet_id))
        log.debug('[SHEET] get {}'.format(self.spreadsheet))
        return self.spreadsheet

    def shared(self, **kwargs):
        """
        default: anyone reader
        examples:
            {'type': 'anyone', 'role': 'reader'}
            {'type': 'user', 'role': 'writer',
            'emailAddress': 'user@example.com'}
        :param kwargs:
        :return:
        """
        if not self.spreadsheet.get('spreadsheetId'):
            raise NotExistSpreadsheet()
        default_role = {'type': 'anyone', 'role': 'reader'}
        shared = self.drive.drive.permissions().create(
            fileId=self.spreadsheet['spreadsheetId'],
            body=default_role if not kwargs else kwargs,
            fields='id'
        ).execute()
        return shared

    def value(self):
        if not self.spreadsheet.get('spreadsheetId'):
            raise NotExistSpreadsheet()
        if not self.sheet_title:
            raise RequiredSheet()
        return SheetValue(
            self.spreadsheet_service,
            self.spreadsheet,
            self.sheet_title
        )

    def format(self):
        if not self.spreadsheet.get('spreadsheetId'):
            raise NotExistSpreadsheet()
        if not self.sheet_title:
            raise RequiredSheet()
        return SheetFormat(
            self.spreadsheet_service,
            self.spreadsheet,
            self.get_sheet(self.sheet_title)
        )

    def chart(self):
        if not self.spreadsheet.get('spreadsheetId'):
            raise NotExistSpreadsheet()
        return SheetCharts(self.spreadsheet_service, self.spreadsheet)

    def add_sheet(self, title):
        if not self.spreadsheet.get('spreadsheetId'):
            raise NotExistSpreadsheet()
        r = {'addSheet': {'properties': {'title': title}}}
        result = self.spreadsheet_service.batchUpdate(
            spreadsheetId=self.spreadsheet['spreadsheetId'],
            body={'requests': [r]}
        ).execute()
        self.sheet_title = title
        add_sheet = result['replies'][0]['addSheet']
        self.sheet_id = add_sheet['properties']['sheetId']
        self.get_spreadsheet(self.spreadsheet['spreadsheetId'])
        log.debug('[SHEET] added {} with {}'.format(self.sheet_id, title))
        return result

    def get_sheet(self, title):
        if not self.spreadsheet.get('spreadsheetId'):
            raise NotExistSpreadsheet()
        for s in self.spreadsheet['sheets']:
            properties = s['properties']
            if title == properties['title']:
                self.sheet_id = properties['sheetId']
                self.sheet_title = title
                log.debug('[SHEET] find {}'.format(self.sheet_id))
                return self.sheet_id

    def get_url(self):
        if not self.spreadsheet.get('spreadsheetId'):
            raise NotExistSpreadsheet()
        return self.spreadsheet.get('spreadsheetUrl')

    def delete_sheet(self, sheet_id):
        if not self.spreadsheet.get('spreadsheetId'):
            raise NotExistSpreadsheet()
        result = self.spreadsheet_service.batchUpdate(
            spreadsheetId=self.spreadsheet['spreadsheetId'],
            body={'requests': [{'deleteSheet': {'sheetId': sheet_id}}]}
        ).execute()
        log.debug('[SHEET] deleted {}'.format(sheet_id))
        return result
