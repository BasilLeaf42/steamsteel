package sources.stratmap

import data.common.SimpleReferenceRecord
import data.common.FileReferenceRecord
import data.strat.culture.CultureEntry
import data.strat.culture.CultureSettlementLevel
import main.BovineM2twCheck
import util.CasUtil
import util.StringUtil
import util.Util
import java.io.BufferedReader
import java.io.File
import java.io.FileNotFoundException
import java.io.FileReader
import java.util.*

class CultureReader(private val main :BovineM2twCheck)
{
	private val agentDirectives by lazy { agentDirectives()}

	fun readCultures()
	{
		val filename = "descr_cultures.txt"
		var readLine :String? = null
		var lineNumber = 0
		try
		{
			main.writeOutput(filename)
			val cultureReader = BufferedReader(FileReader(main.runCfg.dataFolder + filename))
			var settlementLevelsActive = false
			var settlementLevelActive = false
			var activeCulture :CultureEntry? = null
			var activeLevel :CultureSettlementLevel? = null
			while(run { readLine = cultureReader.readLine(); readLine} != null)
			{
				var line :String = StringUtil.standardize(readLine!!)
				lineNumber++
				if(line.startsWith("{"))
				{
					if(!settlementLevelsActive)
						settlementLevelsActive = true
					else if(!settlementLevelActive)
						settlementLevelActive = true
					else
						main.writeStratmapLog(filename, lineNumber, "Parsing error: Opening brace encountered, but settlement levels and settlement level is already active!")
					line = line.substring(1)
				}
				if(line.startsWith("}"))
				{
					when
					{
						settlementLevelActive ->
							settlementLevelActive = false
						settlementLevelsActive ->
							settlementLevelsActive = false
						else ->
							main.writeStratmapLog(filename, lineNumber, "Parsing error: Closing brace encountered, but neither settlement levels or settlement level is active!")
					}
					line = line.substring(1)
				}
				if(line == "")
					continue
				val tokens = StringUtil.split(line, " ")

				//Assignments not culture specific
				if(!settlementLevelActive && !settlementLevelsActive && activeCulture == null)
				{
					if(line.startsWith("symbol"))
						main.data.fileReferencesForCrossCheck.add(FileReferenceRecord(filename, lineNumber, "symbol", tokens[1]))
					if(line.startsWith("siege"))
						main.data.fileReferencesForCrossCheck.add(FileReferenceRecord(filename, lineNumber, "siege", tokens[1]))
					if(line.startsWith("blockade"))
						main.data.fileReferencesForCrossCheck.add(FileReferenceRecord(filename, lineNumber, "blockade", tokens[1]))
				}
				if(settlementLevelsActive && !settlementLevelActive)
				{
					activeLevel = CultureSettlementLevel()
					activeLevel.name = tokens[0]
					//data/ui/<culture name>/cities/<culture name>_<settlement level>.tga
					val buildingCardFile = "ui/" + activeCulture!!.name + "/cities/" + activeCulture.name + "_" + activeLevel.name + ".tga"
					main.data.fileReferencesForCrossCheck.add(FileReferenceRecord(filename, lineNumber, activeCulture.name + "'s settlement level " + activeLevel.name, buildingCardFile))
					activeCulture.settlementLevels.add(activeLevel)
				}
				else if(settlementLevelsActive && settlementLevelActive)
				{
					if(tokens[0] == "normal")
					{
						val modelFile = tokens[1].replace(",", "")
						main.data.fileReferencesForCrossCheck.add(FileReferenceRecord(filename, lineNumber, activeLevel!!.name, modelFile))
						val textures = CasUtil.getCasFileTextures(modelFile.replace("data/", ""), true)
						if(textures.size == 0 && !main.lists.vanillaFiles.contains(modelFile.replace("data/", "")))
						{
							if(File(main.runCfg.dataFolder + modelFile.replace("data/", "")).exists())
								main.writeOutput("Found no textures in settlement model $modelFile. This means the checker probably is lacking code to recognize its textures.")
						}
						for(texture in textures)
							main.data.fileReferencesForCrossCheck.add(FileReferenceRecord(filename, lineNumber, activeLevel.name + "'s model file " + modelFile, texture, null, arrayOf(".dds")))
						activeLevel.settlementLevelReference = tokens[2]
					}
					else if(tokens[0] == "card")
						//These references are not used in the game. Instead, the game reads from a path determined in code - here added as file reference upon encountering the settlement level
						//main.data.fileReferencesForCrossCheck.add(new FileReferenceRecord(filename, lineNumber, activeLevel.name, tokens[1]));
						Util.noop()
					else
						main.writeStratmapLog(filename + " " + lineNumber + ": Parsing error: Encountered unrecognized token \"" + tokens[0] + "\" in settlement level.")
				}
				else if(activeCulture != null)
				{
					if(line.startsWith("portrait_mapping"))
						activeCulture.portraitMapping = tokens[1]
					else if(line.startsWith("rebel_standard_index"))
						activeCulture.rebelStandardIndex = tokens[1].toInt()
					else if(line.startsWith("fort_cost"))
						activeCulture.fortCost = tokens[1].toInt()
					else if(line.startsWith("fort_wall"))
						main.data.fileReferencesForCrossCheck.add(FileReferenceRecord(filename, lineNumber, activeCulture.name, tokens[1]))
					else if(line.startsWith("fort"))
					{
						main.data.fileReferencesForCrossCheck.add(FileReferenceRecord(filename, lineNumber, activeCulture.name, tokens[1].replace(",", "")))
						activeCulture.fortReference = tokens[2]
					}
					else if(line.startsWith("fishing_village"))
					{
						main.data.fileReferencesForCrossCheck.add(FileReferenceRecord(filename, lineNumber, activeCulture.name, tokens[1].replace(",", "")))
						activeCulture.fishingVillageReference = tokens[2]
					}
					else if(line.startsWith("port_land"))
					{
						main.data.fileReferencesForCrossCheck.add(FileReferenceRecord(filename, lineNumber, activeCulture.name, tokens[1].replace(",", "")))
						activeCulture.portReferences.add(tokens[2])
					}
					else if(line.startsWith("port_sea"))
						main.data.fileReferencesForCrossCheck.add(FileReferenceRecord(filename, lineNumber, activeCulture.name, tokens[1].replace(",", "")))
					else if(line.startsWith("watchtower_cost"))
						activeCulture.watchtowerCost = tokens[1].toInt()
					else if(line.startsWith("watchtower"))
					{
						main.data.fileReferencesForCrossCheck.add(FileReferenceRecord(filename, lineNumber, activeCulture.name, tokens[1].replace(",", "")))
						activeCulture.watchtowerReference = tokens[2]
					}
					else if(agentDirectives.contains(tokens[0]) && !main.runCfg.unusedAgents.contains(tokens[0]) && tokens[0] != "admiral")
					{
						activeCulture.agentFileReferences.add(SimpleReferenceRecord(tokens[1], filename, lineNumber))
						activeCulture.agentInfoCards.add(SimpleReferenceRecord(tokens[2], filename, lineNumber))
						activeCulture.agentFileReferences.add(SimpleReferenceRecord(tokens[3], filename, lineNumber))
					}
				}
				if(line.startsWith("culture"))
				{
					if(settlementLevelsActive)
						main.writeStratmapLog(filename, lineNumber, "Parsing error: Starting a new culture while settlement levels are still active. Assuming missing closing braces to try to continue.")
					activeCulture = CultureEntry(tokens[1])
					settlementLevelsActive = false
					settlementLevelActive = false
					main.data.strat.cultureEntries[activeCulture.name] = activeCulture
				}
			}
			cultureReader.close()
		}
		catch(e :FileNotFoundException)
		{
			main.writeOutput("Unable to find culture definition file ($filename). This will be a problem.")
		}
		catch(e :Exception)
		{
			main.fatalParsingError(lineNumber, readLine!!, e)
		}
	}

	private fun agentDirectives() :ArrayList<String>
	{
		val retur = ArrayList<String>()
		retur.add("spy")
		retur.add("assassin")
		retur.add("diplomat")
		retur.add("admiral")
		retur.add("merchant")
		retur.add("priest")
		return retur
	}
}