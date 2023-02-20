#!/usr/bin/python
__author__ = 'Horea Christian'
import argh
import argparse
import sys

def main():
	from repositorg.base import fetch, reposit, reformat
	from repositorg.extractor import redundant
	from repositorg.processing import vidproc, audioproc, imgproc, tag
	argh.dispatch_commands([fetch, imgproc, reposit, reformat, redundant, vidproc, audioproc, tag])

if __name__ == '__main__':
	main()
