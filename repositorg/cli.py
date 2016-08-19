#!/usr/bin/python
__author__ = 'Horea Christian'
import argh
import argparse
import base
import sys

def main():
	from base import reposit, reformat
	from extractor import redundant
	from processing import vidproc
	argh.dispatch_commands([reposit, reformat, redundant, vidproc])

if __name__ == '__main__':
	main()
