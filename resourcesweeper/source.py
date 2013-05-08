SOURCE_FILE_EXTENSIONS = ['.m', '.plist', '.xib']


class Source():
    def __init__(self, directory, name):
        self.directory = directory
        self.name = name

    def get_path(self):
        return '%s%s' % (self.directory, self.name)

    def __str__(self):
        return '%s%s' % (self.directory, self.name)

    def __unicode__(self):
        return self.__str__()

    def __repr__(self):
        return self.__str__()
