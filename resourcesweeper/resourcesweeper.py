from __future__ import print_function
import os
from resource import Resource, get_resource_name
from source import SOURCE_FILE_EXTENSIONS, Source

RESOURCE_NAMES_NOT_REFERENCED_IN_CODE = {'Default'}


def analyze_project_resources(project_root_path):
    subdirectory_paths = get_subdirectory_paths(project_root_path)
    sources = get_sources(subdirectory_paths)
    resources = get_resources(subdirectory_paths)
    resource_occurrences = get_resource_occurrences(sources, resources)
    used_resources = get_used_resources(resource_occurrences)
    used_resources.update(resources_not_referenced_in_code(resources))

    return resources, used_resources


def get_subdirectory_paths(directory_path):
    subdirectories = [name for name in os.listdir(directory_path) if
                      os.path.isdir(os.path.join(directory_path, name)) and not '.' in name]

    paths = {directory_path}

    for subdirectory in subdirectories:
        subdirectory_path = '%s%s/' % (directory_path, subdirectory)
        paths.add(subdirectory_path)
        paths = paths.union(get_subdirectory_paths(subdirectory_path))

    return paths


def get_sources(subdirectory_paths):
    sources = []
    for path in subdirectory_paths:
        source_names = get_file_names(path, SOURCE_FILE_EXTENSIONS)
        for source_name in source_names:
            sources.append(Source(path, source_name))

    return sources


def get_file_names(path, proper_extensions):
    file_names = [name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))]
    file_names_to_return = []
    for file_name in file_names:
        for extension in proper_extensions:
            if file_name.endswith(extension):
                file_names_to_return.append(file_name)
    return file_names_to_return


def get_resources(subdirectory_paths):
    resources = set()

    for path in subdirectory_paths:
        resource_file_names = get_file_names(path, Resource.proper_extensions)
        resource_names = set()
        for resource_file_name in resource_file_names:
            resource_names.add(get_resource_name(resource_file_name))
        for resource_name in resource_names:
            resources.add(Resource(path, resource_name))

    return resources


def get_resource_occurrences(sources, resources):
    resource_occurrences = []

    for source in sources:
        print(source.get_path())
        source_file = open(source.get_path(), 'r')
        source_file_lines = source_file.readlines()
        for line_number, source_file_line in enumerate(source_file_lines):
            for resource in resources:
                count = source_file_line.count('@"%s' % resource.name) + source_file_line.count('>%s' % resource.name)
                if count > 0:
                    resource_occurrences.append(
                        {
                            'count': count,
                            'source': source,
                            'line_number': line_number,
                            'resource': resource
                        })
        source_file.close()

    return resource_occurrences


def get_used_resources(resource_occurrences):
    used_resources = set()
    for resource_occurrence in resource_occurrences:
        used_resources.add(resource_occurrence['resource'])
    return used_resources


def resources_not_referenced_in_code(resources):
    special_resources_to_add = set()
    for resource_name_not_referenced_in_code in RESOURCE_NAMES_NOT_REFERENCED_IN_CODE:
        for resource in resources:
            if resource.name.__eq__(resource_name_not_referenced_in_code):
                special_resources_to_add.add(resource)
    return special_resources_to_add
