package sources.stratmap

import data.FactionEntry
import data.ResourceEntry
import data.common.FileReferenceRecord
import data.common.UsageTrackedName
import data.unit.StratModelEntry
import main.BovineM2twCheck
import sources.stratmap.building.BuildingReader
import sources.stratmap.names.NamesReader
import util.CasUtil
import util.StringUtil
import util.Util
import java.io.BufferedReader
import java.io.FileNotFoundException
import java.io.FileReader

class StratMapReader(private val main :BovineM2twCheck)
{
	private val ignoredFactionDirectives by lazy { ignoredFactionDirectives() }

	private val buildingReader = BuildingReader(main)
	private val cultureReader = CultureReader(main)
	private val descrStratReader = DescrStratReader(main)
	private val namesReader = NamesReader(main)
	private val missionReader = MissionReader(main)

	fun readWhenever()
	{
		buildingReader.readBuildings()
		missionReader.readAll()
		namesReader.readAll()
		readFactions()
		cultureReader.readCultures()
		descrStratReader.readDescrStrat()
		readReligions()
		readStratModels()
		readResources()
		addHardcodedPipReferences()
	}

	private fun readFactions()
	{
		val filename = "descr_sm_factions.txt"
		var readLine :String? = null
		var lineNumber = 0
		try
		{
			main.writeOutput(filename)
			val factionsReader = BufferedReader(FileReader(main.runCfg.dataFolder + filename))
			var faction :FactionEntry = FactionEntry("dummy", "dummy", -1)
			while(run { readLine = factionsReader.readLine(); readLine } != null)
			{
				val line :String = StringUtil.standardize(readLine!!)
				lineNumber++
				if(line == "")
					continue
				val tokens :Array<String> = StringUtil.split(line, " ")
				when(tokens[0])
				{
					"faction" ->
					{
						var factionName = tokens[1]
						if(factionName.endsWith(","))
							factionName = factionName.substring(0, factionName.length - 1)
						faction = FactionEntry(factionName, filename, lineNumber)
						main.data.strat.factionEntries[factionName] = faction
					}
					"culture" ->
						faction.culture = tokens[1]
					"religion" ->
						faction.religion = tokens[1]
					"standard_index" ->
						faction.standardIndex = tokens[1]
					"logo_index" ->
						faction.logoIndex = tokens[1]
					"small_logo_index" ->
						faction.smallLogoIndex = tokens[1]
					"horde_min_units" ->
						faction.hordeMinimumUnits = tokens[1].toInt()
					"horde_max_units" ->
						faction.hordeMaximumUnits = tokens[1].toInt()
					"horde_max_units_reduction_every_horde" ->
						faction.hordeMaximumUnitsReductionEveryHorde = tokens[1].toInt()
					"horde_unit_per_settlement_population" ->
						faction.hordeUnitPerSettlementPopulation = tokens[1].toInt()
					"horde_min_named_characters" ->
						faction.hordeMinNamedCharacters = tokens[1].toInt()
					"horde_max_percent_army_stack" ->
						faction.hordeMaxPercentArmyStack = tokens[1].toInt()
					"horde_disband_percent_on_settlement_capture" ->
						faction.hordeDisbandPercentOnSettlementCapture = tokens[1].toInt()
					"horde_unit" ->
						faction.hordeUnits.add(StringUtil.after(line, "horde_unit "))
					"symbol" ->
					{
						faction.symbolFile = tokens[1]
						val folderEndPosition = faction.symbolFile.lastIndexOf("/")
						val folderPart = faction.symbolFile.substring(0, folderEndPosition)
						val filePart = faction.symbolFile.substring(folderEndPosition + 1)
						val reference = FileReferenceRecord(filename, lineNumber, "Faction " + faction.name, filePart, folderPart)
						main.data.fileReferencesForCrossCheck.add(reference)
					}
					"rebel_symbol" ->
					{
						faction.rebelSymbolFile = tokens[1]
						val folderEndPosition = faction.rebelSymbolFile.lastIndexOf("/")
						val folderPart = faction.rebelSymbolFile.substring(0, folderEndPosition)
						val filePart = faction.rebelSymbolFile.substring(folderEndPosition + 1)
						val reference = FileReferenceRecord(filename, lineNumber, "Faction " + faction.name, filePart, folderPart)
						main.data.fileReferencesForCrossCheck.add(reference)
					}
					"loading_logo" ->
					{
						faction.loadingLogoFile = tokens[1]
						//NOT checking this file reference because the game doesn't use it
						//val folderEndPosition = faction.loadingLogoFile.lastIndexOf("/")
						//val folderPart = faction.loadingLogoFile.substring(0, folderEndPosition)
						//val filePart = faction.loadingLogoFile.substring(folderEndPosition + 1)
						//val reference = FileReferenceRecord(filename, lineNumber, "Faction " + faction.name, filePart, folderPart)
						//main.data.fileReferencesForCrossCheck.add(reference);
					}
					"special_faction_type" ->
					{
						when(tokens[1])
						{
							"papal_faction" ->
								faction.isPapacy = true
							"slave_faction" ->
								faction.isSlave = true
						}
					}
					"disband_to_pools" ->
						faction.disbandingToPools = (tokens[1] != "no")
					else ->
					{
						if(!ignoredFactionDirectives.contains(tokens[0]))
							main.writeStratmapLog(filename, lineNumber, "Unrecognized faction detail ${tokens[0]}")
					}
				}
			}
			factionsReader.close()
			main.data.strat.factionEntries["merc"] = FactionEntry("merc", filename, -1)
		}
		catch(e :FileNotFoundException)
		{
			main.writeOutput("Unable to find list of factions (descr_sm_factions.txt). This will be a problem.")
		}
		catch(e :Exception)
		{
			main.fatalParsingError(lineNumber, readLine!!, e)
		}
	}

