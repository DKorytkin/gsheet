
import requests
import pytest
from json_checker import Checker

from gsheet import Sheet
from gsheet.gsheet import get_sheet_body, create_sheet
from gsheet.exceptions import NotExistSpreadsheet, RequiredSheet
from tests.fixtures import SECRET_FILE_PATH, DOC_TITLE
from tests.checker_params import COLOR


CREATE_DOC_NAME = 'test_create_doc'
CREATE_SHEET_NAME = 'test_create_sheet'
TEST_DATA = ['shared', 'value', 'format', 'chart', 'get_url']
TEST_DATA_WITH_PARAM = [
    ('delete_sheet', 1),
    ('get_sheet', 'test'),
    ('add_sheet', 'add_sheet'),
]
EX_CREATE_DOC = {
    'spreadsheetId': str,
    'properties': {
        'title': CREATE_DOC_NAME,
        'locale': 'ru_RU',
        'autoRecalc': 'ON_CHANGE',
        'timeZone': 'Etc/GMT',
        'defaultFormat': {
            'backgroundColor': COLOR,
            'padding': {
                'top': int,
                'right': int,
                'bottom': int,
                'left': int
            },
            'verticalAlignment': 'BOTTOM',
            'wrapStrategy': 'OVERFLOW_CELL',
            'textFormat': {
                'foregroundColor': dict,
                'fontFamily': str,
                'fontSize': int,
                'bold': bool,
                'italic': bool,
                'strikethrough': bool,
                'underline': bool
            }
        }
    },
    'sheets': [
        {
            'properties': {
                'sheetId': int,
                'title': str,
                'index': int,
                'sheetType': 'GRID',
                'gridProperties': {
                    'rowCount': int,
                    'columnCount': int
                }
            }
        }
    ],
    'spreadsheetUrl': str
}
EX_ADD_SHEET = {
    'spreadsheetId': str,
    'replies': [
        {
            'addSheet': {
                'properties': {
                    'sheetId': int,
                    'title': str,
                    'index': int,
                    'sheetType': 'GRID',
                    'gridProperties': {
                        'rowCount': int,
                        'columnCount': int
                    }
                }
            }
        }
    ]
}
EX_SHEET_TEMPLATE = {
    'properties': {
        'sheetType': 'GRID',
        'sheetId': int,
        'title': str,
    }
}
EX_SHEET_BODY = {
    'properties': {
        'title': str,
        'locale': 'ru_RU'
    },
    'sheets': [EX_SHEET_TEMPLATE]
}


@pytest.mark.parametrize('attr', TEST_DATA)
def test_not_exist_spreadsheet(attr):
    sheet = Sheet(SECRET_FILE_PATH)
    with pytest.raises(NotExistSpreadsheet):
        getattr(sheet, attr)()


@pytest.mark.parametrize('method, param', TEST_DATA_WITH_PARAM)
def test_not_exist_spreadsheet_with_params(method, param):
    sheet = Sheet(SECRET_FILE_PATH)
    current_method = getattr(sheet, method)
    with pytest.raises(NotExistSpreadsheet):
        current_method(param)


@pytest.mark.parametrize('method', ['value', 'format'])
def test_required_sheet(method):
    sheet = Sheet(SECRET_FILE_PATH)
    spreadsheet_id = sheet.drive.get_spreadsheet(DOC_TITLE).get('id')
    sheet.get_spreadsheet(spreadsheet_id)
    with pytest.raises(RequiredSheet):
        getattr(sheet, method)()


def test_create_doc():
    sheet = Sheet(SECRET_FILE_PATH)
    res = sheet.create(CREATE_DOC_NAME, CREATE_SHEET_NAME)
    assert sheet.spreadsheet
    assert sheet.sheet_title == CREATE_SHEET_NAME
    assert Checker(EX_CREATE_DOC).validate(res)
    sheet_url = sheet.get_url()
    assert sheet_url
    assert requests.get(sheet_url).ok


def test_add_sheet(sheet_fixture):
    res = sheet_fixture.add_sheet('test_add_sheet')
    assert sheet_fixture.sheet_title == 'test_add_sheet'
    assert Checker(EX_ADD_SHEET).validate(res)


@pytest.mark.parametrize('title', ['test_title', 1221, '1221421'])
def test_create_sheet_template(title):
    assert Checker(EX_SHEET_TEMPLATE).validate(create_sheet(title))


@pytest.mark.parametrize('titles', [('test doc', 'test sheet'), (122, 35325)])
def test_get_sheet_body(titles):
    assert Checker(EX_SHEET_BODY).validate(get_sheet_body(*titles))
