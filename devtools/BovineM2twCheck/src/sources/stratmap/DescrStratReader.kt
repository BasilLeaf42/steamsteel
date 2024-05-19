package sources.stratmap

import data.common.SimpleReferenceRecord
import data.code.trait.TraitReferenceRecord
import data.common.FileReferenceRecord
import data.strat.*
import data.strat.building.BuildingPluginRecord
import main.BovineM2twCheck
import sources.shared.MapCharacterParsing
import util.StringUtil
import util.Util
import java.io.BufferedReader
import java.io.FileNotFoundException
import java.io.FileReader
import java.util.*

class DescrStratReader(val main :BovineM2twCheck)
{
	private var campaignGeneralSetupComplete = false
	private var playabilityActive = false
	private var activeFaction :String = ""
	private var activeCharacter :MapCharacter? = null
	private var activeSettlement :MapSettlement? = null
	private var armyActive = false
	private var settlementBuildingActive = false
	private var activeSettlementBuildingType :String? = null
	private var activeRegion :String? = null
	private var scriptSectionActive = false
	private val recognizedCampaignGeneralSetupBits by lazy { recognizedCampaignGeneralSetupBits() }
	private val recognizedFactionPersonalities by lazy { recognizedFactionPersonalities() }
	private val ignoredFactionSpecifications by lazy { ignoredFactionSpecifications() }

