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

For all other Linux distributions or operating systems, the script can also be run directly from its containing directory (and thus, needs only be downloaded from here):

```
git clone https://github.com/TheChymera/organamer.git /your/local/organamer/path
pip install [--user] -e /your/local/organamer/path
```

##Usage
Run the script either as `organamer` (if installed globally), or as `./organamer.py` from the containing folder:
```
organamer_reposit.py [-h] [-q] destination source
```

Example:
```
organamer /run/media/chymera/NIKON D5100/DCIM/ /home/chymera/pictures/cameras/nd5100/
```

##Arguments

```
positional arguments:
  destination  Path to store files into (excluding alphanumeric storage
               directories)
  source       Path to reposit files from (all subdirectories will be
               crawled!)

optional arguments:
  -h, --help   show this help message and exit
  -q, --quiet  Do not ask for confirmation - DANGEROUS!
```

---
Released under the GPLv3 license.
Project led by Horea Christian (address all correspondence to: h.chr@mail.ru)
