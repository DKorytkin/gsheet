
import pytest

from gsheet.helpers import get_color, get_range, RowLetterRange


COLORS = [
    ('#000', {'red': 0.0, 'blue': 0.0, 'green': 0.0}),
    ('#f49e42', {
        'red': 0.9568627450980393,
        'blue': 0.2588235294117648,
        'green': 0.6196078431372545
    }),
    ('#122123', {
        'red': 0.07058823529411765,
        'blue': 0.13725490196078433,
        'green': 0.12941176470588234
    }),
    ('red', {'red': 1.0, 'blue': 0.0, 'green': 0.0})
]
RANGES = [
    (('A1:A2', 0), {
        'startColumnIndex': 0,
        'endColumnIndex': 1,
        'startRowIndex': 0,
        'endRowIndex': 2,
        'sheetId': 0
    }),
    (('H1:Z222', 10), {
        'startColumnIndex': 7,
        'endColumnIndex': 26,
        'startRowIndex': 0,
        'endRowIndex': 222,
        'sheetId': 10
    }),
    (('A1:Z222', 999), {
        'startColumnIndex': 0,
        'endColumnIndex': 26,
        'startRowIndex': 0,
        'endRowIndex': 222,
        'sheetId': 999
    }),
]
LAST_TITLE = [
    (['1', '2', '3'], 'C'),
    (['1', ], 'A'),
    (['ids', 'keys', 'values', 'else data'], 'D'),
    (list(range(1, 20)), 'S')
]
NAME_TITLE = [
    (['1', '2', '3'], '2', 'B'),
    (['1', ], '1', 'A'),
    (['ids', 'keys', 'values', 'else data'], 'keys', 'B'),
    (list(range(1, 20)), 12, 'L')
]


@pytest.mark.parametrize('color, ex', COLORS)
def test_get_color(color, ex):
    assert get_color(color) == ex


@pytest.mark.parametrize('params, ex', RANGES)
def test_get_range(params, ex):
    assert get_range(*params) == ex


@pytest.mark.parametrize('params, ex', LAST_TITLE)
def test_get_last_title_column(params, ex):
    r = RowLetterRange(params)
    assert r.get_last_title_column() == ex


@pytest.mark.parametrize('params', [['1', '2'], ['g', 'S', 's'], [1, 23, 4]])
def test_get_first_title_column(params):
    r = RowLetterRange(params)
    assert r.get_first_title_column() == 'A'


@pytest.mark.parametrize('params, current_name, ex', NAME_TITLE)
def test_get_title_column(params, current_name, ex):
    r = RowLetterRange(params)
    assert r.get_title_column(current_name) == ex
