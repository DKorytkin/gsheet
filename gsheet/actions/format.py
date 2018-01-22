
import logging

from gsheet.helpers import get_color, get_range


log = logging.getLogger(__name__)


class SheetFormat(object):

    def __init__(self, service, sheet, sheet_id):
        self.spreadsheet_service = service
        self.spreadsheet = sheet
        self.sheet_id = sheet_id
        self.requests = []

    def format(self, cell_range, user_format):
        """
        :param str cell_range: example 'A1:F1'
        :param dict user_format: example {
            'horizontalAlignment': 'CENTER',
            'verticalAlignment': 'MIDDLE',
            'backgroundColor': {
                'red': 1.0,
                'green': 1.0,
                'blue': 1.0
            },
            'textFormat': {
                'bold': True,
                'foregroundColor': {
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
        log.debug('[Format] {}'.format(req))
        self.requests.append(req)
        return self.requests

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
        self.format(cell_range=cell_range, user_format=r)

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
