import time
import struct
import os

def extract(pak_file_path, destination_root_dir=None, verbose=None):
	pak_file = open(pak_file_path, 'rb')

	if verbose:
		pak_file.seek(0)
		signature = pak_file.read(4)
		print "Signature is " + str(signature)

	pak_file.seek(4)
	directory_offset = struct.unpack('i', pak_file.read(4))[0]
	directory_length = struct.unpack('i', pak_file.read(4))[0]

	if verbose:
		print "Directory offset: " + str(directory_offset)
		print "Directory length: " + str(directory_length)

	files_in_directory = directory_length / 64

	print "Extracting {0} files in archive".format(files_in_directory)

	for directory_entry in xrange(files_in_directory):
		pak_file.seek(directory_offset + (directory_entry * 64))

		file_path = pak_file.read(56).split(b'\x00')[0]
		file_position_in_archive = struct.unpack('i', pak_file.read(4))[0]
		file_length_in_archive = struct.unpack('i', pak_file.read(4))[0]

		path_components = os.path.split(file_path)

		directories = os.path.join(*path_components[:-1])
		basename = path_components[-1]

		destination_dir = os.path.join(destination_root_dir, directories)
		
		print "Extracting '{0}' to directory '{1}'".format(
			basename,
			destination_dir,
		)

		if not os.path.isdir(destination_dir):
			os.makedirs(destination_dir)

		pak_file.seek(file_position_in_archive)
		file_contents = pak_file.read(file_length_in_archive)
		with open(os.path.join(destination_dir, basename), 'wb') as output_file:
			output_file.write(file_contents)

	print "Done extracting archive"
