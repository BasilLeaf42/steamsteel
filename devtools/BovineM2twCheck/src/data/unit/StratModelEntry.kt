package data.unit

import data.common.UsageTrackedName
import java.util.*

class StratModelEntry(name :String?, occurringInFile :String?, lineNumber :Int) :UsageTrackedName(name!!, occurringInFile, lineNumber)
{
	//Checked in StratMap.stratmapModels
	var skeleton :String? = null

	//Not used
	var scale = 0.0

	//Not used
	var indivRange = 0
	var textureAssignments = ArrayList<TextureAssignment>()
	var modelAssignment = ModelAssignment()

	class TextureAssignment
	{
		var lineNumber :Int? = null

		//Checked in StratMap.stratmapModels
		var faction :String? = null

		//Checked through general file references
		var texture :String? = null
	}

	class ModelAssignment
	{
		var lineNumber :Int? = null

		//Checked through general file references
		var modelFile :String? = null

		//Checked through general file references
		var shadowModelFile :String? = null
	}

	override fun toString() :String
	{
		return name
	}
}