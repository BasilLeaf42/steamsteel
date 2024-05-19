package sources.code

import data.CharacterNameReferenceRecord
import data.common.SimpleReferenceRecord
import data.code.script.EventCounterEntry
import data.code.trait.TraitReferenceRecord
import data.common.IntegerValuedReferenceRecord
import main.BovineM2twCheck
import sources.shared.MapCharacterParsing
import sources.shared.SharedDefinitions.simpleScriptEventTypes
import util.StringUtil
import util.Util
import java.io.BufferedReader
import java.io.File
import java.io.FileNotFoundException
import java.io.FileReader

class ScriptReader(val main :BovineM2twCheck)
{
	fun loadScripts()
	{
		loadScript(main.runCfg.stratFolder + "campaign_script.txt", "CS", false)

		val battlesFolder = File(main.runCfg.dataFolder + "world/maps/battle/custom")
		if(battlesFolder.exists())
		{
			val files :Array<File>? = battlesFolder.listFiles()
			if(files != null)
			{
				for(battleFolder in files)
				{
					if(battleFolder.isDirectory)
					{
						loadScript(battleFolder.absolutePath + "/descr_battle.txt", "Battle " + battleFolder.name, true)
					}
				}
			}
		}
	}

	private fun loadScript(filename :String, fileIdentifier :String, missingFileIsOk :Boolean)
	{
		var readLine :String? = null
		var lineNumber = 0
		try
		{
			main.writeOutput("Loading script $filename")
			val scriptFile = BufferedReader(FileReader(filename))
			var currentFaction :String? = null
			var currentSubFaction :String? = null
			var battleSectionStarted = false
			while(run { readLine = scriptFile.readLine(); readLine} != null)
			{
				lineNumber++
				//Ignore case, starting whitespace, multiple spaces and comments
				var line = StringUtil.standardize(readLine!!)
				if(line.startsWith("log "))
					continue
				line = line.replace(" , ", ", ")
				val tokens :Array<String> = StringUtil.split(line, " ")

				//Recognize factions
				if(tokens[0] == "faction")
				{
					currentFaction = tokens[1].replace(",", "")
					currentSubFaction = null
					main.data.code.factionReferences.add(SimpleReferenceRecord(currentFaction, filename, lineNumber))
					if(tokens.size > 3)
					{
						currentSubFaction = tokens[3]
						main.data.code.factionReferences.add(SimpleReferenceRecord(currentSubFaction, filename, lineNumber))
					}
					continue
				}
				if(tokens[0] == "spawn_character")
				{
					main.data.code.factionReferences.add(SimpleReferenceRecord(tokens[1], filename, lineNumber))
				}

				//Recognize when the battle section has started in historic battle scripts, for different processing of stuff before it
				for(i in tokens.indices)
				{
					if(!battleSectionStarted && Util.equalsAny(tokens[i], "battle_time", "weather", "home_faction", "deployment_area_point"))
						battleSectionStarted = true
				}

				findTraitReferences(fileIdentifier, lineNumber, tokens)
				findCounterReferences(fileIdentifier, lineNumber, tokens)
				findBuildingReferences(fileIdentifier, lineNumber, tokens)
				findUnitReferences(fileIdentifier, lineNumber, tokens, battleSectionStarted)
				findCharactersAndLabels(fileIdentifier, lineNumber, line, tokens, currentFaction, currentSubFaction)

				if(tokens[0] == "advance_advice_thread")
					Util.addIfNotPresent(tokens[1], main.data.code.scriptInvokedAdvice)

			}
			scriptFile.close()
		}
		catch(e :FileNotFoundException)
		{
			if(!missingFileIsOk)
				main.writeOutput("Cannot find script $filename. Are you sure you provided the correct location for the data/strat folders?")
		}
		catch(e :Exception)
		{
			main.fatalParsingError(lineNumber, readLine!!, e)
		}
	}

