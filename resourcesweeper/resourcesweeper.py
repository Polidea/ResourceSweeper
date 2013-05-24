import os
from resource import Resource
from filehelper import get_all_file_paths, line_contains_any_of_strings
from source import SOURCE_FILE_EXTENSIONS, Source

RESOURCE_NAMES_NOT_REFERENCED_IN_CODE = {'Default'}


def analyze_project_resources(project_root_path):
    sources = get_sources(project_root_path)
    resources = get_resources(project_root_path)
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


def get_sources(root_path):
    return [Source(path) for path in get_all_file_paths(root_path, SOURCE_FILE_EXTENSIONS)]


def get_file_names(path, proper_extensions):
    file_names = [name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))]
    return [file_name for file_name in file_names
            for extension in proper_extensions
            if file_name.endswith(extension)]


def get_resources(root_path):
    return set([Resource(path) for path in get_all_file_paths(root_path, Resource.proper_extensions)])


def get_resource_occurrences(sources, resources):
    resource_occurrences = []

    for source in sources:
        print source.get_path()
        source_file = open(source.get_path(), 'r')
        source_file_lines = source_file.readlines()
        for line_number, source_file_line in enumerate(source_file_lines):
            for resource in resources:
                if line_contains_any_of_strings(source_file_line, resource.use_cases):
                    resource_occurrences.append(
                        {
                            'source': source,
                            'line_number': line_number,
                            'resource': resource
                        })
        source_file.close()

    return resource_occurrences


def get_used_resources(resource_occurrences):
    return set([resource_occurrence['resource'] for resource_occurrence in resource_occurrences])


def resources_not_referenced_in_code(resources):
    return set([resource for resource in resources
                for resource_name_not_referenced_in_code in RESOURCE_NAMES_NOT_REFERENCED_IN_CODE
                if resource.name == resource_name_not_referenced_in_code])