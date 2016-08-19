from setuptools import setup, find_packages

setup(
	name="repositorg",
	version="",
	description = "Automatically reposit, organize, rename, and process large collections of files",
	author = "Horea Christian",
	author_email = "h.chr@mail.ru",
	url = "https://github.com/TheChymera/repositorg",
	keywords = ["reposit","rename", "organize", "batch", "preprocess"],
	classifiers = [],
	install_requires = [],
	provides = ["repositorg"],
	packages = ["repositorg"],
	entry_points = {'console_scripts' : \
			['repositorg = repositorg.cli:main']
		}
	)
