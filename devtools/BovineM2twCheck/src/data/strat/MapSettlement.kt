package data.strat

class MapSettlement(var ownerFaction :String, val filename :String, val lineNumber :Int)
{
	//TODO check valid value
	var level :String? = null

	//TODO check valid value
	var region :String? = null

	//Not checked
	var yearFounded = 0

	//Not checked
	var population = 0

	//TODO what is this?
	var planSet :String? = null

	//Checked reference in Stratmap.settlements (also ownerFaction)
	var creatorFaction :String? = null

	var isCity = true

	val buildingsPresent = ArrayList<String>()
}