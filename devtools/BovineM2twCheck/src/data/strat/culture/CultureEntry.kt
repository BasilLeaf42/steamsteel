package data.strat.culture

import data.common.SimpleReferenceRecord
import java.util.*

class CultureEntry(var name :String)
{
	//TODO References are probably against descr_aerial_map_bases.txt. Find this in SS/SSHIP to implement.

	//TODO check mapping exists
	var portraitMapping :String? = null

	//TODO check index exists
	var rebelStandardIndex = 0

	//TODO check reference exists
	var fortReference :String? = null

	//Not checked
	var fortCost = 0

	//TODO check reference exists
	var fishingVillageReference :String? = null

	//TODO check references exists
	var portReferences = ArrayList<String>()

	//TODO check reference exists
	var watchtowerReference :String? = null

	//Not checked
	var watchtowerCost = 0

	//Checked file references at Stratmap.factionsAndCultures - except for agents marked as unused in config
	var agentFileReferences = ArrayList<SimpleReferenceRecord>()

	//Checked file references at Stratmap.factionsAndCultures - except for agents marked as unused in config
	var agentInfoCards = ArrayList<SimpleReferenceRecord>()

	//TODO find out where the level reference goes
	var settlementLevels = ArrayList<CultureSettlementLevel>()

}