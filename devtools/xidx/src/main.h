/*
  Program Name: xidx
  Copyright: Vercingetorix (vercingetorix11@gmail.com)
  Author: Vercingetorix (vercingetorix11@gmail.com)
  Date: 03/28/05
  License: This file is considered part of the program 'xidx'
*/


#ifndef _XIDX_MAIN_H
#define _XIDX_MAIN_H

#include <direct.h>
#include <string.h>
#include "shared.h"

#define HELP_HELP_STR "usage: help [command]\nexamples:\n\thelp chpath"

#define HELP_CHPATH_STR \
    "changes the filename paths in a skeleton file\n\n"\
    "usage: chpath <skeleton filename> [LIST] [COPY] [ALL] <filename> <new filename>\n"\
    "specifying \"ALL\" will match all strings as opposed to just the first\n"\ 
    "specifying \"COPY\" will actually copy the files and not modify the paths\n"\
    "specifying \"LIST\" will list the paths\n"\
    "examples:\n\tchpath fs_new_skel ALL data/animations/LIS data/animations/NIS"\
    "\n\tchpath fs_new_skel \"data/animations/LIS 01 Stand Idle.cas\""\
    " \"data/animations/My new animation.cas\""\
    "\n\tchpath fs_new_skel COPY ALL data/animations/ data/animations/new_skel/"
    
#define HELP_SKEL_STR "replaces the skeleton hierarchy with one from a .cas file\n" \
                      "usage: skel <skeleton filename> <cas filename>\n" \
                      "examples:\n\tskel fs_new_skel monster.cas"
#define HELP_SCALE_STR \
    "changes the scale of a skeleton\n" \
    "usage: scale <skeleton filename> [scale value]\n" \
    "if you do not specify a scale value it will print the current one"
    
#define HELP_CLEAR_STR "clears screen"

#define HELP_FORK_STR "passes the command to the system to be executed\n" \
                      "usage: fork <command>\n" \
                      "example:\n\tfork xidx -ts skeleton.idx"
    

/*globals...*/
extern bool  verbose;

//functions to go with shell
struct xidxFunc{    
    xidxFunc( const char* name, const char* usage, int (*execute)(int, char**) ){
        this->name  = name;
        this->usage = usage;
        this->execute = execute;
    }    
    const char* name;
    const char* usage;
    int (*execute)( int, char** );
};    

        
//XIDX 'shell'
class xidxShell{
    public:
        xidxShell();
        ~xidxShell();
    public:
        int Run();
        int Parse( char* );
    public:
        static int help( int, char** );
        static int chpath( int, char** );
        static int clear( int, char** );
        static int loadskel( int, char** );
        static int fork( int, char** );
        static int scale( int, char** );
        static int exit( int, char** );
    private:
        static xidxFunc* getfn( const char* );
        static stack<char*> gettokens( char*, const char*, bool=true );
        static int numargs( const char** );
        static int readfile( const char*, const char*, void*&, FILE*&, int& );
    private:
        char input[256];
};    
    
#endif
