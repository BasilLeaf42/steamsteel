package data.strat.building

import sources.stratmap.building.BuildingRequirementsHolder

class BuildingCapability(capabilityName :String?, occurringInFile :String?, lineNumber :Int)
	:BuildingRequirementsHolder(capabilityName!!, occurringInFile, lineNumber)
{
	//Checking for valid agent type in Stratmap.checkBuildingLevels
	var referredAgent :String? = null

	//Not used
	var magnitude = 0.0
}