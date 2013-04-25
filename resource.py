import os


class Resource():
    proper_extensions = ['.png', '.jpg', '.jpeg']
    retina_resolution_key = '@2x'

    def __init__(self, directory, file_name):
        self.directory = directory
        self.extension = os.path.splitext(file_name)[-1]
        self.name = self.name = os.path.splitext(file_name)[0]
        self.is_retina = self.decide_if_is_retina()

    def decide_if_is_retina(self):
        if self.name.endswith(self.retina_resolution_key):
            self.name = self.name[:self.name.rfind(self.retina_resolution_key)]
            return True
        else:
            return False

    def get_path(self):
        if self.is_retina:
            return '%s%s%s%s' % (self.directory, self.name, self.retina_resolution_key, self.extension)
        else:
            return '%s%s%s' % (self.directory, self.name, self.extension)

