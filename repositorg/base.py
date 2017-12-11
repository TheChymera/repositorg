#!/usr/bin/env python
from __future__ import division
__author__ = 'Horea Christian'
import argh
import os
import string
import hashlib
import warnings
from shutil import copyfile

def rename(root_dir,
	strip_string="",
	append_string="",
	prepend_string="",
	conditional=True,
	execute=False,
	):
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

@argh.arg('-d', '--digits')
@argh.arg('-e', '--extensions', nargs='+', type=str)
@argh.arg('-l', '--letters-start-index', type=int)
@argh.arg('-n', '--numbering-start', type=int)
@argh.arg('-p', '--prefix')
@argh.arg('source', nargs='+', type=str)
def reformat(source,
	digits=4,
	exclude=["Thumbs.db"],
	extensions=[],
	letters_start_index=None,
	numbering_start=0,
	prefix="",
	prompt=True,
	):
	"""Reformat file names in given directory.

	Arguments
	---------
	source : string
		Reformat these files (or ONE directory, in which case all fies are reformatted).
	digits : int
		Create new file names with this many digits.
	exclude: list
		Exclude these file names from the repositing process.
	letters_start_index : int
		Start letter incremention in file name at this letter (a=0, b=1, etc.)
	numbering_start : int
		Start number incremention in file name at this integer.
	prefix: string
		Add this prefix to all new file names.
	prompt: bool
		Ask for confirmation - setting to False is DANGEROUS!
	"""

	if len(source) == 1 and source[0][-1] in ["/","."]:
		source = source[0]
		source = os.path.expanduser(source)
		destination_root = source

		source_files = []
		for root, dirs, files in os.walk(source):
			for name in files:
				if extensions:
					if os.path.splitext(name)[1] in extensions:
						source_files.append(os.path.join(root, name))
				else:
					source_files.append(os.path.join(root, name))
	else:
		source_files = [os.path.expanduser(i) for i in source]

		source_dirs = []
		for abs_source_file, rel_source_file in zip(source_files, source):
			if abs_source_file.endswith(rel_source_file):
				source_dirs.append(abs_source_file[:-len(rel_source_file)])
		source_dirs = sorted(list(set(source_dirs)))
		if len(source_dirs) >= 1:
			warnings.warn("The source files provided are contained in multiple directories. Per defult we are placing the reformatted files in the alphabetically first directory.")
		destination_root = source_dirs[0]

	source_files = sorted(source_files)
	new_files_list = iterative_rename(numbering_start, source_files, destination_root, letters_start_index=letters_start_index, prefix=prefix, digits=digits)
	prompt_and_copy(source_files, new_files_list,
					detele_source=True,
					prompt_message="\nThe original file locations above will be DELETED after copying.\nReview the above operations list carefully and enter 'yes' to continue or 'no' to abort.",
					)

def pair_lastfile(destination_files, source_files):

	destination_files = [os.path.abspath(os.path.expanduser(i)) for i in destination_files]
	source_files = [os.path.abspath(os.path.expanduser(i)) for i in source_files]
	destination_files = sorted(destination_files)
	source_files = sorted(source_files, reverse=True)
	lastfile = destination_files[-1]
	lastfile_shorthash = sha256_hashfile(lastfile, blocks=1)
	lastfile_longhash = sha256_hashfile(lastfile)

	lastfile_pair = None
	if lastfile_shorthash and lastfile_longhash:
		for source_file in source_files:
			file_shorthash = sha256_hashfile(source_file, blocks=1)
			if file_shorthash == lastfile_shorthash:
				file_longhash = sha256_hashfile(source_file)
				if file_longhash == lastfile_longhash:
					lastfile_pair = source_file
					break
	if lastfile_pair:
		return [lastfile, lastfile_pair]
	else:
		destination_dir = os.path.dirname(destination_files[0])
		print("No pair for the last file from "+str(destination_dir)+", namely "+str(lastfile)+" was found.")
		return [lastfile, lastfile_pair]

def sha256_hashfile(file_path, blocks="all"):
	hasher = hashlib.sha256()
	blocksize = hasher.block_size
	try:
		afile = open(file_path, "rb")
	except IOError:
		return
	buf = afile.read(blocksize)
	block_count=0
	while len(buf) > 0:
		if blocks == "all":
			pass
		elif block_count > blocks:
			break
		hasher.update(buf)
		buf = afile.read(blocksize)
		block_count += 1

	return hasher.hexdigest()

