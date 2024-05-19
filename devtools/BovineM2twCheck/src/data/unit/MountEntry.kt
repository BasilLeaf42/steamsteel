package data.unit

import data.common.UsageTrackedName

class MountEntry
	(name :String, lineNumber :Int)
	:UsageTrackedName(name, "descr_mount.txt", lineNumber)
{
	val riderOffsets = ArrayList<String>()
	var riderCount :Int = 1
	var waterTrailEffect :String = ""
	var model :String? = null
	var mountClass :String? = null
	var isVanillaRepresentation :Boolean = false
		private set

	fun createVanillaMountRepresentation(name :String) :MountEntry
	{
		var retur = MountEntry(name, -1)
		retur.isVanillaRepresentation = true
		return retur
	}
}