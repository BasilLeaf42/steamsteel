package sources.code

import data.common.SimpleReferenceRecord
import data.code.trait.TraitReferenceRecord
import main.BovineM2twCheck
import util.StringUtil
import java.io.*

class AncillaryReader(private val main :BovineM2twCheck)
{
	fun readAll()
	{
		readAncillaries()
	}

	private fun readAncillaries()
	{
		val filename = "export_descr_ancillaries.txt"
		var readLine :String? = null
		var lineNumber = 0
		try
		{
			main.writeOutput(filename)
			val inputFile = BufferedReader(FileReader(main.runCfg.dataFolder + filename))
			var content :String
			var affectsCounter = 0
			var currentTriggerName :String? = null
			while(run { readLine = inputFile.readLine(); readLine } != null)
			{
				lineNumber++
				val line :String = StringUtil.standardize(readLine!!)
				val tokens = StringUtil.split(line, " ")
				for(i in tokens.indices)
				{
					when(tokens[i])
					{
						"settlementbuildingexists" ->
							main.data.code.buildingLevelReferences.add(SimpleReferenceRecord(tokens[i + 2], filename, lineNumber))
						"governorbuildingexists" ->
							main.data.code.buildingLevelReferences.add(SimpleReferenceRecord(tokens[i + 2], filename, lineNumber))
						"buildingfinishedbygovernor" ->
							main.data.code.buildingLevelReferences.add(SimpleReferenceRecord(tokens[i + 2], filename, lineNumber))
						"i_eventcounter" ->
							main.data.code.addCheckedEventCounterLocation(SimpleReferenceRecord(tokens[i + 1], filename, lineNumber))
					}
				}
				if(line.startsWith("ancillary"))
				{
					content = tokens[1]
					if(main.data.code.ancillaryNames.contains(content))
						main.writeEdaLog("EDA $lineNumber: Duplicate ancillary \"$content\"")
					else
						main.data.code.ancillaryNames.add(content)
				}
				if(line.startsWith("trigger"))
				{
					if(affectsCounter > 10) main.writeEdaLog("EDA: Trigger $currentTriggerName has too many Affects clauses ($affectsCounter), max is 10")
					affectsCounter = 0
					currentTriggerName = tokens[1]
					if(main.data.code.edaTriggers.contains(currentTriggerName) || main.data.code.traitTriggers[currentTriggerName, false] != null)
						main.writeEdaLog("EDA $lineNumber: Duplicate trigger \"$currentTriggerName\"")
					else
						main.data.code.edaTriggers.add(currentTriggerName)
				}
				if(line.startsWith("ancillary") ||
					line.startsWith("description") ||
					line.startsWith("effectsdescription"))
				{
					content = tokens[1]
					//TODO move to tests
					if(main.data.text.ancillaryDescriptions[content, true] == null)
						main.writeEdaLog("EDA $lineNumber: Ancillary description \"$content\" is missing in export_ancillaries")
				}
				if(line.startsWith("affects"))
				{
					affectsCounter++
					val awardedTrait = tokens[1]
					main.data.code.edaTraitReferences.add(TraitReferenceRecord(filename, lineNumber, awardedTrait, 1, tokens[2]))
//					checkTraitReference("EDA", lineNumber, awardedTrait, "Attempt to award non-existent trait \"%TRAIT%\"", 1, true)
				}
				if(line.contains(" trait ") ||
					line.contains(" fathertrait "))
				{
					var traitNamePosition = 0
					for(token in tokens)
					{
						traitNamePosition++
						if(token == "trait" || token == "fathertrait") break
					}
					val checkedTrait = tokens[traitNamePosition]
					val level :Int = getReferencedTraitLevel(tokens, traitNamePosition)
					main.data.code.edaTraitReferences.add(TraitReferenceRecord(filename, lineNumber, checkedTrait, level))
//					checkTraitReference("EDA", lineNumber, checkedTrait, "Checking for non-existent trait \"%TRAIT%\"", level, false)
				}
			}
			inputFile.close()
		}
		catch (e :FileNotFoundException)
		{
			main.writeOutput("Cannot find the EDA file (" + main.runCfg.dataFolder + "export_descr_ancillaries.txt)")
			main.writeOutput("No checks have been performed on the ancillaries.")
			main.writeOutput("This is okay if you are ONLY using vanilla ancillaries, if not you may have entered your mod's data folder wrong.")
			return
		}
		catch (e :Exception)
		{
			main.fatalParsingError(lineNumber, readLine!!, e)
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
}