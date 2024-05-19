package data.strat.mission

import data.common.SimpleReferenceRecord
import data.common.UsageTrackedName

class MissionEntry
	(name :String, occurringInFile :String, lineNumber :Int, var variant :String)
	: UsageTrackedName(name, occurringInFile, lineNumber)
{
	var parsedLines :Int = 0

	//Checked references at Stratmap.missions
	val eligibleReligions = ArrayList<SimpleReferenceRecord>()
	val religionModifiers = ArrayList<SimpleReferenceRecord>()

	//Checked paybacks at Stratmap.missions
	val paybacks = ArrayList<MissionPayback>()
	var client :String = ""

	//TODO Check settlement reference
	var settlementOwnedCondition :String? = null
	//Checked building level exists at Stratmap.missions
	val buildingTargets = ArrayList<String>()
	//TODO Check ancillary reference
	var ancillaryTarget :String? = null
	//TODO Check agent reference
	var agentTarget :String? = null
	//TODO Check guild references
	val guildHandles = ArrayList<String>()
	//Checked resource exists at Stratmap.missions
	var resourceTarget :String? = null
	//Checked factions exist at Stratmap.missions
	val factions = ArrayList<String>()

	//Checked image references at Stratmap.missions
	var issuedImage :String = ""
	var expiredImage :String = ""
	var successImage :String = ""
	var failedImage :String = ""
}
