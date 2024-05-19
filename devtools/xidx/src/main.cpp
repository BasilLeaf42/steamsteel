/*
  Program Name: xidx
  Copyright: Vercingetorix (vercingetorix11@gmail.com)
  Author: Vercingetorix (vercingetorix11@gmail.com)
  Date: 6/8/05
  License: GPL
  Description: A program to read and write to the idx/dat format for the game 
    Rome: Total War
*/


#include <string.h>
#include <assert.h>
#include "idx.h"
#include "main.h"
#include "shared.h"

#define EXTRACT 1
#define CREATE 2
#define LIST 3
#define IDXSOUND 1
#define IDXANIM  2
#define IDXSKEL  3
   
/*globals*/
bool verbose;

void usage(){
    fprintf( stderr,
    "usage: [options] [files]\n"
    "  -a      idx pack(s) are animation packs, by default they are sound\n"
    "  -s      idx pack(s) are skeleton packs\n"
    "  -c      create\n"
    "  -x      extract\n"
    "  -t      list\n"
    "  -f      output file (output filename must follow)\n"
    "  -v      verbose output\n"
    "  --help  print this help\n"
    "  --shell gives you a simple \'shell\' for entering commands\n"
    "please see the readme for more information\n"
    );
    _sleep( 10000 );
    exit( 1 );
}


        
int main(int argc, char *argv[]){
  int   function = 0;
  char* ofile    = "default.idx";
  int   idxType  = IDXSOUND;  
        verbose  = false;
  stack<const char*> files(1024);
  stack< str > infiles(1024);

  fputs( "idx extractor/packer\nVersion 0.97\nMade by Vercingetorix\n", stderr );
 
  
  if( argc == 1 ) usage();
  for(int i=1; i<argc; i++){
    if( argv[i][0] == '-' ){
      char *pstr = &(argv[i][1]);
      while( *pstr ){
          switch ( *pstr ){
              
              case 'a':
                  idxType = IDXANIM;    
                  break;
              case 's':
                  idxType = IDXSKEL;    
                  break;                  
              case 'x':
                  if( function ) usage();   
                  function = EXTRACT;
                  break;
              case 'c':
                  if( function ) usage();   
                  function = CREATE;
                  break;
              case 't':
                  if( function ) usage();   
                  function = LIST;
                  break;
              case 'v':
                  verbose = true;
                  break;
              case 'f':
                  i++;
                  if( !(i<argc) ){
                    fprintf( stderr, "error: expected output file, try --help\n" );
                    return 1;
                  }    
                  ofile = argv[ i ]; 
                  break;
              case '-':
                  if( !strcmp( argv[i], "--help") ) usage();
                  else if( !strcmp( argv[i], "--shell" ) ){
                      xidxShell shell;
                      return shell.Run();
                  }    
                  else fprintf( stderr, 
                  "error: unkown option \"%s\" try --help\n", pstr );
                  return 1;
              default:
                  fprintf( stderr, 
                  "error: unkown option '%c' try --help\n",*pstr );
                  return 1;  
              } /*case*/
              pstr++;
          }/*pstr*/     
      }/*argument parse*/
      else files.push( argv[i] );
  }/*for loop*/


  
  idxFile *idx;
  if( idxType == IDXSOUND )
      idx = new sidxFile;
  else if( idxType == IDXANIM )
      idx = new aidxFile;
  else if( idxType == IDXSKEL )
      idx = new kidxFile;
  
  int result;
  
  switch (function){
    case EXTRACT:
        for(int i=0; i<files.GetSize(); i++){
            fprintf( stderr, "\nExtracting files in %s...\n", files[i] );
            result = idx->Extract( files[i], false );
            fprintf( stderr, 
                result ? "Successfully extracted%s%s\n" : "Failed to extract%s%s\n",
                " idx pack ", files[i]);
        }   
        break;
    case CREATE:
          /*read filenames from stdin*/
          if( files.empty() ){
              char line[256] = {0};
              while( fgets( line, 255, stdin ) ) {
                  if( strpbrk(line,"\n\r") ) *strpbrk(line,"\n\r") = '\0';
                  infiles.push( line );
              } 
              for(int i=0; i<infiles.GetSize(); i++) 
                  files.push( infiles[i].data );    
          }  
        fprintf( stderr, "\nCreating idx file...\n" );               
        result = idx->Write( ofile, files.GetData(), files.GetSize() );
        fprintf( stderr, 
                result ? "Successfully created%s%s\n" : "Failed to create%s%s\n",
                " idx pack ", ofile);
        break;
    case LIST:
        for(int i=0; i<files.GetSize(); i++){
            fprintf( stderr, "\nListing files in %s...\n", files[i] );
            idx->Extract( files[i], true );
        }   
        break;
    default:
        usage();
        break;
    }    
  delete idx;           		
  return 0;    
}

//XIDX 'shell'

