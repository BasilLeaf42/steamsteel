package sources.stratmap.names

import data.strat.FactionCharacterNames
import main.BovineM2twCheck
import util.StringUtil
import util.Util
import java.io.*

class NamesReader(private val main :BovineM2twCheck)
{
	fun readAll()
	{
		readNames()
		readTranslations()
	}

	private fun readNames()
	{
		var readLine :String? = null
		var lineNumber = 0
		val filename :String = "descr_names.txt"
		try
		{
			main.writeOutput(filename)
			val inputFile = BufferedReader(InputStreamReader(FileInputStream(main.runCfg.dataFolder + filename), "Windows-1252"))
			var currentFaction :String = ""
			var currentNameType :String = ""
			while(run { readLine = inputFile.readLine(); readLine } != null)
			{
				lineNumber++
				val line :String = StringUtil.standardize(readLine!!).trim()
				if(line == "")
					continue
				val tokens :Array<String> = StringUtil.split(line, " ")
				if(line.startsWith("faction:"))
					currentFaction = tokens[1]
				else if(Util.equalsAny(line, "characters", "women", "surnames"))
					currentNameType = line
				else
				{
					if(main.data.strat.names[currentFaction] == null)
						main.data.strat.names[currentFaction] = FactionCharacterNames()
					when(currentNameType)
					{
						"characters" ->
							main.data.strat.names[currentFaction]!!.characterNames.add(line)
						"surnames" ->
							main.data.strat.names[currentFaction]!!.characterSurnames.add(line)
						"women" ->
							main.data.strat.names[currentFaction]!!.womenNames.add(line)
					}
				}
			}
			inputFile.close()
		}
		catch(e :FileNotFoundException)
		{
			main.writeOutput("Cannot find the definition file for faction names (" + main.runCfg.dataFolder + filename + "). You may have entered your mod's data folder wrong.")
		}
		catch(e :Exception)
		{
			main.fatalParsingError(lineNumber, readLine!!, e)
		}
	}

	private fun readNamesText(translationName :String, filename :String)
	{
		if(main.data.strat.nameText[translationName] == null)
			main.data.strat.nameText[translationName] = HashMap<String, String>()
		var readLine :String? = null
		var lineNumber = 0
		try
		{
			main.writeOutput(filename)
			val inputFile = BufferedReader(InputStreamReader(FileInputStream(main.runCfg.dataFolder + filename), "UTF-16"))
			while(run { readLine = inputFile.readLine(); readLine } != null)
			{
				lineNumber++
				val line :String = StringUtil.standardize(readLine!!).trim()
				if(line == "")
					continue
				if(line.startsWith("{"))
				{
					val nameName :String = StringUtil.between(line, "{", "}")!!
					val nameText :String = StringUtil.after(line, "}")
					if(main.data.strat.nameText[translationName]!![nameName] != null)
						main.writeStratmapLog(filename, lineNumber, """Name {$nameName} is duplicated for translation "$translationName".""")
					main.data.strat.nameText[translationName]!![nameName] = nameText
				}
			}
			inputFile.close()
		}
		catch(e :FileNotFoundException)
		{
			if(File("${main.runCfg.dataFolder}$filename.strings.bin").exists())
				main.writeOutput("Cannot find the faction character names file (${main.runCfg.dataFolder}$filename), only its strings.bin equivalent. This tool cannot read strings.bin format, so cannot ensure this content matches descr_names.")
			else
				main.writeOutput("Cannot find the faction character names file (${main.runCfg.dataFolder}$filename) nor its strings.bin equivalent. Cannot ensure this content matches descr_names.")
		}
		catch(e :Exception)
		{
			main.fatalParsingError(lineNumber, readLine!!, e)
		}
	}

	private fun readTranslations()
	{
		readNamesText("default", "text/names.txt")
		val translationFolder :File = File(main.runCfg.dataFolder + "campaign/translation")
		if(translationFolder.exists())
		{
			for(translation :File in translationFolder.listFiles()!!)
			{
				if(translation.isDirectory)
					readNamesText(translation.name, "campaign/translation/${translation.name}/names.txt")
			}
		}
	}
}
