from repositorg import base
from os import path

def test_pair_lastfile():
	source_files = [
			'../../example_data/source/bla01.JPG','../../example_data/source/bla01.NEF',
			'../../example_data/source/bla02.JPG','../../example_data/source/bla02.NEF',
			'../../example_data/source/bla03.JPG','../../example_data/source/bla03.NEF',
			]
	destination_files = ['../../example_data/destination/bar002.JPG','../../example_data/destination/bar002.NEF']
	expected_pair = ['../../example_data/destination/bar002.NEF', '../../example_data/source/bla01.NEF']
	expected_pair = [path.abspath(path.expanduser(i)) for i in expected_pair]
	pair = base.pair_lastfile(destination_files,source_files)

	assert expected_pair == pair