	private fun findCharactersAndLabels(filename :String, lineNumber :Int, line :String, tokens :Array<String>, currentFaction :String?, currentSubFaction :String?)
	{
		if(Util.equalsAny(tokens[0], "move", "siege_settlement"))
		{
			val name = StringUtil.between(line, "${tokens[0]} ", ",")
			if(name != "this")
				main.data.code.labelReferences.add(SimpleReferenceRecord(name!!, filename, lineNumber))
		}
		if(tokens[0] == "console_command" && Util.equalsAny(tokens[1], "kill_character", "move_character", "give_trait", "give_ancillary", "remove_trait"))
		{
			if(!tokens[2].startsWith("\""))
			{
				if(tokens[2] != "this")
					main.data.code.labelReferences.add(SimpleReferenceRecord(tokens[2], filename, lineNumber))
			}
			else
			{
				var characterName :String = tokens[2]
				var hyphenCount = StringUtil.patternCountInString(characterName, "\"")
				if(hyphenCount != 2)
				{
					for(i :Int in 3 until tokens.size)
					{
						characterName = "$characterName ${tokens[i]}"
						hyphenCount = StringUtil.patternCountInString(characterName, "\"")
						if(hyphenCount >= 2)
							break
					}
				}
				if(hyphenCount != 2)
					main.writeSundryLog("$filename $lineNumber: encountered unclosed hyphens or too many hyphens in character name: $line")
				else
				{
					characterName = characterName.replace("\"", "")
					main.data.code.characterNameReferences.add(CharacterNameReferenceRecord(characterName, filename, lineNumber, null, null))
					val nameTokens = StringUtil.split(characterName, " ")
					if(nameTokens.size > 2)
						main.writeScriptLog("$filename $lineNumber: Encountered a character name reference with more than two pieces (first name, last name, ???): $line")
				}
			}
		}

		if(tokens[0] == "character")
		{
			val character = MapCharacterParsing.createCharacter(currentFaction!!, filename, lineNumber, StringUtil.after(line, "character "), true)
			if(character.subFaction == null)
				character.subFaction = currentSubFaction
			main.data.code.scriptedCharacters.add(character)
		}

		if(tokens[0] == "spawn_character")
		{
			val faction :String = tokens[1]
			val character = MapCharacterParsing.createCharacter(faction, filename, lineNumber, StringUtil.after(line, "spawn_character $faction "), true)
			main.data.code.scriptedCharacters.add(character)
		}

		for(i in tokens.indices)
		{
			if(tokens[i] == "i_characterexists")
				main.data.code.labelReferences.add(SimpleReferenceRecord(tokens[i + 1], filename, lineNumber))
		}
	}

	private fun findUnitReferences(fileIdentifier :String, lineNumber :Int, tokens :Array<String>, battleSectionStarted :Boolean)
	{
		if(Util.equalsAny(tokens[0], "inc_recruit_pool", "set_recruit_pool"))
		{
			var unitName = ""
			for(i in 3 until tokens.size)
			{
				if(tokens[i] != "")
					unitName += " " + tokens[i]
			}
			while(unitName.startsWith(" "))
				unitName = unitName.substring(1)
			main.data.code.unitReferences.add(SimpleReferenceRecord(unitName, fileIdentifier, lineNumber))
		}

		if(tokens[0] == "unit" && !battleSectionStarted)
		{
			var unitName = ""
			for(i in 1 until tokens.size)
			{
				if(Util.equalsAny(tokens[i], "exp", "soldiers", "num"))
				{
					while(unitName.startsWith(" "))
						unitName = unitName.substring(1)
					break
				}
				unitName += " " + tokens[i]
			}
			main.data.code.unitReferences.add(SimpleReferenceRecord(unitName, fileIdentifier, lineNumber))
		}

		for(i in tokens.indices)
		{
			if(Util.equalsAny(tokens[i], "unittype", "i_unittypeselected", "adviserecruit"))
			{
				var unitName = ""
				for(j in i + 1 until tokens.size)
				{
					if(tokens[j] != "")
						unitName += tokens[j] + " "
				}
				unitName = unitName.substring(0, unitName.length - 1)
				main.data.code.unitReferences.add(SimpleReferenceRecord(unitName, fileIdentifier, lineNumber))
			}
		}

		if(tokens[0] == "console_command" && tokens[1] == "create_unit")
		{
			var lastCharacterNameToken = 2
			var quoteCount = 0
			for(i in 2 until tokens.size)
			{
				quoteCount += StringUtil.patternCountInString(tokens[i], "\"")
				if(quoteCount % 2 == 0)
				{
					lastCharacterNameToken = i
					break
				}
			}
			var unitName = ""
			for(i in lastCharacterNameToken + 1 until tokens.size)
			{
				unitName += " " + tokens[i]
				quoteCount += StringUtil.patternCountInString(tokens[i], "\"")
				if(quoteCount % 2 == 0)
				{
					unitName = unitName.replace("\"", "")
					while(unitName.startsWith(" "))
						unitName = unitName.substring(1)
					break
				}
			}
			main.data.code.unitReferences.add(SimpleReferenceRecord(unitName, fileIdentifier, lineNumber))
		}
	}

