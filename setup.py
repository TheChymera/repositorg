from setuptools import setup, find_packages

setup(
	name="organamer",
	version="",
	description = "Automatically organize (and rename) large collections of files",
	author = "Horea Christian",
	author_email = "h.chr@mail.ru",
	url = "https://github.com/TheChymera/organamer",
	keywords = ["rename", "organize", "batch"],
	packages = find_packages("src"),
	package_dir = {"":"src"},
	classifiers = [],
	install_requires = [],
	provides = ["organamer"],
	scripts=['src/organamer/extractor.py'],
	entry_points = {'console_scripts' : \
			['organamer_reposit = organamer.cli:reposit',
			'organamer_reformat = organamer.cli:reformat']
		}
	)
