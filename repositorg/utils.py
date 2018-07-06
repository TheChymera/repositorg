import hashlib
from string import Formatter

class CaseFormatter(Formatter):
	"""An extended format string formatter for upper/lowercase functionality."""
	def convert_field(self, value, conversion):
		""" Extend conversion symbol
		Following additional symbol has been added
		* l: convert to string and low case
		* u: convert to string and up case

		default are:
		* s: convert with str()
		* r: convert with repr()
		* a: convert with ascii()
		"""

		if conversion == "u":
			return str(value).upper()
		elif conversion == "l":
			return str(value).lower()
		# Do the default conversion or raise error if no matching conversion found
		super(CaseFormatter, self).convert_field(value, conversion)

		# return for None case
		return value

def sha256_hashfile(file_path, blocks="all"):
	hasher = hashlib.sha256()
	blocksize = hasher.block_size
	try:
		afile = open(file_path, "rb")
	except IOError:
		return
	buf = afile.read(blocksize)
	block_count=0
	while len(buf) > 0:
		if blocks == "all":
			pass
		elif block_count > blocks:
			break
		hasher.update(buf)
		buf = afile.read(blocksize)
		block_count += 1

	return hasher.hexdigest()

def query_yes_no(prompt_message, default_choice="no"):
	"""Print a yes/no prompt via raw_input() and return the answer.

	"prompt_message" is a string that is presented to the user.
	"default_choice" is the presumed answer if the user just hits <Enter>.
		It must be "yes" (the default_choice), "no" or None (meaning
		an answer is required of the user).

	The "answer" return value is one of "yes" or "no".

	Author: fmark (http://stackoverflow.com/users/103225/fmark)
	"""
	import sys

	valid = {"yes": True, "y": True, "ye": True,
			 "no": False, "n": False}
	if default_choice is None:
		prompt = " [y/n] "
	elif default_choice == "yes":
		prompt = " [Y/n] "
	elif default_choice == "no":
		prompt = " [y/N] "
	else:
		raise ValueError("invalid default answer: '%s'" % default_choice)

	while True:
		sys.stdout.write(prompt_message + prompt)
		try:
			choice = raw_input().lower()
		except NameError:
			choice = input().lower()
		if default_choice is not None and choice == '':
			return valid[default_choice]
		elif choice in valid:
			return valid[choice]
		else:
			sys.stdout.write("Please respond with 'yes' or 'no' "
							 "(or 'y' or 'n').\n")
