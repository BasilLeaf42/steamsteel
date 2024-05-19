package sources.stratmap.building

import data.common.SimpleReferenceRecord
import data.code.ResourceReferenceRecord
import data.common.UsageTrackedName
import java.util.*

//Used by building level, level upgrade and capabilities.
open class BuildingRequirementsHolder
	(name :String, occurringInFile :String?, lineNumber :Int)
	:UsageTrackedName(name, occurringInFile, lineNumber)
{
	//Each BuildingRequirementsHolder data structure point must be checked, handled by Stratmap.checkRequirements => checkBuildingRequirementsHolder
	var factionRequirements = ArrayList<SimpleReferenceRecord>()
	var resourceRequirements = ArrayList<ResourceReferenceRecord>()
	var buildingReferences = ArrayList<SimpleReferenceRecord>()
	var buildingLevelReferences = ArrayList<SimpleReferenceRecord>()
	var religionReferences = ArrayList<SimpleReferenceRecord>()

	var cityCastleRequirement = ""

	//This is not stored on this object. Instead, the references are recorded in main.data.code.eventCounters.
	//var eventReferences = ArrayList<SimpleReferenceRecord>()
}