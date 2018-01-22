

class NotExistSpreadsheet(Exception):

    def __init__(self, message='First step must be create or get'):
        self.error_message = message

    def __str__(self):
        return self.error_message


class WrongRange(Exception):

    def __init__(self, message='Wrong cell range, example "A1:A10"'):
        self.error_message = message

    def __str__(self):
        return self.error_message


class RequiredSheet(Exception):

    def __init__(self, message='First step must be add or get sheet'):
        self.error_message = message

    def __str__(self):
        return self.error_message
