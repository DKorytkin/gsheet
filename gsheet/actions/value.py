
import logging

from gsheet.helpers import RowLetterRange


log = logging.getLogger(__name__)


class SheetValue(object):

    def __init__(self, service, sheet, title):
        self.spreadsheet_service = service
        self.spreadsheet = sheet
        self.sheet_title = title
        self.sheet_body = {'value_input_option': 'USER_ENTERED', 'data': []}

    @staticmethod
    def _get_current_row_range(row_number, values):
        t = RowLetterRange(values)
        start = t.get_first_title_column()
        end = t.get_last_title_column()
        row_range = '{start}{start_row}:{end}{end_row}'.format(
            start=start,
            end=end,
            start_row=row_number,
            end_row=row_number
        )
        log.debug('[VALUE] get row range {}'.format(row_range))
        return row_range

    def add_row(self, row_number, values):
        """
        :param int row_number: example 1 == first row
        :param list[list] values: example [
            ["This is B2", "This is C2"],
            ["This is B3", "This is C3"]
        ]
        :return:
        """
        row_range = self._get_current_row_range(row_number, values)
        self.sheet_body['data'].append(
            {
                'range': '{}!{}'.format(self.sheet_title, row_range),
                'majorDimension': 'ROWS',
                'values': [values]
            }
        )
        log.debug('[VALUE] add {}'.format(values))

    def apply(self):
        results = self.spreadsheet_service.values().batchUpdate(
            spreadsheetId=self.spreadsheet['spreadsheetId'],
            body=self.sheet_body
        ).execute()
        log.debug('[VALUE] apply')
        return results

    def clear(self, range_cell):
        """
        :param str range_cell: exapmle A1:A12
        :return:
        """
        results = self.spreadsheet_service.values().clear(
            spreadsheetId=self.spreadsheet['spreadsheetId'],
            range='{}!{}'.format(self.sheet_title, range_cell),
            body={}
        ).execute()
        return results
