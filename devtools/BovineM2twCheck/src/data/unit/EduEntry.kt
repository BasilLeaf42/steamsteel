package data.unit

import data.common.TrackedName

import java.util.ArrayList

class EduEntry(name :String, occurringInFile :String, lineNumber :Int) :TrackedName(name, occurringInFile, lineNumber)
{
	//Checked reference at Unit.unitChecks
	var dictionaryName :String = ""
	//TODO check valid value
	var category :String? = null
	//TODO check valid value
	var voice :String? = null
	//TODO check valid value
	var accent :String? = null
	//Checked reference at Unit.performChecks
	var soldier :String? = null
	//Checked reference at Unit.performChecks
	val officers = ArrayList<String>()
	//Checked reference at Unit.performChecks
	var engine :String? = null
	//Checked reference at Unit.performChecks
	var mountedEngine :String? = null
	//Checked reference at Unit.performChecks
	var mount :String? = null
	//Checked against number of armourModels at Unit.performChecks
	val armourLevels = ArrayList<Int>()
	//Checked reference at Unit.performChecks
	val armourModels = ArrayList<String>()
	//Checked sufficient texture assignments at Unit.performChecks
	val ownership = ArrayList<String>()
	//TODO Check valid attributes
	val attributes = ArrayList<String>()
	//TODO Check valid attributes
	val primaryWeaponAttributes = ArrayList<String>()
	//TODO Check valid attributes
	val secondaryWeaponAttributes = ArrayList<String>()
	//TODO Check valid attributes
	val tertiaryWeaponAttributes = ArrayList<String>()

	//TODO Check banner references
	var factionBanner :String = ""
	var crusadeBanner :String = ""
	var unitBanner :String = ""

	//TODO Check info picture and card picture exists
	var infoPictureDirectory :String = ""
	var cardPictureDirectory :String = ""

	fun isMercenary() :Boolean
	{
		return attributes.contains("mercenary_unit")
	}

	fun uniqueOwnerships() :ArrayList<String>
	{
		val retur = ArrayList<String>()
		for(owner :String in ownership)
		{
			if(!retur.contains(owner))
				retur.add(owner)
		}
		return retur
	}
}
