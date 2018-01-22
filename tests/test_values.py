
import pytest


ROW_DATA = [
    ([1, ['title1', 'title2', 'title3']], {'value_input_option': 'USER_ENTERED', 'data': [{'range': 'Sheet from test!A1:C1', 'majorDimension': 'ROWS', 'values': [['title1', 'title2', 'title3']]}]}),
    ([12, ['1']], {'value_input_option': 'USER_ENTERED', 'data': [{'range': 'Sheet from test!A12:A12', 'majorDimension': 'ROWS', 'values': [['1']]}]})
]


@pytest.mark.parametrize('row_param, ex_result', ROW_DATA)
def test_add_row(sheet_fixture, row_param, ex_result):
    sheet_value = sheet_fixture.value()
    sheet_value.add_row(*row_param)
    assert sheet_value.sheet_body == ex_result
    assert sheet_value.apply()
