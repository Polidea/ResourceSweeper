from __future__ import print_function
import os
import sys
from resource import Resource, get_resource_name
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
        # print header
        # print string
        # print header


def decorated_line(string):
    length = len(string)
    header = ''
    for i in range(length):
        header += '='
    return '%s\n%s\n%s' % (header, string, header)


def resource_and_resource_file_number(resources):
    no_resource_files = 0
    for resource in resources:
        if resource.low_resolution:
            no_resource_files += 1
        if resource.retina_resolution:
            no_resource_files += 1
        if resource.four_inch_resolution:
            no_resource_files += 1
    return len(resources), no_resource_files


def resource_sweeper(project_root_path):
    subdirectory_paths = get_subdirectory_paths(project_root_path)

    sources = []
    for path in subdirectory_paths:
        source_names = get_file_names(path, SOURCE_FILE_EXTENSIONS)
        for source_name in source_names:
            sources.append(Source(path, source_name))

    # for source_file in source_files:
    #     print source_file.get_path()

    resources = set()
    for path in subdirectory_paths:
        resource_file_names = get_file_names(path, Resource.proper_extensions)
        resource_names = set()
        for resource_file_name in resource_file_names:
            resource_names.add(get_resource_name(resource_file_name))
        for resource_name in resource_names:
            resources.add(Resource(path, resource_name))

    resource_occurrences = []

    for source in sources:
        print(source.get_path())
        source_file = open(source.get_path(), 'r')
        source_file_lines = source_file.readlines()
        for line_number, source_file_line in enumerate(source_file_lines):
            for resource in resources:
                count = source_file_line.count('@"%s' % resource.name)
                if count > 0:
                    resource_occurrences.append(
                        {
                            'count': count,
                            'source': source,
                            'line_number': line_number,
                            'resource': resource
                        })
        source_file.close()

    used_resources = set()
    for resource_occurrence in resource_occurrences:
        used_resources.add(resource_occurrence['resource'])

    unused_resources = resources - used_resources

    print('Resources: %d, Files: %d' % (resource_and_resource_file_number(resources)))
    print('Used resources: %d, Files: %d' % (resource_and_resource_file_number(used_resources)))
    print('Unused resources: %d, Files: %d' % (resource_and_resource_file_number(unused_resources)))

    delete_script_file = open('delete_unused_files_python_script.py', 'w')

    print('from delete import delete_files_from_disk_and_pbxproj', file=delete_script_file)
    print('project_root_path = \'%s\'' % project_root_path, file=delete_script_file)
    print('files_to_delete = (', file=delete_script_file)

    for resource in unused_resources:
        for file_name in resource.get_file_names():
            file_string = '\'%s%s\',' % (resource.directory, file_name)
            print(file_string, file=delete_script_file)
    print(')', file=delete_script_file)

    print('delete_files_from_disk_and_pbxproj(files_to_delete, project_root_path)', file=delete_script_file)

    report_file = open('report.txt', 'w')

    print(decorated_line('REPORT FOR ROOT PATH %s' % project_root_path), file=report_file)

    print('\nmissing low resolution files:', file=report_file)
    for resource in used_resources:
        if not resource.low_resolution:
            print('%s%s%s' % (resource.directory,
                              resource.name,
                              resource.extension),
                  file=report_file)

    print('\nmissing retina resolution files:', file=report_file)
    for resource in used_resources:
        if not resource.retina_resolution:
            print('%s%s%s%s' % (resource.directory,
                                resource.name,
                                resource.retina_resolution_key,
                                resource.extension),
                  file=report_file)


def main(arguments):
    if not len(arguments) == 2:
        print('Error: wrong number of arguments.')
    else:
        project_root_path = arguments[1]
        if not project_root_path.endswith('/'):
            project_root_path += '/'
        resource_sweeper(project_root_path=project_root_path)


if __name__ == "__main__":
    main(sys.argv)

