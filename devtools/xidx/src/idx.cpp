/*
  Name: idx.cpp 
  Copyright: Vercingetorix (vercingetorix11@gmail.com)
  Author: Vercingetorix (vercingetorix11@gmail.com)
  Date: 06/01/05
  Status: WIP
  License: This file is considered part of the program 'xidx'
*/

#include "idx.h" 
stack<str> idxSubFile::dirs;

         
/*class defs*/
idxSubFile::idxSubFile(){
    beginFileOffset = fileSize = 0;
    filename[0] = '\0';
    buffer = NULL;
}

idxSubFile::~idxSubFile(){
    Clean();
}
void idxSubFile::SetFilename( const char* str ){
    strncpy( filename, str, 255 );
}    
void idxSubFile::Clean(){
    if( buffer ) free(buffer);
    buffer = NULL;
    //filename[0] = '\0';
    
}    
void idxSubFile::ParseFilename( const char* fname ){
    /*make the path relitive to data\*/
    char* tstr = strdup( fname ); 
    const char* formated = getdpath( tstr );   
    if( !formated ){
        if( strchr( tstr, '/' ) )
            fprintf(stderr,"warning: file %s does not have \"data\" in path\n", tstr);
        strncpy( filename, tstr, 255 );
    } 
    else{
        if( (formated - tstr) >= 3 ){
            if( !strnicmp( &formated[-3], "bi/", 3 ) ){
                formated -= 3;                
            }    
        }    
        strncpy( filename, formated, 255 );
    }    
    free( tstr );
}
void idxSubFile::PrintFilename(){
    puts( filename );    
}    
bool idxSubFile::PrepareDataOut(){
    return true;
}
    
bool idxSubFile::Extract(FILE* fp2){
    if( buffer ) free(buffer);           
    if( !(buffer = (char*)malloc(fileSize)) ) return false;
       
    fseek(fp2, beginFileOffset, SEEK_SET);
    
    if( fread(buffer, sizeof(char), fileSize, fp2) != fileSize )
        return false;
    
    char* pstr = strrchr( filename,'/' );
    
    if( pstr ) {
        *pstr = '\0';
        if( !idxSubFile::dirs.search( str(filename) ) ){
            if( !mkrdir( filename ) ) return false;
            else idxSubFile::dirs.push( filename );
        }
        *pstr = '/';
    }
        
    FILE* fpout = fopen( filename, "wb" );
    if( !fpout ) return false;  

    PrepareDataOut();
     
    fwrite(buffer, sizeof(char), fileSize, fpout);
    free(buffer);
    buffer = NULL;
    fclose( fpout );
    return true;
}  
      
bool idxSubFile::ExtractFile( FILE* fp, FILE* fp2 ){
    
    Clean();
    
    if( fp ) Read(fp);
    if( fp2 ) return Extract(fp2);
         
    return true;
}


bool idxSubFile::WriteFile( FILE* fp, FILE* fp2, const char* fname ){
    FILE* fpin = fopen( fname, "rb" );
    if( !fpin ) return false;
    Clean();
    fileSize = getfilesize( fpin );
    if( !(buffer = (char*)malloc(fileSize)) ) return false;
    fread( buffer, 1, fileSize, fpin );
    fclose( fpin );   
    
    beginFileOffset =  ftell( fp2 );
    
    GatherInfo();       
    Write( fp );  
      
    fwrite( buffer, sizeof(char), fileSize, fp2 );
    
    fflush( fp );
    fflush( fp2 );
    free( buffer );
    buffer = NULL;
    return true;
} 
     
idxFile::idxFile(){
    fileVersion = numFiles = 0;
    subFiles = NULL;
    filetype = NULL;
    fp = fp2 = NULL;
}    

idxFile::~idxFile(){
    if( subFiles ) delete [] subFiles;
}    

