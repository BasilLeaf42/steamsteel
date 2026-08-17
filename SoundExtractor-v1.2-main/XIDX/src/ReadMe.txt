----------------------------------------------
Rome- and Medieval II- Total War IDX packer/extractor

By Vercingetorix (copyright: 2004, 2005); resurrected, updated and ported to Linux/GCC by The Europa Barbarorum Team (copyright: 2011, 2012)

This version of XIDX should build and run under any POSIX compatible environment and Windows NT. 

v1.2 - 15-04-2012


----------------------------------------------
Table of contents:
----------------------------------------------

  Installation
  Usage
  Latest Changes/Update Log
  Building from source
  Licence Agreement

----------------------------------------------
Installation
----------------------------------------------

If you use a source distribution of the XIDX project you can simply extract the 7zip archive and proceed with make.  For more information, see the 
“Building from source” section below.

If you use a binary release of the XIDX project you can simply extract the 7zip archive which should give you the following versions of the XIDX program:
 - bin/xidx:
     This is an AMD64 ELF executable. It should run on Linux (AMD64).
 - bin/xidx_x86.exe:
     This is an x86 PE executable. It should run on 32bit and 64bit versions of Windows OSes (2k, XP, Vista, 7, Server R2 etc.) and Wine.
     It should run on any processor of Core vintage or later (or AMD designs of similar age).
 - bin/xidx_amd64.exe:
     This is an AMD64 PE executable. It should run on 64bit versions of Windows OSes (XP, Vista, 7, Server R2 etc.)

The project does not provide any rule to install it as system administrator, so you may want to select your preferred executable and move it manually to a 
suitable location. It makes sense to ensure that this location is on the search PATH used for looking up programs by name, since XIDX is purely a 
commandline program. (Therefore being on the search PATH will make it easier to invoke the program from arbitrary directories.)

----------------------------------------------
Usage
----------------------------------------------

If you use a platform that is not supported by either of these binaries you can try to build from source instead.

program usage: [options] [files...]
command line options:
      -a      idx pack(s) are animation packs, by default they are assumed to be sound
      -s      idx pack(s) are skeleton packs
      -m      idx packs(s) are Medieval II packs, only applies when creating packs.
      -c      create an idx pack file
      -x      extract idx pack file(s)
      -t      list the contents of idx pack file(s)
      -f      name of idx pack when creating. (output filename must follow)
      -v      verbose output
      -b      adds '.bin' suffix to filenames when extracting, removes it when packing
      --help  print the help
      --shell gives you a simple 'shell' for entering commands

You may only specify one of the three "xtc" options. When you create a idx pack the 
filenames can be specified on the command line (after your options). If no files are 
on the command line, it will read filenames from stdin (standard input) with one filename 
per line.

As a note regarding repacking pack.idx: There are some filenames that have spaces at the end,
as well as duplicate files in the pack.idx. Unfortunatly we have to deal with this and a listing
of the data\animations folder will not suffice. I recommend that you save the file list of the 
vanilla pack before you do any editing. ".\xidx -ta >filenames_in_pack_idx.txt" would do the trick.
When you go to repack the animations you would use this list as the input for filenames. 
i.e. ".\xidx -caf pack.idx <filenames_in_pack_idx.txt". 


Examples:
1)  .\xidx -x music.idx
2)  .\xidx -t music.idx >filenames_in_music_idx.txt
3)  .\xidx -c -f my_music_idx.idx <filenames_in_music_idx.txt

The first example extracts all the files within music.idx (relative to the current working directory).
The second example lists all the files within music.idx and saves the output to filenames_in_music_idx.txt
The third example creates a new idx pack with the name my_music_idx. The files that are to
be archived are within filenames_in_music_idx.txt which is redirected to stdin.

In short, the above three commands extracts the music, lists the the files within the pack
and the repacks them. Logically you would overwrite the vanilla sound files with your own files
before you run step 3.

If you wanted to pack all the files in a folder you could do:
dir  .\data\sounds\SFX\* /a:-D /s /b | .\xidx -cf my_sfk.idx
Where you would change ".\data\sounds\SFX\*" to the folder of your choice.

----------------------------------------------
Latest Changes/Update Log:
----------------------------------------------
v1.2  - 15-04-2012 Fix memory leak when opening archives with the wrong archive type flag
v1.1  - 26-03-2012 Fix memory leaks from exit() in usage
		   Change naming conventions for EVT blobs extracted from EVT packs (more useful info in filenames).
