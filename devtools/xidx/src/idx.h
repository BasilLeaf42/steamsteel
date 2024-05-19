/*
  Name: idx.h 
  Copyright: Vercingetorix (vercingetorix11@gmail.com)
  Author: Vercingetorix (vercingetorix11@gmail.com)
  Date: 06/03/05
  Status: WIP
  License: This file is considered part of the program 'xidx'
  Description: A class to load and write to the idx/dat format for the game 
    Rome: Total War
*/

/*
TODO:    
    Add skeleton structure loading from cas file.
    Add speed scaling.
    
*/

/* 
    
Update log:
    06/07/05 Fixed scaling bugs.
    06/05/05 Added xidxShell.
    06/02/05 Added skeleton extraction/packing.
    06/01/05 Fixed animation scale problem.
    04/23/05 Added animation classes and reorganized a few things.
    04/17/05 First release.
    03/15/05 Started rewrite.
*/


#ifndef IDX_H
#define IDX_H

/*magic numbers*/
const char SSND[] = "SND.PACK";
const char SANM[] = "ANIM.PACK";
const char SSKL[] = "SKEL.PACK";
const unsigned int STRDELIM = 3452816640; 

#define MP3TAG 13


#include "main.h"
#include <stdio.h>
#include <stdlib.h>


class idxSubFile {
    public:
                     idxSubFile();
                     ~idxSubFile();
        virtual bool Read(FILE*)=0;
        virtual bool Write(FILE*)=0;
        virtual bool GatherInfo()=0;
        virtual bool PrepareDataOut();
        virtual void ParseFilename( const char* );
        virtual void PrintFilename();
        void         Clean();
        bool         Extract(FILE*);        
        bool         ExtractFile(FILE*,FILE*);
        bool         WriteFile( FILE* , FILE* , const char* );
        void         SetFilename( const char* );
        
    public: 
         static stack<str> dirs;
         unsigned int  beginFileOffset; //where the file starts
	     unsigned int  fileSize;       //how big it is...	 
	     char filename[256];
	     char *buffer;
};



class idxFile{
    public:
                     idxFile();
                     ~idxFile();
        bool         Write( const char*, const char**, int );
        bool         Extract( const char*, bool);
    private:
        virtual void WriteHeader()=0;
        virtual bool ReadHeader()=0;
        virtual void Init()=0;
        virtual void Allocate(int)=0;
        bool         OpenFiles( const char* , const char*  );
        void         CloseFiles();       
  
    public:
        const char*  filetype;
        unsigned int fileVersion;
        unsigned int numFiles;
        idxSubFile  *subFiles;
        FILE        *fp, *fp2;
};  

class sidxSubFile : public idxSubFile{
    public:
                     sidxSubFile();
        virtual bool Read(FILE*);
        virtual bool Write(FILE*);
        virtual bool GatherInfo();
    private:
        int  control[4];	 //contains info about sound file,
}; 
   
class sidxFile : public idxFile{
    public:
        virtual void Init();
    private:
        virtual void WriteHeader();
        virtual bool ReadHeader();
        virtual void Allocate(int);
    
};

class aidxSubFile : public idxSubFile{
    public:
                     aidxSubFile();
        virtual bool Read(FILE*);
        virtual bool Write(FILE*);
        virtual bool GatherInfo();
        virtual bool PrepareDataOut();
        virtual void ParseFilename( const char* );
        virtual void PrintFilename();
        bool         Scale();        
    private:
        bool         CheckProblemCas();
    public: 
        int   entrySize; 
        float scale; //deprecated??
        short numFrames;
        short numBones;
        char  type;
            
}; 
   
class aidxFile : public idxFile{
    public:
        virtual void Init();
    private:
        virtual void WriteHeader();
        virtual bool ReadHeader();
        virtual void Allocate(int);
    
};

class kidxSubFile : public idxSubFile{
    public:
        kidxSubFile();
        virtual bool Read(FILE*);
        virtual bool Write(FILE*);
        virtual bool GatherInfo();
    public: 
        int   len;
            
}; 
   
class kidxFile : public idxFile{
    public:
        virtual void Init();
    private:
        virtual void WriteHeader();
        virtual bool ReadHeader();
        virtual void Allocate(int);
    
};
#endif
