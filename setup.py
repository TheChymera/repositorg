from setuptools import setup, find_packages

setup(
	name="repositorg",
	version="",
	description = "Automatically reposit, organize, rename, and process large collections of files",
	author = "Horea Christian",
	author_email = "h.chr@mail.ru",
	url = "https://github.com/TheChymera/repositorg",
	keywords = ["reposit","rename", "organize", "batch", "preprocess"],
	packages = find_packages("src"),
	package_dir = {"":"src"},
	classifiers = [],
	install_requires = [],
	provides = ["organamer"],
	entry_points = {'console_scripts' : \
			['organamer_reposit = organamer.cli:reposit',
			'organamer_reformat = organamer.cli:reformat',
			'organamer = organamer.cli:main']
		}
	)
