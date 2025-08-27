# Repositorg
[![Build Status](https://travis-ci.com/TheChymera/repositorg.svg?branch=master)](https://travis-ci.com/TheChymera/repositorg)

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
Additionally we provide a base command-line function, `repositorg` via which you can call our most frequently used functions.

#### repositorg
```
usage: repositorg [-h] {reposit,reformat,redundant,vidproc} ...
```
## Triggers

Repositorg is even better in conjunction with automatic triggers.
Mount or time monitoring functionality is handled out-of-the-box by your Unix-like system, but is best not hacked programmatically
(especially since there is no way for us to know at what time and what devices you would like to reposit from).
Therefore, as soon as you have put together a workflow to suit your needs (see examples), this will need a bit of manual configuration on your part.

#### Trigger by UUID Mount

A very useful way to trigger your workflow is automatically upon device insertion.
For this you need a unique identifier for your device, of which the best is the Universally Unique Identifier (UUID).
To obtain this string, run the following command, and look for the mount point on the output; the UUID will be listed to the right of it, e.g. (here it would be `2016-07-04-02-56-54-00` for the NIKON storage):

```
youruser@yhourhost ~ $ findmnt -o TARGET,UUID
TARGET                            UUID
/                                 60eacce4-5634-4230-a87c-ff9e8d4a92cc
├─/dev
│ ├─/dev/shm
│ ├─/dev/pts
│ ├─/dev/mqueue
│ └─/dev/hugepages
├─/sys
│ ├─/sys/fs/cgroup
│ │ ├─/sys/fs/cgroup/unified
│ │ ├─/sys/fs/cgroup/systemd
│ │ ├─/sys/fs/cgroup/cpuset
│ │ ├─/sys/fs/cgroup/freezer
│ │ └─/sys/fs/cgroup/cpu,cpuacct
│ ├─/sys/firmware/efi/efivars
│ ├─/sys/fs/fuse/connections
│ └─/sys/kernel/debug
├─/proc
│ └─/proc/sys/fs/binfmt_misc
├─/run
│ ├─/run/media/chymera/NIKON D750 2016-07-04-02-56-54-00
│ ├─/run/user/115
│ └─/run/user/1000
├─/tmp
└─/boot                           3E21-D52A

```

After having determined the UUID, setting your workflow up to automatically execute is as simple as creating a new executable file under `~/.repositorg/sources/<UUID>.sh` (as seen here).
To test the workflow, you can start the UUID trigger script (run `.repositorg/uuid_trigger.sh`), and (re)insert your medium.
If you wish your system to always be on the lookout for device insertion, you can use the included [OpenRC](.gentoo/app-misc/repositorg/files/repositorg_uuid.initd) or [systemd](.gentoo/app-misc/repositorg/files/repositorg_uuid.service) service files, or add the following line to your user crontab (start editing the crontab by running `crontab -e`):

```
@reboot . /etc/profile ; ~/.repositorg/UUID_trigger.sh
```

## Examples

### One-Liners

```
repositorg reformat -l 0 -n 79 -p nd750_ a/*MOV

repositorg vidproc -p "-crf 16 -c:a copy" nd750_a00{00,01,02,03,37,38,39,70,71}.MOV

repositorg vidproc -p "-crf 16 -c:a copy -filter:v 'crop=1080:1080:420:0'" nd750_a00{80..84}.MOV

repositorg vidproc -p "-crf 16 -c:a copy -filter:v 'crop=1280:1080:320:0'" nd750_a00{85,86}.MOV
```

### Workflows

Workflows are best stored in files under a dedicated Repositorg directory in the user's home path at `~/.repositorg`, for which we distribute an [example](.repositorg).
An [UUID trigger](.repositorg/UUID_trigger.sh) is also provided, which can be called at boot, to monitor for mount events.
UUIDs-based workflows ([example](.repositorg/sources/UUIDs/EXAMPLE-UUID.sh)) are best stored one directory level deeper.
We further provide examples for [SAMBA fetching](.repositorg/sources/example_samba.sh), and client-side [SSH pushing](.repositorg/repositorg_push.sh) (with the associated server-side [post-hook](.repostiorg/sources/example-device_post-hook.sh)).

#### Reposit audio recordings using a continuous namespace with one hierarchical level:

This assumes that you are starting with `.wav` files produced by your recorder.

```
cd /run/media/chymera/DEVICE0/recordings_directory/
repositorg audioproc *
repositorg tag -e mp3 -a "Horea Christian" *
repositorg reposit --letters 1 --in-regex '^.*\.(?P<extension>(mp3))$' --out-string '{LETTERS}/s41_{LETTERS}{DIGITS}.{extension!l}' /run/media/chymera/PHONE0/recordings/external\ recordings/ ~/pu_data/audio/s41/
rm *mp3
```

## Known issues

### Command Prompt Broken after `repositorg audioproc` or `repositorg vidproc`

Both `repositorg audioproc` or `repositorg vidproc` call `ffmpeg` internally.
When this program is parallelized, the command prompt may end up broken after the pool has finished executing.
This is likely because some strange character is returned to the terminal.
The solution is to type `reset` into the terminal (you may not actually see the test), press Enter and wait or repeat once.


---
Project led by Horea Christian (address correspondence to: horea.christ@yandex.com)
