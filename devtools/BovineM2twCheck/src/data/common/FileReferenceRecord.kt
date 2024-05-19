package data.common

open class FileReferenceRecord
@JvmOverloads
constructor
(  val file :String?
   ,val lineNumber :Int?
   ,val referringEntryName :String?
   ,var referencedFile :String
   ,var referencedFolder :String? = null
   ,var additionalPossibleExtensions :Array<String>? = null
   ,var alternativeExtension :String? = null
   ,var vanillaFilesAreAvailable :Boolean = true
)
{
	private fun splitFolderAndFile()
	{
		val lastFolderSeparatorIndex = referencedFile.lastIndexOf("/")
		referencedFolder = referencedFile.substring(0, lastFolderSeparatorIndex + 1)
		referencedFile = referencedFile.substring(lastFolderSeparatorIndex + 1)
	}

	private fun adjustFolder()
	{
		if(referencedFolder != null)
		{
			if(referencedFolder!!.startsWith("data/"))
				referencedFolder = referencedFolder!!.substring(5)
			if(!referencedFolder!!.endsWith("/"))
				referencedFolder += "/"
		}
	}

	override fun toString() :String
	{
		return referencedFile
	}

	init
	{
		if(referencedFolder == null)
			splitFolderAndFile()
		adjustFolder()
	}
}