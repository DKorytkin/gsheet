
import logging

from helpers import get_range


log = logging.getLogger(__name__)


class SheetCharts(object):

    def __init__(self, service, sheet):
        self.spreadsheet_service = service
        self.spreadsheet = sheet
        self.requests = []

    @staticmethod
    def _get_axis(**kwargs):
        """
        :param kwargs: key title, value position
        :return:
        """
        return [{'position': v, 'title': k} for k, v in kwargs.items()]

    @staticmethod
    def _get_source_range(cell_range, sheet_id):
        """
        :param str cell_range: example 'H1:H28'
        :param int sheet_id:
        :return:
        """
        s = {'sourceRange': {
            'sources': [get_range(cell_range, sheet_id)]
        }}
        return s

    def _get_domains(self, cell_range, sheet_id):
        """
        From sheet title
        :param str cell_range: example A1:A28
        :return:
        """
        return [{'domain': self._get_source_range(cell_range, sheet_id)}]

    def _get_series(self, cell_ranges, sheet_id):
        """
        :param list[str] cell_ranges: example ['A1:A7', 'B1:B7', 'C1:C7']
        :param int sheet_id:
        :return:
        """
        s = [{
            'series': self._get_source_range(cell_range, sheet_id),
            'targetAxis': 'LEFT_AXIS'
        } for cell_range in cell_ranges]
        return s

    def _get_basic_chart(self, domain_cell_range, cell_ranges, sheet_id):
        """
        :param domain_cell_range: example titles A1:A27
        :param cell_ranges: example content ['H1:H27', 'I1:I27', 'J1:J27']
        :param sheet_id: content source sheet
        :return:
        """
        return {
            'chartType': 'COLUMN',
            'legendPosition': 'BOTTOM_LEGEND',
            'axis': self._get_axis(Team='BOTTOM_AXIS', Count='LEFT_AXIS'),
            # TODO get max range
            'domains': self._get_domains(domain_cell_range, sheet_id),
            'series': self._get_series(cell_ranges, sheet_id),
            'headerCount': 1
        }

    def add(self, title, domain_cell_range, cell_ranges, sheet_id):
        """
        :param str title: chart title
        :param domain_cell_range: example titles A1:A27
        :param cell_ranges: example content ['H1:H27', 'I1:I27', 'J1:J27']
        :param sheet_id: content source sheet
        :return:
        """
        s = [{'addChart': {
            'chart': {
                'spec': {
                    'title': title,
                    'basicChart': self._get_basic_chart(
                        domain_cell_range,
                        cell_ranges,
                        sheet_id
                    )
                },
                'position': {
                    'newSheet': True
                }
            }}}]
        self.requests.append(s)
        return s

    def delete(self, chart_ids):
        d = [{'deleteEmbeddedObject': {'objectId': i}} for i in chart_ids]
        self.requests.extend(d)

    def apply(self):
        result = self.spreadsheet_service.batchUpdate(
            spreadsheetId=self.spreadsheet['spreadsheetId'],
            body={'requests': self.requests}
        ).execute()
        self.requests = []
        return result
