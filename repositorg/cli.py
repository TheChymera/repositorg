#!/usr/bin/python
__author__ = 'Horea Christian'
import argh
import argparse
import base
import sys

def main():
	from extractor import redundant_dirs
	from base import reposit, reformat
	argh.dispatch_commands([reposit, reformat, redundant_dirs])

if __name__ == '__main__':
	main()
