import sys
from resourcesweeper.classsweeper import analyze_project_resources
from resourcesweeper.outputgenerator import generate_delete_script_for_classes


def files_count_of_classes(classes):
    return sum([ios_class.files_count() for ios_class in classes])


def main(arguments):
    if not len(arguments) == 3:
        print('Error: wrong number of arguments.')
    else:
        project_root_path = arguments[1]
        if not project_root_path.endswith('/'):
            project_root_path += '/'

        main_m_file_path = arguments[2]
        if not main_m_file_path.endswith('/'):
            main_m_file_path += '/'

        project_classes, not_referenced_classes = analyze_project_resources(project_root_path=project_root_path,
                                                                            main_m_file_path=main_m_file_path)

        print('\nBrief report:')
        print('All project .m & .h files count: %d' % (files_count_of_classes(project_classes)))
        print('Not referenced .m & .h files count: %d' % (files_count_of_classes(not_referenced_classes)))

        generate_delete_script_for_classes(output_filename='delete_unused_classes.py',
                                           project_root_path=project_root_path,
                                           not_referenced_classes=not_referenced_classes)


if __name__ == "__main__":
    main(sys.argv)