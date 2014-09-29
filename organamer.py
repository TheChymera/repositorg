#!/usr/bin/env python
from __future__ import division
__author__ = 'Horea Christian'

def rename(root_dir, strip_string="", append_string="", prepend_string="", conditional=True, execute=False):
	import os
	root_dir = os.path.expanduser(root_dir)
	old_filenames=[]
	new_filenames=[]
	for root, dirs, files in os.walk(root_dir):
		for old_name in files:
			new_name = old_name
			#strip the strip_string value from the file names:
			if strip_string in old_name:
				new_name = old_name.strip(strip_string)
				#prepend prepend_string value stripped filenames:
				if conditional:
					new_name = prepend_string + new_name
			#prepend prepend_string value to all filenames:
			if not conditional:
				new_name = prepend_string + new_name
			if new_name != old_name:
				old_filenames.append(os.path.join(root, old_name))
				new_filenames.append(os.path.join(root, new_name))

	#check list consistency:
	if len(new_filenames) != len(old_filenames):
		raise RuntimeError("Lists of old and new filenames are not of the same length. Unsafe to continue")

	if execute:
		for i in range(len(new_filenames)):
			os.rename(old_filenames[i], new_filenames[i])
		return False
	else:
		return [old_filenames, new_filenames]

def pair_lastfile(destination_files, source_files):
	import os
	lastfile_found = False
	
	destination_files = sorted(destination_files)
	source_files = sorted(source_files, reverse=True)
	lastfile = destination_files[-1]
	lastfile_shorthash = sha256_hashfile(lastfile, blocks=1)
	lastfile_longhash = sha256_hashfile(lastfile)
	
	for source_file in source_files:
		file_shorthash = sha256_hashfile(source_file, blocks=1)
		if file_shorthash == lastfile_shorthash:
			file_longhash = sha256_hashfile(source_file)
			if file_longhash == lastfile_longhash:
				lastfile_pair = source_file
				lastfile_found = True
				break

	if lastfile_found:
		return [lastfile,lastfile_pair]
	else:
		print("No pair for the last file from "+str(destination_dir)+", namely "+str(lastfile)+" was found.")
		return False

def sha256_hashfile(file_path, blocks="all"):
	import hashlib
	hasher = hashlib.sha256()
	blocksize = hasher.block_size
	afile = open(file_path, "rb")
	buf = afile.read(blocksize)
	block_count=0
	while len(buf) > 0:
		if block_count > blocks:
			break
		elif blocks == "all":
			pass
		hasher.update(buf)
		buf = afile.read(blocksize)
		block_count += 1
	
	return hasher.hexdigest()

def reposit_files(destination_root, source_root, digits=4, letters=1, prefix=None, parent_prefix=True, prompt=True):
	import os
	import string
	from shutil import copyfile
	
	destination_root = os.path.expanduser(destination_root)
	destination_files_list = []
	for root, dirs, files in os.walk(destination_root):
		for name in files:
			destination_files_list.append(os.path.join(root, name))

	source_root = os.path.expanduser(source_root)
	source_files_list = []
	for root, dirs, files in os.walk(source_root):
		for name in files:
			source_files_list.append(os.path.join(root, name))

	lastfile,lastfile_pair = pair_lastfile(destination_files_list, source_files_list)
	digits_start = int(os.path.splitext(lastfile)[0][-digits:])
	letters_start = os.path.splitext(lastfile)[0][-(digits+letters):-digits]
	letters_start_index = string.lowercase.index(letters_start)
	
	source_files_list = sorted(source_files_list)
	old_names = source_files_list[source_files_list.index(lastfile_pair)+1:]
	
	if parent_prefix:
		prefix = os.path.basename(destination_root)
	
	new_names = []
	digits_new = digits_start+1
	count=0

	while digits_new <= 10**digits - 1 and count <= len(old_names)-1:
		source_file_name, extension = os.path.splitext(old_names[count])
		#make sure files with the same path but different extensions keep the same name:
		if source_file_name == os.path.splitext(old_names[count-1])[0]:
			digits_new -= 1
		if digits_new == 10**digits:
			digits_new = 0
			letters_start_index += 1
			letters_start = string.lowercase[letters_start_index]
		#create formatting template of length `digits`:
		formatting_string = "%0"+str(digits)+"d"
		padded_digits = formatting_string % digits_new
		new_name = os.path.join(destination_root, letters_start, prefix+"_"+letters_start+padded_digits+extension)
		new_names.append(new_name)
		count += 1
		digits_new += 1
	
	if len(old_names) != len(new_names):
		raise RuntimeError("Lists of old and new filenames are not of the same length. Unsafe to continue")
	
	if len(old_names) == 0:
		print("No files found to reposit. Aborting.")
		quit()

	if prompt:
		for i in range(len(old_names)):
			print("Preparing to copy `"+str(old_names[i])+"` to `"+str(new_names[i])+"`.")
		if not query_yes_no("Review the above operations list carefully and enter 'yes' to continue or 'no' to abort."):
			quit()

	for i in range(len(old_names)):
		print("Copying `"+str(old_names[i])+"` to `"+str(new_names[i])+"`.")
		copyfile(old_names[i], new_names[i])
		print("Finished!")
	
def query_yes_no(question, default="no"):
	"""Ask a yes/no question via raw_input() and return their answer.
	
	"question" is a string that is presented to the user.
	"default" is the presumed answer if the user just hits <Enter>.
		It must be "yes" (the default), "no" or None (meaning
		an answer is required of the user).
	
	The "answer" return value is one of "yes" or "no".
	
	Author: fmark (http://stackoverflow.com/users/103225/fmark)
	"""
	import sys
	
	valid = {"yes": True, "y": True, "ye": True,
			 "no": False, "n": False}
	if default is None:
		prompt = " [y/n] "
	elif default == "yes":
		prompt = " [Y/n] "
	elif default == "no":
		prompt = " [y/N] "
	else:
		raise ValueError("invalid default answer: '%s'" % default)
	
	while True:
		sys.stdout.write(question + prompt)
		choice = raw_input().lower()
		if default is not None and choice == '':
			return valid[default]
		elif choice in valid:
			return valid[choice]
		else:
			sys.stdout.write("Please respond with 'yes' or 'no' "
							 "(or 'y' or 'n').\n")
	