bool idxFile::OpenFiles( const char* filename, const char* mode ){
    char  datfn[ 256 ];
    char  idxfn[ 256 ];
    char* ext; 
    strncpy( datfn, filename, 250 );
    ext = strrchr ( datfn, '.' );
    if( ext ) *ext = '\0';
    strncpy(idxfn, datfn, 250);
    strcat( datfn, ".dat" );
    strcat( idxfn, ".idx" );
    
    fp = fopen( idxfn, mode );
    if( !fp ) {
        fprintf( stderr, "failed to open %s\n", idxfn );
        return false;
    }    
    fp2 = fopen( datfn, mode );
    if( !fp2 ){
        fprintf( stderr, "failed to open %s\n", datfn );
        fclose( fp );
        return false;
    } 
    return true;
}
void idxFile::CloseFiles(){
    if( fp ) fclose(fp);
    if( fp2) fclose(fp2);
    fp = fp2 = NULL;
}

      
bool idxFile::Write( const char* filename, const char** files, int count ){
    Init();
    if( !OpenFiles( filename, "wb" ) ) return false;
    
    WriteHeader(); 
    Allocate( count );
    
    for( int i = 0; i<count; i++ ){
        //parse
        subFiles->ParseFilename( files[i] );
        int result = subFiles->WriteFile( fp, fp2, subFiles->filename );
        if( !result ) fprintf( stderr, "failed to open file %s\n", subFiles->filename);
        else if( verbose ) puts( subFiles->filename );
        else fprintf(stderr,"Packing file %d/%d\r",i,count); 
        numFiles += result;
    } 
    WriteHeader();   
    CloseFiles();  
    return numFiles;
}  
bool idxFile::Extract(const char* filename, bool list){
    if( !OpenFiles( filename, "rb" ) ) return false;
    
    if( !ReadHeader() ) return false;
    Allocate( numFiles );
    for( int i = 0; i<numFiles; i++ ){
        int result = subFiles->ExtractFile( fp, list ? NULL : fp2 );
        if( !result ) fprintf( stderr, 
               "error reading archived file in \"%s\"\n", filename);
        else if( verbose||list ) subFiles->PrintFilename();
        else fprintf(stderr,"Extracting file %d/%d\r",i,numFiles); 
    }
    
    CloseFiles();
    return true;
}

/*Sound sub idx file*/
sidxSubFile::sidxSubFile(){
    control[0]  = control[1] = control[2] = control[3] = 0;
}

bool sidxSubFile::Read( FILE* fp ){
    if( !fp ) return false;
    fread(&beginFileOffset, sizeof(int), 1, fp);
    fread(&fileSize, sizeof(int), 1, fp);
    fread(control, sizeof(int), 4, fp);
        
    /*read filename*/
    for( int i=0; (filename[i?i-1:0]||!i)&&i<255; i++) filename[i] = fgetc(fp);
    fseek( fp, 3, SEEK_CUR);
    
    return true;
}  

bool sidxSubFile::Write( FILE* fp ){
    if( !fp ) return false;
    
    fwrite( &beginFileOffset, sizeof(int), 1, fp);
    fwrite( &fileSize, sizeof(int), 1, fp);
    fwrite( control, sizeof(int), 4, fp);
    fwrite( filename, sizeof(char), strlen( filename ), fp);
    fwrite( &STRDELIM, sizeof(int), 1, fp);
    
    return true;
}     

bool sidxSubFile::GatherInfo(){
    
    if( stristr(filename, ".mp3") ){
        control[0] = control[1] = control[2] = 0;
        control[3] = MP3TAG;
    }
    else{
        int* iptr = (int*) buffer;
        while( *iptr != 544501094/*fmt */&&iptr<(int*)(buffer+fileSize-16) ) iptr++;
        control[0] = *(iptr+3);
        control[1] = 16;
        control[2] = *(((short*)(iptr))+5);
        control[3] = *(((short*)(iptr))+4) == 1 ? 1 : 2; /*compression?*/     
    } 
    return true;
}    
  
  
/*Sound idx file*/
void sidxFile::Allocate( int s ){
    if( subFiles ) delete [] subFiles;
    subFiles = new sidxSubFile[ s ];
}  

void sidxFile::Init(){
    fileVersion = 4;
    filetype    = SSND;    
} 
   
bool sidxFile::ReadHeader(){
    char checktype[16] = {0};
    fread( checktype,1,8,fp);
    if( strcmp( checktype, SSND) ) {
        fprintf( stderr, "File is not a sound idx archive\n");
        return false;
    }    
    fseek( fp, 12,  SEEK_SET  ); 
    fread( &numFiles, sizeof(int), 1, fp);
    fseek( fp, 24,  SEEK_SET  );  
    return true;
} 

