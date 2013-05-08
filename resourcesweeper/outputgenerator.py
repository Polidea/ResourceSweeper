from __future__ import print_function
import os


def generate_report(output_filename, project_root_path, resources, used_resources):
    if os.path.isfile(output_filename):
        os.remove(output_filename)
    report_file = open(output_filename, 'w')

    print(decorated_line('REPORT FOR PROJECT IN ROOT PATH %s' % project_root_path), file=report_file)

    print('\nResources and files:', file=report_file)
    unused_resources = resources - used_resources
    print('Number of all resources: %d, files: %d' % (resource_and_resource_file_number(resources)), file=report_file)
    print('Number of used resources: %d, files: %d' % (resource_and_resource_file_number(used_resources)),
          file=report_file)
    print('Number of unused resources: %d, files: %d' % (resource_and_resource_file_number(unused_resources)),
          file=report_file)

    all_resources_size = get_size(resources) / 1024.0 / 1024.0
    used_resources_size = get_size(used_resources) / 1024.0 / 1024.0
    unused_resources_size = get_size(unused_resources) / 1024.0 / 1024.0

    used_resources_part = used_resources_size / all_resources_size * 100
    unused_resources_part = unused_resources_size / all_resources_size * 100

    print('\nDisk usage:', file=report_file)
    print('All resources size: %f MiB [100.00%%]' % all_resources_size, file=report_file)
    print('Used resources size: %f MiB [%.2f%%]' % (used_resources_size, used_resources_part), file=report_file)
    print('Unused resources size: %f MiB [%.2f%%]' % (unused_resources_size, unused_resources_part), file=report_file)

    print('\nMissing low resolution files in used resources:', file=report_file)
    for resource in used_resources:
        if not resource.low_resolution:
            print('%s%s%s' % (resource.directory.replace(project_root_path, ''),
                              resource.name,
                              resource.extension),
                  file=report_file)

    print('\nMissing retina resolution files in used resources:', file=report_file)
    for resource in used_resources:
        if not resource.retina_resolution:
            print('%s%s%s%s' % (resource.directory.replace(project_root_path, ''),
                                resource.name,
                                resource.retina_resolution_key,
                                resource.extension),
                  file=report_file)

    print('\n--> Saved report file: %s\n' % output_filename)


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


def get_size(resources):
    size = 0
    for resource in resources:
        resource_file_names = resource.get_file_names()
        for file_name in resource_file_names:
            if os.path.isfile(resource.directory + file_name):
                size += os.path.getsize(resource.directory + file_name)
    return size


def generate_delete_script(output_filename, project_root_path, unused_resources):
    if os.path.isfile(output_filename):
        os.remove(output_filename)

    delete_script_file = open(output_filename, 'w')

    print('from resourcesweeper.delete import delete_files_from_disk_and_pbxproj\n', file=delete_script_file)
    print('project_root_path = \'%s\'' % project_root_path, file=delete_script_file)
    print('files_to_delete = (', file=delete_script_file)

    for resource in unused_resources:
        for file_name in resource.get_file_names():
            file_string = '    \'%s%s\',' % (resource.directory, file_name)
            print(file_string, file=delete_script_file)
    print(')', file=delete_script_file)

    print('delete_files_from_disk_and_pbxproj(files_to_delete, project_root_path)', file=delete_script_file)
    delete_script_file.close()

    print('--> Saved delete script: %s' % output_filename)
    print('    Comment files you want to leave and run "python %s"\n' % output_filename)

    print('--> To optimize pngs use script:')
    print('    "python %s %s"\n' % ('optimize_pngs.py', project_root_path))


