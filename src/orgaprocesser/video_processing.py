def simple_processing(files_path, rotate=False, crop=None):
	command = "ffmpeg -i nd750_a0040.MOV -vf "transpose=dir=clock, transpose=dir=clock, crop=1080:1080" -crf 16 -c:a copy out.mkv "

if __name__ == '__main__':
	simple_processing(rotate=True, crop="")
