package data.code.script

import data.common.SimpleReferenceRecord
import data.common.UsageTrackedName
import java.util.*

class EventCounterEntry
	constructor(name :String, occurringInFile :String? = null, lineNumber :Int? = -1)
	:UsageTrackedName(name, occurringInFile, lineNumber)
{
	val setLocations = ArrayList<SimpleReferenceRecord>()
	val checkedLocations = ArrayList<SimpleReferenceRecord>()
	var isHistoric = false
	var isDecision = false

	fun locationsEnumerated(): String
	{
		var locations = ""
		for(reference :SimpleReferenceRecord in setLocations)
			locations += "${reference.filename}:${reference.lineNumber} "
		for(reference :SimpleReferenceRecord in checkedLocations)
			locations += "${reference.filename}:${reference.lineNumber} "
		return locations
	}
}