typedef int (*FNPTR_INT_VOID_PTR)(void*);
static xidxFunc 
functions[] = {
                xidxFunc( "help:?:man", HELP_HELP_STR, &xidxShell::help ),
                xidxFunc( "exit:quit", "exits xidx", &xidxShell::exit ),
                xidxFunc( "chpath", HELP_CHPATH_STR, &xidxShell::chpath ),
                xidxFunc( "scale", HELP_SCALE_STR, &xidxShell::scale ),
                //todo://xidxFunc( "skel", HELP_SKEL_STR, &xidxShell::loadskel ),
                xidxFunc( "clear:cls:clr", HELP_CLEAR_STR, &xidxShell::clear ),
                xidxFunc( "fork:~:`", HELP_FORK_STR, &xidxShell::fork )
              };    
                                
xidxShell::xidxShell(){
    input[0] = '\0';
}

xidxShell::~xidxShell(){
}
int xidxShell::numargs( const char** args ){
    int count = 0;
    while( *args ) {
        args++;
        count++;
    }
    return count;
}
//omits empty tokens
stack<char*> xidxShell::gettokens( char* str, const char* delim, bool quotes ){
    char** strp = &str;
    char* pstr;
    char* (*tokenizer)( char**, const char*) = quotes ? &qstrsep : strsep;
    stack<char*> tokens;
    
    pstr = tokenizer( strp, delim );
    while( pstr ){       
        if( pstr && *pstr != '\0' ){
            tokens.push( pstr );
            //puts( pstr );
        }    
        pstr = tokenizer( strp, delim );        
    }    
    return tokens;
}    
xidxFunc* xidxShell::getfn( const char* name ){
    for( int i = 0, size = sizeof(functions)/sizeof(xidxFunc); i < size; i++ ){
        char* str = strdup( functions[i].name );
        char* pstr;
        pstr = strtok( str, ":" );
        while( pstr ){           
            if( !stricmp( name, pstr ) ){
                free( str );
                return &functions[i];    
            }
            pstr = strtok( NULL, ":" );
        }
        free( str );        
    }
    fprintf( stderr, "error: `%s` is not a valid command try `help`\n", name );
    return NULL;
}

int xidxShell::readfile( const char* filename, const char* mode, void*& buffer,
                            FILE*& fp, int& fsize ){
    fp = fopen( filename, mode );
    if( !fp ){
        fprintf( stderr, "error: failed to open file `%s`\n", filename );
        return -2;
    }
    fsize = getfilesize( fp );
    if( !(buffer = malloc( fsize ) ) ){
        fprintf( stderr, "error: failed to allocate memory\n" );
        return -3;
    }    
    if( fread( buffer, 1, fsize, fp ) != fsize ){
        fprintf( stderr, "error: an error occured while reading file\n" );
        free( buffer );
        return -4;
    }
    fseek( fp, 0, SEEK_SET );
    return 0;
}    
        
int xidxShell::help( int argc, char** argv ){
    char command[256] = {0};
    xidxFunc* function = NULL;
    
    if( argc != 0 ){
        for( int i = 0; i < argc; i++ ){
            function = getfn( argv[i] );
            if( !function ) return -1;
            fprintf( stdout, "%s\n", function->usage );
        }    
    }    
    else{
        fprintf( stdout, "commands are:\n" );
        for( int i = 0, size = sizeof(functions)/sizeof(xidxFunc); i < size; i++ ){
            fprintf( stdout, "    " );
            for( int k = 0; functions[i].name[k] && functions[i].name[k]!=':'; k++)
                fputc( functions[i].name[k], stdout );
        }                 
        fprintf( stdout, "\nfor command usage type help <command>\n" );
    }
    
    return 0;
}
int xidxShell::scale( int argc, char** argv ){
    FILE* fp;
    int   fsize;
    char* buffer;
    int   result;

    if( argc != 1 && argc != 2 ){
        fputs( "incorrect number of arguments. try `help scale`\n", stderr );
        return -1;
    }
    
    result = readfile( argv[0], "r+b", (void*&)buffer, fp, fsize );
    if( result ) return result;
    
    
    float scale = *(float*)(buffer);
    fprintf( stdout, "current scale is %4.2f\n", scale );
    
    if( argc == 2 ){
        float newscale = atof( argv[1] );
        int nbones = *(short*)(buffer+4);
        float* bnpos = (float*)(buffer+16);
        
        fprintf( stdout, "new scale is %4.2f\n", newscale );
        
        *(float*)(buffer) = newscale;
        scale = newscale / scale;
        
        for( int i = 0; i < nbones; i++ ){
            bnpos[0] *= scale;
            bnpos[1] *= scale;
            bnpos[2] *= scale;
            bnpos += 6;
        }
        fseek( fp, 0, SEEK_SET );
        fwrite( buffer, 1, fsize, fp );
    }
    
    free( buffer );
    fclose( fp );
    return 0;            
}
    
