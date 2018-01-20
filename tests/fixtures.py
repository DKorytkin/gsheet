
import pytest

from gsheet import Sheet


@pytest.yield_fixture(scope='session')
def gsheet_fixture():
    s = Sheet()
    s.create(doc_title='Test document', sheet_title='test sheet')
    spreadsheet_id = s.spreadsheet.get('spreadsheetId')
    drive = s.drive
    print('URL', s.get_url())
    yield s
    drive.delete_file(spreadsheet_id)


@pytest.yield_fixture(scope='function')
def sheet_fixture(gsheet_fixture):
    s = gsheet_fixture
    test_sheet_name = 'Sheet from test'
    s.add_sheet(test_sheet_name)
    sheet_id = s.get_sheet(test_sheet_name)
    yield s
    s.delete_sheet(sheet_id)
