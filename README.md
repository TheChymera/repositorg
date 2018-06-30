# Repositorg
[![Build Status](https://travis-ci.org/TheChymera/repositorg.svg?branch=master)](https://travis-ci.org/TheChymera/repositorg)

Repositorg is Python module that lets you automatically reposit, organize, rename, and process large collections of files (e.g. pictures, or video).

## Installation

#### On [Gentoo Linux](http://en.wikipedia.org/wiki/Gentoo_linux) and [Derivatives](http://en.wikipedia.org/wiki/Category:Gentoo_Linux_derivatives):

Repositorg is available for [Portage](http://en.wikipedia.org/wiki/Portage_(software)) via the [chymeric overlay](https://github.com/TheChymera/chymeric) as **app-misc/repositorg**.
Just run the following command:

```
emerge app-misc/repositorg
```

*If you are not yet using this overlay, it can be enabled with just two commands, as seen in [the README](https://github.com/TheChymera/chymeric).*

#### On all other Operating Systems:

For all other Linux distributions or operating systems, the script can also be run directly from
its containing directory (and thus, needs only be downloaded from here):

```
git clone https://github.com/TheChymera/repositorg.git /your/local/repositorg/path
pip install [--user] -e /your/local/repositorg/path
```

## Usage
Functions from the `repositorg` module can be called from within the module directoy via Python, e.g.  `python -c 'import base; base.reposit()'`.
Additionally we provide the a base command-line function, `repositorg` via which you can call our most frequently used functions.

#### repositorg
```
usage: repositorg [-h] {reposit,reposit_legacy,reformat,redundant,vidproc} ...
```

## Examples

### One-Liners

```
repositorg reformat -l 0 -n 79 -p nd750_ a/*MOV

repositorg reposit_legacy --letters 1 -p nd750_ -e NEF JPG -d 4 ~/Pictures/cameras/nd750/ /run/media/chymera/NIKON\ D750/DCIM/100ND750/

repositorg reposit_legacy -p gh3_ -e MP4 -d 6 /run/media/user/video0/Video/cameras/gopro_hero3/ /run/media/user/8765-4321/DCIM/103GOPRO/

repositorg vidproc -p "-crf 16 -c:a copy" nd750_a00{00,01,02,03,37,38,39,70,71}.MOV

repositorg vidproc -p "-crf 16 -c:a copy -filter:v 'crop=1080:1080:420:0'" nd750_a00{80..84}.MOV

repositorg vidproc -p "-crf 16 -c:a copy -filter:v 'crop=1280:1080:320:0'" nd750_a00{85,86}.MOV

organamer_reposit . smb://192.168.65.219/Pryce_Labor/Christian/transit -u SAMBAuser%SAMBApassword -p "age_" -l 0 -e "jpg"
```

The last call is to the legacy `organamer_reposit` function which we have stopped providing 19-08-2016.

### Workflows

#### Reposit audio recordings using a continuous namespace with one hierarchical level:

This assumes that you are starting with `.wav` files produced by your recorder.

```
cd /run/media/chymera/DEVICE0/recordings_directory/
repositorg audioproc *
repositorg tag -e mp3 -a "Horea Christian" *
repositorg repositi_legacy --letters 1 -p deviceid_ -e mp3 -d 4 ~/audio_directory/deviceid ./
rm *mp3
```

---
Released under the GPLv3.
Project led by Horea Christian (address all correspondence to: h.chr@mail.ru)