int xidxShell::fork( int argc, char** argv ){
    char tmpstr[256];
    str final="";
    
    for( int i = 0; i < argc; i++ ){
        if( strchr( argv[i], ' ' ) ){
            snprintf( tmpstr, 255, "\"%s\"", argv[i] );            
        }
        else strncpy( tmpstr, argv[i], sizeof(tmpstr) );
        final += str(tmpstr) + ' ';
    }   
    //puts( final.data );
    return system( final.data );
}    
    
int xidxShell::loadskel( int argc, char** argv ){
    //todo
    return 0;
}
        
int xidxShell::chpath( int argc, char** argv ){
    const char* skeleton = NULL;
    const char* oldfn = NULL;
    const char* newfn = NULL;
    bool  wildcard = false;
    bool  list = false;
    bool  copy = false;
    FILE* fp = NULL;
    char* buffer;
    int   count = 0, fsize = 0;
    
    for( int i = 0; i < argc; i++ ){
        strrep( argv[i], '\\', '/' );
        if( !stricmp( argv[i], "all" ) ) wildcard = true;
        else if( !stricmp( argv[i], "list" ) ) list = true;
        else if( !stricmp( argv[i], "copy" ) ) copy = true;
        else if( !skeleton ) skeleton = argv[i];
        else if( !oldfn ) oldfn = argv[i];
        else if( !newfn ) newfn = argv[i];
    }
    if( (list && newfn) || (!list && !newfn) || (copy && !newfn) || !oldfn || !skeleton ){
        fprintf( stderr, "error: incorrect number of arguments. try `help chpath`\n");
        return -1;
    }
    //read in file
    int result = readfile( skeleton, "rb", (void*&)buffer, fp, fsize );
    if( result ) return result; //error occured
    fclose( fp );
       
    if( !newfn && list ) newfn = "";
    //search and replace
    for( int i = 0, len = strlen(oldfn), len2 = strlen(newfn); i < fsize; i++ ){
        if( !strnicmp( &buffer[i], oldfn, len ) ){
            int diff = len - len2;
            
            if( list ){
                fprintf( stdout, "%s\n", &buffer[i] );
            }
            if( copy ){                
                char* old = strdup( &buffer[i] );
                char* tmp = (char*)malloc( strlen( old ) + 1 + len2 );
                strcpy( tmp, newfn );
                strcat( tmp, &old[len] );             
                strrep( old, '/', '\\' );
                strrep( tmp, '/', '\\' );
                
                char* pch = strrchr( tmp, '\\' );
                if( pch ){
                    *pch = '\0';
                    mkrdir( tmp );
                    *pch = '\\';
                }
                    
                stack<char*> args;
                args.push( "copy" );
                args.push( "/b" );
                args.push( old );
                args.push( tmp );
                fork( args.size(), args.data() );
                
                free( tmp );
                free( old );
            }
            if( !list && !copy ){
                if( diff < 0 ){
                    fsize += -diff;
                    buffer = (char*)realloc( buffer, fsize ); 
                }
                else{
                    fsize -= diff;
                }
                memmove( &buffer[i+len2], &buffer[i+len], fsize - (len2+i) );
                memcpy( &buffer[i], newfn, len2 );
                count++;
            }    
            if( !wildcard ) break;
        }    
    }
    //write out file
    if( !list && !copy ){        
        fp = fopen( skeleton, "wb" );
        fwrite( buffer, 1, fsize, fp );        
        fclose( fp );
        fprintf( stdout, "replaced %d %s\n", count, count==1 ? "string" : "strings");
    }
    free( buffer );    

    return 0;
} 

int xidxShell::exit( int argc, char** argv ){
    ::exit(0);
    return 0;
}    

int xidxShell::clear( int argc, char** argv ){
    return system( "cls" );
} 

int xidxShell::Parse( char* input2 ){
    char command[sizeof(input)] = {0};
    char args[sizeof(input)] = {0};
    stack< char* > tokens;
    xidxFunc* function = NULL;
    
    sscanf( input2, "%s %[^\n]\n", command, args );
    if( command[0] == '\0' ) return 0;
    
    function = getfn( command );     
    if( !function ) return -1; 
    
    tokens = gettokens( args, " " );
    tokens.push( NULL );
    return function->execute( tokens.size() - 1, tokens.data() );   
}   
 
int xidxShell::Run(){
    fprintf( stderr, "(xidx) " );
    while( fgets( input, sizeof(input), stdin ) ){
        for( int i = 0, loop = 0, front = 0; input[i]; i++ ){
            if( loop != 0 ){
                if( input[i] == '\"' ){
                    loop = 0;
                    continue;
                }
            }        
            else if( input[i] == '\"' ){
                loop = 1;
                continue;
            }
            else if( input[i] == ';' || input[i] == '\n' ){
                input[i] = '\0';                
                Parse( &input[front] );
                front = ++i;
            }    
            
        }  
        fprintf( stderr, "(xidx) " );       
    }
 
    return 0;
}    




    
