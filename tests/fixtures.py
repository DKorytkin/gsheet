
import os

import pytest

from gsheet import Sheet


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SECRET_FILE_PATH = os.path.join(os.path.dirname(BASE_DIR), 'secret_key.json')

DOC_TITLE = 'Test document'
SHEET_TITLE = 'Sheet from test'


@pytest.yield_fixture(scope='session')
def gsheet_fixture():
    s = Sheet(SECRET_FILE_PATH)
    s.create(doc_title=DOC_TITLE, sheet_title='test sheet')
    spreadsheet_id = s.spreadsheet.get('spreadsheetId')
    drive = s.drive
    yield s
    drive.delete_file(spreadsheet_id)


@pytest.yield_fixture(scope='function')
def sheet_fixture(gsheet_fixture):
    s = gsheet_fixture
    s.add_sheet(SHEET_TITLE)
    sheet_id = s.get_sheet(SHEET_TITLE)
    yield s
    s.delete_sheet(sheet_id)
