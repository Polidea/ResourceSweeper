from __future__ import print_function
import os


def generate_report(output_filename, project_root_path, resources, used_resources):
    if os.path.isfile(output_filename):
        os.remove(output_filename)
    report_file = open(output_filename, 'w')

    print(decorated_line('REPORT FOR ROOT PATH %s' % project_root_path), file=report_file)

    print('\nMissing low resolution files in used resources:', file=report_file)
    for resource in used_resources:
        if not resource.low_resolution:
            print('%s%s%s' % (resource.directory,
                              resource.name,
                              resource.extension),
                  file=report_file)

    print('\nMissing retina resolution files in used resources:', file=report_file)
    for resource in used_resources:
        if not resource.retina_resolution:
            print('%s%s%s%s' % (resource.directory,
                                resource.name,
                                resource.retina_resolution_key,
                                resource.extension),
                  file=report_file)

    unused_resources = resources - used_resources

    print('\nNumber of all resources: %d, files: %d' % (resource_and_resource_file_number(resources)), file=report_file)
    print('Number of used resources: %d, files: %d' % (resource_and_resource_file_number(used_resources)),
          file=report_file)
    print('Number of unused resources: %d, files: %d' % (resource_and_resource_file_number(unused_resources)),
          file=report_file)

    report_file.close()


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
    pass