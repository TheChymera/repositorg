#Organamer

Organamer is Python module that lets you automatically organize (and rename) large collections of files for storage (e.g. pictures).

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
Functions from the `organamer` module can be called from within the module directoy via Python, e.g.  `python -c 'import base; base.reposit()'`.
Additionally we provide the a base command-line function, `organamer` via which you can call our most frequently used functions.
For `organamer_reposit` and `organamer_reformat` we provide legacy direct command line bindings.

####organamer
```
usage: organamer [-h] {reposit,redundant-dirs} ...
```

####organamer_reposit
```
usage: organamer_reposit [-h] [-l LETTERS] [-e EXTENSION] [-p PREFIX] [-a]
                         [-u USER_PASSWORD] [-d DIGITS] [-q]
                         destination source
```

####organamer_reformat
```
usage: organamer_reformat [-h] [-q] [-i LETTERS_START_INDEX] [-d DIGITS]
                          [-p PREFIX]
                          directory
```

###Examples
```
organamer reposit -p gh3_ -e MP4 -d 6 /run/media/user/video0/Video/cameras/gopro_hero3/ /run/media/user/8765-4321/DCIM/103GOPRO/

organamer_reposit "/home/user/pictures/cameras/nd5100/" "/run/media/user/NIKON D5100/DCIM/" -p nd750_ -e JPG -e NEF

organamer_reposit . smb://192.168.65.219/Pryce_Labor/Christian/transit -u SAMBAuser%SAMBApassword -p "age_" -l 0 -e "jpg"

organamer_reformat . -d 4 -p "pcr_"
```

---
Released under the GPLv3.
Project led by Horea Christian (address all correspondence to: h.chr@mail.ru)
