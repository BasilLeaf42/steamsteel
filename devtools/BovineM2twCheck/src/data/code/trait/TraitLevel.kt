package data.code.trait

import data.common.SimpleReferenceRecord
import java.util.ArrayList

class TraitLevel(val levelName :String)
{
	//levelName checked for description existence

	//Checked for description existence
	var description :String? = null

	//Checked for description existence
	var effectsDescription :String? = null

	//Checked for description existence
	var epithetDescription :String? = null

	//Checked for duplicate threshold value
	var threshold = 0

	//Checked for description existence
	var gainMessage :String? = null

	//Checked for description existence
	var loseMessage :String? = null

	//Checked for valid effect names in TraitsAncillariesScript.traitChecks
	var effects = ArrayList<SimpleReferenceRecord>()
}
