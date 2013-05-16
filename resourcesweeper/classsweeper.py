import time
from iosclass import CLASS_EXTENSIONS, IosClass
from resourcesweeper import get_subdirectory_paths, get_file_names


def analyze_project_resources(project_root_path, main_m_file_path):
    subdirectory_paths = get_subdirectory_paths(project_root_path)
    project_classes = get_classes(subdirectory_paths)
    set_dependencies(tuple(project_classes))
    not_referenced_classes = get_non_referenced_classes(project_classes, main_m_file_path)

    print '\nnot referenced classes:'
    for a_class in not_referenced_classes:
        print a_class

    return project_classes, not_referenced_classes


def get_classes(subdirectory_paths):
    classes = set()
    for path in subdirectory_paths:
        source_names = get_file_names(path, CLASS_EXTENSIONS)
        for source_name in source_names:
            classes.add(IosClass(path, source_name))

    return classes


def set_dependencies(project_classes):
    for a_class in project_classes:
        print(a_class)

        a_class_file_paths = a_class.file_paths()
        for a_class_file_path in a_class_file_paths:
            class_file = open(a_class_file_path, 'r')
            class_file_lines = class_file.readlines()
            for class_file_line in class_file_lines:
                for a_a_class in project_classes:
                    if line_contains_any_of_class_use_cases(class_file_line, a_a_class.use_cases):
                        a_class.used_classes.add(a_a_class)
            class_file.close()


def line_contains_any_of_class_use_cases(class_file_line, class_use_cases):
    contains = False
    line = class_file_line.lower()
    for class_use_case in class_use_cases:
        contains = class_use_case in line
        if contains:
            break
    return contains


def get_non_referenced_classes(project_classes, main_m_file_path):
    not_referenced_classes = project_classes.copy()
    for main_class in not_referenced_classes:
        if main_class.directory.__eq__(main_m_file_path) and 'main'.__eq__(main_class.name):
            remove_used_classes(main_class, not_referenced_classes)
            break

    sorted_not_referenced_classes = list(not_referenced_classes)
    sorted_not_referenced_classes.sort(key=lambda k: k.__str__())

    return sorted_not_referenced_classes


def remove_used_classes(a_class, classes):
    if a_class in classes:
        classes.remove(a_class)
        for used_class in a_class.used_classes:
            remove_used_classes(used_class, classes)


