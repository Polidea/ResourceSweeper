CLASS_EXTENSIONS = ['.h', '.m']

import os


class IosClass():
    def __init__(self, directory, class_name_with_extension):
        self.directory = directory
        self.name = os.path.splitext(class_name_with_extension)[0]
        self.used_classes = set()
        self.use_cases = self.generate_use_cases()
        self.has_m_extension_file = self.exists_m_file()
        self.has_h_extension_file = self.exists_h_file()

    def generate_use_cases(self):
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

    def exists_m_file(self):
        return os.path.isfile(self.directory + self.name + '.m')

    def exists_h_file(self):
        return os.path.isfile(self.directory + self.name + '.h')

    def full_path(self):
        return self.directory + self.name

    def file_paths(self):
        file_paths = []
        if self.has_m_extension_file:
            file_paths.append(self.directory + self.name + '.m')
        if self.has_h_extension_file:
            file_paths.append(self.directory + self.name + '.h')
        return file_paths

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
        return self.directory + self.name

    def __unicode__(self):
        return self.__str__()

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.directory == other.directory and self.name == other.name

    def __hash__(self):
        return hash(self.directory + self.name)
