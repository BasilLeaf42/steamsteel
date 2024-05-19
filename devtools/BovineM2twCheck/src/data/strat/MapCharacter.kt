package data.strat

import data.common.TrackedName
import util.StringUtil
import util.Util
import java.util.ArrayList

class MapCharacter(var ownerFaction :String, filename :String?, lineNumber :Int, name :String)
	:TrackedName(name, filename, lineNumber)
{
	//Name is used to check for name definitions' existence with ownerFaction/subFaction at Script.namesAndLabels

	//Checked reference at Stratmap.characters and Script.otherScriptChecks
	var subFaction :String? = null

	//Checked reference at Stratmap.characters
	var type :String = ""

	//Checked against character type at Stratmap.checkGender - but only for characters on the map, not for character records
	var isFemale = false

	//Checked against duplicate leader at Stratmap.characters
	var isLeader = false
	var isHeir = false

	var isFamilyMember :Boolean = false
	var age = 0

	//TODO check for collisions
	var x = 0
	var y = 0
	var direction :String = ""

	//TODO check valid value
	var portrait :String = ""

	//TODO check valid value
	var label :String = ""

	//Checked reference at Stratmap.characters
	var battleModel :String = ""

	//Checked reference at Stratmap.characters
	var stratModel :String? = null

	//TODO check valid value
	var ability :String? = null

	//TODO check references
	var ancillaries = ArrayList<String>()

	fun hasMatchingGender() :Boolean
	{
		return (Util.equalsAny(type,  "princess", "witch") && isFemale)
			|| (!Util.equalsAny(type,  "princess", "witch") && !isFemale)
	}
}