from __future__ import print_function
from copy import copy
import os

SPECIAL_CASE_FILE_NAME = {'main.m'}


def delete_files_from_disk_and_pbxproj(file_paths, project_root_path):
    xcodeprojs = [name for name in os.listdir(project_root_path) if name.endswith('.xcodeproj')]
    if len(xcodeprojs) != 1:
        raise Exception('Wrong number of xcodeprojs in path: %s' % project_root_path)

    file_names_to_delete = get_file_names(file_paths)
    delete_lines_containing_files_in_file(file_names_to_delete,
                                          '%s%s/project.pbxproj' % (project_root_path, xcodeprojs[0]))
    remove_files_at_paths(file_paths)


def get_file_names(file_paths):
    file_names = set()

    for file_path in file_paths:
        file_names.add(file_path[file_path.rfind('/') + 1:])

    return file_names


def delete_lines_containing_files_in_file(file_names, pbxproj_file_path):
    original_lines = get_lines_from_file_at_path(pbxproj_file_path)

    if original_lines:
        file_names_with_prefix_postfix = set(
            ['/* ' + file_name + ' */' for file_name in file_names if not file_name in SPECIAL_CASE_FILE_NAME])

        lines_to_remove = set(
            [line for line in original_lines for file_name in file_names_with_prefix_postfix if file_name in line])

        changed_lines = copy(original_lines)
        for line in lines_to_remove:
            changed_lines.remove(line)

        print('Number of all lines in project.pbxproj: ', len(original_lines))
        print('Number of lines after removal in project.pbxproj: ', len(changed_lines))
        print('Number of lines removed from project.pbxproj: ', len(original_lines) - len(changed_lines))

        write_lines_to_file_at_path(changed_lines, pbxproj_file_path)


def get_lines_from_file_at_path(file_path):
    lines = []
    try:
        with open(file_path, 'r') as a_file:
            lines = a_file.readlines()
    except IOError:
        print('Error: Could not open file to read: %s' % file_path)
    return lines


def write_lines_to_file_at_path(lines, file_path):
    try:
        with open(file_path, 'w') as a_file:
            for line in lines:
                a_file.write(line)
    except IOError:
        print('Error: Could not open file to write: %s' % file_path)


def remove_files_at_paths(file_paths):
    size = 0
    removed_files_count = 0
    for file_path in file_paths:
        if os.path.isfile(file_path):
            size += os.path.getsize(file_path)
            os.remove(file_path)
            removed_files_count += 1
    print('Removed %d files with total size: %f MiB' % (removed_files_count, size / 1024.0 / 1024.0))