@argh.arg('-d', '--digits')
@argh.arg('-e', '--extensions', nargs='+', type=str)
@argh.arg('-n', '--numbering-start', type=int)
@argh.arg('-l', '--letters-start-index', type=int)
@argh.arg('-p', '--prefix')
@argh.arg('source', nargs='+', type=str)
def reposit(destination_root, source,
	digits=4,
	exclude=["Thumbs.db"],
	extensions=[],
	letters=0,
	letters_start_index=None,
	numbering_start=None,
	parent_prefix=False,
	prefix="",
	no_ask=False,
	user_password=None,
	):
	"""Organamer's core repositing function

	Arguments
	---------
	destination_root : string
		Reposit the files into this directory.
	source : list
		Reposit the files from this directory. Alternatively can contain a list of files to reposit.
	digits : int
		Create new file names with this many digits.
	exclude: list
		Exclude these file names from the repositing process.
	extensions: list
		Consider only files with these extensions.
	letters : int
		Prepend this many letters to the digits in the new file names.
		The files are reposited in destination_root subdirectories specific for every letter.
	letters_start_index : int
		Start letter incremention in file name at this letter (a=0, b=1, etc.)
	numbering_start : int
		Start number incremention in file name at this integer.
	parent_prefix : bool
		Add the name of the root dir as a prefix to all new file names.
	prefix: string
		Add this prefix to all new file names.
	user_password: string
		User and password for your remote file source (format: 'user%password')
	no_ask: bool
		Do not ask for confirmation - setting to True is DANGEROUS!

	Notes
	-----
	Currently breaks for letters > 1 because the string.lowercase.index() function only takes one argument.
	"""
	#check if extension is at all specified
	if extensions:
	#check if the extension is formated correctly (leading period, as seen with `os.path.splitext()`)
		for i in range(len(extensions)):
			if extensions[i][0] != ".":
				extensions[i] = "."+extensions[i]

	destination_root = os.path.abspath(os.path.expanduser(destination_root))
	destination_files_list = []
	for root, dirs, files in os.walk(destination_root):
		for name in files:
			if name not in exclude:
				if extensions:
					if os.path.splitext(name)[1] in extensions:
						destination_files_list.append(os.path.join(root, name))
				else:
					destination_files_list.append(os.path.join(root, name))
	destination_files_list = sorted(destination_files_list)

	# check whether a path (and not a list) is parsed
	if len(source) == 1 and source[0][-1] == "/":
		source = source[0]
		#BEGIN copatibility for smb (samba share) download:
		if source[0:6] == "smb://":
			if not user_password:
				raise RuntimeError("Please specify a user and login for the SAMBA share. The proper format is username%password")
			from subprocess import call, list2cmdline
			import time

			tmpdir = "/tmp/organamer-"+time.strftime("%Y%m%d_%H%M%S")
			os.makedirs(tmpdir)

			_,_,ip,share,files_path = source.split("/", 4)
			lcd_part = "lcd "+tmpdir+"; cd "+files_path+"; prompt; mget *"+extension
			call(["smbclient", "//"+ip+"/"+share, "-U", user_password, "-c", lcd_part])
			source = tmpdir
		#END smb capability
		else:
			source = os.path.expanduser(source)

		source_files_list = []
		for root, dirs, files in os.walk(source):
			for name in files:
				if extensions:
					if os.path.splitext(name)[1] in extensions:
						source_files_list.append(os.path.join(root, name))
				else:
					source_files_list.append(os.path.join(root, name))
	# assume this is then a list of files
	else:
		source_files_list = source

	source_files_list = sorted(source_files_list)
	source_files_list = [os.path.abspath(os.path.expanduser(i)) for i in source_files_list]

	if len(destination_files_list) == 0:
		old_names = source_files_list
		if not numbering_start:
			numbering_start= 0
		if not letters_start_index:
			letters_start_index = 0
	else:
		lastfile, lastfile_pair = pair_lastfile(destination_files_list, source_files_list)
		if not numbering_start:
			numbering_start = int(os.path.splitext(lastfile)[0][-digits:])
		if letters >= 1 and not letters_start_index:
			letters_start = os.path.splitext(lastfile)[0][-(digits+letters):-digits]
			try:
				letters_start_index = string.lowercase.index(letters_start)
			except AttributeError:
				letters_start_index = string.ascii_lowercase.index(letters_start)
		else:
			letters_start_index = None

		if lastfile_pair:
			old_names = source_files_list[source_files_list.index(lastfile_pair)+1:]
		else:
			old_names = source_files_list

		if len(old_names) == 0:
			print("No files found to reposit. Exiting.")
			quit()

		if parent_prefix:
			if destination_root[-1] == "/":
				destination_root = destination_root[:-1]
			prefix = os.path.basename(destination_root)
			prefix += "_"

		# don't start numbering at the last digit, otherwise you would overwrite the file
		numbering_start += 1

	new_names = iterative_rename(numbering_start, old_names, destination_root, letters_start_index, prefix=prefix, digits=digits)

	if len(old_names) != len(new_names):
		raise RuntimeError("Lists of old and new filenames are not of the same length. Unsafe to continue")

	prompt_and_copy(old_names, new_names,
		prompt = not no_ask,
		prompt_message="Review the above operations list carefully and enter 'yes' to continue or 'no' to abort.",
		)

