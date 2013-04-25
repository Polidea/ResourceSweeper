SOURCE_FILE_EXTENSIONS = ['.m']


class Source():
    def __init__(self, directory, name):
        self.directory = directory
        self.name = name

    def get_path(self):
        return '%s%s' % (self.directory, self.name)