	private fun readStratModels()
	{
		val filename = "descr_model_strat.txt"
		var readLine :String? = null
		var lineNumber = 0
		try
		{
			main.writeOutput(filename)
			val stratModelReader = BufferedReader(FileReader(main.runCfg.dataFolder + filename))
			var stratModel = StratModelEntry("dummy", null, -1)
			while(run { readLine = stratModelReader.readLine(); readLine } != null)
			{
				var line :String = StringUtil.standardize(readLine!!)
				lineNumber++
				if(Util.equalsAny(line, "", "ignore_registry"))
					continue
				var tokens :Array<String> = StringUtil.split(line, " ")
				when(tokens[0])
				{
					"type" ->
					{
						stratModel = StratModelEntry(tokens[1], filename, lineNumber)
						main.data.strat.stratModels.add(stratModel)
					}
					"texture", "texture_no_move" ->
					{
						line = line.replace(",".toRegex(), " ").replace("  ".toRegex(), " ")
						tokens = StringUtil.split(line, " ")
						var textureFilename = ""
						for(i in 2 until tokens.size)
						{
							textureFilename += tokens[i]
							if(i != tokens.size - 1)
								textureFilename += " "
						}
						val texture = StratModelEntry.TextureAssignment()
						texture.faction = tokens[1].replace(",".toRegex(), "")
						texture.lineNumber = lineNumber
						texture.texture = textureFilename
						stratModel.textureAssignments.add(texture)
						main.data.fileReferencesForCrossCheck.add(FileReferenceRecord(filename, lineNumber, stratModel.name, textureFilename, null, arrayOf(".dds")))
					}
					"model_flexi", "model_flexi_c", "model_flexi_m" ->
					{
						var modelFilename = ""
						for(i in 1 until tokens.size - 1)
						{
							modelFilename += tokens[i]
							if(i != tokens.size - 2)
								modelFilename += " "
						}
						if(modelFilename.endsWith(","))
							modelFilename = modelFilename.substring(0, modelFilename.length - 1)
						stratModel.modelAssignment.modelFile = modelFilename
						main.data.fileReferencesForCrossCheck.add(FileReferenceRecord(filename, lineNumber, stratModel.name, modelFilename))
					}
					"shadow_model_flexi" ->
					{
						var modelFilename = ""
						for(i in 1 until tokens.size - 1)
						{
							modelFilename += tokens[i]
							if(i != tokens.size - 2)
								modelFilename += " "
						}
						if(modelFilename.endsWith(","))
							modelFilename = modelFilename.substring(0, modelFilename.length - 1)
						stratModel.modelAssignment.shadowModelFile = modelFilename
						main.data.fileReferencesForCrossCheck.add(FileReferenceRecord(filename, lineNumber, stratModel.name, modelFilename))
					}
					"skeleton" ->
						stratModel.skeleton = tokens[1]
					"scale" ->
						stratModel.scale = tokens[1].toDouble()
					"indiv_range" ->
						stratModel.indivRange = tokens[1].toInt()
					else ->
						main.writeStratmapLog(filename, lineNumber, """Unrecognized directive in line, "$line"""")
				}
			}
			stratModelReader.close()
		}
		catch(e :FileNotFoundException)
		{
			main.writeOutput("Unable to find list of strat models (descr_model_strat.txt). This may cause false reports.")
		}
		catch(e :Exception)
		{
			main.fatalParsingError(lineNumber, readLine!!, e)
		}
	}

	private fun readResources()
	{
		val filename = "descr_sm_resources.txt"
		var readLine :String? = null
		var lineNumber = 0
		try
		{
			main.writeOutput(filename)
			val resourceReader = BufferedReader(FileReader(main.runCfg.dataFolder + filename))
			var resource = ResourceEntry("dummy", filename, lineNumber)
			while(run { readLine = resourceReader.readLine(); readLine } != null)
			{
				val line :String = StringUtil.standardize(readLine!!)
				lineNumber++
				if(line == "")
					continue
				val tokens :Array<String> = StringUtil.split(line, " ")
				var modelJustFound = false
				when(tokens[0])
				{
					"mine" ->
					{
						resource = ResourceEntry("mine", filename, lineNumber)
						main.data.strat.resources.add(resource)
						resource.modelFile = tokens[1]
						main.data.fileReferencesForCrossCheck.add(FileReferenceRecord(filename, lineNumber, "mine", resource.modelFile!!))
						modelJustFound = true
					}
					"type" ->
					{
						resource = ResourceEntry(tokens[1], filename, lineNumber)
						main.data.strat.resources.add(resource)
					}
					"trade_value" ->
						resource.tradeValue = tokens[1].toInt()
					"item" ->
					{
						resource.modelFile = tokens[1]
						main.data.fileReferencesForCrossCheck.add(FileReferenceRecord(filename, lineNumber, resource.name, resource.modelFile!!))
						modelJustFound = true
					}
					"icon" ->
					{
						resource.iconFile = tokens[1]
						main.data.fileReferencesForCrossCheck.add(FileReferenceRecord(filename, lineNumber, resource.name, resource.iconFile!!))
					}
					"has_mine" ->
						resource.hasMine = true
				}
				if(modelJustFound)
				{
					val modelFileName :String = resource.modelFile!!.replace("data/", "")
					resource.textureFiles.addAll(CasUtil.getCasFileTextures(modelFileName, true))
					if(resource.textureFiles.size == 0 && !main.lists.vanillaFiles.contains(modelFileName))
						main.writeOutput("Found no textures in resource model $modelFileName. This means the checker probably is lacking code to recognize its textures.")
					for(textureFile in resource.textureFiles)
					{
						val reference = FileReferenceRecord(filename, lineNumber, resource.name, textureFile, null, arrayOf(".dds"))
						main.data.fileReferencesForCrossCheck.add(reference)
					}
				}
			}
			resourceReader.close()
		}
		catch(e :FileNotFoundException)
		{
			main.writeOutput("Unable to find list of campaign map resources ($filename). This may cause false reports.")
		}
		catch(e :Exception)
		{
			main.fatalParsingError(lineNumber, readLine!!, e)
		}
	}

	private fun readReligions()
	{
		val filename = "descr_religions.txt"
		var readLine :String? = null
		var lineNumber = 0
		try
		{
			main.writeOutput(filename)
			val religionReader = BufferedReader(FileReader(main.runCfg.dataFolder + filename))
			var religionActive = false
			var activeReligion :UsageTrackedName? = null
			var religionsActive = false
			while(run { readLine = religionReader.readLine(); readLine } != null)
			{
				var line :String = StringUtil.standardize(readLine!!).trim()
				lineNumber++
				if(line.startsWith("{"))
					line = line.substring(1).trim()
				if(line.startsWith("}"))
				{
					religionActive = false
					activeReligion = null
					religionsActive = false
					line = line.substring(1).trim()
				}
				if(line == "")
					continue
				val tokens :Array<String> = StringUtil.split(line, " ")
				when
				{
					tokens[0] == "religions" ->
						religionsActive = true
					tokens[0] == "religion" ->
					{
						val religionName = tokens[1]
						religionActive = true
						activeReligion = main.data.strat.religions[religionName, false]
						if(activeReligion == null)
							main.writeStratmapLog(filename, lineNumber, "Setting details for religion \"$religionName\", which is not present in the enumeration of religions.")
					}
					religionsActive ->
						main.data.strat.religions.add(UsageTrackedName(line, filename, lineNumber))
					religionActive ->
					{
						if(line.startsWith("pip_path"))
							main.data.fileReferencesForCrossCheck.add(FileReferenceRecord(filename, lineNumber, "Religion " + activeReligion!!.name, tokens[1]))
					}
				}
			}
			religionReader.close()
		}
		catch(e :FileNotFoundException)
		{
			main.writeOutput("Unable to find list of religions ($filename). This may cause false reports.")
		}
		catch(e :Exception)
		{
			main.fatalParsingError(lineNumber, readLine!!, e)
		}
	}

	fun readLast()
	{
		var popeReligion :String? = null
		for(faction :FactionEntry in main.data.strat.factionEntries.values)
		{
			if(faction.isPapacy)
				popeReligion = faction.religion
		}
		if(popeReligion != null)
		{
			for(faction :FactionEntry in main.data.strat.factionEntries.values)
			{
				if(faction.religion == popeReligion)
					faction.isEligibleForPopeMissions = true
			}
		}
	}

	private fun addHardcodedPipReferences()
	{
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_admin.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_besieged.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_blockaded.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_boom.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_buildings.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_buildings_fun.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_buildings_law.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_construction.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_corruption.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_culture_penalty.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_demolition.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_devastation.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_diplomatic_income.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_diplomatic_outgoings.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_disasters.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_distance_to_capital.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_entertained.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_excommunication.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_farming_level.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_farms.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_farms_built.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_fear.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_food_imports.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_garrison.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_glory.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_governors_influence.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_health.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_looting.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_mining.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_no_governance.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_placeholder.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_plague.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_recession.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_recruitment.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_recruits.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_religious_unrest.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_resources.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_slavery.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_squalour.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_taxes.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_tax_bonus.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_tax_penalty.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_tax_rate_bonus.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_tax_rate_penalty.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_trade.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_triumph.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_turmoil.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_underpopulation.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_unit_disbands.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_upkeep.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_wages.tga"))
		main.data.fileReferencesForCrossCheck.add(FileReferenceRecord("", -1, "Hardcoded settlement detail pip images", "ui/pips/pip_wonder.tga"))
	}

	private fun ignoredFactionDirectives() :ArrayList<String>
	{
		val retur = ArrayList<String>()
		retur.add("primary_colour")
		retur.add("secondary_colour")
		retur.add("triumph_value")
		retur.add("custom_battle_availability")
		retur.add("can_sap")
		retur.add("can_build_siege_towers")
		retur.add("can_have_princess")
		retur.add("has_family_tree")
		retur.add("prefers_naval_invasions")
		retur.add("can_transmit_plague")
		return retur
	}
}