	fun readDescrStrat()
	{
		//Read descr_strat for trait/unit usage
		val filename = "descr_strat.txt"
		var lineNumber = 0
		var readLine :String? = null
		try
		{
			main.writeOutput(filename)
			val descrStratReader = BufferedReader(FileReader(main.runCfg.stratFolder + filename))
			while(run { readLine = descrStratReader.readLine(); readLine } != null)
			{
				lineNumber++

				//Ignore case, starting whitespace, multiple spaces and comments
				var line :String = StringUtil.standardize(readLine!!)
				line = line.replace(" , ", ", ") //Common weird way to separate tokens
				line = line.trim() //Occasionally a trailing space will muck up the system
				if(line == "")
					continue
				val tokens = StringUtil.split(line, " ")
				if(tokens[0] == "script")
				{
					resetActives()
					scriptSectionActive = true
				}
				if(scriptSectionActive)
				{
					//TODO read scripts listed here, currently ignoring the rest of DS.
					break
				}
				if(!campaignGeneralSetupComplete)
				{
					readGeneralSetupLine(filename, lineNumber, line, tokens)
					if(!campaignGeneralSetupComplete)
						continue
				}

				//Strat map contents not related to specific faction
				if(tokens[0] == "resource")
				{
					resetActives()
					main.data.strat.mapResources.add(MapResource(tokens[1], tokens[2], tokens[3]))
					continue
				}
				if(activeRegion != null)
				{
					when(tokens[0])
					{
						"farming_level", "famine_threat" ->
							continue
						"fort" ->
						{
							val fort = MapFort()
							main.data.strat.mapForts.add(fort)
							fort.x = tokens[1].toInt()
							fort.y = tokens[2].toInt()
							fort.type = tokens[3]
							fort.culture = tokens[5]
							continue
						}
						"watchtower" ->
						{
							val tower = MapWatchtower(tokens[1].toInt(), tokens[2].toInt())
							main.data.strat.watchtowers.add(tower)
							continue
						}
					}
				}
				if(activeSettlement == null && tokens[0] == "region")
				{
					resetActives()
					activeRegion = tokens[1]
					continue
				}
				if(tokens[0] == "faction_standings")
				{
					resetActives()
					main.data.strat.factionReferences.add(SimpleReferenceRecord(tokens[1].replace(",", ""), filename, lineNumber))
					for(i in 3 until tokens.size)
						main.data.strat.factionReferences.add(SimpleReferenceRecord(tokens[i].replace(",", ""), filename, lineNumber))
					continue
				}
				if(tokens[0] == "faction_relationships")
				{
					resetActives()
					main.data.strat.factionReferences.add(SimpleReferenceRecord(tokens[1].replace(",", ""), filename, lineNumber))
					val relationship :String = tokens[2].replace(",", "")
					if(!Util.equalsAny(relationship, "at_war_with", "allied_to", "allied_with", "protectorate_of"))
						main.writeStratmapLog(filename, lineNumber, """Faction relationship "$relationship" is not recognized.""")
					for(i in 3 until tokens.size)
						main.data.strat.factionReferences.add(SimpleReferenceRecord(tokens[i].replace(",", ""), filename, lineNumber))
					continue
				}

				//Faction startup specifications
				if(tokens[0] == "faction")
				{
					resetActives()
					activeFaction = tokens[1].replace(",", "")
					main.data.strat.factionReferences.add(SimpleReferenceRecord(activeFaction, filename, lineNumber))
					for(i in 2 until tokens.size)
					{
						val personality :String = tokens[i].replace(",", "")
						if(!recognizedFactionPersonalities.contains(personality))
							main.writeStratmapLog(filename, lineNumber, """Unrecognized faction personality "$personality"""")
					}
					continue
				}
				if(activeFaction != "")
					readFactionSpecification(filename, lineNumber, line, tokens)
				else
					main.writeSundryLog("$filename $lineNumber: Parsing error - Unrecognized directive on line: $line")
			}
			descrStratReader.close()
		}
		catch(e :FileNotFoundException)
		{
			main.writeOutput("Cannot find descr_strat.txt. Are you sure you provided the correct location for the strat folder?")
		}
		catch(e :Exception)
		{
			main.fatalParsingError(lineNumber, readLine!!, e)
		}
	}

	private fun readGeneralSetupLine(filename :String, lineNumber :Int, line :String, tokens :Array<String>)
	{
		if(Util.equalsAny(tokens[0], "resource", "faction"))
		{
			campaignGeneralSetupComplete = true
			return
		}
		if(playabilityActive)
		{
			if(tokens[0] == "end")
				playabilityActive = false
			else
				main.data.strat.factionReferences.add(SimpleReferenceRecord(tokens[0], filename, lineNumber))
			return
		}

		//Campaign general setup
		if(tokens[0] == "campaign")
		{
			val campaignName = tokens[1]
			if(!main.runCfg.stratFolder.lowercase().contains(campaignName))
				main.writeStratmapLog(filename, lineNumber, "Campaign name ($campaignName) does not match the strat folder name (${main.runCfg.stratFolder})")
			return
		}
		if(Util.equalsAny(tokens[0], "playable", "unlockable", "nonplayable"))
		{
			playabilityActive = true
			return
		}
		if(!recognizedCampaignGeneralSetupBits.contains(tokens[0]))
			main.writeStratmapLog(filename, lineNumber, "Unrecognized campaign general setup directive on line: $line")
	}

	private fun readFactionSpecification(filename :String, lineNumber :Int, lineContent :String, tokens :Array<String>)
	{
		var line = lineContent
		if(ignoredFactionSpecifications.contains(tokens[0]))
			return
		var recognizedDirective = false
		when(tokens[0])
		{
			"settlement" ->
			{
				activeCharacter = null
				armyActive = false
				activeSettlement = MapSettlement(activeFaction, filename, lineNumber)
				if(tokens.size > 1 && tokens[1] == "castle")
					activeSettlement!!.isCity = false
				main.data.strat.mapSettlements.add(activeSettlement!!)
				return
			}
			"}" ->
			{
				when
				{
					settlementBuildingActive ->
						settlementBuildingActive = false
					activeSettlement != null ->
						activeSettlement = null
					else ->
						main.writeStratmapLog(filename, lineNumber, "Closing brace without recognized open element (settlement or settlement building)")
				}
				return
			}
			"name_faction" ->
			{
				main.data.strat.characterTypeReferences.add(SimpleReferenceRecord(tokens[1], filename,  lineNumber))
				main.data.strat.factionReferences.add(SimpleReferenceRecord(tokens[2], filename,  lineNumber))
			}
		}
		if(activeSettlement != null)
		{
			if(settlementBuildingActive)
			{
				if(tokens[0] == "type")
				{
					recognizedDirective = true
					main.data.strat.buildingReferences.add(SimpleReferenceRecord(tokens[1], filename, lineNumber))
					main.data.strat.buildingLevelReferences.add(SimpleReferenceRecord(tokens[2], filename, lineNumber))
					activeSettlement!!.buildingsPresent.add("${tokens[1]} ${tokens[2]}")
					activeSettlementBuildingType = tokens[1]
				}
				if(tokens[0] == "creator")
				{
					recognizedDirective = true
					main.data.strat.factionReferences.add(SimpleReferenceRecord(tokens[1], filename, lineNumber))
				}
				if(tokens[0] == "health")
					recognizedDirective = true
				if(tokens[0] == "plugin")
				{
					recognizedDirective = true
					main.data.strat.buildingPluginReferences.add(BuildingPluginRecord(filename, lineNumber, activeSettlementBuildingType, tokens[1], tokens[2]))
				}
			}
			else if(tokens[0] == "building")
			{
				recognizedDirective = true
				settlementBuildingActive = true
			}
			else
			{
				recognizedDirective = true
				when(tokens[0])
				{
					"level" ->
						activeSettlement!!.level = tokens[1]
					"region" ->
						activeSettlement!!.region = tokens[1]
					"year_founded" ->
						activeSettlement!!.yearFounded = tokens[1].toInt()
					"population" ->
						activeSettlement!!.population = tokens[1].toInt()
					"plan_set" ->
						activeSettlement!!.planSet = tokens[1]
					"faction_creator" ->
						activeSettlement!!.creatorFaction = tokens[1]
					else ->
						recognizedDirective = false
				}
			}
		}
		if(tokens[0] == "character")
		{
			recognizedDirective = true
			activeCharacter = MapCharacterParsing.createCharacter(activeFaction, filename, lineNumber, StringUtil.after(line, "character "), false)
			main.data.strat.mapCharacters.add(activeCharacter!!)
			armyActive = false
		}
		else if(tokens[0] == "character_record")
		{
			recognizedDirective = true
			val record = MapCharacter(activeFaction, filename, lineNumber, StringUtil.between(line, " ", ",")!!.trim())
			main.data.strat.characterRecords.add(record)
			record.isFemale = line.contains("female,")
		}
		else if(tokens[0] == "relative")
		{
			recognizedDirective = true
			val record = CharacterRelationships(activeFaction, filename, lineNumber)
			main.data.strat.characterRelationships.add(record)
			record.characterName = StringUtil.between(line, " ", ",")!!
			val relatives = StringUtil.split(line, ",")
			for(i in 1 until relatives.size)
			{
				if(relatives[i].trim() != "end")
					record.relations.add(relatives[i].trim())
			}
		}
		else if(activeCharacter != null)
		{
			recognizedDirective = true
			if(tokens[0] == "army")
				armyActive = true
			else if(tokens[0] == "unit")
			{
				if(!armyActive)
					main.writeStratmapLog(filename, lineNumber, "Unit specified without preceding army keyword.")
				var unitName = ""
				for(i in 1 until tokens.size)
				{
					if(Util.equalsAny(tokens[i], "exp", "soldiers", "num"))
					{
						unitName = unitName.trim()
						break
					}
					unitName += " " + tokens[i]
				}
				main.data.strat.referencedUnits.add(SimpleReferenceRecord(unitName, filename, lineNumber))
			}
			else if(tokens[0] == "ancillaries")
			{
				for(i in 1 until tokens.size)
					activeCharacter!!.ancillaries.add(tokens[i].replace(",", ""))
			}
			else if(tokens[0] == "traits")
			{
				for(j in 1 until tokens.size)
					tokens[j] = tokens[j].replace(",", "")
				var j = 1
				while(j < tokens.size)
				{
					if(tokens[j].matches("[0-9]+".toRegex()) || tokens[j] == "")
					{
						j++
						continue
					}
					else
					{
						val awardedTrait = tokens[j]
						val awardedAmount = tokens[j + 1]
						j++
						main.data.strat.traitReferences.add(TraitReferenceRecord(filename, lineNumber, awardedTrait, null, awardedAmount.toInt()))
					}
					j++
				}
			}
			else
				recognizedDirective = false
		}
		if(!recognizedDirective)
			main.writeSundryLog("$filename $lineNumber: Parsing error - Unrecognized directive on line: $line")
	}

	private fun resetActives()
	{
		activeFaction = ""
		activeRegion = null
		activeCharacter = null
		armyActive = false
		activeSettlement = null
		settlementBuildingActive = false
	}

	private fun recognizedCampaignGeneralSetupBits() :ArrayList<String>
	{
		val retur = ArrayList<String>()
		retur.add("start_date")
		retur.add("end_date")
		retur.add("timescale")
		retur.add("marian_reforms_disabled")
		retur.add("rebelling_characters_active")
		retur.add("gladiator_uprising_disabled")
		retur.add("night_battles_enabled")
		retur.add("show_date_as_turns")
		retur.add("brigand_spawn_value")
		retur.add("pirate_spawn_value")
		retur.add("free_upkeep_forts")
		return retur
	}

	private fun recognizedFactionPersonalities() :ArrayList<String>
	{
		val retur = ArrayList<String>()
		retur.add("balanced")
		retur.add("religious")
		retur.add("trader")
		retur.add("comfortable")
		retur.add("bureaucrat")
		retur.add("craftsman")
		retur.add("sailor")
		retur.add("fortified")
		retur.add("craftsmen")
		retur.add("tzar")
		retur.add("smith")
		retur.add("saladin")
		retur.add("tahar")
		retur.add("arslan")
		retur.add("alfonso")
		retur.add("roger")
		retur.add("vlad")
		retur.add("wyvadslaw")
		retur.add("robert")
		retur.add("doge")
		retur.add("guy")
		retur.add("knud")
		retur.add("subotai")
		retur.add("heinrich")
		retur.add("richard")
		retur.add("mao")
		retur.add("genghis")
		retur.add("stalin")
		retur.add("napoleon")
		retur.add("henry")
		retur.add("caesar")
		return retur
	}

	private fun ignoredFactionSpecifications() :ArrayList<String>
	{
		val retur = ArrayList<String>()
		retur.add("ai_label")
		retur.add("denari")
		retur.add("denari_kings_purse")
		retur.add("re_emergent")
		retur.add("undiscovered")
		retur.add("dead_until_emerged")
		retur.add("dead_until_resurrected")
		retur.add("{")
		return retur
	}
}