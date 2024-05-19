package sources.stratmap.building

import data.ResourceEntry
import data.common.SimpleReferenceRecord
import data.code.ResourceReferenceRecord
import data.strat.building.*
import main.BovineM2twCheck
import util.StringUtil
import java.io.BufferedReader
import java.io.FileNotFoundException
import java.io.FileReader
import java.util.*

class BuildingReader(private val main :BovineM2twCheck)
{
	private val singleDecimalCapabilities by lazy { singleDecimalCapabilities() }
	private val singleIntCapabilities by lazy { singleIntCapabilities() }
	private val singleIntCapabilitiesWithBonus by lazy { singleIntCapabilitiesWithBonus() }
	private val agentRelatedCapabilities by lazy { agentRelatedCapabilities() }

	fun readBuildings()
	{
		val filename = "export_descr_buildings.txt"
		var readLine :String? = null
		var lineNumber = 0
		try
		{
			main.writeOutput(filename)
			val buildingFile = BufferedReader(FileReader(main.runCfg.dataFolder + filename))
			var openBracesCount = 0
			var buildingActive = false
			var buildingLevelsActive = false
			var buildingLevelActive = false
			var capabilityActive = false
			var upgradesActive = false
			var pluginsActive = false
			var activeEntry = BuildingEntry("dummy", filename, -1)
			var activeLevel :BuildingLevelEntry = BuildingLevelEntry("dummy", filename, -1)
			while(run { readLine = buildingFile.readLine(); readLine } != null)
			{
				lineNumber++
				//Ignore case, starting whitespace, multiple spaces and comments
				val line :String = StringUtil.standardize(readLine!!)
				if(line == "")
					continue
				val tokens = StringUtil.split(line, " ")
				val directive = tokens[0]
				if(directive == "{")
				{
					openBracesCount++
					continue
				}
				if(directive == "}")
				{
					openBracesCount--
					when(openBracesCount)
					{
						0 ->
							buildingActive = false
						1 ->
						{
							buildingLevelsActive = false
							pluginsActive = false
						}
						2 ->
							buildingLevelActive = false
						3 ->
						{
							capabilityActive = false
							upgradesActive = false
						}
					}
					continue
				}
				if(directive == "plugins")
					pluginsActive = true
				//TODO Should not ignore everything inside plugins after all?
				if(pluginsActive)
					continue
				if(directive == "hidden_resources")
				{
					for(i in 1 until tokens.size)
					{
						val hiddenResource = ResourceEntry(tokens[i], filename, lineNumber)
						hiddenResource.isHidden = true
						main.data.strat.resources.add(hiddenResource)
					}
					continue
				}
				if(directive == "building")
				{
					if(buildingActive)
						main.writeStratmapLog(filename, lineNumber, "Parsing error - Opening building entry while already open.")
					buildingActive = true
					activeEntry = BuildingEntry(tokens[1], filename, lineNumber)
					main.data.strat.buildings.add(activeEntry)
					continue
				}
				if(directive == "religion")
				{
					if(buildingLevelActive)
						main.writeStratmapLog(filename, lineNumber, "Parsing error - Religion assignment while building level is open (should be on building generally).")
					activeEntry.religion = tokens[1]
					continue
				}
				if(directive == "convert_to")
				{
					if(!buildingLevelActive)
						activeEntry.convertTo = tokens[1]
					else
						activeLevel.convertToLevel = tokens[1].toInt()
					continue
				}
				if(directive == "levels")
				{
					if(!buildingActive || buildingLevelsActive)
						main.writeStratmapLog(filename, lineNumber, "Parsing error - Opening levels section while already open or no building entry open.")
					buildingLevelsActive = true
					for(i in 1 until tokens.size)
						activeEntry.buildingLevels.add(BuildingLevelEntry(tokens[i], filename, lineNumber))
					continue
				}
				if(buildingActive && buildingLevelsActive && !buildingLevelActive)
				{
					var level :BuildingLevelEntry? = activeEntry.buildingLevels[directive, false]
					if(level == null)
					{
						main.writeStratmapLog(filename, lineNumber, "Parsing error - defining building level \"$directive\" which is not already enumerated in the building's levels.")
						activeEntry.buildingLevels.add(BuildingLevelEntry(directive, filename, lineNumber))
						level = activeEntry.buildingLevels[directive, false]
					}
					activeLevel = level!!
					buildingLevelActive = true
					readRequirements(level, StringUtil.after(line, " "), filename, lineNumber)
					continue
				}
				if(buildingActive && buildingLevelsActive && buildingLevelActive && !capabilityActive && !upgradesActive)
				{
					when(directive)
					{
						"capability" ->
							capabilityActive = true
						"upgrades" ->
							upgradesActive = true
						"material" ->
							activeLevel.material = tokens[1]
						"construction" ->
							activeLevel.constructionTime = tokens[1].toInt()
						"cost" ->
							activeLevel.cost = tokens[1].toInt()
						"settlement_min" ->
							activeLevel.settlementLevelRequirement = tokens[1]
					}
					continue
				}
				if(buildingActive && buildingLevelActive && buildingLevelActive && upgradesActive && capabilityActive)
				{
					main.writeStratmapLog(filename, lineNumber, "Parsing error - Both upgrades and capability sections are open at the same time!")
					continue
				}
				if(buildingActive && buildingLevelActive && buildingLevelActive && upgradesActive)
				{
					val upgrade = BuildingLevelUpgrade(tokens[0], filename, lineNumber)
					activeLevel.upgrades.add(upgrade)
					readRequirements(upgrade, StringUtil.exceptBefore(line, " "), filename, lineNumber)
					continue
				}
				if(buildingActive && buildingLevelActive && buildingLevelActive && capabilityActive)
				{
					if(directive == "recruit_pool")
						activeLevel.recruitmentCapabilities.add(readRecruitmentCapability(line, filename, lineNumber))
					else
						activeLevel.generalCapabilities.add(readBuildingCapability(line, filename, lineNumber))
					continue
				}
				main.writeStratmapLog(filename, lineNumber, "Parsing error - Unrecognized directive for line \"$line\"")
			}
			buildingFile.close()
		}
		catch(e :FileNotFoundException)
		{
			main.writeOutput("Cannot find export_descr_buildings.txt. Are you sure you provided the correct location for the data folder?")
		}
		catch(e :Exception)
		{
			main.fatalParsingError(lineNumber, readLine!!, e)
		}
	}

