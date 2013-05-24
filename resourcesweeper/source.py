import os

SOURCE_FILE_EXTENSIONS = ['.m', '.plist', '.xib']


class Source():
    def __init__(self, path):
        self.directory, self.name = os.path.split(path)
        pass

    def get_path(self):
        return os.path.join(self.directory, self.name)

    def __str__(self):
        return os.path.join(self.directory, self.name)

    def __unicode__(self):
        return self.__str__()

    def __repr__(self):
        return self.__str__()
