from __future__ import print_function
import os
from PIL import Image
from resource import get_resource_name
from resourcesweeper import get_subdirectory_paths, get_sources


def generate_convert_script(output_filename, project_root_path, used_resources):
    if os.path.isfile(output_filename):
        os.remove(output_filename)
    script_file = open(output_filename, 'w')

    default_jpg_quality = 80

    print('from resourcesweeper.convert import convert_images_to_jpg\n', file=script_file)
    print('project_root_path = \'%s\'' % project_root_path, file=script_file)
    print('jpg_quality = %d' % default_jpg_quality, file=script_file)
    print('image_paths = (', file=script_file)
    image_to_convert_paths = get_pngs_to_convert(used_resources)
    for image_path in image_to_convert_paths:
        print('    \'%s\',' % image_path, file=script_file)
    print(')', file=script_file)
    print('\nconvert_images_to_jpg(project_root_path, jpg_quality, image_paths)', file=script_file)

    script_file.close()

    png_size = 0
    jpg_size = 0
    for image_path in image_to_convert_paths:
        png_size += os.path.getsize(image_path)
        temp_name = '%s_temp%s' % (os.path.splitext(image_path)[0], os.path.splitext(image_path)[-1])
        convert_image_to_jpg(image_path, default_jpg_quality, temp_name)
        jpg_size += os.path.getsize(temp_name)
        os.remove(temp_name)
    png_size = png_size / 1024.0 / 1024.0
    jpg_size = jpg_size / 1024.0 / 1024.0

    print('\n--> Saved convert script: %s' % output_filename)
    print('    Change "jpg_quality" to desired value, comment files you want to leave and run:\n    "python %s"\n' %
          output_filename)
    if (jpg_size > 0):
        print('    Images to convert:')
        for image_path in image_to_convert_paths:
            print('        %s' % image_path)
        print('')
        print('    Old total size: %f MiB' % png_size)
        print('    Predicted total JPG size (using quality=%d): %f MiB (%0.2f%% old size)\n' % (
            default_jpg_quality, jpg_size, jpg_size / png_size * 100))
    else:
        print('    Wee! There are no pngs that can be converted to jpg!\n')


def get_pngs_to_convert(used_resources):
    files_with_used_alpha = set()
    pngs_resources = [resource for resource in used_resources if resource.extension == '.png']
    for png_resource in pngs_resources:
        for png_name in png_resource.get_file_names():
            image = Image.open(png_resource.directory + png_name)
            image.load()
            if image.mode == 'RGBA':
                red, green, blue, alpha = image.split()
                for pixel in list(alpha.getdata()):
                    if pixel != 255:
                        files_with_used_alpha.add(png_resource.directory + png_name)
                        break
    png_files = set()
    for resource in used_resources:
        if resource.extension == '.png':
            for resource_file in resource.get_file_names():
                png_files.add(resource.directory + resource_file)
    return png_files - files_with_used_alpha


def convert_images_to_jpg(project_root_path, jpg_quality, image_paths):
    old_size = 0
    new_size = 0
    for image_path in image_paths:
        old_size += os.path.getsize(image_path)
        file_name = os.path.splitext(image_path)[0]
        jpg_file_name = file_name + '.jpg'
        print('Converting %s ----> %s' % (image_path, jpg_file_name))
        convert_image_to_jpg(image_path, jpg_quality, jpg_file_name)
        swap_image_in_pbxproj(project_root_path, image_path, jpg_file_name)
        os.remove(image_path)
        new_size += os.path.getsize(jpg_file_name)

    file_names = [os.path.splitext(get_resource_name(img_path[img_path.rfind('/') + 1:]))[0] for img_path in
                  image_paths]
    sources = get_sources(get_subdirectory_paths(project_root_path))
    for source in sources:
        print(source)
        source_file = open(source.get_path())
        source_file_lines = source_file.readlines()
        source_file.close()
        resource_in_this_source = False
        for line in source_file_lines:
            for image_name in file_names:
                if image_name in line:
                    resource_in_this_source = True
                    break
        if resource_in_this_source:
            os.remove(source.get_path())
            source_file = open(source.get_path(), 'w')
            for line in source_file_lines:
                fixed_line = line
                for image_name in file_names:
                    fixed_line = fixed_line.replace(image_name, image_name + '.jpg')
                source_file.write(fixed_line)

    old_size = old_size / 1024.0 / 1024.0
    new_size = new_size / 1024.0 / 1024.0
    if old_size != 0:
        print('\n')
        print('Old size: %f MiB' % old_size)
        print('New size: %f MiB' % new_size)
        print('Difference: %f MiB' % (old_size - new_size))
        print('New size is %f%% of old size.' % (100 * new_size / old_size))
    print('\n')


def convert_image_to_jpg(file_path, jpg_quality, output_file_path=None):
    if output_file_path is not None:
        jpg_file_path = output_file_path
    else:
        jpg_file_path = file_path
    image = Image.open(file_path)
    image.convert('RGB').save(jpg_file_path, 'JPEG', quality=jpg_quality, optimize=True, progressive=True)


def swap_image_in_pbxproj(project_root_path, old_image_path, new_image_path):
    old_image_name = old_image_path[old_image_path.rfind('/') + 1:]
    xcodeprojs = [name for name in os.listdir(project_root_path) if name.endswith('.xcodeproj')]
    if len(xcodeprojs) != 1:
        raise Exception('Wrong number of xcodeprojs in path: %s' % project_root_path)
    pbxproj_path = '%s%s/project.pbxproj' % (project_root_path, xcodeprojs[0])
    pbxproj = open(pbxproj_path)
    pbxproj_lines = [line.replace('.png', '.jpg') if old_image_name in line else line for line in pbxproj.readlines()]
    pbxproj.close()
    os.remove(pbxproj_path)
    pbxproj = open(pbxproj_path, 'w')
    for line in pbxproj_lines:
        pbxproj.write(line)
    pbxproj.close()
