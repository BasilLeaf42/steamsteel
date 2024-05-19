package data.sound

class MusicEventOrState(val name :String)
{
	var folder :String? = null
	var filename :String? = null

	override fun equals(other :Any?) :Boolean
	{
		if(other is MusicEventOrState)
			return name == other.name && folder == other.folder && filename == other.filename
		return false
	}

	override fun hashCode() :Int
	{
		var result = name.hashCode()
		result = 31 * result + (folder?.hashCode() ?: 0)
		result = 31 * result + (filename?.hashCode() ?: 0)
		return result
	}
}