	private fun readRequirements(target :BuildingRequirementsHolder, line :String, filename :String, lineNumber :Int)
	{
		var remainingBits = line
		if(remainingBits.startsWith(" "))
			remainingBits = remainingBits.substring(1)
		if(remainingBits == "")
			return
		remainingBits = readCityCastleBuildingRequirement(target, remainingBits)
		if(remainingBits.isNotEmpty() && !remainingBits.startsWith("requires "))
		{
			main.writeStratmapLog(filename, lineNumber, """Parsing failure, expected "requires" at the start of this section to read requirements: "$line" ("castle" or "city" before "requires" is allowed)""")
			return
		}
		remainingBits = StringUtil.after(remainingBits, "requires ")
		var negationActive = 0
		while(remainingBits.isNotEmpty())
		{
			if(remainingBits.startsWith(" "))
			{
				remainingBits = remainingBits.substring(1)
				continue
			}
			negationActive++
			if(remainingBits == "port" || remainingBits.startsWith("port "))
			{
				remainingBits = remainingBits.substring(4)
				continue
			}
			if(remainingBits == "castle_port" || remainingBits.startsWith("castle_port "))
			{
				remainingBits = remainingBits.substring(11)
				continue
			}
			if(remainingBits.startsWith("factions "))
			{
				var references = StringUtil.between(remainingBits, "{", "}")
				references = references!!.trim().replace(",", "")
				for(token in StringUtil.split(references, " "))
					target.factionRequirements.add(SimpleReferenceRecord(token, filename, lineNumber))
				remainingBits = StringUtil.after(remainingBits, "}")
				continue
			}
			if(remainingBits.startsWith("resource ") || remainingBits.startsWith("hidden_resource "))
			{
				var name = StringUtil.between(remainingBits, " ", " ")
				if(name == null)
					name = StringUtil.after(remainingBits, " ")
				target.resourceRequirements.add(ResourceReferenceRecord(name, filename, lineNumber, remainingBits.startsWith("hidden_resource")))
				remainingBits = StringUtil.after(remainingBits, name)
				continue
			}
			if(remainingBits.startsWith("region_religion "))
			{
				val religionName = StringUtil.between(remainingBits, " ", " ")!!
				target.religionReferences.add(SimpleReferenceRecord(religionName, filename, lineNumber))
				remainingBits = StringUtil.after(remainingBits, "$religionName ")
				remainingBits = StringUtil.exceptBefore(remainingBits, " ")
				continue
			}
			if(remainingBits.startsWith("building_present_min_level "))
			{
				val buildingName = StringUtil.between(remainingBits, " ", " ")!!
				var buildingLevelName = StringUtil.between(remainingBits, "$buildingName ", " ")
				if(buildingLevelName == null)
					buildingLevelName = StringUtil.after(remainingBits, "$buildingName ")
				target.buildingReferences.add(SimpleReferenceRecord(buildingName, filename, lineNumber))
				target.buildingLevelReferences.add(SimpleReferenceRecord(buildingLevelName, filename, lineNumber))
				remainingBits = StringUtil.after(remainingBits, "$buildingName $buildingLevelName")
				continue
			}
			if(remainingBits.startsWith("building_present "))
			{
				var buildingName :String? = StringUtil.between(remainingBits, " ", " ")
				if(buildingName == null)
					buildingName = StringUtil.after(remainingBits, "building_present ")
				target.buildingReferences.add(SimpleReferenceRecord(buildingName, filename, lineNumber))
				remainingBits = StringUtil.after(remainingBits, buildingName)
				continue
			}
			if(remainingBits.startsWith("event_counter "))
			{
				var name :String = StringUtil.after(remainingBits, " ")
				if(name.contains(" "))
					name = StringUtil.before(name, " ")
				main.data.code.addCheckedEventCounterLocation(SimpleReferenceRecord(name, filename, lineNumber))
				remainingBits = StringUtil.after(remainingBits, name)
				remainingBits = StringUtil.after(remainingBits, " ")
				when(val specificValue :Int? = StringUtil.before(remainingBits, " ").toIntOrNull())
				{
					1 ->
					{
						//Skip the value
						remainingBits = StringUtil.after(remainingBits, " ")
					}
					else ->
					{
						var valueString :String = "$specificValue"
						if(valueString == "null")
							valueString = "missing"
						else
							remainingBits = StringUtil.after(remainingBits, " ")

						main.writeSundryLog("$filename $lineNumber: Parsing error - Event counter check requires \"1\" after the event counter name, here it is $valueString.")
					}
				}
				if(remainingBits.length == 1)
					remainingBits = ""
				continue
			}
			if(remainingBits.startsWith("and ") || remainingBits.startsWith("or ") || remainingBits.startsWith("not "))
			{
				if(remainingBits.startsWith("not "))
					negationActive = 1
				//3 is fine because any remaining space at the start gets cut off before reading next token
				remainingBits = remainingBits.substring(3)
				continue
			}
			main.writeStratmapLog(filename, lineNumber, "Parsing failure, encountered unexpected requirement parts: \"$remainingBits\".")
			return
		}
	}