	private fun findBuildingReferences(fileIdentifier :String, lineNumber :Int, tokens :Array<String>)
	{
		for(i in tokens.indices)
		{
			if(tokens[i] == "create_building")
				main.data.code.buildingLevelReferences.add(SimpleReferenceRecord(tokens[i + 2], fileIdentifier, lineNumber))
			if(tokens[i] == "settlementbuildingexists")
				main.data.code.buildingLevelReferences.add(SimpleReferenceRecord(tokens[i + 2], fileIdentifier, lineNumber))
			if(tokens[i] == "buildingname")
				main.data.code.buildingLevelReferences.add(SimpleReferenceRecord(tokens[i + 2], fileIdentifier, lineNumber))
			if(tokens[i] == "numbuildingscompletedfaction")
				main.data.code.buildingLevelReferences.add(SimpleReferenceRecord(tokens[i + 1], fileIdentifier, lineNumber))
			if(tokens[i] == "settlementbuildingfinished")
				main.data.code.buildingLevelReferences.add(SimpleReferenceRecord(tokens[i + 2], fileIdentifier, lineNumber))
			if(tokens[i] == "destroy_buildings")
				main.data.code.buildingLevelReferences.add(SimpleReferenceRecord(tokens[i + 2], fileIdentifier, lineNumber))
			if(tokens[i] == "set_building_health")
				main.data.code.buildingLevelReferences.add(SimpleReferenceRecord(tokens[i + 2], fileIdentifier, lineNumber))
		}
	}

	private fun findCounterReferences(fileIdentifier :String, lineNumber :Int, tokens :Array<String>)
	{
		if(tokens[0] == "historic_event")
		{
			main.data.code.addSetEventCounterLocation(SimpleReferenceRecord(tokens[1], fileIdentifier, lineNumber))
			val historicEvent :EventCounterEntry = main.data.code.eventCounters[tokens[1], false]!!
			historicEvent.isHistoric = true
			if(tokens.size > 2 && tokens[2] == "true")
				historicEvent.isDecision = true
		}
		val simpleEventTypes = simpleScriptEventTypes()
		if(tokens[0] == "event" && simpleEventTypes.contains(tokens[1]))
		{
			if(tokens[1] == "counter")
				main.data.code.addSetEventCounterLocation(SimpleReferenceRecord(tokens[2], fileIdentifier, lineNumber))
			else if(tokens.size > 2)
			{
				var historicEvent :EventCounterEntry? = main.data.code.eventCounters[tokens[2], false]
				if(historicEvent == null)
				{
					historicEvent = EventCounterEntry(tokens[2], fileIdentifier, lineNumber)
					historicEvent.isUsed = true
					historicEvent.isHistoric = true
					main.data.code.eventCounters.add(historicEvent)
				}
				if(tokens.size > 3 && tokens[3] == "true")
					historicEvent.isDecision = true
				historicEvent.setLocations.add(SimpleReferenceRecord(tokens[2], fileIdentifier, lineNumber))
			}
		}
		if(tokens[0] == "event" && tokens[1] == "emergent_faction")
		{
			val fullEventName = "the_" + tokens[2] + "_emerge"
			val event = EventCounterEntry(fullEventName, fileIdentifier, lineNumber)
			event.isUsed = true
			event.isHistoric = true
			main.data.code.eventCounters.add(event)
		}
		if(tokens[0] == "set_event_counter")
			main.data.code.addSetEventCounterLocation(SimpleReferenceRecord(tokens[1], fileIdentifier, lineNumber))
		if(tokens[0] == "generate_random_counter")
			main.data.code.addSetEventCounterLocation(SimpleReferenceRecord(tokens[1], fileIdentifier, lineNumber))
		if(tokens[0] == "inc_event_counter")
			main.data.code.addSetEventCounterLocation(SimpleReferenceRecord(tokens[1], fileIdentifier, lineNumber))
		if(tokens[0] == "monitor_event" && tokens[1] == "eventcounter" && tokens[2] == "eventcountertype")
			main.data.code.addCheckedEventCounterLocation(SimpleReferenceRecord(tokens[3], fileIdentifier, lineNumber))
		if(tokens[0] == "declare_counter")
			main.data.code.addDeclaredCounter(SimpleReferenceRecord(tokens[1], fileIdentifier, lineNumber))
		if(tokens[0] == "log_counter")
			main.data.code.addCheckedDeclaredCounterLocation(SimpleReferenceRecord(tokens[1], fileIdentifier, lineNumber))
		if(Util.equalsAny(tokens[0], "inc_counter", "set_counter"))
			main.data.code.addSetDeclaredCounterLocation(IntegerValuedReferenceRecord(tokens[1], fileIdentifier, lineNumber, tokens[2]))
		for(i in tokens.indices)
		{
			if(tokens[i] == "i_comparecounter")
				main.data.code.addCheckedDeclaredCounterLocation(SimpleReferenceRecord(tokens[i + 1], fileIdentifier, lineNumber))
			if(tokens[i] == "i_eventcounter")
				main.data.code.addCheckedEventCounterLocation(SimpleReferenceRecord(tokens[i + 1], fileIdentifier, lineNumber))
		}
	}

