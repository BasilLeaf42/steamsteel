package data.common

import java.util.*

class FileReferenceCollection<Gen :FileReferenceRecord>
{
	var contents = ArrayList<Gen>()
	fun add(reference :Gen)
	{
		contents.add(reference)
	}

	fun containsReferenceTo(folder :String, filename :String) :Boolean
	{
		for(record in contents)
		{
			if(folder == record.referencedFolder && filename == record.referencedFile)
				return true
		}
		return false
	}
}