void sidxFile::WriteHeader(){
    fseek( fp, 0,  SEEK_SET  ); 
    fseek( fp2, 0, SEEK_SET  );
    int zero[2] ={0};
    
    fwrite( filetype, sizeof(char), strlen(filetype), fp);
    fwrite( &fileVersion, sizeof(int), 1, fp);
    fwrite( &numFiles, sizeof(int), 1, fp);
    fwrite( zero, sizeof(int), 2, fp);
    
    fwrite( filetype, sizeof(char), strlen(filetype), fp2);
    fwrite( &fileVersion, sizeof(int), 1, fp2);
    fwrite( &numFiles, sizeof(int), 1, fp2);
    fwrite( zero, sizeof(int), 2, fp2);
    
    fflush( fp );
    fflush( fp2 );
    
}   

/*Animation sub idx file*/
aidxSubFile::aidxSubFile(){
    entrySize = 0;
    scale = 1.0f;
    numFrames =  numBones = 0;
}
void aidxSubFile::PrintFilename(){
    if( verbose && scale != 1.0f ){
        fprintf( stdout, "%s;scale=%f\n", filename, scale );
    }
    else idxSubFile::PrintFilename();
}
void aidxSubFile::ParseFilename( const char* fname ){
    char* tstr = strdup( fname );
    char* pstr = stristr( tstr, ";scale=" );
    if( pstr ){
        sscanf( pstr, ";scale=%f", &scale );
        *pstr = '\0';         
    }
    else scale = 1.0f;
    idxSubFile::ParseFilename( tstr );
    //strcpy( filename, tstr);
    free( tstr );
}      
    
bool aidxSubFile::PrepareDataOut(){
    bool result;
    scale = 1.0f / scale;
    result = Scale();
    scale = 1.0f / scale;
    return result;
}    
     
bool aidxSubFile::Scale(){
    if( !buffer ) return false;        
    
    if( (scale != 1.0f) && (buffer[4] == 1) ){           
        //if( CheckProblemCas() ) return true; 
               
        //float* pelvis = (float*) &buffer[ (numFrames*numBones*16)+5 ];        
        //float* dist = (float*) &pelvis[ numFrames*3 ];
        //float* root = (float*) &dist[ 4*((numFrames-1) / 2) ];
        //float* end = &root[ numFrames*3 ];
        //for( int i = 0; i < 3*numFrames; i++ ){            
        //    pelvis[i] *= scale;
        //    root[i] *= scale;
        //}    
        //for( int i = 0; i < 4*((numFrames-1) / 2); i++ ){
        //    dist[ i ] *= scale;
        //}
        float* start = (float*) &buffer[ (numFrames*numBones*16)+5 ];
        int loop = numFrames*3*2 + (4*((numFrames-1) / 2)) + 8;
        
        for( int i = 0; i < loop; i++ ){
            start[i] *= scale;
        }    
    }    
    return true;
}
    
bool aidxSubFile::Read( FILE* fp ){
    if( !fp ) return false;
    
    fread(&entrySize, sizeof(int), 1, fp);   
    fread(&beginFileOffset, sizeof(int), 1, fp);
    fread(&fileSize, sizeof(int), 1, fp);
    fread(&scale, sizeof(float), 1, fp);
    fread(&numFrames, sizeof(short), 1, fp);
    fread(&numBones, sizeof(short), 1, fp);
    fread(&type, sizeof(char), 1, fp);        
    fread(filename,(entrySize>265) ? 255 : (entrySize-10+1),1,fp);
    
    return true;
}  

bool aidxSubFile::Write( FILE* fp ){
    if( !fp ) return false;
    fwrite(&entrySize, sizeof(int), 1, fp);   
    fwrite(&beginFileOffset, sizeof(int), 1, fp);
    fwrite(&fileSize, sizeof(int), 1, fp);
    fwrite(&scale, sizeof(float), 1, fp);
    fwrite(&numFrames, sizeof(short), 1, fp);
    fwrite(&numBones, sizeof(short), 1, fp);
    fwrite(&type, sizeof(char), 1, fp);
    fwrite(filename,strlen(filename)+1,1,fp);
    
    return true;
}     

