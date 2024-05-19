package data.strat.building

import data.common.UsageTrackedCollection
import data.common.UsageTrackedName

class BuildingEntry(name :String?, occurringInFile :String?, lineNumber :Int)
	:UsageTrackedName(name!!, occurringInFile, lineNumber)
{
	val buildingLevels = UsageTrackedCollection<BuildingLevelEntry>()

	//Checking reference in Stratmap.checkBuildings
	var religion :String? = null

	//Checking reference in Stratmap.checkBuildings
	var convertTo :String? = null
}