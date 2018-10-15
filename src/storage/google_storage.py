from base_storage import BaseStorage


class GoogleCalendarStorage(BaseStorage):
    '''
    Dummy class which could syncronize
    with a google calendar instance
    '''

    ENGINE_NAME = 'google_storage'

    def __init__(self, engine_name):
        BaseStorage.__init__(self, engine_name)


