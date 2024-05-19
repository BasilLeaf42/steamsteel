package processing

import data.CharacterNameReferenceRecord
import data.code.script.EventCounterEntry
import data.common.DuplicateCount
import data.common.IntegerValuedReferenceRecord
import data.common.SimpleReferenceRecord
import data.common.UsageTrackedName
import data.strat.FactionCharacterNames
import data.strat.MapCharacter
import data.unit.ModelDbEntry
import main.BovineM2twCheck
import util.StringUtil
import util.Util
import java.io.File

class Script(private val main :BovineM2twCheck)
{
	fun checkAll()
	{
		characters()
		namesAndLabels()
		eventsAndCounters()
		otherScriptChecks()
	}

	private fun characters()
	{
		for(character in main.data.code.scriptedCharacters)
		{
			if(character.battleModel.isNotEmpty())
			{
				val battleModel :ModelDbEntry? = main.data.unit.battleModels[character.battleModel, true]
				if(battleModel == null)
					main.writeScriptLog(character.filename, character.lineNumber, """Reference to non-existent battle model "${character.battleModel}".""")
			}
			if(character.stratModel != null)
			{
				val stratModel = main.data.strat.stratModels[character.stratModel, true]
				if(stratModel == null)
					main.writeScriptLog(character.filename, character.lineNumber, """Reference to non-existent strat model "${character.stratModel}".""")
			}
			if(main.data.strat.factionEntries[character.ownerFaction] == null)
				main.writeScriptLog(character.filename, character.lineNumber, "Character has owner faction ${character.ownerFaction} which does not exist.")
			if(character.subFaction != null && main.data.strat.factionEntries[character.subFaction!!] == null)
				main.writeScriptLog(character.filename, character.lineNumber, "Character has sub faction ${character.subFaction} which does not exist.")
			if(main.data.unit.findCharacterType(character.ownerFaction, character.type) == null)
				main.writeScriptLog(character.filename, character.lineNumber, "Character has unrecognized type ${character.type} for faction ${character.ownerFaction}.")
			if(!character.hasMatchingGender())
				main.writeScriptLog(character.filename, character.lineNumber, "Character does not have gender matching its type.")
		}
	}

