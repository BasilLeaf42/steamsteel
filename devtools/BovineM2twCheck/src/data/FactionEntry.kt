package data

import data.common.TrackedName
import java.util.ArrayList

class FactionEntry(name :String, filename :String, lineNumber :Int) :TrackedName(name, filename, lineNumber)
{
	var symbolFile :String = ""
	var rebelSymbolFile :String = ""
	var loadingLogoFile :String = ""

	var disbandingToPools = true

	//Checked for valid culture at Stratmap.factionsAndCultures
	var culture :String = ""

	//Not used beyond checking that only one such exists
	var isSlave = false

	//Jointly used for checking missions
	var isPapacy = false
	var isEligibleForPopeMissions = false
	var religion :String = ""

	var standardIndex :String? = null
	var logoIndex :String? = null
	var smallLogoIndex :String? = null

	var hordeMinimumUnits = 0
	var hordeMaximumUnits = 0
	var hordeMaximumUnitsReductionEveryHorde = 0
	var hordeUnitPerSettlementPopulation = 0
	var hordeMinNamedCharacters = 0
	var hordeMaxPercentArmyStack = 0
	var hordeDisbandPercentOnSettlementCapture = 0
	var hordeUnits = ArrayList<String>()

	fun isHorde() :Boolean
	{
		return hordeMinimumUnits > 0
				|| hordeMaximumUnits > 0
				|| hordeMaximumUnitsReductionEveryHorde > 0
				|| hordeUnitPerSettlementPopulation > 0
				|| hordeMinNamedCharacters > 0
				|| hordeMaxPercentArmyStack > 0
				|| hordeDisbandPercentOnSettlementCapture > 0
	}

	override fun toString() :String
	{
		return "$name ($culture)"
	}
}