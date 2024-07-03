#!/usr/bin/env python3
'''
This shouldn't be blank...
'''
# MIT License
#
# Copyright (c) 2024 Todd McDaniel
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# pysparsemac.py ###############################################################
#
#   A module to handle the creation and manipulation of sparse disk images on MacOS.
#
#    0.0.1  2024.05.18      Initial release, thanks PyCon24! tjm
#                           Demo.
#    0.0.2  2024.05.19      types added. tjm
#    0.0.3  2024.06.18      cleaned up, prepare for Github/PyPI. tjm
#    0.0.4  2024.06.18      removed types. tjm
#    0.0.5  2024.06.28      error checking, exceptions. tjm
#    0.1.0  2024.06.29      public release. tjm
#    0.1.1  2024.07.01      reworked suprocesses, destination path, tjm
#                           compressed path
#
################################################################################

# Notes: #######################################################################
#
# /usr/bin/hdiutil create -size 700m -type SPARSE -fs 'APFS' -volname test_backup ~/Desktop/test_backup_sparse.dmg
# /usr/bin/hdiutil attach ~/Desktop/test_backup_sparse.dmg.sparseimage
# /usr/bin/hdiutil detach /dev/disk15
# /usr/bin/hdiutil convert test_sparse.dmg.sparseimage -format ULMO -o test
#
#
#
################################################################################

# TTD: #########################################################################
#
#   docs <<<<<<
#   module packaging?
#   compressed disk destination_dir --DONE
#   more error checking
#   more exception messages
#   all functions return a dict with success field?!?
#   remove hardcoded tmp, use location of create_disk path --DONE
#   better/readable variable, function names in the demo function, make it easier to follow.
#   add fuction to dispose of uncompressed dmg
#   how about some comments?!?
#
#
################################################################################

import os
import pathlib
import subprocess


def create_disk(path, name, size):
    '''
    Accepts destination path, volume name, and pre-compressed volume size.

    Returns result of image creation.
    '''
    path_expanded = pathlib.Path(path + '.sparseimage').expanduser()

    if not os.path.isfile(path_expanded):
        try:
            create_proc = subprocess.check_output(["/usr/bin/hdiutil", "create", "-size", size, "-type", "SPARSE", "-fs", "APFS", "-volname", name, path_expanded], encoding='utf-8')
            return create_proc.rsplit(': ', maxsplit=1)[-1].rstrip()
        except subprocess.CalledProcessError:
            print(create_proc.returncode, create_proc.output)

    return False


def mount_disk(path):
    '''
    Accepts image path.

    Returns volume ID and path if the image is mounted successfully.
    '''
    try:
        mount_proc = subprocess.check_output(["/usr/bin/hdiutil", "attach", path], encoding='utf-8')
        last_line = mount_proc.rsplit('\t\n', maxsplit=1)[-1]
        volume_items = last_line.split('\t')

        volume_id = volume_items[0].rstrip()
        volume_path = volume_items[-1].rstrip()

        return {'volume_id': volume_id, 'volume_path': volume_path}

    except subprocess.CalledProcessError:
        print(mount_proc.returncode, mount_proc.output)

    return None


# def compress_disk(path, name):
def compress_disk(path):
    '''
    Accepts image path and destination compressed dmg name.

    Returns path of compressed image (and compression results).
    '''

    # sythesize path for for compressed image
    compressed_name = path.rsplit('.', maxsplit=1)[:-1][0].split('.')
    compressed_extension = compressed_name.pop()
    compressed_name = compressed_name[0] + '+compressed.' + compressed_extension

    if '.dmg' not in compressed_name:
        compressed_name += '.dmg'

    test_destination = pathlib.Path(compressed_name).expanduser()
    if test_destination.exists():
        raise FileExistsError(f'{test_destination} exists!')

    try:
        compress_proc = subprocess.check_output(["/usr/bin/hdiutil", "convert", path, "-format", "ULMO", "-o", compressed_name], encoding='utf-8')

        # might want to pull out interesting stats for logging?
        compress_proc_lines = compress_proc.split('\n')
        compressed_path = None

        for line in compress_proc_lines:
            if 'created:' in line:
                compressed_path = line.split(': ')[-1]
            # elif 'Savings' in line:
            #     disk_savings = line.split(': ')[-1]

        # print(disk_savings, compressed_path)
        return compressed_path

    except subprocess.CalledProcessError:
        print(compress_proc.returncode, compress_proc.output)

    return None


def unmount_disk(vol_id):
    '''
    Accepts destination path, volume name, and pre-compressed volume size.

    Returns result of image creation.
    '''
    try:
        unmount_proc = subprocess.check_output(["/usr/bin/hdiutil", "detach", vol_id], encoding='utf-8')
        return True

    except subprocess.CalledProcessError:
        # pysparsemac/pysparsemac.py:167:14: E0601: Using variable 'unmount_proc' before assignment (used-before-assignment)
        print(unmount_proc.returncode, unmount_proc.output)

    return False


def move_final_disk(path, destination_dir):
    '''
    Accepts original location and destination.

    Returns results of move.
    '''
    destination_file = path.split('/')[-1]
    destination_path = pathlib.Path(destination_dir).expanduser()
    test_destination = pathlib.Path(f'{destination_path}/{destination_file}')

    if test_destination.exists():
        raise FileExistsError(f'{test_destination} exists!')

    try:
        move_proc = subprocess.check_output(["/bin/mv", "-n", path, destination_path], encoding='utf-8')
        return True

    except subprocess.CalledProcessError:
        # pysparsemac/pysparsemac.py:190:14: E0601: Using variable 'move_proc' before assignment (used-before-assignment)
        print(move_proc.returncode, move_proc.output)

    return False


def demo_it():
    '''
    Provides a demonstration usage example.
    '''

#   Do a better job with your variable names here.
#   Do a better job with your variable names here.
#   Do a better job with your variable names here.
#   Do a better job with your variable names here.

    new_disk_path = create_disk('~/test_sparse.dmg', 'test_sparse_disk', '70m')

    if new_disk_path:
        print('Successfully created sparse disk.')

        volume_info = mount_disk(new_disk_path)
        if volume_info:
            print('Successfully mounted volume.')

            #
            #   Write your data to the disk now.
            #

            unmount_success = unmount_disk(volume_info['volume_id'])
            if unmount_success:
                print('Successfully unmounted disk.')
            else:
                print('Error unmounting disk.')

            compressed_path = compress_disk(new_disk_path)
            if compressed_path:
                print('Successfully compressed disk.')
            else:
                print('Error compressing disk')

            move_success = move_final_disk(compressed_path, "~/Desktop")
            if move_success:
                print('Successfully moved disk.')
            else:
                print('Error moving disk.')
        else:
            print('Failed to mount disk.')
    else:
        print("Failed to create disk, or disk exists.")


def main():
    '''
    ?
    '''
    demo_it()


if __name__ == '__main__':
    main()
