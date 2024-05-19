package data.sound

import data.common.FileReferenceRecord

class VoiceFileReference
(   file :String
	,lineNumber :Int
	,referringEntryName :String?
	,referencedFile :String
	,referencedFolder :String?
	,vanillaFilesAreAvailable :Boolean
)
:FileReferenceRecord
(   file
	,lineNumber
	,referringEntryName
	,referencedFile
	,referencedFolder
	,null
	,null
	,vanillaFilesAreAvailable
)
{
	var soundName :String? = null
	var accent :String? = null
	var vocal :String? = null
}