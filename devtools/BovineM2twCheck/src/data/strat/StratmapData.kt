package data.strat

import data.FactionEntry
import data.ResourceEntry
import data.common.SimpleReferenceRecord
import data.code.ResourceReferenceRecord
import data.code.trait.TraitReferenceRecord
import data.common.UsageTrackedCollection
import data.common.UsageTrackedName
import data.strat.building.BuildingEntry
import data.strat.building.BuildingPluginRecord
import data.strat.culture.CultureEntry
import data.strat.mission.MissionEntry
import data.strat.mission.MissionPayout
import data.unit.StratModelEntry
import main.BovineM2twCheck
import java.util.*
import kotlin.collections.ArrayList

class StratmapData(private val main :BovineM2twCheck)
{
	val stratModels = UsageTrackedCollection<StratModelEntry>()
	val factionEntries = HashMap<String, FactionEntry>()
	val cultureEntries = HashMap<String, CultureEntry>()

	val resources = UsageTrackedCollection<ResourceEntry>()
	val resourceReferences = ArrayList<ResourceReferenceRecord>()

	val buildings = UsageTrackedCollection<BuildingEntry>()
	val religions = UsageTrackedCollection<UsageTrackedName>()

	val buildingReferences = ArrayList<SimpleReferenceRecord>()
	val buildingLevelReferences = ArrayList<SimpleReferenceRecord>()
	val buildingPluginReferences = ArrayList<BuildingPluginRecord>()

	//TODO check references
	val characterTypeReferences = ArrayList<SimpleReferenceRecord>()

	//TODO check references
	val traitReferences = ArrayList<TraitReferenceRecord>()

	//TODO check references
	val referencedUnits = ArrayList<SimpleReferenceRecord>()

	//TODO check references
	val factionReferences = ArrayList<SimpleReferenceRecord>()

	//TODO check references and map collision
	val mapResources = ArrayList<MapResource>()

	//TODO check references and map collision
	val mapSettlements = ArrayList<MapSettlement>()

	//TODO check references and map collision
	val mapCharacters = ArrayList<MapCharacter>()

	//No checks made on these, but used to verify character relationships
	val characterRecords = ArrayList<MapCharacter>()

	//Checked existence of each character at Stratmap.checkRelationships
	val characterRelationships = ArrayList<CharacterRelationships>()

	//TODO check map collision
	val mapForts = ArrayList<MapFort>()
	val watchtowers = ArrayList<MapWatchtower>()

	//TODO check existence wherever else may be referenced
	val names = HashMap<String, FactionCharacterNames>()
	val nameText = HashMap<String, HashMap<String, String>>()

	//TODO check usage
	val missionPayouts = UsageTrackedCollection<MissionPayout>()
	val missions = ArrayList<MissionEntry>()
	fun getAllFactionNames(culture :String?) :ArrayList<String>
	{
		val retur = ArrayList<String>()
		for(entry in factionEntries.values)
		{
			if(culture == null || culture == entry.culture)
				retur.add(entry.name)
		}
		return retur
	}

	fun verifyBuildingReferenceExists(reference :SimpleReferenceRecord, errorTemplate :String)
	{
		val building = buildings[reference.reference, true]
		if(building == null)
		{
			var errorMessage = errorTemplate.replace("%FILE%", reference.filename)
			errorMessage = errorMessage.replace("%LINENUMBER%", "" + reference.lineNumber)
			errorMessage = errorMessage.replace("%REF%", "" + reference.reference)
			main.writeStratmapLog(errorMessage)
		}
	}

	fun verifyBuildingLevelOrBuildingExists(reference :SimpleReferenceRecord)
	{
		if(buildingLevelDoesNotExist(reference))
			verifyBuildingReferenceExists(reference, "%FILE% %LINENUMBER%: Neither building nor building level \"%REF%\" exists.")
	}

	private fun buildingLevelDoesNotExist(reference :SimpleReferenceRecord) :Boolean
	{
		for(building in main.data.strat.buildings.getAll())
		{
			val level = building.buildingLevels[reference.reference, true]
			if(level != null)
				return false
		}
		return true
	}

	fun findCharacterOrRecord(name :String, preferredFaction :String) :MapCharacter?
	{
		var retur :MapCharacter? = null
		for(character in main.data.strat.mapCharacters)
		{
			if(character.name == name)
			{
				retur = character
				if(character.ownerFaction == preferredFaction)
					return retur
			}
		}
		for(record in main.data.strat.characterRecords)
		{
			if(record.name == name)
			{
				retur = record
				if(record.ownerFaction == preferredFaction)
					return retur
			}
		}
		return retur
	}

}