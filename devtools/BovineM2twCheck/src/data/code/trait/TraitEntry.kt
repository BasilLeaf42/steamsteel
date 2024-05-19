package data.code.trait

import data.common.SimpleReferenceRecord
import data.common.UsageTrackedName
import java.util.*

class TraitEntry(name :String?, lineNumber :Int) :UsageTrackedName(name!!, "export_descr_character_traits", lineNumber)
{
	//Enumeration check at TraitsAncillariesScript.traitChecks
	var targetCharacterTypes = ArrayList<String>()

	//Checked against which description is used, unless flagged not to in run configuration.
	var isHidden = false

	//Not used
	var noGoingBackLevel :Int? = null

	//Checked existence at TraitsAncillariesScript.traitChecks
	//Checked against the trait levels to report if any of them have effects, causing the antitrait lingering effects bug.
	val antiTraits = ArrayList<String>()

	//Checked existence at TraitsAncillariesScript.traitChecks
	val excludedCultures = ArrayList<SimpleReferenceRecord>()

	//Checked existence at TraitsAncillariesScript.traitChecks
	val factionReferences = ArrayList<SimpleReferenceRecord>()

	//Checked existence at TraitsAncillariesScript.traitChecks
	val religionReferences = ArrayList<SimpleReferenceRecord>()

	val traitLevels = ArrayList<TraitLevel>()

	//Flags used for reporting unused traits
	var isAwarded = false
	var isTested = false
}