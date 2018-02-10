
import logging
from string import ascii_uppercase

from colour import Color

from gsheet.exceptions import WrongRange


log = logging.getLogger(__name__)


def get_color(color_str: str):
    c = Color(color_str)
    return {'red': c.get_red(), 'blue': c.get_blue(), 'green': c.get_green()}


def get_range(cell_range: str, sheet_id: int):
    """
    # Converts string range to GridRange examples:
    #   "A3:B4" -> {
                        sheetId: id of current sheet,
                        startRowIndex: 2,
                        endRowIndex: 4,
                        startColumnIndex: 0,
                        endColumnIndex: 2
                    }
    #   "A5:B"  -> {
                        sheetId: id of current sheet,
                        startRowIndex: 4,
                        startColumnIndex: 0,
                        endColumnIndex: 2
                    }
    :param str cell_range:
    :param int sheet_id:
    :return: _range
    """
    if ':' not in cell_range:
        raise WrongRange()
    start, end = cell_range.split(":")
    _range = {}
    range_az = range(ord('A'), ord('Z') + 1)
    if ord(start[0]) in range_az:
        _range['startColumnIndex'] = ord(start[0]) - ord('A')
        start = start[1:]
    if ord(end[0]) in range_az:
        _range['endColumnIndex'] = ord(end[0]) - ord('A') + 1
        end = end[1:]
    if len(start) > 0:
        _range['startRowIndex'] = int(start) - 1
    if len(end) > 0:
        _range['endRowIndex'] = int(end)
    _range['sheetId'] = sheet_id
    return _range


class RowLetterRange(object):

    def __init__(self, title):
        """
        :param list title: example ['id', 'key', 'value']
        """
        self.title = title

    @staticmethod
    def _index_to_letter(number):
        """
        For example:
            1 > "A"
            12 > "L"
            123 > "DS"
            1234 > "AUL"
        :param int number:
        :return: str title:
        """
        title = ''
        while number:
            mod = (number - 1) % len(ascii_uppercase)
            number = int((number - mod) / len(ascii_uppercase))
            title += ascii_uppercase[mod]
        return title[::-1]

    @staticmethod
    def get_first_title_column():
        return ascii_uppercase[0]

    def get_title_column(self, title):
        number = self.title.index(title) + 1
        return self._index_to_letter(number)

    def get_last_title_column(self):
        return self._index_to_letter(len(self.title))