v1.0  - 24-02-2012 Fix bug in generated filenames for evt packs, fix version reporting.
v0.99 - 17-01-2012 Fix Valgrind warnings about unitialised variables, fix bug in sound packing.
		   Fix makefile to generate statically linked binaries for Windows.
v0.98 - 17-10-2011 Port/fixes to build on Linux with GCC (tested AMD64 builds of GCC 4.3.2, 4.5.2)
		   Builds with GCC-Mingw32 (tested AMD64 build, version 4.4.4)
		   Fix lurking segfaults on exit and inside the fork function of the XIDX shell.
		   Fix memory allocation, so the tool does not allocate lots of memory it never uses.
		   Add -m option for building Medieval II versions of supported pack types.
		   Add -b option for transparent suffix ('.bin') manipulation (useful with skeletons for avoiding name collisions).
		   Add -e option for assembly/disassembly of event packs.
		   Strip batch files, MS Visual Studio project file etc., added makefile.

v0.97 - 19-10-2005 Fixed problem where BI animations would not pak
v0.94 - 09-06-2005 Further fixes. Added skeleton scaling.
v0.93 - 08-06-2005 Major bug fixes regarding animation scaling
v0.91 - 06-06-2005 Added xidx shell.
v0.89 - 02-06-2005 Added skeleton extraction/packing. Fixed animation scale problem.
v0.82 - 23-04-2005 Animation packs now supported
v0.70 - 17-04-2005 Released

----------------------------------------------
Building from source
----------------------------------------------
The XIDX project now ships a makefile which can be used with GNU make to make building the project easier. For compiling the project 
using the makefile you will need a reasonably modern GCC distribution (G++ frontend) and/or MINGW frontend to same if you intend to 
build a Windows executable. Note that the makefile additionally performs cross compilation to build Windows executables through MINGW. 
The frontends to GCC which it will attempt to use for compiling the project are: g++, i586-mingw32msvc-g++, i686-w64-mingw32-g++, and 
x86_64-w64-mingw32-g++. 

Note that if both i586-mingw32msvc-g++ and i686-w64-mingw32-g++ are found the latter is skipped. The former should be compatible roughly
with all processors of Pentium vintage or later, the latter offers compatibility with Core processors and later. 

If you happen to have other MINGW C++ programs installed you may be able to use dynamically linked versions of the MINGW executables. These have the 
benefit of smaller executable sizes. To do this, simply leave the STATICS variable blank. Generated binaries will then depend on libgcc_sjlj-1.dll and 
libstc++-6.dll in order to work.

When a frontend cannot be found the makefile will skip compilation for the corresponding target platform automatically. 
This means that the makefile may generate the following executables:
  - bin/xidx:
      This is the native executable. It's target platform is whatever the default target platform happens to be (typically the same as the build platform).
      Thus if you run an AMD64 flavour of Linux, this will be an AMD64 ELF binary.
  - bin/xidx_x86.exe:
      This is a statically linked x86 PE executable. It should run on 32bit and 64bit versions of Windows OSes (XP, Vista, 7, Server R2 etc.)
  - bin/xidx_amd64.exe:
      This is a statically linked AMD64 PE executable. It should run on 64bit versions of Windows OSes (XP, Vista, 7, Server R2 etc.)

The dependencies are minimal, any proper POSIX compatible environment with a C++ standard library should satisfy the minimum requirements. When compiling 
for Windows based systems the code uses some Windows specific non-deprecated aliases of deprecated POSIX standard functions as this may help to suppress 
C++ standard conformance warnings when building on Windows.

The makefile provides the following three targets:
  - build:
      This is the default target and builds the program from source. This target includes provisions for cross compiling XIDX to build the Windows 
      binaries on Linux/Unix through MINGW.
  - bin:
      This target sets up the bin/ directory for use by the build target. This target is not intended to be called manually.
  - clean:
      Removes the bin/ directory structure.

It should be possible to build the source using toolchains other than G++ and G++/MINGW, however the makefile doesn't attempt to support this out of the box.

----------------------------------------------
Licence Agreement:
----------------------------------------------
Terms of Use
This software is free and there is no warranty what so ever. Use at your own risk. 
See licence.txt for a copy of the program licence.

    Copyright (C) 2004, 2005  Vercingetorix <vercingetorix11@gmail.com>
    Copyright (C) 2011, 2012  The Europa Barbarorum Team <webmaster@europabarbarorum.com>

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details at 
    http://www.fsf.org/licensing/licenses/gpl.txt
