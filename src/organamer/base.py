#!/usr/bin/env python
from __future__ import division
__author__ = 'Horea Christian'
import os

def rename(root_dir, strip_string="", append_string="", prepend_string="", conditional=True, execute=False):
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

	# actually perform the renaming operation in this function
	if execute:
		for i in range(len(new_filenames)):
			os.rename(old_filenames[i], new_filenames[i])
		return False
	else:
		return [old_filenames, new_filenames]

def reformat(root_directory, digits=4, letters=1, prefix=None, parent_prefix=True, prompt=True, exclude=["Thumbs.db"]):
	root_directory = os.path.expanduser(root_directory)
	original_files_list = []
	for root, dirs, files in os.walk(root_directory):
		for name in files:
			if name not in exclude:
				original_files_list.append(os.path.join(root, name))
	original_files_list = sorted(original_files_list)
	new_files_list = iterative_rename(0, original_files_list, root_directory, prefix="pcr_")
	prompt_and_copy(original_files_list, new_files_list,
					"The original file locations above will be DELETED after copying.\nReview the above operations list carefully and enter 'yes' to continue or 'no' to abort."
					)
	for original_name in original_files_list:
		os.remove(original_name)

def pair_lastfile(destination_files, source_files):
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
		destination_dir = os.path.basename(destination_files[0])
		print("No pair for the last file from "+str(destination_dir)+", namely "+str(lastfile)+" was found.")

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

def reposit(destination_root, source_root, digits=4, letters=1, parent_prefix=True, prompt=True, user_password=None, smb_extension=""):
	import string

	destination_root = os.path.expanduser(destination_root)
	destination_files_list = []
	for root, dirs, files in os.walk(destination_root):
		for name in files:
			destination_files_list.append(os.path.join(root, name))

	#BEGIN copatibility for smb (samba share) download:
	if source_root[0:6] == "smb://":
		if not user_password:
			raise RuntimeError("Please specify a user and login for the SAMBA share. The proper format is username%password")
		from subprocess import call, list2cmdline
		import time

		tmpdir = "/tmp/organamer-"+time.strftime("%Y%m%d_%H%M%S")
		os.makedirs(tmpdir)

		_,_,ip,share,files_path = source_root.split("/", 4)
		lcd_part = "lcd "+tmpdir+"; cd "+files_path+"; prompt; mget *."+smb_extension
		print lcd_part
		print list2cmdline(["smbclient", "//"+ip+"/"+share, "-U", user_password, "-c", lcd_part])
		call(["smbclient", "//"+ip+"/"+share, "-U", user_password, "-c", lcd_part])
		source_root = tmpdir
	#END smb capability

	source_root = os.path.expanduser(source_root)
	source_files_list = []
	for root, dirs, files in os.walk(source_root):
		for name in files:
			source_files_list.append(os.path.join(root, name))
	source_files_list = sorted(source_files_list)

	if len(destination_files_list) == 0:
		old_names = source_files_list
		new_names=iterative_rename(0, old_names, destination_root, prefix="pcr_")
	else:
		lastfile,lastfile_pair = pair_lastfile(destination_files_list, source_files_list)
		digits_start = int(os.path.splitext(lastfile)[0][-digits:])
		letters_start = os.path.splitext(lastfile)[0][-(digits+letters):-digits]
		letters_start_index = string.lowercase.index(letters_start)

		old_names = source_files_list[source_files_list.index(lastfile_pair)+1:]
		if len(old_names) == 0:
			print("No files found to reposit. Aborting.")
			quit()

		if parent_prefix:
			if destination_root[-1] == "/":
				destination_root = destination_root[:-1]
			prefix = os.path.basename(destination_root)
			prefix += "_"

		# don't start numbering at the last digit, otherwise you would overwrite the file
		digits_start += 1
		new_names = iterative_rename(digits_start, old_names, destination_root, letters_start_index, prefix=prefix)

	if len(old_names) != len(new_names):
		raise RuntimeError("Lists of old and new filenames are not of the same length. Unsafe to continue")

	prompt_and_copy(old_names, new_names, "Review the above operations list carefully and enter 'yes' to continue or 'no' to abort.")

def iterative_rename(digits_start, old_names, destination_root="/tmp", letters_start_index=None, prefix="", digits=4):
	count=0
	new_names=[]
	while digits_start <= 10**digits - 1 and count <= len(old_names)-1:
		source_file_name, extension = os.path.splitext(old_names[count])
		#make sure files with the same path but different extensions keep the same name:
		if source_file_name == os.path.splitext(old_names[count-1])[0]:
			digits_start -= 1
		if digits_start == 10**digits:
			digits_start = 0
			if letters_start_index:
				letters_start_index += 1
				letters_start = string.lowercase[letters_start_index]
		if not letters_start_index:
			letters_start=""
		#create formatting template of length `digits`:
		formatting_string = "%0"+str(digits)+"d"
		padded_digits = formatting_string % digits_start
		#concatenate the name:
		new_name = os.path.join(destination_root, letters_start, prefix+letters_start+padded_digits+extension)
		new_names.append(new_name)
		count += 1
		digits_start += 1
	return new_names

def prompt_and_copy(files_from, files_to, prompt_message="Copy? [yes/no]", prompt=True):
	"""
	Print a prompt for the copy phase, and if answered yes, copy.
	"""
	from shutil import copyfile

	if prompt:
		for i in range(len(files_from)):
			print("Preparing to copy `"+str(files_from[i])+"` to `"+str(files_to[i])+"`.")
		if not query_yes_no(prompt_message):
			quit()

	for i in range(len(files_from)):
		print("Copying `"+str(files_from[i])+"` to `"+str(files_to[i])+"`.")
		copyfile(files_from[i], files_to[i])
		print("Finished!")

def query_yes_no(prompt_message, default="no"):
	"""Print a yes/no prompt via raw_input() and return the answer.

	"prompt_message" is a string that is presented to the user.
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
		sys.stdout.write(prompt_message + prompt)
		choice = raw_input().lower()
		if default is not None and choice == '':
			return valid[default]
		elif choice in valid:
			return valid[choice]
		else:
			sys.stdout.write("Please respond with 'yes' or 'no' "
							 "(or 'y' or 'n').\n")

if __name__ == "__main__":
	reformat_names("~/testdata/gt.ep/gel_electrophoresis/")
