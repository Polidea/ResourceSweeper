import os


class IosClass():
    EXTENSIONS = ('.h', '.m')

    def __init__(self, path):
        self.directory, class_name_with_extension = os.path.split(path)
        self.name = os.path.splitext(class_name_with_extension)[0]
        self.used_classes = set()
        self.use_cases = self.__generate_use_cases()
        self.has_m_extension_file = self.__exists_m_file()
        self.has_h_extension_file = self.__exists_h_file()

    def __generate_use_cases(self):
        name = self.name.lower()
        return ('#import "' + name + '.h"',
                '/' + name + '.h',
                '@class ' + name + ';',
                '@protocol ' + name + ';',
                ' : ' + name + ' ',
                '[' + name + ' ',
                '(' + name + '*',
                '(' + name + ' *',
                '    ' + name + '*',
                '    ' + name + ' *',
                '@"' + name + '"')

    def __exists_m_file(self):
        return os.path.isfile(os.path.join(self.directory, self.name + '.m'))

    def __exists_h_file(self):
        return os.path.isfile(os.path.join(self.directory, self.name + '.h'))

    def get_file_paths(self):
        return [os.path.join(self.directory, file_name) for file_name in self.get_file_names()]

    def get_file_names(self):
        file_names = []
        if self.has_m_extension_file:
            file_names.append(self.name + '.m')
        if self.has_h_extension_file:
            file_names.append(self.name + '.h')
        return file_names

    def files_count(self):
        a = 0
        if self.has_m_extension_file:
            a += 1
        if self.has_h_extension_file:
            a += 1
        return a

    def __str__(self):
        return self.__get_path()

    def __get_path(self):
        return os.path.join(self.directory, self.name)

    def __unicode__(self):
        return self.__str__()

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.directory == other.directory and self.name == other.name

    def __hash__(self):
        return hash(self.__get_path())

    def __cmp__(self, other):
        return cmp(str(self), str(other))
