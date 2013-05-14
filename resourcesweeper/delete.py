from __future__ import print_function
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
    pbxproj_file = open(pbxproj_file_path, 'r')
    lines = pbxproj_file.readlines()
    pbxproj_file.close()

    file_names_with_prefix = set()
    for file_name in file_names:
        if not file_name in SPECIAL_CASE_FILE_NAME:
            file_names_with_prefix.add('/* ' + file_name + ' */')

    os.remove(pbxproj_file_path)

    line_count_before = len(lines)

    lines_to_remove = set()
    for line in lines:
        for file_name in file_names_with_prefix:
            if file_name in line:
                lines_to_remove.add(line)

    for line in lines_to_remove:
        lines.remove(line)

    line_count_after = len(lines)

    print('Number of all lines in project.pbxproj: ', line_count_before)
    print('Number of lines after removal in project.pbxproj: ', line_count_after)
    print('Number of lines removed from project.pbxproj: ', line_count_before - line_count_after)

    pbxproj_file = open(pbxproj_file_path, 'w')

    for line in lines:
        pbxproj_file.write(line)

    pbxproj_file.close()


def remove_files_at_paths(file_paths):
    size = 0
    removed_files_count = 0
    for file_path in file_paths:
        if os.path.isfile(file_path):
            size += os.path.getsize(file_path)
            os.remove(file_path)
            removed_files_count += 1
    print('Removed %d files with total size: %f MiB' % (removed_files_count, size / 1024.0 / 1024.0))

