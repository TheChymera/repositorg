import os

import subprocess
import os
import time


def simple_processing(files_path, input_ext, output_ext, parameters="-vf 'transpose=dir=clock, transpose=dir=clock, crop=1080:1080' -crf 16 -c:a copy", max_processes =4):
	if input_ext == output_ext:
		raise ValueError("The input and output extensions should be different. If you want to keep the format try to de/capitalize the new extension.")

	files_path = os.path.expanduser(files_path)
	in_paths = os.listdir(files_path)
	in_paths = [in_path for in_path in in_paths if in_path.endswith(input_ext)]
	paths_dict = {key:key for key in in_paths}

	paths_dict.update((x, os.path.splitext(y)[0]+"."+output_ext) for x,y in paths_dict.items())

	processes = set()
	for key in paths_dict:
		in_file_path = os.path.join(files_path,key)
		out_file_path = os.path.join(files_path,paths_dict[key])
		processes.add(subprocess.Popen(["ffmpeg","-i",in_file_path,parameters,out_file_path]))
		if len(processes) >= max_processes:
			os.wait()
			processes.difference_update([
				p for p in processes if p.poll() is not None])

if __name__ == '__main__':
	simple_processing("~/data/cameras/nd750/a/", "MOV", "mkv")