	private fun readCityCastleBuildingRequirement(target: BuildingRequirementsHolder, remainingBits :String) :String
	{
		var bits = remainingBits
		if(bits == "castle" || bits.startsWith("castle "))
		{
			bits = StringUtil.after(bits, "castle")
			target.cityCastleRequirement = "castle"
		}
		if(bits == "city" || bits.startsWith("city "))
		{
			bits = StringUtil.after(bits, "city")
			target.cityCastleRequirement = "city"
		}
		if(bits.startsWith(" "))
			bits = bits.substring(1)
		return bits
	}

	private fun readRecruitmentCapability(line :String, filename :String, lineNumber :Int) :RecruitmentCapability
	{
		var remainingBits = line.substring("recruit_pool ".length)
		val targetUnit = StringUtil.between(line, "\"", "\"")
		val retur = RecruitmentCapability(targetUnit, filename, lineNumber)
		remainingBits = remainingBits.substring(targetUnit!!.length + 3)
		retur.initialPool = StringUtil.before(remainingBits, " ").toDouble()
		remainingBits = StringUtil.after(remainingBits, " ")
		retur.replenishment = StringUtil.before(remainingBits, " ").toDouble()
		remainingBits = StringUtil.after(remainingBits, " ")
		retur.max = StringUtil.before(remainingBits, " ").toDouble()
		remainingBits = StringUtil.after(remainingBits, " ")
		retur.unitExperience = StringUtil.before(remainingBits, " ").toInt()
		remainingBits = StringUtil.after(remainingBits, " ")

		readRequirements(retur, remainingBits, filename, lineNumber)
		return retur
	}

