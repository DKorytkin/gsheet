
from json_checker import Or

RANGE = {
    'startColumnIndex': int,
    'endColumnIndex': int,
    'startRowIndex': int,
    'endRowIndex': int,
    'sheetId': int
}
COLOR = {
    'red': Or(float, int),
    'blue': Or(float, int),
    'green': Or(float, int),
}
