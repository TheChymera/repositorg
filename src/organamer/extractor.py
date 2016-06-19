#!/usr/bin/env python
__author__ = 'Horea Christian'
import os
import string
import hashlib
from shutil import copyfile
from base import prompt_and_copy
import argh

def file_extractor(base_dir):
	"""Renames files to their parent directory name, and numerates them in case there is more than one per folder

	Mandatory Argumens:
	base_dir -- the directory in which to query for sub-directories whose files to rename

	ATTENTION:
	there are still multiple issues with this module:
	* It is not tested on subdirectories of subdirectories
	* It does not provide the option to filter the files to be renamed by format
	"""
	old_filenames = []
	new_filenames = []
	for root, dirs, files in os.walk(base_dir):
		# print(1,root,dirs,files)
		if dirs==[]:
			for ix, old_name in enumerate(sorted(files)):
				new_name = old_name
				_,new_filename_extension = os.path.splitext(old_name)
				# print(2,root, dirs)
				# print(3,new_filename_extension)
				old_filenames.append(os.path.join(root, old_name))
				if len(files) >=2:
					number="_"+str(ix)
				else:
					number=""
				new_filenames.append(os.path.normpath(root)+number+new_filename_extension)

	prompt_and_copy(old_filenames, new_filenames, "Review the above operations list carefully and enter 'yes' to continue or 'no' to abort.")

argh.dispatch_commands([file_extractor])
