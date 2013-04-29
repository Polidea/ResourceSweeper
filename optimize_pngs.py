import sys
from resourcesweeper.convert import generate_convert_script
from resourcesweeper.resourcesweeper import analyze_project_resources


def main(arguments):
    if not len(arguments) == 2:
        print('Error: wrong number of arguments.')
    else:
        project_root_path = arguments[1]
        if not project_root_path.endswith('/'):
            project_root_path += '/'

        resources, used_resources = analyze_project_resources(project_root_path=project_root_path)

        generate_convert_script(output_filename='convert_images.py',
                                project_root_path=project_root_path,
                                used_resources=used_resources)


if __name__ == "__main__":
    main(sys.argv)