package processing

import data.common.FileReferenceRecord
import main.BovineM2twCheck
import util.StringUtil
import util.Util
import java.io.File

class FileReferences(val main :BovineM2twCheck)
{
	fun checkFileReferences()
	{
		verifyNoLookupsPresent()
		for(reference in main.data.fileReferencesForCrossCheck.contents)
			checkFileReference(reference)
	}

	private fun verifyNoLookupsPresent()
	{
		reportSuperfluousFile(main.runCfg.dataFolder, "descr_names_lookup.txt")
		reportSuperfluousFile(main.runCfg.dataFolder, "descr_quotes_lookup.txt")
		reportSuperfluousFile(main.runCfg.dataFolder, "descr_religions_lookup.txt")
		reportSuperfluousFile(main.runCfg.dataFolder, "descr_climates_lookup.txt")
		reportSuperfluousFile(main.runCfg.dataFolder, "message_text_lookup.txt")
		reportSuperfluousFile(main.runCfg.dataFolder, "historic_battles_subtitles_lookup.txt")
		reportSuperfluousFile(main.runCfg.dataFolder, "factionintrosubtitles_lookup.txt")
		reportSuperfluousFile(main.runCfg.dataFolder, "shortcuts_lookup.txt")
		reportSuperfluousFile(main.runCfg.dataFolder, "prebattle_speeches_subtitles_lookup.txt")
		reportSuperfluousFile(main.runCfg.dataFolder, "battle_event_subtitles_lookup.txt")
		reportSuperfluousFile(main.runCfg.stratFolder, "descr_regions_and_settlement_name_lookup.txt")
	}

	private fun reportSuperfluousFile(folder :String, filename :String)
	{
		if(File(folder + filename).exists())
			main.writeFileReferenceLog("Your mod includes $filename. This file is redundant in M2TW (but necessary in RTW), and can be deleted for slightly reduced mod size.")
	}

	fun listUnused()
	{
		checkFilesUsage("unit_models", true, "Model DB", "Unit")
		checkFilesUsage("unit_sprites", true, "Model DB", "Unit")
		checkFilesUsage("models_strat", false, "Strat models", "Stratmap")
		checkFilesUsage("siege_engines", true, "Siege engines", "Unit")
		checkFilesUsage("ui/pips", true, "Settlement detail pip images", "Stratmap")
		checkFilesUsage("ui/unit_info", true, "Unit information pictures (unit details page)", "Unit")
		checkFilesUsage("ui/units", true, "Unit card pictures (army composition panel)", "Unit")
		checkFilesUsage("ui/custom_portraits", true, "Custom characters", "Stratmap")
		//NOT checking these files because the game doesn't use them
		//checkFilesUsage("loading_screen/symbols", true, "Loading screen symbols", "Stratmap");
	}

	private fun checkFilesUsage(path :String, includeSubFolders :Boolean, relevantArea :String, relevantLog :String)
	{
		val folder = File(main.runCfg.dataFolder + "/" + path)
		val contents = folder.listFiles()
		if(contents != null)
		{
			for(content in contents)
			{
				val referenceName = (path + "/" + content.name).lowercase()
				if(content.name == ".svn")
					continue
				if(content.isDirectory)
				{
					if(includeSubFolders)
						checkFilesUsage(referenceName, includeSubFolders, relevantArea, relevantLog)
					else
						continue
				}
				else
				{
					if(referenceName.matches(".*[0-9][0-9][0-9].texture".toRegex()))
					{
						//This is a sprite texture, not directly referenced by the game, but rather
						//through its corresponding sprite file. Check for occurrence of that one.
						val dotPosition = referenceName.indexOf(".")
						if(!main.data.encounteredFileReferences.contains(referenceName.substring(0, dotPosition - 4) + ".spr"))
						{
							main.writeUnitLog(null, "", null, "File \"$referenceName\" is not referenced in the $relevantArea")
							main.performRemovalInstructions(referenceName)
						}
					}
					else if(!main.data.encounteredFileReferences.contains(referenceName))
					{
						var allowed = false
						for(allowedNonReference in main.lists.acceptedNonreferencedFiles)
						{
							if(referenceName.contains(allowedNonReference))
							{
								allowed = true
								break
							}
						}
						if(!allowed)
						{
							when(relevantLog)
							{
								"Unit" -> main.writeUnitLog(null, "", null, "File \"$referenceName\" is not referenced in the $relevantArea")
								"Stratmap" -> main.writeStratmapLog("File \"$referenceName\" is not referenced in the $relevantArea")
								else -> throw IllegalArgumentException("Need to point to relevant log $relevantLog")
							}
							main.performRemovalInstructions(referenceName)
						}
					}
				}
			}
		}
	}

	fun checkFileReference(reference :FileReferenceRecord)
	{
		var referencedFilename = reference.referencedFile
		var exists = File(main.runCfg.dataFolder + reference.referencedFolder + referencedFilename).exists()
		if(!exists && reference.additionalPossibleExtensions != null)
		{
			for(additionalExtension in reference.additionalPossibleExtensions!!)
			{
				referencedFilename = reference.referencedFile + additionalExtension
				exists = File(main.runCfg.dataFolder + reference.referencedFolder + referencedFilename).exists()
				if(exists)
					break
			}
		}
		if(!exists && reference.alternativeExtension != null)
		{
			val filenameSansExtension = StringUtil.beforeLast(reference.referencedFile, ".")
			referencedFilename = filenameSansExtension + reference.alternativeExtension
			exists = File(main.runCfg.dataFolder + reference.referencedFolder + referencedFilename).exists()
		}
		if(!exists)
		{
			var acceptable = main.lists.acceptedMissingFiles.contains(reference.referencedFolder + reference.referencedFile)
			if(!acceptable)
				acceptable = reference.vanillaFilesAreAvailable && main.lists.vanillaFiles.contains(reference.referencedFolder + reference.referencedFile)
			if(!acceptable)
			{
				if(reference.additionalPossibleExtensions != null && reference.vanillaFilesAreAvailable)
				{
					for(additionalExtension in reference.additionalPossibleExtensions!!)
					{
						acceptable = main.lists.vanillaFiles.contains(reference.referencedFolder + reference.referencedFile + additionalExtension)
						if(acceptable)
							break
					}
				}
				if(!acceptable && reference.vanillaFilesAreAvailable && reference.alternativeExtension != null)
				{
					val filenameSansExtension = StringUtil.beforeLast(reference.referencedFile, ".")
					acceptable = main.lists.vanillaFiles.contains(reference.referencedFolder + filenameSansExtension + reference.alternativeExtension)
				}
				if(!acceptable)
					main.writeFileReferenceLog(reference)
			}
		}

		var folder :String = reference.referencedFolder!!
		if(folder.contains("/data/"))
			folder = StringUtil.after(folder, "/data/")
		Util.addIfNotPresent(folder + referencedFilename, main.data.encounteredFileReferences)
	}
}