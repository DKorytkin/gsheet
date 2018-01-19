
import logging
from string import ascii_uppercase

import httplib2
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
from colour import Color

from app_config import parse_config, get_config


log = logging.getLogger(__name__)

sheet_id_generator = (sheet_id for sheet_id in range(5))

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
            'sheetId': next(sheet_id_generator),
            'title': title,
        }
    }
    return sheet_template


def get_doc(doc_title, sheet_title):
    doc = DOC_TEMPLATE.copy()
    doc['properties']['title'] = doc_title
    doc['sheets'].append(create_sheet(sheet_title))
    return doc


def get_color(color_str: str):
    c = Color(color_str)
    return {'red': c.get_red(), 'blue': c.get_blue(), 'green': c.get_green()}


class TableTitle(object):

    def __init__(self):
        self.base_title = get_config('google.base_title')
        self.test_title = get_config('google.test_title')
        self.title = self.base_title + self.test_title

    def get_title_column(self, title):
        number = self.title.index(title)
        return ascii_uppercase[number]

    def get_last_title_column(self):
        number = self.title.index(self.title[-1])
        return ascii_uppercase[number]

    def get_first_title_column(self):
        number = self.title.index(self.title[0])
        return ascii_uppercase[number]


def get_range(cell_range: str, sheet_id: int):
    """
    # Converts string range to GridRange examples:
    #   "A3:B4" -> {
                        sheetId: id of current sheet,
                        startRowIndex: 2,
                        endRowIndex: 4,
                        startColumnIndex: 0,
                        endColumnIndex: 2
                    }
    #   "A5:B"  -> {
                        sheetId: id of current sheet,
                        startRowIndex: 4,
                        startColumnIndex: 0,
                        endColumnIndex: 2
                    }
    :param str cell_range:
    :param int sheet_id:
    :return: _range
    """
    start, end = cell_range.split(":")[0:2]
    _range = {}
    range_az = range(ord('A'), ord('Z') + 1)
    if ord(start[0]) in range_az:
        _range['startColumnIndex'] = ord(start[0]) - ord('A')
        start = start[1:]
    if ord(end[0]) in range_az:
        _range['endColumnIndex'] = ord(end[0]) - ord('A') + 1
        end = end[1:]
    if len(start) > 0:
        _range['startRowIndex'] = int(start) - 1
    if len(end) > 0:
        _range['endRowIndex'] = int(end)
    _range['sheetId'] = sheet_id
    return _range


class GoogleDocs(object):

    def __init__(self, config=None):
        self.config = config if config else parse_config().get('google')
        self._credentials = ServiceAccountCredentials.from_json_keyfile_name(
            filename=self.config.get('secret_file'),
            scopes=self.config.get('services')
        )
        self._http_auth = self._credentials.authorize(httplib2.Http())
        self._sheets = discovery.build('sheets', 'v4', http=self._http_auth)
        self._drive = discovery.build('drive', 'v3', http=self._http_auth)
        self.sheet = Sheet(self._sheets, self._drive)
        self.drive = Drive(self._drive)


class Drive(object):

    def __init__(self, drive):
        self.drive = drive

    def get_spreadsheet(self, name):
        """
        Get last sheet by name
        :param str name: 'test'
        :return:
        """
        res = self.drive.files().list(
            q=f'name="{name}"',
            spaces='drive',
            fields='files(id, name)',
            pageToken=None
        ).execute()
        for file in res.get('files', []):
            return file


class SheetValue(object):

    def __init__(self, service, sheet, title):
        self.spreadsheet_service = service
        self.spreadsheet = sheet
        self.sheet_title = title
        self.table_title = TableTitle()
        self.sheet_body = {'value_input_option': 'USER_ENTERED', 'data': []}

    def add_table_title(self):
        start = self.table_title.get_first_title_column()
        end = self.table_title.get_last_title_column()
        cell_range = f'{start}1:{end}1'
        title = get_config('google.base_title')
        title += get_config('google.test_title')
        self.sheet_body['data'].append(
            {
                'range': f'{self.sheet_title}!{cell_range}',
                'majorDimension': 'ROWS',
                'values': [title]
            }
        )

    def add_row(self, row_number, values):
        """
        :param int row_number: example 1 == first row
        :param list[list] values: example [
            ["This is B2", "This is C2"],
            ["This is B3", "This is C3"]
        ]
        :return:
        """
        start = self.table_title.get_first_title_column()
        end = self.table_title.get_last_title_column()
        cell = f'{self.sheet_title}!{start}{row_number}:{end}{row_number}'
        self.sheet_body['data'].append(
            {
                'range': cell,
                'majorDimension': 'ROWS',
                'values': values
            }
        )

    def apply(self):
        results = self.spreadsheet_service.values().batchUpdate(
            spreadsheetId=self.spreadsheet['spreadsheetId'],
            body=self.sheet_body
        ).execute()
        return results

    def clear(self, range_cell):
        """
        :param str range_cell: exapmle A1:A12
        :return:
        """
        results = self.spreadsheet_service.values().clear(
            spreadsheetId=self.spreadsheet['spreadsheetId'],
            range=f'{self.sheet_title}!{range_cell}',
            body={}
        ).execute()
        return results


