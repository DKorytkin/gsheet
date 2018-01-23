
import pytest
from json_checker import Checker

from tests.checker_params import RANGE


AXIS_DATA = [
    (
        {'k': 'ss', 'k1': 'sss1'},
        [{'position': 'ss', 'title': 'k'}, {'position': 'sss1', 'title': 'k1'}]
    ),
    (
        {'key1': 'value1'},
        [{'position': 'value1', 'title': 'key1'}]
    )
]
BASE_CHAR_DATA = [
    ('A1:H12', ['A2:H2'], 1),
    ('A1:A22', ['A2:H22', 'B2:B22'], 12),
]
ADD_DATA = [
    ('TEST title', 'A1:H12', ['A2:H2'], 1),
    ('TEST title 11', 'A1:A22', ['A2:H22', 'B2:B22'], 12),
]
EX_AXIS = [{'position': str, 'title': str}]
EX_SOURCE_RANGE = {'sourceRange': {'sources': [RANGE]}}
EX_DOMAINS = [{'domain': EX_SOURCE_RANGE}]
EX_SERIES = [{'series': EX_SOURCE_RANGE, 'targetAxis': 'LEFT_AXIS'}]
EX_BASE_CHAR = {
    'chartType': 'COLUMN',
    'legendPosition': 'BOTTOM_LEGEND',
    'axis': EX_AXIS,
    'domains': EX_DOMAINS,
    'series': EX_SERIES,
    'headerCount': int
}
EX_ADD = [
    {'addChart': {
        'chart': {
            'spec': {'title': str, 'basicChart': EX_BASE_CHAR},
            'position': {'newSheet': True}
        }
    }}
]
EX_DELETE = [{'deleteEmbeddedObject': {'objectId': int}}]
EX_APPLY = []


@pytest.mark.parametrize('params, ex_result', AXIS_DATA)
def test_get_axis(sheet_fixture, params, ex_result):
    sheet_chart = sheet_fixture.chart()
    assert sheet_chart._get_axis(**params) == ex_result


@pytest.mark.parametrize('params', [('A1:A11', 1), ('A4:G15', 44)])
def test_get_source_range(sheet_fixture, params):
    sheet_chart = sheet_fixture.chart()
    res = sheet_chart._get_source_range(*params)
    assert Checker(EX_SOURCE_RANGE).validate(res)


@pytest.mark.parametrize('params', [('A1:A11', 1), ('A4:G15', 44)])
def test_get_domains(sheet_fixture, params):
    sheet_chart = sheet_fixture.chart()
    assert Checker(EX_DOMAINS).validate(sheet_chart._get_domains(*params))


@pytest.mark.parametrize('params', [(['A1:A11'], 1), (['A4:G15', 'A1:A2'], 4)])
def test_get_series(sheet_fixture, params):
    sheet_chart = sheet_fixture.chart()
    assert Checker(EX_SERIES).validate(sheet_chart._get_series(*params))


@pytest.mark.parametrize('params', BASE_CHAR_DATA)
def test_get_basic_chart(sheet_fixture, params):
    sheet_chart = sheet_fixture.chart()
    res = sheet_chart._get_basic_chart(*params)
    assert Checker(EX_BASE_CHAR).validate(res)


@pytest.mark.parametrize('params', ADD_DATA)
def test_add(sheet_fixture, params):
    sheet_chart = sheet_fixture.chart()
    assert Checker(EX_ADD).validate(sheet_chart.add(*params))
    assert sheet_chart.requests


@pytest.mark.parametrize('ids', [[1], list(range(100))])
def test_delete_char(sheet_fixture, ids):
    sheet_chart = sheet_fixture.chart()
    sheet_chart.delete(ids)
    assert Checker(EX_DELETE).validate(sheet_chart.requests)


@pytest.mark.skip('Must be develop')
def test_apply_char(sheet_fixture):
    sheet_chart = sheet_fixture.chart()
    assert Checker(EX_APPLY).validate(sheet_chart.apply())
    assert not sheet_chart.requests