	private fun eventsAndCounters()
	{
		for(declaredCounter in main.data.code.declaredCounters.getAll())
		{
			if(declaredCounter.setLocations.size > 0)
			{
				var setToValue = false
				for(setLocation :IntegerValuedReferenceRecord in declaredCounter.setLocations)
				{
					if(setLocation.value != "0")
					{
						setToValue = true
						break
					}
				}
				if(!setToValue)
					main.writeScriptLog("Declared counter ${declaredCounter.name} is set at ${declaredCounter.setLocations.size} locations, but never to anything other than 0.")
			}
			if(declaredCounter.declaredLocations.size > 1)
			{
				var report = "Declared counter ${declaredCounter.name} is declared more than once: "
				for(location in declaredCounter.declaredLocations)
				{
					report += "${location.filename}:${location.lineNumber} "
				}
				main.writeScriptLog(report)
			}
			if(declaredCounter.setLocations.size == 0)
			{
				when
				{
					declaredCounter.checkedLocations.size == 0 ->
						main.writeScriptLog("""${declaredCounter.declaredLocations[0].filename} ${declaredCounter.declaredLocations[0].lineNumber}: Declared counter "${declaredCounter.name}" is declared but never set or checked.""")
					declaredCounter.declaredLocations.size == 0 ->
						main.writeScriptLog("""Declared counter "${declaredCounter.name}" is checked but neither declared nor set.""")
					else ->
						main.writeScriptLog("""${declaredCounter.declaredLocations[0].filename} ${declaredCounter.declaredLocations[0].lineNumber}: Declared counter "${declaredCounter.name}" is declared and checked but never set.""")
				}
			}
			else if(declaredCounter.checkedLocations.size == 0)
			{
				if(declaredCounter.declaredLocations.size == 0)
					main.writeScriptLog("""Declared counter "${declaredCounter.name}" is set but neither declared nor checked.""")
				else
					main.writeScriptLog("""${declaredCounter.declaredLocations[0].filename} ${declaredCounter.declaredLocations[0].lineNumber}: Declared counter "${declaredCounter.name}" is declared and set but never checked.""")
			}
			else if(declaredCounter.declaredLocations.size == 0)
				main.writeScriptLog("""Declared counter "${declaredCounter.name}" is set and checked but lacks declaration.""")
			else
			{
				val declaredAtLine = declaredCounter.declaredLocations[0]
				for(setLocation in declaredCounter.setLocations)
				{
					if(declaredAtLine.filename == setLocation.filename && declaredAtLine.lineNumber > setLocation.lineNumber)
						main.writeScriptLog("""${setLocation.filename} ${setLocation.lineNumber}: Declared counter "${declaredCounter.name}" is set before being declared (${declaredAtLine.filename}:${declaredAtLine.lineNumber}).""")
				}
				for(checkedLocation in declaredCounter.checkedLocations)
				{
					if(declaredAtLine.filename == checkedLocation.filename && declaredAtLine.lineNumber > checkedLocation.lineNumber)
						main.writeScriptLog("""${checkedLocation.filename} ${checkedLocation.lineNumber}: Declared counter "${declaredCounter.name}" is checked before being declared (${declaredAtLine.filename}:${declaredAtLine.lineNumber}).""")
				}
			}
		}

		for(eventCounter in main.data.code.eventCounters.getAll())
		{
			if(eventCounter.setLocations.size > 0 && eventCounter.checkedLocations.size == 0)
			{
				if(!Util.equalsAny(eventCounter.name, "disable_no_brigands", "disable_no_pirates") && !eventCounter.isHistoric)
					main.writeScriptLog("""${eventCounter.filename} ${eventCounter.lineNumber}: Event counter "${eventCounter.name}" is set but never checked.""")
			}
			if(eventCounter.checkedLocations.size > 0 && eventCounter.setLocations.size == 0)
			{
				if(!Util.equalsAny(eventCounter.name, "disable_no_brigands", "disable_no_pirates", "dummy"))
				{
					for(reference in eventCounter.checkedLocations)
						main.writeScriptLog("""${reference.filename} ${reference.lineNumber}: Event counter "${eventCounter.name}" is checked but never set.""")
				}
			}
			if(main.data.code.declaredCounters[eventCounter.name, false] != null)
			{
				var location :String? = null
				when
				{
					eventCounter.filename != null ->
						location = "${eventCounter.filename} ${eventCounter.lineNumber}"
					eventCounter.setLocations.size > 0 ->
						location = "${eventCounter.setLocations[0].filename} ${eventCounter.setLocations[0].lineNumber}"
					eventCounter.checkedLocations.size > 0 ->
						location = "${eventCounter.checkedLocations[0].filename} ${eventCounter.checkedLocations[0].lineNumber}"
				}
				main.writeScriptLog("""$location: Event counter "${eventCounter.name}" is also a declared counter. This indicates an unintentional mixup of syntax for event counters and declared counters. You should decide whether this should be a declared counter or an event counter.""")
			}
		}

		for(historicEvent :EventCounterEntry in main.data.code.getHistoricEvents())
		{
			if(main.data.text.historicEventNames[historicEvent.name, true] == null)
				main.writeScriptLog("""Historic event "${historicEvent.name}" lacks title text. It is set and/or checked at these locations: ${historicEvent.locationsEnumerated()}""")
			if(main.data.text.historicEventDescriptions[historicEvent.name, true] == null)
				main.writeScriptLog("""Historic event "${historicEvent.name}" lacks description text. It is set and/or checked at these locations: ${historicEvent.locationsEnumerated()}""")
		}

		for(historicEventName :UsageTrackedName in main.data.text.historicEventNames.getAll())
		{
			if(main.data.text.historicEventDescriptions[historicEventName.name, false] == null)
				main.writeScriptLog("""Historic event "$historicEventName" has only title, not description.""")
			val event :EventCounterEntry? = main.data.code.eventCounters[historicEventName.name, false]
			if(event == null || event.setLocations.size == 0)
				main.writeScriptLog("""Historic event "${historicEventName.name}" is never triggered in the script.""")
		}

		for(dupe :DuplicateCount in main.data.text.historicEventNames.getDuplicates())
		{
			main.writeScriptLog("""Historic event "${dupe.name}" has its title duplicated (${dupe.count} times).""")
		}
		for(dupe :DuplicateCount in main.data.text.historicEventDescriptions.getDuplicates())
		{
			main.writeScriptLog("""Historic event "${dupe.name}" has its description duplicated (${dupe.count} times).""")
		}

		for(historicEventName :UsageTrackedName in main.data.text.historicEventDescriptions.getAll())
		{
			if(main.data.text.historicEventNames[historicEventName.name, false] == null)
				main.writeScriptLog("Historic event \"$historicEventName\" has only description, not title.")
		}
	}