class SheetFormat(object):

    def __init__(self, service, sheet, sheet_id):
        self.spreadsheet_service = service
        self.spreadsheet = sheet
        self.sheet_id = sheet_id
        self.table_title = TableTitle()
        self.requests = []

    def _format(self, cell_range, user_format):
        """
        :param str cell_range: example 'A1:F1'
        :param dict user_format: example {
            'horizontalAlignment': 'CENTER',
            'verticalAlignment': 'MIDDLE',
            'backgroundColor': {
                'red': 1.0,
                'green': 1.0,
                'blue': 1.0
            }
            'textFormat': {
                'bold': True,
                foregroundColor: {
                    'red': 1.0,
                    'green': 1.0,
                    'blue': 1.0
                }
            }
        }
        :return:
        """
        req = {
                'repeatCell': {
                    'range': get_range(cell_range, self.sheet_id),
                    'cell': {'userEnteredFormat': user_format},
                    'fields': 'userEnteredFormat'
                }
        }
        log.debug(f'Format {req}')
        self.requests.append(req)
        return self.requests

    def format_title(self, cell_range=None):
        if not cell_range:
            start = self.table_title.get_first_title_column()
            end = self.table_title.get_last_title_column()
            cell_range = f'{start}1:{end}1'
        r = {
            'horizontalAlignment': 'CENTER',
            'verticalAlignment': 'MIDDLE',
            'backgroundColor': get_color('#ccc'),
            'textFormat': {
                'bold': True,
                'foregroundColor': get_color('#000')
            }
        }
        self._format(cell_range=cell_range, user_format=r)

    def format_cell(self, cell_range, b_color='#fff', f_color='#000'):
        r = {
            'horizontalAlignment': 'CENTER',
            'verticalAlignment': 'MIDDLE',
            'backgroundColor': get_color(b_color),
            'textFormat': {
                'bold': True,
                'foregroundColor': get_color(f_color)
            }
        }
        self._format(cell_range=cell_range, user_format=r)

    def merge(self, cell_range: str):
        """
        :param str cell_range: example 'A2:A7'
        :return: self.requests
        """
        self.requests.append(
            {'mergeCells': {
                'range': get_range(cell_range, self.sheet_id),
                'mergeType': 'MERGE_ALL'
            }}
        )
        return self.requests

    def apply(self):
        result = self.spreadsheet_service.batchUpdate(
            spreadsheetId=self.spreadsheet['spreadsheetId'],
            body={'requests': self.requests}
        ).execute()
        self.requests = []
        return result


