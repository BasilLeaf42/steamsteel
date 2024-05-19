package data.strat

import java.util.*

class CharacterRelationships(var faction :String, var filename :String, var lineNumber :Int)
{
	//Checked existence at Stratmap.checkRelationships
	var characterName :String = ""

	//Checked existence at Stratmap.checkRelationships
	var relations = ArrayList<String>()
}