package data.code.script

import data.common.IntegerValuedReferenceRecord
import data.common.SimpleReferenceRecord
import data.common.UsageTrackedName
import java.util.*

class DeclaredCounterEntry
	constructor(name :String, filename :String? = null, lineNumber :Int? = -1)
	:UsageTrackedName(name, filename, lineNumber)
{
	val declaredLocations = ArrayList<SimpleReferenceRecord>()
	val setLocations = ArrayList<IntegerValuedReferenceRecord>()
	val checkedLocations = ArrayList<SimpleReferenceRecord>()
}