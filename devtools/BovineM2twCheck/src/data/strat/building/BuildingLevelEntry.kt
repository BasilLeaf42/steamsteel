package data.strat.building

import sources.stratmap.building.BuildingRequirementsHolder
import java.util.*

class BuildingLevelEntry(name :String?, occurringInFile :String?, lineNumber :Int)
	:BuildingRequirementsHolder(name!!, occurringInFile, lineNumber)
{
	var generalCapabilities = ArrayList<BuildingCapability>()
	var recruitmentCapabilities = ArrayList<RecruitmentCapability>()

	//Checking that the upgrade level exists in Stratmap.checkBuildingLevels
	//Checking requirements in Stratmap.checkRequirements
	var upgrades = ArrayList<BuildingLevelUpgrade>()

	//Checking that level exists in Stratmap.checkBuildingLevels
	var convertToLevel :Int? = null

	//Not used
	var material :String? = null

	//Not used
	var constructionTime = 0

	//Not used
	var cost = 0

	//Checking for valid values in Stratmap.checkBuildingLevels
	var settlementLevelRequirement :String? = null
}