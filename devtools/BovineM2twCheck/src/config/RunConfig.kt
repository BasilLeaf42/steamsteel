package config

import util.StringUtil
import java.io.BufferedReader
import java.io.FileReader
import java.util.*

class RunConfig(configurationFile :String)
{
	var dataFolder :String = ""
	var stratFolder :String = ""
	var vanillaAnimationsRequired = true
	var hiddenTraitsDescriptionSuppression = false
	var accentPrefixesSuppression = false
	var soundFileIntegritySuppression = false
	var diplomacySpeechIsAvailable = true
	var vanillaSkeletonsOnly = false

	var unusedAgents = ArrayList<String>()
	var unusedRemovalCommands = ArrayList<String>()

	var configOk = true

	init
	{
		val configReader = BufferedReader(FileReader(configurationFile))
		var readLine :String?
		while(run { readLine = configReader.readLine() ; readLine } != null)
		{
			var line :String = readLine!!
			val commentStart :Int = line.indexOf(";")
			if(commentStart >= 0)
				line = line.substring(0, commentStart)
			if(line == "")
				continue

			val tokens :Array<String> = StringUtil.split(line, "=")
			when(tokens[0])
			{
				"DATAFOLDER" ->
					dataFolder = StringUtil.ensureEndsWith(tokens[1], "/")
				"STRAT" ->
					stratFolder = dataFolder + StringUtil.ensureEndsWith(tokens[1], "/")
				"VANILLA_ANIMATIONS_REQUIRED" ->
				{
					if(tokens[1] == "NO")
						vanillaAnimationsRequired = false
				}
				"HIDDEN_TRAIT_DESCRIPTIONS_SUPPRESSED" ->
				{
					if(tokens[1] == "YES")
						hiddenTraitsDescriptionSuppression = true
				}
				"ACCENT_PREFIXES_SUPPRESSED" ->
				{
					if(tokens[1] == "YES")
						accentPrefixesSuppression = true
				}
				"SOUNDFILE_INTEGRITY_SUPPRESSED" ->
				{
					if(tokens[1] == "YES")
						soundFileIntegritySuppression = true
				}
				"UNUSED_AGENT" ->
					unusedAgents.add(tokens[1])
				"REMOVE_UNUSED_FILES" ->
					unusedRemovalCommands.add(tokens[1])
			}
		}
	}
}