	private fun readBuildingCapability(line :String, filename :String, lineNumber :Int) :BuildingCapability
	{
		val retur = BuildingCapability(StringUtil.before(line, " "), filename, lineNumber)
		var remainingBits = StringUtil.after(line, " ")
		when
		{
			agentRelatedCapabilities.contains(retur.name) ->
			{
				val agentName = StringUtil.before(remainingBits, " ")
				retur.referredAgent = agentName
				remainingBits = StringUtil.exceptBefore(remainingBits, " ")
				val magnitude = StringUtil.before(remainingBits, " ")
				retur.magnitude = magnitude.toDouble()
				remainingBits = StringUtil.exceptBefore(remainingBits, " ")
			}
			singleDecimalCapabilities.contains(retur.name) ->
			{
				var magnitude = StringUtil.before(remainingBits, " ")
				if(magnitude == "bonus")
				{
					remainingBits = StringUtil.exceptBefore(remainingBits, " ")
					magnitude = StringUtil.before(remainingBits, " ")
				}
				retur.magnitude = magnitude.toDouble()
				remainingBits = StringUtil.exceptBefore(remainingBits, " ")
			}
			singleIntCapabilities.contains(retur.name) ->
			{
				var magnitude = StringUtil.before(remainingBits, " ")
				if(magnitude == "bonus")
				{
					remainingBits = StringUtil.exceptBefore(remainingBits, " ")
					magnitude = StringUtil.before(remainingBits, " ")
				}
				retur.magnitude = magnitude.toDouble()
				remainingBits = StringUtil.exceptBefore(remainingBits, " ")
			}
			singleIntCapabilitiesWithBonus.contains(retur.name) ->
			{
				val bonusKeyword = StringUtil.before(remainingBits, " ")
				if(bonusKeyword != "bonus")
				{
					main.writeStratmapLog(filename, lineNumber, "Capability " + retur.name + " expects keyword \"bonus\" after it: " + line)
					//Flush the logs as this may cause a crash trying to read the magnitude
					main.flushLogs()
					retur.magnitude = bonusKeyword.toDouble()
				}
				else
				{
					remainingBits = StringUtil.after(remainingBits, " ")
					val magnitude = StringUtil.before(remainingBits, " ")
					retur.magnitude = magnitude.toDouble()
				}
				remainingBits = StringUtil.exceptBefore(remainingBits, " ")
			}
			else ->
				main.writeStratmapLog(filename, lineNumber, "Parsing failure, encountered unexpected building capability named \"${retur.name}\": $line")
		}
		if(remainingBits == "")
			return retur

		readRequirements(retur, remainingBits, filename, lineNumber)
		return retur
	}

	private fun singleDecimalCapabilities() :ArrayList<String>
	{
		val retur = ArrayList<String>()
		retur.add("religion_level")
		retur.add("amplify_religion_level")
		retur.add("retrain_cost_bonus")
		return retur
	}

	private fun singleIntCapabilities() :ArrayList<String>
	{
		val retur = ArrayList<String>()
		retur.add("wall_level")
		retur.add("tower_level")
		retur.add("gate_strength")
		retur.add("recruitment_slots")
		retur.add("farming_level")
		retur.add("taxable_income_bonus")
		retur.add("road_level")
		retur.add("trade_fleet")
		retur.add("mine_resource")
		retur.add("weapon_melee_simple")
		retur.add("weapon_melee_blade")
		retur.add("weapon_projectile")
		retur.add("weapon_artillery_gunpowder")
		retur.add("weapon_artillery_mechanical")
		retur.add("weapon_missile_gunpowder")
		retur.add("weapon_missile_mechanical")
		retur.add("weapon_naval_gunpowder")
		retur.add("armour")
		retur.add("pope_approval")
		retur.add("pope_disapproval")
		retur.add("stage_games")
		retur.add("stage_races")

		//Apparently do not need "bonus" even though bonus is in the name
		retur.add("archer_bonus")
		retur.add("gun_bonus")
		retur.add("cavalry_bonus")
		retur.add("heavy_cavalry_bonus")
		retur.add("navy_bonus")
		retur.add("population_growth_bonus")
		retur.add("population_health_bonus")
		retur.add("construction_time_bonus_defensive")
		retur.add("construction_time_bonus_religious")
		retur.add("construction_time_bonus_stone")
		retur.add("construction_time_bonus_wooden")
		retur.add("construction_time_bonus_other")
		return retur
	}

	private fun singleIntCapabilitiesWithBonus() :ArrayList<String>
	{
		val retur = ArrayList<String>()
		retur.add("free_upkeep")
		retur.add("income_bonus")
		retur.add("trade_base_income_bonus")
		retur.add("trade_level_bonus")
		retur.add("happiness_bonus")
		retur.add("law_bonus")
		retur.add("population_loyalty_bonus")
		retur.add("recruits_exp_bonus")
		retur.add("recruits_morale_bonus")
		retur.add("recruitment_cost_bonus_naval")
		retur.add("construction_cost_bonus_defensive")
		retur.add("construction_cost_bonus_religious")
		retur.add("construction_cost_bonus_stone")
		retur.add("construction_cost_bonus_wooden")
		retur.add("construction_cost_bonus_other")
		return retur
	}

	private fun agentRelatedCapabilities() :ArrayList<String>
	{
		val retur = ArrayList<String>()
		retur.add("agent")
		retur.add("agent_limit")
		return retur
	}
}