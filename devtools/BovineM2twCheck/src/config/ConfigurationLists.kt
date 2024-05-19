package config

import data.unit.SkeletonEntry
import main.BovineM2twCheck
import util.StringUtil
import java.io.BufferedReader
import java.io.FileNotFoundException
import java.io.FileReader
import java.util.*

class ConfigurationLists(private val main :BovineM2twCheck)
{
	val acceptedMissingFiles = ArrayList<String>()
	val vanillaFiles = ArrayList<String>()
	val acceptedNonreferencedFiles = ArrayList<String>()
	val acceptedMissingSkeletons = ArrayList<String>()
	val acceptedUnusedSkeletons = ArrayList<String>()
	val acceptedUnusedMounts = ArrayList<String>()
	val acceptedUnusedEngines = ArrayList<String>()
	val acceptedUnusedBattleModels = ArrayList<String>()
	val acceptedUnusedStratModels = ArrayList<String>()
	val acceptedMissingMounts = ArrayList<String>()
	val genericSounds = ArrayList<String>()
	val acceptedAccentPrefixes = HashMap<String, ArrayList<String>>()
	private val unquotedDiplomatSounds = ArrayList<String>()

	fun readConfig()
	{
		if(!main.runCfg.configOk)
		{
			main.writeOutput("Skipping reading configuration files due to fatal fault.")
			return
		}
		main.writeOutput("Reading configuration files...")
		readPlainConfigFile(acceptedMissingFiles, "config/acceptedMissingFiles.txt", "Unable to find list of acceptable missing files ({filename}), assuming none are okay.")
		readPlainConfigFile(vanillaFiles, "config/vanillaFiles.txt", "Unable to find list of vanilla files ({filename}). This makes the checker report any vanilla file references in your mod as missing!")
		readPlainConfigFile(acceptedNonreferencedFiles, "config/acceptedNonReferencedFiles.txt", "Unable to find list of acceptable files not referenced anywhere ({filename}), assuming none are okay")
		//Unit stuff
		readPlainConfigFile(acceptedMissingMounts, "config/acceptedMissingMounts.txt", "Unable to find list of acceptable missing mounts ({filename}), assuming none are okay")
		readPlainConfigFile(acceptedUnusedMounts, "config/acceptedUnusedMounts.txt", "Unable to find list of acceptable unused mounts ({filename}), assuming none are okay")
		readPlainConfigFile(acceptedUnusedEngines, "config/acceptedUnusedEngines.txt", "Unable to find list of acceptable unused engines ({filename}), assuming none are okay")
		readPlainConfigFile(acceptedMissingSkeletons, "config/acceptedMissingSkeletons.txt", "Unable to find list of acceptable missing skeletons ({filename}), assuming none are okay")
		readPlainConfigFile(acceptedUnusedSkeletons, "config/acceptedUnusedSkeletons.txt", "Unable to find list of acceptable unused skeletons ({filename}), assuming none are okay")
		readPlainConfigFile(acceptedUnusedBattleModels, "config/acceptedUnusedBattleModels.txt", "Unable to find list of acceptable unused battle models ({filename}), assuming none are okay")
		//Stratmap
		readPlainConfigFile(acceptedUnusedStratModels, "config/acceptedUnusedStratModels.txt", "Unable to find list of acceptable unused strat models ({filename}), assuming none are okay")
		//Sound and diplomacy stuff
		readPlainConfigFile(genericSounds, "config/genericSounds.txt", "Cannot find {filename}. Assuming all sounds are specific to factions. This will probably produce additional false warnings in output.")
		readPlainConfigFile(unquotedDiplomatSounds, "config/unquotedDiplomacySounds.txt", "Cannot find {filename}. Assuming all diplomat sounds require a text in diplomacy_speech.txt. This will probably produce additional false errors in output.")

		var readLine :String?
		if(!main.runCfg.accentPrefixesSuppression)
		{
			try
			{
				main.writeOutput("acceptedAccentPrefixes.txt")
				val acceptedAccentPrefixFile :BufferedReader = BufferedReader(FileReader("config/acceptedAccentPrefixes.txt"))
				var currentAcceptedList = ArrayList<String>()
				while(run { readLine = acceptedAccentPrefixFile.readLine() ; readLine } != null)
				{
					var line :String = readLine!!
					line = StringUtil.standardize(line)
					if(line == "")
						continue
					if(line.startsWith("["))
					{
						val accentName :String? = StringUtil.between(line, "[", "]")
						currentAcceptedList = ArrayList()
						acceptedAccentPrefixes[accentName!!] = currentAcceptedList
					}
					else
						currentAcceptedList.add(line)
				}
				acceptedAccentPrefixFile.close()
			}
			catch(e :FileNotFoundException)
			{
				main.writeOutput("Cannot find acceptedAccentPrefixes.txt. No verification of accent versus file prefix will be made.")
			}
		}
	}

	private fun readPlainConfigFile(targetList :ArrayList<String>, filename :String, notFoundErrorMessage :String)
	{
		var readLine :String?
		//General config lists
		try
		{
			main.writeOutput(filename)
			val reader :BufferedReader = BufferedReader(FileReader(filename))
			while(run { readLine = reader.readLine(); readLine} != null)
				targetList.add(readLine?.lowercase() ?:"")
			reader.close()
		}
		catch(e :FileNotFoundException)
		{
			main.writeOutput(notFoundErrorMessage.replaceFirst("{filename}", filename))
		}
	}

	fun unquotedDiplomatSoundsInclude(diplomacySound :String) :Boolean
	{
		for(pattern in unquotedDiplomatSounds)
		{
			if(diplomacySound.contains(pattern))
				return true
		}
		return false
	}

	fun readVanillaSkeletons()
	{
		main.runCfg.vanillaSkeletonsOnly = true
		try
		{
			var readLine :String?
			var lineNumber :Int = 0
			main.writeOutput("vanillaSkeletons.txt")
			val skeletonListFile :BufferedReader = BufferedReader(FileReader("config/vanillaSkeletons.txt"))
			while(run { readLine = skeletonListFile.readLine(); readLine} != null)
			{
				var line :String = readLine!!
				line = StringUtil.standardize(line)
				lineNumber++
				if(line == "")
					continue
				main.data.unit.skeletons.add(SkeletonEntry(line, "vanillaSkeletons.txt", lineNumber))
			}
			skeletonListFile.close()
		}
		catch(e :FileNotFoundException)
		{
			main.writeOutput("Cannot find the vanillaSkeletons.txt config file and the mod's skeleton file is not present. This will probably cause a ton of false reports.")
		}
	}
}