

from tests.fixtures import DOC_TITLE


def test_get_spreadsheet(sheet_fixture):
    sheet = sheet_fixture
    find_spreadsheet = sheet.drive.get_spreadsheet(DOC_TITLE)
    find_spreadsheet_id = find_spreadsheet.get('id')
    assert find_spreadsheet_id == sheet.spreadsheet.get('spreadsheetId')


def test_negative_get_spreadsheet(sheet_fixture):
    drive = sheet_fixture.drive
    assert not drive.get_spreadsheet('askdjfkasjgjsalkdjkjglkasjdgjljsd')
