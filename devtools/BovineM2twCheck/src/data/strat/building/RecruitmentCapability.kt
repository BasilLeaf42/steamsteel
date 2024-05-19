package data.strat.building

import sources.stratmap.building.BuildingRequirementsHolder

class RecruitmentCapability(name :String?, occurringInFile :String?, lineNumber :Int)
	:BuildingRequirementsHolder(name!!, occurringInFile, lineNumber)
{
	var initialPool = 0.0
	var replenishment = 0.0
	var max = 0.0
	var unitExperience = 0
}