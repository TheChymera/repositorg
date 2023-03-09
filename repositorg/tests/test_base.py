from os import path, listdir

DATA_DIR = path.abspath(path.join(path.dirname(path.realpath(__file__)),'../../example_data/'))

def test_pair_lastfile():
	from ..base import pair_lastfile
	source_files = [
			'source_a/bla01.JPG','source_a/bla01.NEF',
			'source_a/bla02.JPG','source_a/bla02.NEF',
			'source_a/bla03.JPG','source_a/bla03.NEF',
			]
	destination_files = ['destination/bar002.JPG','destination/bar002.NEF']
	expected_pair = ['destination/bar002.NEF', 'source_a/bla01.NEF']

	destination_files = [path.join(DATA_DIR,i) for i in destination_files]
	source_files = [path.join(DATA_DIR,i) for i in source_files]
	expected_pair = [path.join(DATA_DIR,i) for i in expected_pair]

	pair = pair_lastfile(destination_files,source_files)

	assert expected_pair == pair

def test_reposit_default_args(tmp_path):
	from ..base import reposit
	tmp_path = str(tmp_path)
	in_dir = path.join(DATA_DIR, "source_a")
	reposit(in_dir, tmp_path, no_ask=True)
	expected_files = (
		"0000.JPG",
		"0000.NEF",
		"0001.JPG",
		"0001.NEF",
		"0002.JPG",
		"0002.NEF",
		"0003.JPG",
		"0003.NEF",
		"0004.JPG",
		"0004.NEF",
		"0005.JPG",
		"0005.NEF",
		"0006.JPG",
		"0006.NEF",
		"0007.JPG",
		"0007.NEF",
		"0008.JPG",
		"0008.NEF",
		"0009.JPG",
		"0009.NEF",
		"0010.JPG",
		"0010.NEF",
		"0011.JPG",
		"0011.NEF",
		"0012.JPG",
		"0012.NEF",
		"0013.JPG",
		"0013.NEF",
		"0014.JPG",
		"0014.NEF",
		"0015.JPG",
		"0015.NEF",
		"0016.JPG",
		"0016.NEF",
		"0017.JPG",
		"0017.NEF",
		"0018.JPG",
		"0018.NEF",
		)
	# Do as many files come out as they should?
	assert len(listdir(tmp_path)) == len(expected_files)
	# Do they have the correct filenames?
	for i in listdir(tmp_path):
		assert i in expected_files
