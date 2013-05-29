import time
import struct
import os

SIGNATURE_POSITION = 0
SIGNATURE_LENGTH = 4

DIRECTORY_OFFSET_POSITION = 4
DIRECTORY_OFFSET_LENGTH = 4

DIRECTORY_SIZE_POSITION = 8
DIRECTORY_SIZE_LENGTH = 4

DIRECTORY_ENTRY_LENGTH = 64
DIRECTORY_ENTRY_FILE_PATH_LENGTH = 56
DIRECTORY_ENTRY_FILE_OFFSET_LENGTH = 4
DIRECTORY_ENTRY_FILE_LENGTH = 4

def unpack_integer(binary_value):
    return struct.unpack('i', binary_value)[0]

def unpack_null_terminated_string(binary_value):
    return binary_value.split(b'\x00')[0]

def extract(pak_file_path, unpack_root_dir=None, verbose=None):
    pak_file = open(pak_file_path, 'rb')

    if verbose:
        pak_file.seek(SIGNATURE_POSITION)
        signature = pak_file.read(SIGNATURE_LENGTH)
        print "Signature is " + str(signature)

    pak_file.seek(DIRECTORY_OFFSET_POSITION)
    directory_offset_in_binary = pak_file.read(DIRECTORY_OFFSET_LENGTH)
    directory_offset = unpack_integer(directory_offset_in_binary)

    pak_file.seek(DIRECTORY_SIZE_POSITION)
    directory_size_in_binary = pak_file.read(DIRECTORY_SIZE_LENGTH)
    directory_size = unpack_integer(directory_size_in_binary)

    if verbose:
        print "Directory offset: " + str(directory_offset)
        print "Directory length: " + str(directory_size)

    entries_in_directory = directory_size / DIRECTORY_ENTRY_LENGTH 

    print "Extracting {0} files in archive".format(entries_in_directory)

    for directory_entry in xrange(entries_in_directory):
        pak_file.seek(directory_offset + (directory_entry * DIRECTORY_ENTRY_LENGTH))

        file_path_in_binary = pak_file.read(DIRECTORY_ENTRY_FILE_PATH_LENGTH)
        file_path = unpack_null_terminated_string(file_path_in_binary)

        file_offset_in_archive_in_binary = pak_file.read(DIRECTORY_ENTRY_FILE_OFFSET_LENGTH)
        file_offset_in_archive = unpack_integer(file_offset_in_archive_in_binary)

        file_length_in_binary = pak_file.read(DIRECTORY_ENTRY_FILE_LENGTH)
        file_length = unpack_integer(file_length_in_binary)

        file_path_components = os.path.split(file_path)
        file_path_directories = os.path.join(*file_path_components[:-1])
        file_path_basename = file_path_components[-1]

        unpack_dir = os.path.join(unpack_root_dir, file_path_directories)
        
        print "Extracting '{0}' to directory '{1}'".format(
            file_path_basename,
            unpack_dir,
        )

        if not os.path.isdir(unpack_dir):
            os.makedirs(unpack_dir)

        pak_file.seek(file_offset_in_archive)
        file_contents = pak_file.read(file_length)
        with open(os.path.join(unpack_dir, file_path_basename), 'wb') as output_file:
            output_file.write(file_contents)

    print "Done extracting archive"
