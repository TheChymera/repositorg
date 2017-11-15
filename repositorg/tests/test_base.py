from repositorg import base
from os import path

DATA_DIR = path.abspath(path.join(path.dirname(path.realpath(__file__)),'../../example_data/'))

def test_pair_lastfile():
	source_files = [
			'source/bla01.JPG','source/bla01.NEF',
			'source/bla02.JPG','source/bla02.NEF',
			'source/bla03.JPG','source/bla03.NEF',
			]
	destination_files = ['destination/bar002.JPG','destination/bar002.NEF']
	expected_pair = ['destination/bar002.NEF', 'source/bla01.NEF']

	destination_files = [path.join(DATA_DIR,i) for i in destination_files]
	source_files = [path.join(DATA_DIR,i) for i in source_files]
	expected_pair = [path.join(DATA_DIR,i) for i in expected_pair]

	pair = base.pair_lastfile(destination_files,source_files)

	assert expected_pair == pair
