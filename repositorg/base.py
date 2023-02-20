#!/usr/bin/env python
from __future__ import division
__author__ = 'Horea Christian'
import argh
import os
from distutils import dir_util
import string
import re
import warnings
from shutil import copyfile

from repositorg.utils import CaseFormatter, pair_lastfile, query_yes_no

def fetch(in_base, in_id,
	out_base='/var/tmp/repositorg/',
	in_id_is_file=False,
	in_path='',
	):
	"""Fetch data and reposit verbatim inside repositorg temporal directory

	Parameters
	----------
	in_base : str
		Base input directory from which to copy files.
	in_id : str
		UUID of the source device.
		This string will be added as a subidrectory under the `out_base` directory.
	out_base : str, optional
		Output base directory.
		A subdirectory named according to the value of `in_id` will be created under this directory to contain the output files.
	in_id_is_file : bool, optional
		Whether the value passed to `in_id` is a file name or path.
		If `True`, the `in_id` will be stripped of the extension and its basename will be extracted.
	in_path : str, optional
		An additional subpath to be added under the `in_base` directory.
	"""

	if in_id_is_file:
		in_id = os.path.basename(in_id)
		in_id = os.path.splitext(in_id)[0]
	in_path = os.path.join(in_base,in_path)
	out_path = os.path.join(out_base,in_id)

	if not os.path.isdir(in_path):
		return False
	dir_util.copy_tree(in_path, out_path,
		preserve_mode=0
		)

def rename(root_dir,
	strip_string="",
	append_string="",
	prepend_string="",
	conditional=True,
	execute=False,
	):
	"""Basic renaming function, with the ability to strip, append, and prepend literal strings.

	Parameters
	----------
	root_dir : str
		Directory from which to list files.
	strip_string : str, optional
		String which to strip from the beginning and end of file names.
		Note that as by Python's `.strip()` method, this is done iteratively; i.e. if this value is set to "la" and the file name ends in "lala", both occurences will be stripped.
	append_string : str, optional
		String which to append to the file name.
	prepend_string : str, optional
		String which to prepend to the file name (this can be done conditionally contingent on `conditional`).
	conditional : bool, optional
		Whether to only prepend string if it has been stripped.
	execute : bool, optional
		Whether to perform the rename; else two lists are returned: the containing the old filenames, the second containing the new file names.

	Returns
	-------
	old_filenames : list
		List of old filenames.
	new_filenames : list
		List of new filenames.
	"""

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
	return old_filenames, new_filenames

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
		if len(source_dirs) > 1:
			warnings.warn("The source files provided are contained in multiple directories. Per defult we are placing the reformatted files in the alphabetically first directory.")
		destination_root = source_dirs[0]

	source_files = sorted(source_files)
	new_files_list = iterative_rename(numbering_start, source_files, destination_root, letters_start_index=letters_start_index, prefix=prefix, digits=digits)
	prompt_and_copy(source_files, new_files_list,
					detele_source=True,
					prompt_message="\nThe original file locations above will be DELETED after copying.\nReview the above operations list carefully and enter 'yes' to continue or 'no' to abort.",
					)

