
import pytest
from json_checker import Checker, And

from gsheet import Sheet
from gsheet.exceptions import NotExistSpreadsheet

from tests.fixtures import SECRET_FILE_PATH, SHEET_TITLE


EX_RESULT = {
    'value_input_option': 'USER_ENTERED',
    'data': [
        {
            'range': And(str, lambda x: SHEET_TITLE in x),
            'majorDimension': 'ROWS',
            'values': [[str]]
        }
    ]
}

ROW_DATA = [
    ([1, ['title1', 'title2', 'title3']], EX_RESULT),
    ([12, ['1']], EX_RESULT)
]
ROW_RANGE = [
    ([12, ['key1', 'key2']], 'A12:B12'),
    ([1, list(range(1, 20))], 'A1:S1'),
]


@pytest.mark.parametrize('row_param, ex_result', ROW_DATA)
def test_add_row(sheet_fixture, row_param, ex_result):
    sheet_value = sheet_fixture.value()
    sheet_value.add_row(*row_param)
    assert Checker(ex_result).validate(sheet_value.sheet_body )
    assert sheet_value.apply()


@pytest.mark.parametrize('cell', ['A1:A12', 'A22:AH32'])
def test_clear(sheet_fixture, cell):
    sheet_value = sheet_fixture.value()
    assert sheet_value.clear(cell)


@pytest.mark.parametrize('params, ex_result', ROW_RANGE)
def test_get_current_row_range(sheet_fixture, params, ex_result):
    sheet_value = sheet_fixture.value()
    res = sheet_value._get_current_row_range(*params)
    assert res == ex_result


def test_negative_add_value_without_spreadsheet():
    sheet = Sheet(SECRET_FILE_PATH)
    with pytest.raises(NotExistSpreadsheet):
        sheet.value()


def test_negative_add_value_without_sheet():
    # TODO
    pass
