package data.code.trait

import data.common.SimpleReferenceRecord
import data.common.UsageTrackedName
import java.util.*

class TraitTriggerEntry(name :String, occurringInFile :String, lineNumber :Int)
	:UsageTrackedName(name, occurringInFile, lineNumber)
{
	//Reported when equals "BecomesFactionLeader" due to the related crashing bug
	//Otherwise, checked for valid event names
	var triggeringEvent :String? = null

	//TODO Check for valid settlements
	var referredSettlements = ArrayList<SimpleReferenceRecord>()

	//Checked for existing buildings or building levels at TraitsAncillariesScript.checkTraitBuildingReferences
	var referredBuildings = ArrayList<SimpleReferenceRecord>()

	//Checked for valid attributes in TraitsAncillariesScript.traitTriggerChecks
	var referredAttributes = ArrayList<SimpleReferenceRecord>()

	//TODO Check for valid attributes
	var referredUnitAttributes = ArrayList<SimpleReferenceRecord>()

	//Checked for existing traits at TraitsAncillariesScript.traitTriggerChecks
	var referredTraits = ArrayList<TraitReferenceRecord>()

	//Checked for valid faction at TraitsAncillariesScript.traitTriggerChecks
	var referredFactions = ArrayList<SimpleReferenceRecord>()

	//Check for valid culture at TraitsAncillariesScript.traitTriggerChecks
	var referredCultures = ArrayList<SimpleReferenceRecord>()

	//Checked for valid religion at TraitsAncillariesScript.traitTriggerChecks
	var referredReligions = ArrayList<SimpleReferenceRecord>()

	//TODO check for valid ancillary
	var referredAncillaries = ArrayList<SimpleReferenceRecord>()

	//TODO check for valid mission
	var referredMissions = ArrayList<SimpleReferenceRecord>()

	//TODO check for valid mission penalty/reward setting
	var referredMissionPaybacks = ArrayList<SimpleReferenceRecord>()

	//TODO check for valid loyalty level
	var referredSettlementLoyaltyLevels = ArrayList<SimpleReferenceRecord>()

	//TODO check for valid diplomatic stance
	var referredDiplomaticStances = ArrayList<SimpleReferenceRecord>()

	var affects = ArrayList<AffectClause>()

	var isGeneralInvoked :Boolean = false

	//Event counter references are not stored here, but rather on main.data.code.eventCounters instead, for common process with other such references
}