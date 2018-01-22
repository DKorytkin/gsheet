
import logging


log = logging.getLogger(__name__)


class Drive(object):

    def __init__(self, drive):
        self.drive = drive

    def delete_file(self, file_id):
        res = self.drive.files().delete(fileId=file_id).execute()
        log.debug('[DRIVE] deleted file {}'.format(file_id))
        return res

    def get_spreadsheet(self, name):
        """
        Get last sheet by name
        :param str name: 'test'
        :return:
        """
        res = self.drive.files().list(
            q='name="{}"'.format(name),
            spaces='drive',
            fields='files(id, name)',
            pageToken=None
        ).execute()
        for file in res.get('files', []):
            log.debug('[DRIVE] find file by name {}'.format(name))
            return file
