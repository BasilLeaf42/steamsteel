----------------------------------------------
Rome Total War idx packer/extracter
By Vercingetorix

v0.97 - 10/19/05


----------------------------------------------
Installation Instructions:
----------------------------------------------
Installation

To extract sounds -
Unzip xidx.exe and extract_sounds_idx.bat to your Rome-Total war\data\sounds folder
and run extract_all_idx.bat.

To extract animations -
Unzip xidx.exe and extract_animations.bat to your Rome-Total war\data\animations folder
and run extract_animations.bat.

To extract skeletons -
Unzip xidx.exe and extract_skeletons.bat to your Rome-Total war\data\animations folder
and run extract_skeletons.bat.

----------------------------------------------
Important Notes
----------------------------------------------

program usage: [options] [files...]
command line options:
      -a      idx pack(s) are animation packs, by default they are assumed to be sound
      -s      idx pack(s) are skeleton packs	
      -c      create an idx pack file
      -x      extract idx pack file(s)
      -t      list the contents of idx pack file(s)
      -f      name of idx pack when creating. (output filename must follow)
      -v      verbose output
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

--New in v0.93--
Listing the contents of the animation pack will only list the filenames. 
To list both the file names and the scaling information add the verbose option ("-v").

----------------------------------------------
File List:
----------------------------------------------
xidx.exe
ReadMe.txt
extract_sounds.bat
extract_animations.bat
pack_animations.bat
extract_skeletons.bat
pack_skeletons.bat
pack_example_music_idx.bat
src/xidx.dev
src/main.cpp
src/main.h
src/idx.cpp
src/idx.h
src/shared.cpp
src/shared.h

----------------------------------------------
Latest Changes/Update Log:
----------------------------------------------
v0.97 - 10/19/05 Fixed problem where BI animations would not pak
v0.94 - 06/09/05 Further fixes. Added skeleton scaling.
v0.93 - 06/08/05 Major bug fixes regarding animation scaling
v0.91 - 06/06/05 Added xidx shell.
v0.89 - 06/02/05 Added skeleton extraction/packing. Fixed animation scale problem.
v0.82 - 04/23/05 Animation packs now supported
v0.70 - 04/17/05 Released
----------------------------------------------
Licence Agreement:
----------------------------------------------
Terms of Use
This software is free and there is no warranty what so ever. Use at your own risk. 

Copywrite notice

    Copyright (C) <2004,2005>  <Vercingetorix (vercingetorix11@gmail.com)>

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details at 
    http://www.fsf.org/licensing/licenses/gpl.txt
