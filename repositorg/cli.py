#!/usr/bin/python
__author__ = 'Horea Christian'
import argh
import argparse
import sys

def main():
	from repositorg.base import reposit, reposit_legacy, reformat
	from repositorg.extractor import redundant
	from repositorg.processing import vidproc, audioproc, tag
	argh.dispatch_commands([reposit, reposit_legacy, reformat, redundant, vidproc, audioproc, tag])

if __name__ == '__main__':
	main()
