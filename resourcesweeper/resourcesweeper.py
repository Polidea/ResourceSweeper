from source import Source
from resource import Resource
from filehelper import get_all_file_paths, line_contains_any_of_strings

RESOURCE_NAMES_NOT_REFERENCED_IN_CODE = {'Default'}


def analyze_project_resources(project_root_path):
    sources = get_sources(project_root_path)
    resources = get_resources(project_root_path)
    resource_occurrences = get_resource_occurrences(sources, resources)
    used_resources = get_used_resources(resource_occurrences)
    used_resources.update(resources_not_referenced_in_code(resources - used_resources))

    return resources, used_resources


def get_sources(root_path):
    return [Source(path) for path in get_all_file_paths(root_path, Source.EXTENSIONS)]


def get_resources(root_path):
    return set([Resource(path) for path in get_all_file_paths(root_path, Resource.EXTENSIONS)])


def get_resource_occurrences(sources, resources):
    resource_occurrences = []

    for source in sources:
        print(source.get_path())
        try:
            with open(source.get_path(), 'r') as source_file:
                for line_number, source_file_line in enumerate(source_file):
                    for resource in resources:
                        if line_contains_any_of_strings(source_file_line, resource.use_cases):
                            resource_occurrences.append(
                                {
                                    'source': source,
                                    'line_number': line_number,
                                    'resource': resource
                                })
        except IOError:
            print('Error: could not open ' + source.get_path())

    return resource_occurrences


def get_used_resources(resource_occurrences):
    return set([resource_occurrence['resource'] for resource_occurrence in resource_occurrences])


def resources_not_referenced_in_code(resources):
    return set([resource for resource in resources
                for resource_name_not_referenced_in_code in RESOURCE_NAMES_NOT_REFERENCED_IN_CODE
                if resource.name == resource_name_not_referenced_in_code])