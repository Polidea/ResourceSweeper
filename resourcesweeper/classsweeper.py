import os
from iosclass import IosClass
from filehelper import line_contains_any_of_strings, get_all_file_paths


def analyze_project_resources(project_root_path, main_m_file_path):
    project_classes = get_classes(project_root_path)
    set_dependencies(tuple(project_classes))
    not_referenced_classes = get_non_referenced_classes(project_classes, main_m_file_path)

    return project_classes, not_referenced_classes


def get_classes(root_path):
    return set([IosClass(path) for path in get_all_file_paths(root_path, IosClass.EXTENSIONS)])


def set_dependencies(project_classes):
    for a_class in project_classes:
        print(a_class)

        a_class_file_paths = a_class.get_file_paths()
        for a_class_file_path in a_class_file_paths:
            try:
                with open(a_class_file_path, 'r') as opened_file:
                    for line in opened_file:
                        for a_a_class in project_classes:
                            if a_class != a_a_class and line_contains_any_of_strings(line.lower(), a_a_class.use_cases):
                                a_class.used_classes.add(a_a_class)
            except IOError:
                print 'Error: Could not open ' + a_class_file_path


def get_non_referenced_classes(project_classes, main_m_file_path):
    not_referenced_classes = project_classes.copy()
    for main_class in not_referenced_classes:
        if os.path.samefile(main_class.directory, main_m_file_path) and main_class.name == 'main':
            remove_used_classes(main_class, not_referenced_classes)
            break

    sorted_not_referenced_classes = list(not_referenced_classes)
    sorted_not_referenced_classes.sort()

    return sorted_not_referenced_classes


def remove_used_classes(a_class, classes):
    if a_class in classes:
        classes.remove(a_class)
        for used_class in a_class.used_classes:
            remove_used_classes(used_class, classes)