bool aidxSubFile::GatherInfo(){
    if( !buffer ) return false;
    
    entrySize = strlen(filename) + 10;
    //scale = 1.0f;
    numFrames = ((short*)buffer)[0];
    numBones = ((short*)buffer)[1]; 
    type = ((char*)buffer)[4];   
    Scale();
    //CheckProblemCas();
    
    return true;
}    
  
  
/*Animation idx file*/
void aidxFile::Allocate( int s ){
    if( subFiles ) delete [] subFiles;
    subFiles = new aidxSubFile[ s ];
}  

void aidxFile::Init(){
    fileVersion = 4;
    filetype    = SANM;    
} 
   
bool aidxFile::ReadHeader(){
    char checktype[16] = {0};
    fread( checktype,1,10,fp);
    if( strcmp( checktype, SANM) ) {
        fprintf( stderr, "File is not a animation idx archive\n");
        return false;
    }    
    fseek( fp, 16,  SEEK_SET  ); 
    fread( &numFiles, sizeof(int), 1, fp);
    return true;
} 

void aidxFile::WriteHeader(){
    fseek( fp, 0,  SEEK_SET  ); 
    fseek( fp2, 0, SEEK_SET  );
    short zero=0;
    
    fwrite( filetype, sizeof(char), strlen(filetype)+1, fp);
    fwrite( &zero, sizeof(short), 1, fp);
    fwrite( &fileVersion, sizeof(int), 1, fp);
    fwrite( &numFiles, sizeof(int), 1, fp);
   
    fwrite( filetype, sizeof(char), strlen(filetype)+1, fp2);
    fwrite( &zero, sizeof(short), 1, fp2);
    fwrite( &fileVersion, sizeof(int), 1, fp2);
    fwrite( &numFiles, sizeof(int), 1, fp2);
    
    fflush( fp );
    fflush( fp2 );
    
}   

/*Skeleton sub idx file*/
kidxSubFile::kidxSubFile(){
    len = 0;
}
    
bool kidxSubFile::Read( FILE* fp ){
    if( !fp ) return false;
    
    fread( &len, sizeof(int), 1, fp );   
    fread( &beginFileOffset, sizeof(int), 1, fp);
    fread( &fileSize, sizeof(int), 1, fp );        
    fread( filename, len ,1,fp);
    
    return true;
}  

bool kidxSubFile::Write( FILE* fp ){
    if( !fp ) return false;
    
    fwrite( &len, sizeof(int), 1, fp );   
    fwrite( &beginFileOffset, sizeof(int), 1, fp);
    fwrite( &fileSize, sizeof(int), 1, fp );        
    fwrite( filename, len, sizeof(char), fp );
    
    return true;
}     

bool kidxSubFile::GatherInfo(){
    if( !buffer ) return false;
    
    len = strlen(filename) + 1;
    
    return true;
}    
  
  
/*Skeleton idx file*/
void kidxFile::Allocate( int s ){
    if( subFiles ) delete [] subFiles;
    subFiles = new kidxSubFile[ s ];
}  

void kidxFile::Init(){
    fileVersion = 3;
    filetype    = SSKL;    
} 
   
bool kidxFile::ReadHeader(){
    char checktype[16] = {0};
    fread( checktype,1,10,fp);
    if( strncmp( checktype, SSKL, strlen(SSKL) ) ) {
        fprintf( stderr, "File is not a skeleton idx archive\n" );
        return false;
    }    
    fseek( fp, 16,  SEEK_SET  ); 
    fread( &numFiles, sizeof(int), 1, fp );
    return true;
} 

void kidxFile::WriteHeader(){
    fseek( fp, 0,  SEEK_SET  ); 
    fseek( fp2, 0, SEEK_SET  );
    short zero=0;
    
    fwrite( filetype, sizeof(char), strlen(filetype)+1, fp);
    fwrite( &zero, sizeof(short), 1, fp);
    fwrite( &fileVersion, sizeof(int), 1, fp);
    fwrite( &numFiles, sizeof(int), 1, fp);
   
    fwrite( filetype, sizeof(char), strlen(filetype)+1, fp2);
    fwrite( &zero, sizeof(short), 1, fp2);
    fwrite( &fileVersion, sizeof(int), 1, fp2);
    fwrite( &numFiles, sizeof(int), 1, fp2);
    
    fflush( fp );
    fflush( fp2 );
    
}   
