import argh
import os
import shlex
import subprocess
import time

@argh.arg('source', nargs='+', type=str)
@argh.arg('-e', '--extensions', nargs='+', type=str)
def audioproc(source,
	extensions=[],
	output_ext="mp3",
	parameters="-codec:a libmp3lame -qscale:a 2",
	max_processes =4,
	):
	"""Process audio files in a given directory.

	Arguments
	---------
	source : list
		Reposit the files from this directory. Alternatively can contain a list of files to reposit.
	extensions: list
		Consider only files with these extensions.
	output_ext : string
		Create processed files with this extension.
	parameters: string
		Pass these parameters to ffmpeg (the program used for video re-encoding).
	max_processes: int
		Run up to this many processes at a time.

	Notes
	-----
	If the CLI binding complains of too few arguments, the mandatory positional argument "source" might be caugt by one of the others.
	Try separating it with " -- " from the rest of the call.
	"""


	#check if the extensions are formated correctly (leading period, as seen with `os.path.splitext()`):
	if extensions:
		for i in range(len(extensions)):
			if extensions[i][0] != ".":
				extensions[i] = "."+extensions[i]
	if output_ext[0] != ".":
		output_ext = "."+output_ext

	if len(source) == 1 and source[0][-1] == "/":
		source = source[0]
		source = os.path.expanduser(source)
		in_paths = os.listdir(source)
		in_paths = [os.path.join(source,in_path) for in_path in in_paths]
	else:
		in_paths = [os.path.expanduser(in_path) for in_path in source]

	if extensions:
		in_paths = [in_path for in_path in in_paths if os.path.splitext(in_path)[1] in extensions]

	paths_dict = {key:key for key in in_paths}
	paths_dict.update((x, os.path.splitext(y)[0]+output_ext) for x,y in paths_dict.items())

	processes = set()
	for key in paths_dict:
		safe_original_name = '"'+key+'"'
		safe_destination_name = '"'+paths_dict[key]+'"'
		raw_command = " ".join(["ffmpeg -i", safe_original_name, parameters, safe_destination_name])
		args = shlex.split(raw_command)
		processes.add(subprocess.Popen(args))
		if len(processes) >= max_processes:
			os.wait()
			processes.difference_update([
				p for p in processes if p.poll() is not None])
	while None in [p.poll() for p in processes]:
		time.sleep(0.5)
	#We need to explicitly terminate the master process here, as otherwise the shell "hangs" and the user needs to press enter to return to a new prompt.
	os.system('kill %d' % os.getpid())

@argh.arg('source', nargs='+', type=str)
@argh.arg('-e', '--extensions', nargs='+', type=str)
def vidproc(source,
	extensions=[],
	output_ext="mkv",
	parameters="-vf 'transpose=dir=clock, transpose=dir=clock, crop=1080:1080' -crf 16 -c:a copy",
	max_processes=4,
	):
	"""Process video files in a given directory.

	Arguments
	---------
	source : list
		Reposit the files from this directory. Alternatively can contain a list of files to reposit.
	extensions: list
		Consider only files with these extensions.
	output_ext : string
		Create processed files with this extension.
	parameters: string
		Pass these parameters to ffmpeg (the program used for video re-encoding).
	max_processes: int
		Run up to this many processes at a time.

	Notes
	-----
	If the CLI binding complains of too few arguments, the mandatory positional argument "source" might be caugt by one of the others.
	Try separating it with " -- " from the rest of the call.
	"""


	#check if the extensions are formated correctly (leading period, as seen with `os.path.splitext()`):
	if extensions:
		for i in range(len(extensions)):
			if extensions[i][0] != ".":
				extensions[i] = "."+extensions[i]
	if output_ext[0] != ".":
		output_ext = "."+output_ext

	if len(source) == 1 and source[0][-1] == "/":
		source = source[0]
		source = os.path.expanduser(source)
		in_paths = os.listdir(source)
		in_paths = [os.path.join(source,in_path) for in_path in in_paths]
	else:
		in_paths = [os.path.expanduser(in_path) for in_path in source]

	if extensions:
		in_paths = [in_path for in_path in in_paths if os.path.splitext(in_path)[1] in extensions]

	paths_dict = {key:key for key in in_paths}
	paths_dict.update((x, os.path.splitext(y)[0]+output_ext) for x,y in paths_dict.items())

	processes = set()
	for key in paths_dict:
		safe_original_name = '"'+key+'"'
		safe_destination_name = '"'+paths_dict[key]+'"'
		raw_command = " ".join(["ffmpeg -i", safe_original_name, parameters, safe_destination_name])
		args = shlex.split(raw_command)
		processes.add(subprocess.Popen(args))
		if len(processes) >= max_processes:
			os.wait()
			processes.difference_update([
				p for p in processes if p.poll() is not None])
	while None in [p.poll() for p in processes]:
		time.sleep(0.5)
	#We need to explicitly terminate the master process here, as otherwise the shell "hangs" and the user needs to press enter to return to a new prompt.
	os.system('kill %d' % os.getpid())