class SheetCharts(object):

    def __init__(self, service, sheet):
        self.spreadsheet_service = service
        self.spreadsheet = sheet
        self.requests = []

    @staticmethod
    def _get_axis(**kwargs):
        """
        :param kwargs: key title, value position
        :return:
        """
        return [{'position': v, 'title': k} for k, v in kwargs.items()]

    @staticmethod
    def _get_source_range(cell_range, sheet_id):
        """
        :param str cell_range: example 'H1:H28'
        :param int sheet_id:
        :return:
        """
        s = {'sourceRange': {
            'sources': [get_range(cell_range, sheet_id)]
        }}
        return s

    def _get_domains(self, cell_range, sheet_id):
        """
        From sheet title
        :param str cell_range: example A1:A28
        :return:
        """
        return [{'domain': self._get_source_range(cell_range, sheet_id)}]

    def _get_series(self, cell_ranges, sheet_id):
        """
        :param list[str] cell_ranges: example ['A1:A7', 'B1:B7', 'C1:C7']
        :param int sheet_id:
        :return:
        """
        s = [{
            'series': self._get_source_range(cell_range, sheet_id),
            'targetAxis': 'LEFT_AXIS'
        } for cell_range in cell_ranges]
        return s

    def _get_basic_chart(self, domain_cell_range, cell_ranges, sheet_id):
        """
        :param domain_cell_range: example titles A1:A27
        :param cell_ranges: example content ['H1:H27', 'I1:I27', 'J1:J27']
        :param sheet_id: content source sheet
        :return:
        """
        return {
            'chartType': 'COLUMN',
            'legendPosition': 'BOTTOM_LEGEND',
            'axis': self._get_axis(Team='BOTTOM_AXIS', Count='LEFT_AXIS'),
            # TODO get max range
            'domains': self._get_domains(domain_cell_range, sheet_id),
            'series': self._get_series(cell_ranges, sheet_id),
            'headerCount': 1
        }

    def add(self, title, domain_cell_range, cell_ranges, sheet_id):
        """
        :param str title: chart title
        :param domain_cell_range: example titles A1:A27
        :param cell_ranges: example content ['H1:H27', 'I1:I27', 'J1:J27']
        :param sheet_id: content source sheet
        :return:
        """
        s = [{'addChart': {
            'chart': {
                'spec': {
                    'title': title,
                    'basicChart': self._get_basic_chart(
                        domain_cell_range,
                        cell_ranges,
                        sheet_id
                    )
                },
                'position': {
                    'newSheet': True
                }
            }}}]
        self.requests.append(s)
        return s

    def delete(self, chart_ids):
        d = [{'deleteEmbeddedObject': {'objectId': i}} for i in chart_ids]
        self.requests.extend(d)

    def apply(self):
        result = self.spreadsheet_service.batchUpdate(
            spreadsheetId=self.spreadsheet['spreadsheetId'],
            body={'requests': self.requests}
        ).execute()
        self.requests = []
        return result


class Sheet(object):

    def __init__(self, sheets, drive):
        self.drive = drive
        self.spreadsheet_service = sheets.spreadsheets()
        self.spreadsheet = None
        self.sheet_id = None
        self.sheet_title = None

    def create(self, doc_title, sheet_title):
        self.spreadsheet = self.spreadsheet_service.create(
            body=get_doc(doc_title, sheet_title)
        ).execute()
        self.sheet_title = sheet_title
        log.debug(f'[SHEET] created {doc_title}')
        return self.spreadsheet

    def get_spreadsheet(self, spreadsheet_id):
        self.spreadsheet = self.spreadsheet_service.get(
            spreadsheetId=spreadsheet_id
        ).execute()
        log.debug(f'[SHEET] get {self.spreadsheet}')
        return self.spreadsheet

    def shared(self, **kwargs):
        """
        examples:
            {'type': 'anyone', 'role': 'reader'}
            {'type': 'user', 'role': 'writer',
            'emailAddress': 'user@example.com'}
        :param kwargs:
        :return:
        """
        default_role = {'type': 'anyone', 'role': 'reader'}
        shared = self.drive.permissions().create(
            fileId=self.spreadsheet['spreadsheetId'],
            body=default_role if not kwargs else kwargs,
            fields='id'
        ).execute()
        return shared

    @property
    def value(self):
        return SheetValue(
            self.spreadsheet_service,
            self.spreadsheet,
            self.sheet_title
        )

    @property
    def format(self):
        return SheetFormat(
            self.spreadsheet_service,
            self.spreadsheet,
            self.get_sheet(self.sheet_title)
        )

    @property
    def chart(self):
        return SheetCharts(self.spreadsheet_service, self.spreadsheet)

    def add_sheet(self, title):
        r = {'addSheet': {'properties': {'title': title}}}
        result = self.spreadsheet_service.batchUpdate(
            spreadsheetId=self.spreadsheet['spreadsheetId'],
            body={'requests': [r]}
        ).execute()
        self.sheet_title = title
        add_sheet = result['replies'][0]['addSheet']
        self.sheet_id = add_sheet['properties']['sheetId']
        self.get_spreadsheet(self.spreadsheet['spreadsheetId'])
        log.debug(f'[SHEET] added {self.sheet_id} with {title}')
        return result

    def get_sheet(self, title):
        for s in self.spreadsheet['sheets']:
            properties = s['properties']
            if title == properties['title']:
                self.sheet_id = properties['sheetId']
                self.sheet_title = title
                log.debug(f'[SHEET] find {self.sheet_id} by {title}')
                return self.sheet_id

    def get_url(self):
        return self.spreadsheet.get('spreadsheetUrl')

    def delete_sheet(self, sheet_id):
        result = self.spreadsheet_service.batchUpdate(
            spreadsheetId=self.spreadsheet['spreadsheetId'],
            body={'requests': [{'deleteSheet': {'sheetId': sheet_id}}]}
        ).execute()
        log.debug(f'[SHEET] deleted {sheet_id}')
        return result