import pandas as pd
from os import path

def compile_votes(raw_votes):
	raw_votes = path.abspath(path.expanduser(raw_votes))
	df = pd.read_csv(raw_votes)