	private fun findTraitReferences(fileIdentifier :String, lineNumber :Int, tokens :Array<String>)
	{
		for(i in tokens.indices)
		{
			if(tokens[i] == "give_trait")
			{
				var lastCharacterNamePosition = i + 1
				val hyphenCount = StringUtil.patternCountInString(tokens[lastCharacterNamePosition], "\"")
				if(hyphenCount == 1)
				{
					while(lastCharacterNamePosition < tokens.size && !tokens[lastCharacterNamePosition].contains("\""))
						lastCharacterNamePosition++
					lastCharacterNamePosition++
				}
				val traitNamePosition = lastCharacterNamePosition + 1
				val awardedTrait = tokens[traitNamePosition]
				main.data.code.scriptTraitReferences.add(TraitReferenceRecord(fileIdentifier, lineNumber, awardedTrait, 1, tokens[traitNamePosition + 1]))
//				checkTraitReference(fileIdentifier, lineNumber, awardedTrait, "Attempt to award non-existent trait \"%TRAIT%\"", 1, true)
			}
			else if(tokens[i] == "traits")
			{
				for(j in i + 1 until tokens.size)
				{
					tokens[j] = tokens[j].replace(",", "")
					if(tokens[j].matches("[0-9]+".toRegex()) || tokens[j] == "")
						continue
					else
					{
						if(!tokens[j + 1].matches("[0-9]+".toRegex()))
							tokens[j + 1] = tokens[j + 1].replace(",", "")
						val awardedTrait = tokens[j]
						main.data.code.scriptTraitReferences.add(TraitReferenceRecord(fileIdentifier, lineNumber, awardedTrait, 1, tokens[j + 1]))
//						checkTraitReference(fileIdentifier, lineNumber, awardedTrait, "Attempt to award non-existent trait \"%TRAIT%\"", 1, true)
					}
				}
			}
			else if(tokens[i] == "trait" || tokens[i] == "fathertrait")
			{
				val checkedTrait = tokens[i + 1]
				val level :Int = getReferencedTraitLevel(tokens, i + 1)
				main.data.code.scriptTraitReferences.add(TraitReferenceRecord(fileIdentifier, lineNumber, checkedTrait, level))
//				checkTraitReference(fileIdentifier, lineNumber, checkedTrait, "Monitor is checking non-existent trait \"%TRAIT%\"", level, false)
			}
		}
	}

	private fun getReferencedTraitLevel(tokens :Array<String>, traitNameTokenIndex :Int) :Int
	{
		val operator = tokens[traitNameTokenIndex + 1]
		var level = tokens[traitNameTokenIndex + 2].toInt()
		if(operator == ">")
			level++
		else if(operator == "<")
			level--
		return level
	}

	fun loadCustomScripts()
	{
		for(customScript in main.data.code.customScripts)
		{
			val scriptFile = File(main.runCfg.dataFolder + customScript)
			if(scriptFile.exists())
				loadScript(main.runCfg.dataFolder + customScript, customScript.substring(customScript.lastIndexOf("/") + 1), false)
			else
				main.writeScriptLog("Advice refers to script \"$customScript\", which does not exist.")
		}
	}
}