@argh.arg('-d', '--digits')
@argh.arg('-n', '--numbering-start', type=int)
@argh.arg('-l', '--letters-start-index', type=int)
def reposit(in_root, out_root,
	in_regex='.*',
	out_regex='.*',
	out_string='',
	digits=4,
	exclude=["Thumbs.db"],
	letters=1,
	letters_start_index=None,
	numbering_start=None,
	parent_prefix=False,
	prefix="",
	no_ask=False,
	user_password=None,
	):
	"""Repositorg's core repositing function

	Arguments
	---------
	in_regex : string
		A regex string used to parse input file names, this can include a capture group called `number`, which will be used to sort files if the sorting of input file names is not desired (i.e. due to nuisance prefixes).
		Example: `"^(?P<prefix>_DSC|DSC_)(?P<number>[0-9]*)\.(?P<extension>NEF|JPG)$"`.
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

	out_root = os.path.abspath(os.path.expanduser(out_root))
	out_files_list = []
	for root, dirs, files in os.walk(out_root):
		for name in files:
			if name not in exclude:
				if re.match(out_regex, name):
					out_files_list.append(os.path.join(root, name))
	out_files_list = sorted(out_files_list)

	in_files_list = []
	for root, dirs, files in os.walk(in_root):
		for name in files:
			if re.match(in_regex, name):
				entry = re.match(in_regex, name).groupdict()
				entry["path"] = os.path.join(root, name)
				in_files_list.append(entry)
	if in_files_list == []:
		print('There are no files matching "{}" in the "{}" directory which we can reposit.'.format(in_regex,in_root))
		return

	try:
		in_files_list = sorted(in_files_list, key=lambda el: el["number"])
	except KeyError:
		in_files_list = sorted(in_files_list, key=lambda el: el["path"])
	in_files_list = [i["path"] for i in in_files_list]
	in_files_list = [os.path.abspath(os.path.expanduser(i)) for i in in_files_list]

	if len(out_files_list) == 0:
		old_names = in_files_list
		if not numbering_start:
			numbering_start = 0
		if not letters_start_index:
			letters_start_index = 0
	else:
		lastfile, lastfile_pair = pair_lastfile(out_files_list, in_files_list)
		if not lastfile_pair:
			print("  Checking whether in_files are in fact new or historical copy.")
			_, out_file_pair_for_last_in_file = pair_lastfile(in_files_list, out_files_list)
			if out_file_pair_for_last_in_file != None:
				print("    The source file list appears to be a subset of the already existing destination file list. Not proceeding.")
				return
		if not numbering_start and '{DIGITS}' in out_string:
			try:
				numbering_start = int(os.path.splitext(lastfile)[0][-digits:])
			except ValueError:
				# it could be that the target dir does not contain files in the same pattern.
				numbering_start = 0
			else:
				# don't start numbering at the last digit, otherwise you would overwrite the file
				numbering_start += 1
		if letters >= 1 and '{LETTERS}' in out_string and not letters_start_index:
			letters_start = os.path.splitext(lastfile)[0][-(digits+letters):-digits]
			try:
				letters_start_index = string.lowercase.index(letters_start)
			except AttributeError:
				letters_start_index = string.ascii_lowercase.index(letters_start)
		else:
			letters_start_index = None

		if lastfile_pair:
			old_names = in_files_list[in_files_list.index(lastfile_pair)+1:]
		else:
			old_names = in_files_list

		if len(old_names) == 0:
			print("No files found to reposit. Exiting.")
			quit()

		if parent_prefix:
			if destination_root[-1] == "/":
				destination_root = destination_root[:-1]
			prefix = os.path.basename(destination_root)
			prefix += "_"


	new_names = generate_names(numbering_start, old_names, out_string, in_regex, out_root, letters_start_index, digits=digits)
	if len(old_names) != len(new_names):
		raise RuntimeError("Lists of old and new filenames are not of the same length. Unsafe to continue")

	prompt_and_copy(old_names, new_names,
		prompt = not no_ask,
		prompt_message="Review the above operations list carefully and enter 'yes' to continue or 'no' to abort.",
		)

def generate_names(digits_start, old_names, out_string, in_regex,
	out_root="/var/tmp/repositorg",
	letters_start_index=None,
	digits=4,
	):
	count=0
	new_names=[]
	while count <= len(old_names)-1:
		#make sure files with the same path but different extensions keep the same name:
		#for lists of length 1, the last element is the only element, thus we require the list to be of length 2 at least
		if os.path.splitext(old_names[count])[0] == os.path.splitext(old_names[count-1])[0] and len(old_names) >= 2:
			try:
				digits_start -= 1
			except TypeError:
				pass
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
		#Source variables from source file name:
		substitutions = re.match(in_regex, os.path.basename(old_names[count]))
		substitutions = substitutions.groupdict()
		#create formatting template of length `digits`:
		if digits_start and digits or digits_start == 0 and digits:
			formatting_string = "%0"+str(digits)+"d"
			padded_digits = formatting_string % digits_start
			substitutions['DIGITS'] = padded_digits
			digits_start += 1
		substitutions['LETTERS'] = letters_start
		#Format the name:
		myformatter = CaseFormatter()
		new_name = myformatter.format(out_string, **substitutions)
		#concatenate the path:
		new_name = os.path.join(out_root, new_name)
		new_names.append(new_name)
		count += 1
	return new_names

def iterative_rename(digits_start, old_names,
	destination_root="/var/tmp",
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


