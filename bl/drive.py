

class Drive(object):

    def __init__(self, drive):
        self.drive = drive

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
            return file
