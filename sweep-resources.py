import sys
from resourcesweeper.outputgenerator import generate_report, resource_and_resource_file_number_and_total_size
from resourcesweeper.outputgenerator import generate_delete_script_for_resources
from resourcesweeper.resourcesweeper import analyze_project_resources


def main(arguments):
    if not len(arguments) == 2:
        print('Error: wrong number of arguments.')
    else:
        project_root_path = arguments[1]
        if not project_root_path.endswith('/'):
            project_root_path += '/'

        resources, used_resources = analyze_project_resources(project_root_path=project_root_path)
        unused_resources = list(resources - used_resources)
        unused_resources.sort()

        print('\nBrief report:')
        print('All resources: %d, files: %d, total size: %.2f MiB' % (
            resource_and_resource_file_number_and_total_size(resources)))
        print('Used resources: %d, files: %d, total size: %.2f MiB' % (
            resource_and_resource_file_number_and_total_size(used_resources)))
        print('Unused resources: %d, files: %d, total size: %.2f MiB' % (
            resource_and_resource_file_number_and_total_size(unused_resources)))

        generate_report(output_filename='report.txt',
                        project_root_path=project_root_path,
                        resources=resources,
                        used_resources=used_resources)

        generate_delete_script_for_resources(output_filename='delete_unused_files.py',
                                             project_root_path=project_root_path,
                                             unused_resources=unused_resources)


if __name__ == "__main__":
    main(sys.argv)