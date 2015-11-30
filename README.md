#Organamer

Organamer is a script suite made to help you automatically organize (and rename) large collections of files for storage (e.g. pictures).

##Installation

####On [Gentoo Linux](http://en.wikipedia.org/wiki/Gentoo_linux) and [Derivatives](http://en.wikipedia.org/wiki/Category:Gentoo_Linux_derivatives):

Organamer is available for [Portage](http://en.wikipedia.org/wiki/Portage_(software)) via the [chymeric overlay](https://github.com/TheChymera/chymeric) as **app-misc/organamer**.
Just run the following command:

```
emerge app-misc/organamer
```

*If you are not yet using this overlay, it can be enabled with just two commands, as seen in [the README](https://github.com/TheChymera/chymeric).*

####On all other Operating Systems:

For all other Linux distributions or operating systems, the script can also be run directly from 
its containing directory (and thus, needs only be downloaded from here):

```
git clone https://github.com/TheChymera/organamer.git /your/local/organamer/path
pip install [--user] -e /your/local/organamer/path
```

##Usage
Functions from the `organamer` module can be called via python, e.g.  `python -c 'import organamer; 
organamer.base.reposit()'`.
Additionally we provide a more specific CLI scripts which you can run the most frequently used of our 
functions:

####organamer_reposit
```
usage: organamer_reposit [-h] [-l LETTERS] [-e EXTENSION] [-p PREFIX] [-a]
                         [-u USER_PASSWORD] [-d DIGITS] [-q]
                         destination source
```

Examples:
```
organamer_reposit "/home/chymera/pictures/cameras/nd5100/" "/run/media/chymera/NIKON D5100/DCIM/" -p nd750_

organamer_reposit . smb://192.168.65.219/Pryce_Labor/Christian/transit -u SAMBAuser%SAMBApassword -p "age_" -l 0 -e "jpg"
```

Arguments:

```
positional arguments:
  destination           Path to store files into (excluding alphanumeric
                        storage directories)
  source                Path to reposit files from (all subdirectories will be
                        crawled!)

optional arguments:
  -h, --help            show this help message and exit
  -l LETTERS, --letters LETTERS
                        Prepend the specified number of letters to
                        theincremental nummeration (default is 1).
  -e EXTENSION, --extension EXTENSION
                        Filter by this extension (currently works for SAMBA
                        share download ONLY).
  -p PREFIX, --prefix PREFIX
                        Add this prefix to all files.
  -a, --parent-prefix   Add the name of the rot dir as a prefix to all files
                        (defult FALSE).
  -u USER_PASSWORD, --user-password USER_PASSWORD
                        User and password for your remote file source (format:
                        `user%password`)
  -d DIGITS, --digits DIGITS
                        Numerate files using the specified number of digits.
  -q, --quiet           Do not ask for confirmation - DANGEROUS!

```


####organamer_reformat
```
usage: organamer_reformat [-h] [-q] [-i LETTERS_START_INDEX] [-d DIGITS]
                          [-p PREFIX]
                          directory
```

Example:
```
organamer_reformat . -d 4 -p "pcr_"
```

Arguments:

```
positional arguments:
  directory             The directory containing the files that need
                        reformatting.

optional arguments:
  -h, --help            show this help message and exit
  -q, --quiet           Do not ask for confirmation - DANGEROUS!
  -i LETTERS_START_INDEX, --letters-start-index LETTERS_START_INDEX
                        Numerate with letters starting at this index (default
                        is None; specify values as integers: 0=a, 1=b, etc.).
  -d DIGITS, --digits DIGITS
                        Numerate files using the specified number of digits.
  -p PREFIX, --prefix PREFIX
                        Add this prefix to all files.
```


---
Released under the GPLv3 license.
Project led by Horea Christian (address all correspondence to: h.chr@mail.ru)
