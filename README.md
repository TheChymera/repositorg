#Organamer

Organamer is a script suite made to help you automatically organize (and rename) large collections of files for storage (e.g. pictures).

##Installation

####On [Gentoo Linux](http://en.wikipedia.org/wiki/Gentoo_linux) and [Derivatives](http://en.wikipedia.org/wiki/Category:Gentoo_Linux_derivatives):

Organamer is available for [Portage](http://en.wikipedia.org/wiki/Portage_(software)) via the [chymeric overlay](https://github.com/TheChymera/chymeric) as **[media-gfx/organamer](https://github.com/TheChymera/chymeric/tree/master/media-gfx/stackHDR)**.
Just run the following command:

```
emerge media-gfx/stackHDR
```

*If you are not yet using this overlay, it can be enabled with just two commands, as seen in [the README](https://github.com/TheChymera/chymeric).*

####On all other Operating Systems:

For all other Linux distributions or operating systems, the script can also be run directly from its containing directory (and thus, needs only be downloaded from here):

```
git clone https://github.com/TheChymera/stackHDR.git /your/mkstage4/directory
cd /your/mkstage4/directory
chmod +x mkstage4.sh
```

*Please bear in mind that this will not pull in any dependencies, make sure you have already installed everything under the Dependencies section.*

##Dependencies:

* **[Hugin](http://en.wikipedia.org/wiki/Hugin_(software))** - in [Portage](http://en.wikipedia.org/wiki/Portage_(software)) as **media-gfx/hugin**
* **[UFRaw](http://en.wikipedia.org/wiki/UFRaw)** - in Portage as **media-gfx/ufraw**

##Usage
Run the script either as `stackHDR` (if installed globally), or as `./stackHDR.sh` from the containing folder:
```
stackHDR [-d] <directory-name> [-f] <one-filename> [-a -e -k -r]
```

Example:
```
stackHDR -f ~/path/to/your/pics/folder/DSC_1337.NEF -f ~/path/to/your/pics/folder/DSC_1933.NEF -f ~/path/to/your/pics/folder/DSC_2014.NEF -ae
```

##Arguments

```
required:
	-d: The directory containing your files (will stack all RAW files therein).
	-f: File to add to stack, repeat as needed. Files should be in the same directory.
    
optional:
	-a: Align images.
	-e: Use enfuse to fuse the images together.
	-k: Keep intermediately created files.
	-r: Remove original RAW files. DO NOT USE unless your files are backed up.
	-h: Show this message.
```

---
Released under the GPLv3 license.
Project led by Horea Christian (address all correspondence to: h.chr@mail.ru)
