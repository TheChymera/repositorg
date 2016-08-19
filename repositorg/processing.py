import argh
import os
import shlex
import subprocess
import time

@argh.arg('source', nargs='+', type=str)
@argh.arg('-e', '--extensions', nargs='+', type=str)
def vidproc(source, extensions=[], output_ext="mkv", parameters="-vf 'transpose=dir=clock, transpose=dir=clock, crop=1080:1080' -crf 16 -c:a copy", max_processes =4):
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
	If the function complains of too few arguments, the mandatory positional argument "source" might be caugt by one of the others.
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

	in_paths = [in_path for in_path in in_paths if os.path.splitext(in_path)[1] in extensions]
	paths_dict = {key:key for key in in_paths}
	paths_dict.update((x, os.path.splitext(y)[0]+output_ext) for x,y in paths_dict.items())

	processes = set()
	for key in paths_dict:
		raw_command = " ".join(["ffmpeg -i", key, parameters, paths_dict[key	]])
		args = shlex.split(raw_command)
		processes.add(subprocess.Popen(args))
		if len(processes) >= max_processes:
			os.wait()
			processes.difference_update([
				p for p in processes if p.poll() is not None])

	# command = "ffmpeg -i nd750_a0040.MOV -vf "transpose=dir=clock, transpose=dir=clock, crop=1080:1080" -crf 16 -c:a copy out.mkv "

if __name__ == '__main__':
	vidproc(["~/data/cameras/nd750/a/"], extensions=["MOV"])
