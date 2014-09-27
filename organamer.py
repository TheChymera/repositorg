#!/usr/bin/env python
from __future__ import division
__author__ = 'Horea Christian'

def rename(root_dir, strip_string="", append_string="", prepend_string="", conditional=True, execut=False):
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
	print [lastfile,lastfile_pair]
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

def reposit_files(destination_root, source_root, digits=4, letters=1, parent_prefix=True):
    import os
    
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
    print digits_start, letters_start
    
    source_files_list = sorted(source_files_list)
    rename_list = source_files_list[source_files_list.index(lastfile_pair):]
    
    new_names = []
    #~ for i in range(len(rename_list)):
	#~ print rename_list[i]
	
    digits_new = digits_start+1
    count=0
    while digits_new < 10**digits - 1 and count <= len(rename_list):
	formatting_string = "%0"+str(digits)+"d"
	padded_digits = formatting_string % digits_new
	new_names.append(os.path.join(source_root, "_"+letters_start+padded_digits))
	count += 1
	digits_new += 1
	
    print new_names
	
