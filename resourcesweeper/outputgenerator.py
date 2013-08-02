from __future__ import print_function
import os


def generate_report(output_filename, project_root_path, resources, used_resources):
    try:
        with open(output_filename, 'w') as report_file:
            report_file.write(decorated_line('REPORT FOR PROJECT IN PATH %s' % os.path.split(project_root_path)[1]))

            report_file.write('\n\nResources and files:')
            unused_resources = resources - used_resources
            report_file.write(
                '\nNumber of all resources: %d, files: %d' % (resource_and_resource_file_number(resources)))
            report_file.write(
                '\nNumber of used resources: %d, files: %d' % (resource_and_resource_file_number(used_resources)))
            report_file.write(
                '\nNumber of unused resources: %d, files: %d' % (resource_and_resource_file_number(unused_resources)))

            all_resources_size = get_size(resources) / 1024.0 / 1024.0
            if all_resources_size > 0:
                used_resources_size = get_size(used_resources) / 1024.0 / 1024.0
                unused_resources_size = get_size(unused_resources) / 1024.0 / 1024.0

                used_resources_part = used_resources_size / all_resources_size * 100
                unused_resources_part = unused_resources_size / all_resources_size * 100

                report_file.write('\n\nDisk usage:')
                report_file.write('\nAll resources size: %f MiB [100.00%%]' % all_resources_size)
                report_file.write('\nUsed resources size: %f MiB [%.2f%%]' % (used_resources_size, used_resources_part))
                report_file.write(
                    '\nUnused resources size: %f MiB [%.2f%%]' % (unused_resources_size, unused_resources_part))

            report_file.write('\n\nMissing low resolution files in used resources:\n')
            for resource in used_resources:
                if not resource.low_resolution:
                    report_file.write(os.path.join(resource.directory.replace(project_root_path, ''),
                               resource.name + resource.extension) + '\n')

            report_file.write('\n\nMissing retina resolution files in used resources:\n')
            for resource in used_resources:
                if not resource.retina_resolution:
                    report_file.write(os.path.join(resource.directory.replace(project_root_path, ''),
                               resource.name + resource.retina_resolution_key + resource.extension) + '\n')

            print('\n--> Saved report file: %s\n' % output_filename)

    except IOError:
        print('Error: Could not save report file: %s' % output_filename)


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


def resource_and_resource_file_number_and_total_size(resources):
    number_of_resources, number_of_resource_files = resource_and_resource_file_number(resources)
    return number_of_resources, number_of_resource_files, get_size(resources) / 1024.0 / 1024.0


def get_size(resources):
    return sum([os.path.getsize(file_path)
                for resource in resources
                for file_path in resource.get_file_paths()
                if os.path.isfile(file_path)])


def generate_delete_script_for_resources(output_filename, project_root_path, unused_resources):
    try:
        with open(output_filename, 'w') as delete_script_file:

            delete_script_file.write('from resourcesweeper.delete import delete_files_from_disk_and_pbxproj\n')
            delete_script_file.write('\nproject_root_path = \'%s\'' % project_root_path)
            delete_script_file.write('\nfiles_to_delete = (')

            for resource in unused_resources:
                for file_name in resource.get_file_names():
                    file_string = '\n    \'%s\',' % os.path.join(resource.directory, file_name)
                    delete_script_file.write(file_string)
            delete_script_file.write('\n)')

            delete_script_file.write('\ndelete_files_from_disk_and_pbxproj(files_to_delete, project_root_path)')

            print('--> Saved delete script: %s' % output_filename)
            print('    Comment files you want to leave and run "python %s"\n' % output_filename)

            print('--> To prepare pngs optimization script use (this will not change any of your files):')
            print('    "python %s %s"\n' % ('optimize_pngs.py', project_root_path))

    except IOError:
        print('Error: Could not save delete script: %s' % output_filename)


def generate_delete_script_for_classes(output_filename, project_root_path, not_referenced_classes):
    try:
        with open(output_filename, 'w') as delete_script_file:

            delete_script_file.write('from resourcesweeper.delete import delete_files_from_disk_and_pbxproj\n')
            delete_script_file.write('\nproject_root_path = \'%s\'' % project_root_path)
            delete_script_file.write('\nfiles_to_delete = (')

            for a_class in not_referenced_classes:
                for file_name in a_class.get_file_names():
                    file_string = '\n    \'%s\',' % os.path.join(a_class.directory, file_name)
                    delete_script_file.write(file_string)
            delete_script_file.write('\n)')

            delete_script_file.write('\ndelete_files_from_disk_and_pbxproj(files_to_delete, project_root_path)')

            print('--> Saved delete script: %s' % output_filename)
            print('    Comment files you want to leave and run "python %s"\n' % output_filename)

    except IOError:
        print('Error: Could not save delete script: %s' % output_filename)


