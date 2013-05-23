from iosclass import CLASS_EXTENSIONS, IosClass
from resourcesweeper import get_subdirectory_paths, get_file_names


def analyze_project_resources(project_root_path, main_m_file_path):
    subdirectory_paths = get_subdirectory_paths(project_root_path)
    project_classes = get_classes(subdirectory_paths)
    set_dependencies(tuple(project_classes))
    not_referenced_classes = get_non_referenced_classes(project_classes, main_m_file_path)

    return project_classes, not_referenced_classes


def get_classes(subdirectory_paths):
    return set([IosClass(path, source_name) for path in subdirectory_paths
                for source_name in get_file_names(path, CLASS_EXTENSIONS)])


def set_dependencies(project_classes):
    for a_class in project_classes:
        print(a_class)

        a_class_file_paths = a_class.file_paths()
        for a_class_file_path in a_class_file_paths:
            try:
                with open(a_class_file_path, 'r') as opened_file:
                    for line in opened_file:
                        for a_a_class in project_classes:
                            if line_contains_any_of_class_use_cases(line, a_a_class.use_cases):
                                a_class.used_classes.add(a_a_class)
            except IOError:
                print 'Error: Could not open ' + a_class_file_path


def line_contains_any_of_class_use_cases(class_file_line, class_use_cases):
    line = class_file_line.lower()
    for class_use_case in class_use_cases:
        if class_use_case in line:
            return True

    return False


def get_non_referenced_classes(project_classes, main_m_file_path):
    not_referenced_classes = project_classes.copy()
    for main_class in not_referenced_classes:
        if main_class.directory == main_m_file_path and main_class.name == 'main':
            remove_used_classes(main_class, not_referenced_classes)
            break

    sorted_not_referenced_classes = list(not_referenced_classes)
    sorted_not_referenced_classes.sort(key=lambda k: str(k))

    return sorted_not_referenced_classes


def remove_used_classes(a_class, classes):
    if a_class in classes:
        classes.remove(a_class)
        for used_class in a_class.used_classes:
            remove_used_classes(used_class, classes)


