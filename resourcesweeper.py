import os
import sys
from resource import Resource
from source import SOURCE_FILE_EXTENSIONS, Source


def get_subdirectory_paths(directory_path):
    subdirectories = [name for name in os.listdir(directory_path) if
                      os.path.isdir(os.path.join(directory_path, name)) and not '.' in name]

    paths = []

    for subdirectory in subdirectories:
        subdirectory_path = '%s%s/' % (directory_path, subdirectory)
        paths.append(subdirectory_path)
        paths += get_subdirectory_paths(subdirectory_path)

    return paths


def get_file_names(path, proper_extensions):
    file_names = [name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))]

    file_names_to_return = []

    for file_name in file_names:
        for extension in proper_extensions:
            if file_name.endswith(extension):
                file_names_to_return.append(file_name)

    return file_names_to_return


def inform_user(string):
    length = len(string)
    header = ''
    for i in range(length):
        header += '='
    print header
    print string
    print header


def resource_sweeper(project_root_path):
    subdirectory_paths = get_subdirectory_paths(project_root_path)

    sources = []
    for path in subdirectory_paths:
        source_names = get_file_names(path, SOURCE_FILE_EXTENSIONS)
        for source_name in source_names:
            sources.append(Source(path, source_name))

    # for source_file in source_files:
    #     print source_file.get_path()

    resources = []
    for path in subdirectory_paths:
        resource_names = get_file_names(path, Resource.proper_extensions)
        for resource_name in resource_names:
            resources.append(Resource(path, resource_name))

    # for resource in resources:
    #     print resource.get_path()


    for source in sources:
        inform_user('Analysis source file: %s STARTED' % source.get_path())
        source_file = open(source.get_path(), 'r')
        source_file_contents = source_file.read()
        source_file.close()
        inform_user('Analysis source file: %s FINISHED' % source.get_path())


def main(arguments):
    if not len(arguments) == 2:
        print 'Error: wrong number of arguments.'
    else:
        project_root_path = arguments[1]
        if not project_root_path.endswith('/'):
            project_root_path += '/'
        resource_sweeper(project_root_path=project_root_path)


if __name__ == "__main__":
    main(sys.argv)

