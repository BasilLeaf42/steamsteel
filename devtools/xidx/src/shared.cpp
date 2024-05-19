/*
  Program Name: xidx
  Copyright: Vercingetorix (vercingetorix11@gmail.com)
  Author: Vercingetorix (vercingetorix11@gmail.com)
  Date: 6/5/05
  License: This file is considered part of the program 'xidx'
*/


#include "shared.h"

/*general functions*/
int getfilesize(FILE *fp){
    int curpos = ftell(fp);
    fseek(fp,0,SEEK_END); 
    int fsize=ftell(fp); 
    fseek(fp,curpos,SEEK_SET); 
    return fsize;
} 
/*recursive mkdir*/
bool mkrdir( const char* dir){
    int result;
    //puts(dir);
    result = _mkdir( dir );
    if( !result || result == 17 ){
        return true;
    }
    else{
        char* level = strdup( dir ), *pch;
        strrep( level, '/', '\\' );
    
        if( (pch = strrchr(level,'\\')) ) *pch = '\0';
        else{
            free( level );
            return false;
        }    
        mkrdir( level );
        _mkdir( dir );
        free( level );
        return true;
    }        
}     
/*extracts the data path from a filename*/
char* getdpath( char* str){
    strrep( str, '\\', '/' ); 
        
    for( int i=strlen(str); i>=0; i-- ) 
        if( !strnicmp(&str[i], "data/", 5 ) ) {
            return &str[i];
        } 
    return NULL;
}
/*case insensitive strstr*/
char* stristr( const char* str, const char* sstr){
    int len = strlen(sstr);
    while(*str){
        if( !strnicmp(str,sstr, len) ) return (char*)str;
        else str++;
    }
    return NULL;               
}
//strtok replacement
char* strsep( char** strp, const char* delim ){
    if( !(*strp) ) return NULL;
    char* str = *strp;
    char* tmp = str;
        
    while( *str ){        
        if( strchr( delim, *str ) ){
            *str = '\0';
            *strp = str + 1;
            return tmp; 
        } 
        str++;              
    }
    *strp = NULL;
    return tmp;
}
//same as strsep() but anything within "" is exempted from the delimators
char* qstrsep( char** strp, const char* delim ){
    if( !(*strp) ) return NULL;
    char* str = *strp;
    char* start = str;
    char* buffer = strdup( str );
    char* pbuff = buffer;
    char* tmp;
    bool  inquotes = false;
    int   len = strlen( buffer );
    memset( buffer, 0, len );
    
    while( *str ){
        if( inquotes ){
            if( *str == '\"' ){
                str++;
                inquotes = false;
                if( *str == '\0' ){
                    strcpy( start, buffer );
                }    
                continue;
            }
        }        
        else if( *str == '\"' ){
            str++;
            inquotes = true;
            continue;
        }    
        else if( strchr( delim, *str ) ){
            strcpy( start, buffer );
            free( buffer );
            *str = '\0';
            *strp = str + 1;            
            return start; 
        }
        *pbuff++ = *str++;
    }
    
    free( buffer );
    *strp = NULL;
    return start;
}    

//replaces one char with another in a string, returns the number replaced. 
int strrep( char* str, int c, int r ){
    int count = 0;
    while( *str ){
        if( *str == c ) {
            *str = (char) r;
            count++;
        }    
        str++;
    }    
    return count;
}    



