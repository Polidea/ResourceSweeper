import os


class Resource():
    EXTENSIONS = ('.png', '.jpg')
    retina_resolution_key = '@2x'
    four_inch_resolution_key = '-568h'

    def __init__(self, path):
        self.directory, resource_name_with_extension = os.path.split(path)
        resource_name_with_extension = get_resource_name(resource_name_with_extension)
        self.name, self.extension = os.path.splitext(resource_name_with_extension)
        self.low_resolution = self.__exists_low_resolution()
        self.retina_resolution = self.__exists_retina_resolution()
        self.four_inch_resolution = self.__exists_four_inch_resolution()
        self.use_cases = self.__generate_use_cases()
        pass

    def __exists_low_resolution(self):
        return os.path.isfile(os.path.join(self.directory, self.name + self.extension))

    def __exists_retina_resolution(self):
        return os.path.isfile(os.path.join(self.directory, self.name + self.retina_resolution_key + self.extension))

    def __exists_four_inch_resolution(self):
        return os.path.isfile(
            os.path.join(self.directory,
                         self.name + self.four_inch_resolution_key + self.retina_resolution_key + self.extension))

    def __generate_use_cases(self):
        return ('@"' + self.name + '"',
                '>' + self.name + '<',
                '@"' + self.name + self.extension + '"',
                '>' + self.name + self.extension + '<',
                '@"' + self.name + self.retina_resolution_key + '"',
                '>' + self.name + self.retina_resolution_key + '<',
                '@"' + self.name + self.retina_resolution_key + self.extension + '"',
                '>' + self.name + self.retina_resolution_key + self.extension + '<',
                '@"' + self.name + self.four_inch_resolution_key + self.retina_resolution_key + '"',
                '>' + self.name + self.four_inch_resolution_key + self.retina_resolution_key + '<',
                '@"' + self.name + self.four_inch_resolution_key + self.retina_resolution_key + self.extension + '"',
                '>' + self.name + self.four_inch_resolution_key + self.retina_resolution_key + self.extension + '<')

    def get_file_paths(self):
        return [os.path.join(self.directory, file_name) for file_name in self.get_file_names()]

    def get_file_names(self):
        file_names = []
        if self.low_resolution:
            file_names.append('%s%s' % (self.name, self.extension))
        if self.retina_resolution:
            file_names.append('%s%s%s' % (self.name, self.retina_resolution_key, self.extension))
        if self.four_inch_resolution:
            file_names.append(
                '%s%s%s%s' % (self.name, self.four_inch_resolution_key, self.retina_resolution_key, self.extension))
        return tuple(file_names)

    def __str__(self):
        return '[LR: %d, RR: %d, 4R: %d] %s ' % (
            self.low_resolution,
            self.retina_resolution,
            self.four_inch_resolution,
            os.path.join(self.directory, self.name + self.extension)
        )

    def __unicode__(self):
        return self.__str__()

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.directory == other.directory and self.name == other.name

    def __hash__(self):
        return hash(os.path.join(self.directory, self.name))


def get_resource_name(file_name):
    name = os.path.splitext(file_name)[0]
    if name.endswith(Resource.retina_resolution_key):
        name = name[:name.rfind(Resource.retina_resolution_key)]
    if name.endswith(Resource.four_inch_resolution_key):
        name = name[:name.rfind(Resource.four_inch_resolution_key)]
    return '%s%s' % (name, os.path.splitext(file_name)[-1])