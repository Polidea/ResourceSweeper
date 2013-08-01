import fnmatch
import os


def get_all_file_paths(root_path, matching_extensions):
    matches = []
    extension_filters = ['*' + extension for extension in matching_extensions]
    for root, dirnames, filenames in os.walk(root_path):
        for filename_filter in extension_filters:
            for filename in fnmatch.filter(filenames, filename_filter):
                matches.append(os.path.join(root, filename))
    return matches


def line_contains_any_of_strings(line, strings):
    for string in strings:
        if string in line:
            return True

    return False