	private fun namesAndLabels()
	{
		for(character :MapCharacter in main.data.code.scriptedCharacters)
		{
			val nameTokens = StringUtil.split(character.name, " ")
			if(nameTokens.size > 2)
				main.writeScriptLog("${character.filename} ${character.lineNumber}: Character's name has more than two pieces - first name, last name, ???.")
			else if(character.name != "random_name")
			{
				var faction = character.ownerFaction
//Seems the name is always pointing to the owner faction
//				if(character.subFaction != null)
//					faction = character.subFaction!!
				val factionNames :FactionCharacterNames? = main.data.strat.names[faction]
				when
				{
					factionNames == null ->
						main.writeScriptLog("${character.filename} ${character.lineNumber}: Character of faction $faction cannot have name checked, cannot find any names defined for that faction! Wrong faction?")
					character.isFemale && factionNames.womenNames.contains(nameTokens[0]) ->
						Util.noop()
					!character.isFemale && factionNames.characterNames.contains(nameTokens[0]) ->
						Util.noop()
					character.isFemale ->
						main.writeScriptLog(character.filename, character.lineNumber, "First name ${nameTokens[0]} is not defined in women names for its faction $faction.")
					else ->
						main.writeScriptLog("${character.filename} ${character.lineNumber}: First name ${nameTokens[0]} is not defined in male names for its faction $faction.")
				}
				if(factionNames != null && nameTokens.size > 1 && !factionNames.characterSurnames.contains(nameTokens[1]))
					main.writeScriptLog("${character.filename} ${character.lineNumber}: Surname ${nameTokens[1]} is not defined in surnames for its faction $faction.")
			}
		}

		for(nameReference :CharacterNameReferenceRecord in main.data.code.characterNameReferences)
		{
			var found = false
			for(character in main.data.strat.mapCharacters)
			{
				if(character.name == nameReference.reference)
				{
					found = true
					break
				}
			}
			if(!found)
			{
				for(character in main.data.code.scriptedCharacters)
				{
					if(character.name == nameReference.reference)
					{
						found = true
						break
					}
				}
			}
			if(!found)
				main.writeScriptLog(nameReference.filename, nameReference.lineNumber, "Character name reference to \"${nameReference.reference}\", which is not a starting character or scripted character.")
		}

		//Search both labels and single name character names, as both are reachable like this.
		for(labelReference :SimpleReferenceRecord in main.data.code.labelReferences)
		{
			var found = false
			for(character in main.data.strat.mapCharacters)
			{
				if(Util.equalsAny(labelReference.reference, character.label, character.name))
				{
					found = true
					break
				}
			}
			if(!found)
			{
				for(character in main.data.code.scriptedCharacters)
				{
					if(Util.equalsAny(labelReference.reference, character.label, character.name))
					{
						found = true
						break
					}
				}
			}
			if(!found)
				main.writeScriptLog(labelReference.filename, labelReference.lineNumber, "Character label reference to \"${labelReference.reference}\", which is not a label given to any starting character or scripted character.")
		}
	}

	private fun otherScriptChecks()
	{
		for(unitReference in main.data.code.unitReferences)
		{
			if(main.data.unit.eduEntries[unitReference.reference] == null)
				main.writeScriptLog("""${unitReference.filename} ${unitReference.lineNumber}: Unit reference "${unitReference.reference}" does not exist.""")
		}

		for(reference in main.data.code.scriptTraitReferences)
		{
			val trait = main.data.code.traits[reference.reference, reference.referencedLevel != -1]
			if(trait == null)
				main.writeScriptLog("${reference.filename} ${reference.lineNumber}: Reference to nonexistent trait ${reference.reference}")
			else
			{
				if(reference.awardedAmount != null)
					trait.isAwarded = true
				if(reference.referencedLevel != -1)
				{
					trait.isTested = true
					if(reference.referencedLevel > trait.traitLevels.size)
						main.writeScriptLog("${reference.filename} ${reference.lineNumber}: Test for trait level ${reference.referencedLevel}, ${trait.name} has only ${trait.traitLevels.size} levels.")
				}
			}
		}
	}

	fun listUnused()
	{
		for(unusedAdvice in main.data.code.adviceThreads.getUnused())
			main.writeScriptLog("Advice thread \"" + unusedAdvice.name + "\" is never invoked.")

		val showMeFolder = File(main.runCfg.dataFolder + "scripts/show_me")
		if(showMeFolder.exists())
		{
			val showMeContents = showMeFolder.listFiles()
			if(showMeContents != null)
			{
				for(scriptFile in showMeContents)
				{
					val fileName = StringUtil.standardize(scriptFile.name)
					var isUsed = false
					for(customScript in main.data.code.customScripts)
					{
						if(customScript.endsWith(fileName))
							isUsed = true
					}
					if(!isUsed)
						main.writeScriptLog("Advice script file \"" + scriptFile.name + "\" is not invoked by any advice threads.")
				}
			}
		}
	}
}