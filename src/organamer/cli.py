#!/usr/bin/python
__author__ = 'Horea Christian'
import argparse
import base

def reposit():
	parser = argparse.ArgumentParser()
	parser.add_argument("destination", help="Path to store files into (excluding alphanumeric storage directories)", type=str)
	parser.add_argument("source", help="Path to reposit files from (all subdirectories will be crawled!)", type=str)
	parser.add_argument("-u", "--user-password", help="User and password for your remote file source (format: `user%password`)", type=str)
	parser.add_argument("-q", "--quiet", help="Do not ask for confirmation - DANGEROUS!", action="store_false")
	args = parser.parse_args()

	base.reposit(destination_root=args.destination, source_root=args.source, prompt=args.quiet, user_password=args.user_password)