def iterative_rename(digits_start, old_names,
	destination_root="/tmp",
	letters_start_index=None,
	prefix="",
	digits=4,
	):
	count=0
	new_names=[]
	while digits_start <= 10**digits - 1 and count <= len(old_names)-1:
		source_file_name, extension = os.path.splitext(old_names[count])
		#make sure files with the same path but different extensions keep the same name:
		#for lists of length 1, the last element is the nly element, thus we require the list to be of length 2 at least
		if source_file_name == os.path.splitext(old_names[count-1])[0] and len(old_names) >= 2:
			digits_start -= 1
		if digits_start == 10**digits:
			digits_start = 0
			if letters_start_index or letters_start_index == 0:
				letters_start_index += 1
		if letters_start_index or letters_start_index == 0:
			try:
				letters_start = string.lowercase[letters_start_index]
			except AttributeError:
				letters_start = string.ascii_lowercase[letters_start_index]
		else:
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

def prompt_and_copy(files_from, files_to,
	detele_source=False,
	prompt_message="Copy?",
	prompt=True,
	):
	"""
	Print a prompt with the summary of the copy phase, and if answered yes, copy.
	"""

	if prompt:
		for i in range(len(files_from)):
			print("Preparing to copy '{}' to '{}'.".format(str(files_from[i]),str(files_to[i])))
		if not query_yes_no(prompt_message):
			quit()

	for i in range(len(files_from)):
		print("Copying '{}' to '{}'.".format(str(files_from[i]),str(files_to[i])))
		if not os.path.exists(os.path.dirname(files_to[i])):
			os.makedirs(os.path.dirname(files_to[i]))
		copyfile(files_from[i], files_to[i])
		print("Finished!")
		if detele_source:
			print("Deleting '{}'".format(str(files_from[i])))
			os.remove(files_from[i])
			print("Deleted!")



def query_yes_no(prompt_message, default_choice="no"):
	"""Print a yes/no prompt via raw_input() and return the answer.

	"prompt_message" is a string that is presented to the user.
	"default_choice" is the presumed answer if the user just hits <Enter>.
		It must be "yes" (the default_choice), "no" or None (meaning
		an answer is required of the user).

	The "answer" return value is one of "yes" or "no".

	Author: fmark (http://stackoverflow.com/users/103225/fmark)
	"""
	import sys

	valid = {"yes": True, "y": True, "ye": True,
			 "no": False, "n": False}
	if default_choice is None:
		prompt = " [y/n] "
	elif default_choice == "yes":
		prompt = " [Y/n] "
	elif default_choice == "no":
		prompt = " [y/N] "
	else:
		raise ValueError("invalid default answer: '%s'" % default_choice)

	while True:
		sys.stdout.write(prompt_message + prompt)
		try:
			choice = raw_input().lower()
		except NameError:
			choice = input().lower()
		if default_choice is not None and choice == '':
			return valid[default_choice]
		elif choice in valid:
			return valid[choice]
		else:
			sys.stdout.write("Please respond with 'yes' or 'no' "
							 "(or 'y' or 'n').\n")
