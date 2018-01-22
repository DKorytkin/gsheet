
import pytest
from json_checker import Checker

from gsheet import Sheet
from gsheet.exceptions import NotExistSpreadsheet

from tests.fixtures import SECRET_FILE_PATH
from tests.checker_params import RANGE, COLOR


EX_RESULT = [
    {'repeatCell': {
        'range': RANGE,
        'cell': {
            'userEnteredFormat': {
                'horizontalAlignment': 'CENTER',
                'verticalAlignment': 'MIDDLE',
                'backgroundColor': COLOR,
                'textFormat': {
                    'bold': bool,
                    'foregroundColor': COLOR
                }
            }
        },
        'fields': 'userEnteredFormat'
    }}
]
EX_MERGE_RESULT = [{'mergeCells': {'range': RANGE, 'mergeType': 'MERGE_ALL'}}]

FORMAT_PARAMS = [
    (dict(cell_range='A1:A12', b_color='#fff', f_color='#000'), EX_RESULT),
    (dict(cell_range='A1:A12'), EX_RESULT),
    (dict(cell_range='A1:A2', b_color='#666', f_color='#215123'), EX_RESULT),
]


@pytest.mark.parametrize('params, ex_result', FORMAT_PARAMS)
def test_format_cell(sheet_fixture, params, ex_result):
    sheet_format = sheet_fixture.format()
    sheet_format.format_cell(**params)
    assert Checker(ex_result).validate(sheet_format.requests)
    assert sheet_format.apply()
    assert not sheet_format.requests


@pytest.mark.parametrize('cell', ['A1:A12', 'A12:H12'])
def test_merge_cell(sheet_fixture, cell):
    sheet_format = sheet_fixture.format()
    sheet_format.merge(cell)
    assert Checker(EX_MERGE_RESULT).validate(sheet_format.requests)
    assert sheet_format.apply()
    assert not sheet_format.requests


def test_negative_format_without_spreadsheet():
    sheet = Sheet(SECRET_FILE_PATH)
    with pytest.raises(NotExistSpreadsheet):
        sheet.format()


def test_negative_format_without_sheet():
    # TODO
    pass
