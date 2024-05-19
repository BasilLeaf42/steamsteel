package data.unit

import java.util.*

class EngineModelGroup
{
	//Checked for recognized model group name
	var names = ArrayList<String>()

	//Checked at Unit.engineUnitChecks
	var skeleton :String? = null

	//Checked file reference
	var boneMap :String? = null

	//Checked file reference
	var collision :String? = null
	var meshes = ArrayList<EngineMesh>()

	fun name() :String
	{
		var retur = names[0]
		for(i in 1 until names.size) retur += ", " + names[i]
		return retur
	}
}