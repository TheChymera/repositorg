#!/usr/bin/python
__author__ = 'Horea Christian'
import argparse
import base
import sys

def reposit():
	parser = argparse.ArgumentParser()
	parser.add_argument("destination", help="Path to store files into (excluding alphanumeric storage directories)", type=str)
	parser.add_argument("source", help="Path to reposit files from (all subdirectories will be crawled!)", type=str)
	parser.add_argument("-l", "--letters", help="Prepend the specified number of letters to theincremental nummeration (default is 0).", default=1, type=int)
	parser.add_argument("-e", "--extension", help="Filter by this extension.", type=str)
	parser.add_argument("-p", "--prefix", help="Add this prefix to all files.", default="", type=str)
	parser.add_argument("-a", "--parent-prefix", help="Add the name of the rot dir as a prefix to all files (defult FALSE).", action="store_true")
	parser.add_argument("-u", "--user-password", help="User and password for your remote file source (format: `user%%password`)", type=str)
	parser.add_argument("-d", "--digits", help="Numerate files using the specified number of digits.", default=4, type=int)
	parser.add_argument("-q", "--quiet", help="Do not ask for confirmation - DANGEROUS!", action="store_false")
	args = parser.parse_args()

	base.reposit(destination_root=args.destination, source_root=args.source, prompt=args.quiet, digits=args.digits, letters=args.letters, extension=args.extension, parent_prefix=args.parent_prefix, prefix=args.prefix, user_password=args.user_password)

def reformat():
	parser = argparse.ArgumentParser()
	parser.add_argument("directory", help="The directory containing the files that need reformatting.", type=str)
	parser.add_argument("-q", "--quiet", help="Do not ask for confirmation - DANGEROUS!", action="store_false")
	parser.add_argument("-i", "--letters-start-index", help="Numerate with letters starting at this index (default is None; specify values as integers: 0=a, 1=b, etc.).", type=int)
	parser.add_argument("-d", "--digits", help="Numerate files using the specified number of digits.", default=4, type=int)
	parser.add_argument("-p", "--prefix", help="Add this prefix to all files.", type=str)
	args = parser.parse_args()

	base.reformat(root_directory=args.directory, prompt=args.quiet, digits=args.digits, letters_start_index=args.letters_start_index, prefix=args.prefix)
