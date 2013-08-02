import os
import sys

from unittest import TestCase

import sweep_resources, sweep_classes

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))


class FakeSink(object):
    def write(self, *args):
        pass

    def writelines(self, *args):
        pass

    def close(self, *args):
        pass


class IntegrityResourcesTest(TestCase):
    def setUp(self):
        self.path = os.path.join(CURRENT_PATH, 'test_project', 'iPokeMon-dev')
        sys.stdout = FakeSink()

    def test_resources(self):
        result_report_path = os.path.join(CURRENT_PATH, 'report.txt')
        result_delete_script_path = os.path.join(CURRENT_PATH, 'delete_unused_files.py')
        self.assertFalse(os.path.exists(result_report_path))
        self.assertFalse(os.path.exists(result_delete_script_path))

        sweep_resources.main((None, self.path))

        template_report = open(os.path.join(CURRENT_PATH, 'test_project', 'report.txt')).readlines()

        self.assertTrue(os.path.exists(result_report_path))
        result_report = open(result_report_path).readlines()
        self.assertEqual(len(template_report), len(result_report))
        line_number = len(result_report)
        for i in xrange(3, line_number):
            self.assertEqual(template_report[i], result_report[i])

        self.assertTrue(os.path.exists(result_delete_script_path))
        result_delete_script = open(result_delete_script_path).readlines()
        template_delete_script = open(os.path.join(CURRENT_PATH, 'test_project', 'delete_unused_files.txt')).readlines()

        self.assertEqual(len(template_delete_script), len(result_delete_script))

        self.assertEqual(result_delete_script[0],
                         'from resourcesweeper.delete import delete_files_from_disk_and_pbxproj\n')
        self.assertTrue(result_delete_script[2].startswith('project_root_path = \''))
        self.assertTrue(result_delete_script[2].endswith('/ResourceSweeper/tests/test_project/iPokeMon-dev/\'\n'))
        self.assertEqual(result_delete_script[3], 'files_to_delete = (\n')

        for i in xrange(4, len(result_delete_script) - 2):
            result_line = result_delete_script[i]
            template_line = template_delete_script[i]
            self.assertTrue(
                result_line.endswith(template_line),
                'line {} with text {} :: not ends with :: {}'.format(i, result_line, template_line))

        self.assertEqual(result_delete_script[-2], template_delete_script[-2])
        self.assertEqual(result_delete_script[-1], template_delete_script[-1])

    def tearDown(self):
        sys.stdout = sys.__stdout__
        os.remove(os.path.join(CURRENT_PATH, 'delete_unused_files.py'))
        os.remove(os.path.join(CURRENT_PATH, 'report.txt'))


class IntegrityClassTest(TestCase):

    def setUp(self):
        self.path_to_project = os.path.join(CURRENT_PATH, 'test_project', 'iPokeMon-dev')
        self.path_to_main = os.path.join(CURRENT_PATH, 'test_project', 'iPokeMon-dev', 'Master')
        sys.stdout = FakeSink()

    def test_classes(self):
        delete_script_path = os.path.join(CURRENT_PATH, 'delete_unused_classes.py')
        self.assertFalse(os.path.exists(delete_script_path))

        sweep_classes.main((None, self.path_to_project, self.path_to_main))

        self.assertTrue(os.path.exists(delete_script_path))
        result_delete_script = open(delete_script_path).readlines()
        template_delete_script = open(os.path.join(CURRENT_PATH, 'test_project', 'delete_unused_classes.txt')).readlines()

        self.assertEqual(len(template_delete_script), len(result_delete_script))

        self.assertEqual(result_delete_script[0],
                         'from resourcesweeper.delete import delete_files_from_disk_and_pbxproj\n')
        self.assertTrue(result_delete_script[2].startswith('project_root_path = \''))
        self.assertTrue(result_delete_script[2].endswith('/ResourceSweeper/tests/test_project/iPokeMon-dev/\'\n'))
        self.assertEqual(result_delete_script[3], 'files_to_delete = (\n')

        for i in xrange(4, len(result_delete_script) - 2):
            result_line = result_delete_script[i]
            template_line = template_delete_script[i]
            self.assertTrue(
                result_line.endswith(template_line),
                'line {} with text {} :: not ends with :: {}'.format(i, result_line, template_line))

        self.assertEqual(result_delete_script[-2], template_delete_script[-2])
        self.assertEqual(result_delete_script[-1], template_delete_script[-1])

    def tearDown(self):
        sys.stdout = sys.__stdout__
        os.remove(os.path.join(CURRENT_PATH, 'delete_unused_classes.py'))
