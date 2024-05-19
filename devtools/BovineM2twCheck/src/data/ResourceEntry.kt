package data

import data.common.UsageTrackedName
import java.util.*

class ResourceEntry(name :String, occurringInFile :String?, lineNumber :Int) :UsageTrackedName(name, occurringInFile, lineNumber)
{
	var tradeValue :Int? = null
	var modelFile :String? = null
	var textureFiles = ArrayList<String>()
	var iconFile :String? = null
	var hasMine = false
	var isHidden = false
}