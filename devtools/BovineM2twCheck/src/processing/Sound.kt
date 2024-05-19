package processing

import data.common.FileReferenceCollection
import data.common.FileReferenceRecord
import data.common.UsageTrackedName
import data.sound.MusicEventOrState
import data.sound.VoiceFileReference
import main.BovineM2twCheck
import java.io.File

class Sound(private val main :BovineM2twCheck)
{
	private val requiredMusicStates by lazy { requiredMusicStates() }

	fun soundChecks()
	{
		checkAccentFactions()
		diplomacy()
		music()
		if(!main.runCfg.accentPrefixesSuppression)
		{
			checkAccentPrefixes(main.data.sound.campMapVoiceReferences)
			checkAccentPrefixes(main.data.sound.battleMapVoiceReferences)
		}
	}

	private fun checkAccentFactions()
	{
		for(accentName in main.data.sound.accentFactions.keys)
		{
			if(main.data.sound.accentFactions[accentName]!!.size == 0)
				main.writeSoundLog("Accent $accentName has no factions and can be deleted.")
			for(referencedFaction in main.data.sound.accentFactions[accentName]!!)
			{
				if(main.data.strat.factionEntries[referencedFaction] == null)
					main.writeSoundLog("Accent $accentName includes faction $referencedFaction which does not exist.")
			}
		}
		for(faction in main.data.strat.factionEntries.keys)
		{
			if(faction == "merc")
				continue
			var hasAccent :Boolean = false
			for(accentAssignment :ArrayList<String> in main.data.sound.accentFactions.values)
			{
				for(assignedFaction :String in accentAssignment)
				{
					if(assignedFaction == faction)
						hasAccent = true
				}
			}
			if(!hasAccent)
				main.writeSoundLog("Faction $faction has no assigned accents in descr_sounds_accents.txt")
		}
	}

	private fun diplomacy()
	{
		for(dupe in main.data.sound.diplomacySpeechHeaders.getDuplicates())
			main.writeSoundLog("""Diplomacy text: Duplicate description "${dupe.name}", occurs ${dupe.count} times.""")
		if(main.runCfg.diplomacySpeechIsAvailable)
		{
			for(diplomacyReference in main.data.sound.diplomacySoundReferences)
			{
				val referenced :UsageTrackedName? = main.data.sound.diplomacySpeechHeaders[diplomacyReference.reference, true]
				if(referenced == null && !main.lists.genericSounds.contains(diplomacyReference.reference) && !main.lists.unquotedDiplomatSoundsInclude(diplomacyReference.reference))
					main.writeSoundLog("""${diplomacyReference.filename} ${diplomacyReference.lineNumber}: Referenced diplomacy sound name "${diplomacyReference.reference}" is missing in diplomacy_speech.txt (and not set as unquoted in config/unquotedDiplomacySounds.txt).""")
			}
		}
	}

	private fun music()
	{
		/*
		for(musicEvent in main.data.sound.genericMusic)
		{
			//TODO how are these referenced?
			if(true)
				main.writeSoundLog(""""${musicEvent.name}" music event is never triggered (well, it quite possibly is, but I don't yet know how it is triggered)""")
		}
		*/
		for(musicType in main.data.sound.musicTypeFactionAssignments.keys)
		{
			if(main.data.sound.musicTypeFactionAssignments[musicType]!!.size == 0)
				main.writeSoundLog("Music type $musicType applies to no factions and can be deleted.")
			for(faction in main.data.sound.musicTypeFactionAssignments[musicType]!!)
			{
				if(main.data.strat.factionEntries[faction] == null)
					main.writeSoundLog("Music type $musicType applies to faction $faction which does not exist")
				for(otherMusicType in main.data.sound.musicTypeFactionAssignments.keys)
				{
					if(otherMusicType != musicType)
					{
						for(possiblyDupeFaction in main.data.sound.musicTypeFactionAssignments[otherMusicType]!!)
						{
							if(possiblyDupeFaction == faction)
								main.writeSoundLog("Faction $faction is assigned both music type $musicType and $otherMusicType")
						}
					}
				}
			}
		}
		for(musicType in main.data.sound.musicStates.keys)
		{
			val definedMusicStates :ArrayList<MusicEventOrState> = main.data.sound.musicStates[musicType]!!
			for(i :Int in definedMusicStates.indices)
			{
				for(j :Int in i+1 until definedMusicStates.size)
				{
					if(definedMusicStates[i] == definedMusicStates[j])
						main.writeSoundLog("Music type $musicType's music state ${definedMusicStates[i].name} uses music file ${definedMusicStates[i].filename} more than once.")
				}
			}
		}
		for(requiredState in requiredMusicStates)
		{
			for(musicType :String in main.data.sound.musicTypeFactionAssignments.keys)
			{
				var found :Boolean = false
				if(main.data.sound.musicStates[musicType] == null)
				{
					var existingMusicStates = main.data.sound.musicStates.keys.joinToString(", ")
					main.writeSoundLog("Music states for type $musicType not found among music types (these are $existingMusicStates). Probably a typo?")
				}
				else
				{
					for(state :MusicEventOrState in main.data.sound.musicStates[musicType]!!)
					{
						if(state.name == requiredState)
						{
							found = true
							break
						}
					}
					if(!found)
						main.writeSoundLog("Music type $musicType has no music defined for state $requiredState")
				}
			}
		}
	}

	private fun checkAccentPrefixes(referenceCollection :FileReferenceCollection<VoiceFileReference>)
	{
		for(reference :VoiceFileReference in referenceCollection.contents)
		{
			val acceptedPrefixesForAccent :ArrayList<String>? = main.lists.acceptedAccentPrefixes[reference.accent]
			if(acceptedPrefixesForAccent == null)
				main.writeSoundLog("Cannot find accepted accent prefixes for accent ${reference.accent}")

			//Check that the file has acceptable prefix
			if(!main.lists.genericSounds.contains(reference.soundName) && acceptedPrefixesForAccent != null)
			{
				var isAccepted :Boolean = false
				for(acceptedPrefix in acceptedPrefixesForAccent)
				{
					if(reference.soundName!!.startsWith(acceptedPrefix))
					{
						isAccepted = true
						break
					}
				}
				if(!isAccepted)
					main.writeSoundLog("""${reference.file} ${reference.lineNumber}: Warning - Referenced sound name "${reference.soundName}" for entry ${reference.referringEntryName}.${reference.vocal} has a prefix not defined for its accent (${reference.accent}). Intended?""")
			}
		}
	}

	fun listUnused()
	{
		checkSfxEventsUsage()

		checkFilesUsage("sounds/sfx", main.data.sound.effects, "sound effects", "descr_sounds_generic.txt, descr_structure_effects.txt, descr_event_effects.txt, descr_sounds_events.txt, descr_sounds_units_anims.txt", true)
		checkFilesUsage("sounds/effect_evt", main.data.sound.effects, "event effects", "descr_sounds_generic.txt, descr_structure_effects.txt, descr_event_effects.txt, descr_sounds_events.txt, descr_sounds_units_anims.txt", false)

		checkVoiceFilesUsage("sounds/voice/human/localized/camp_map", main.data.sound.campMapVoiceReferences, "strat map", "export_descr_sounds_stratmap_voice.txt")
		checkVoiceFilesUsage("sounds/voice/human/localized/battle_map", main.data.sound.battleMapVoiceReferences, "battle", "export_descr_sounds_units_voice.txt, export_descr_sounds_soldier_voice.txt")
		checkVoiceFilesUsage("sounds/voice/human/localized/narration", main.data.sound.narrationVoiceReferences, "narration", "export_descr_sounds_narration.txt")
		checkVoiceFilesUsage("sounds/voice/human/localized/advice", main.data.sound.adviceVoiceReferences, "advice", "export_descr_sounds_advice.txt")
		checkFilesUsage("sounds/music", main.data.sound.musicStates, "music", "descr_sounds_music.txt")

		for(diplomacySpeechHeader in main.data.sound.diplomacySpeechHeaders.getUnused())
		{
			if(!main.lists.unquotedDiplomatSoundsInclude(diplomacySpeechHeader.name))
				main.writeSoundLog("""${diplomacySpeechHeader.filename} ${diplomacySpeechHeader.lineNumber}: Diplomacy text "${diplomacySpeechHeader.name}" is not used by any diplomat accent in DSSV strat.""")
		}
	}

	private fun checkSfxEventsUsage()
	{
		for(effectEvent :FileReferenceRecord in main.data.sound.effects.contents)
		{
			var isReferenced = false
			for(reference in main.data.sound.effectReferences)
			{
				if(reference.reference == effectEvent.referringEntryName)
				{
					isReferenced = true
					break
				}
			}
			if(!isReferenced)
				main.writeSoundLog("${effectEvent.file} ${effectEvent.lineNumber}: Sound effect ${effectEvent.referringEntryName} is not used in any of your sound event files.")
		}
	}

	@Suppress("UNCHECKED_CAST")
	private fun checkVoiceFilesUsage(folder :String, relevantReferences :FileReferenceCollection<VoiceFileReference>, soundTypeName :String, referencingFiles :String)
	{
		checkFilesUsage(folder, relevantReferences as FileReferenceCollection<FileReferenceRecord>, soundTypeName, referencingFiles, false)
	}

	private fun checkFilesUsage(folder :String, relevantReferences :FileReferenceCollection<FileReferenceRecord>, soundTypeName :String, referencingFiles :String, includeSubFolders :Boolean)
	{
		var theFolder = folder
		if(!theFolder.endsWith("/"))
			theFolder = "$theFolder/"
		val files :Array<File>? = File("${main.runCfg.dataFolder}$folder").listFiles()
		if(files != null)
		{
			for(soundFile :File in files)
			{
				if(soundFile.isDirectory)
				{
					if(includeSubFolders)
						checkFilesUsage("$theFolder${soundFile.name}", relevantReferences, soundTypeName, referencingFiles, includeSubFolders)
				}
				else
				{
					val soundFilename :String = soundFile.name.lowercase()
					if(!relevantReferences.containsReferenceTo(theFolder, soundFilename))
					{
						main.writeSoundLog("""Warning - $soundTypeName sound file "$theFolder$soundFilename" is not used in $referencingFiles""")
						main.performRemovalInstructions("$theFolder${soundFile.name}")
					}
				}
			}
		}
	}

	@Suppress("SameParameterValue")
	private fun checkFilesUsage(folder :String, relevantReferences :HashMap<String, ArrayList<MusicEventOrState>>, soundTypeName :String, referencingFiles :String)
	{
		val files :Array<File>? = File(main.runCfg.dataFolder + folder).listFiles()
		var theFolder = folder
		if(!theFolder.endsWith("/"))
			theFolder = "$folder/"
		if(files != null)
		{
			for(soundFile :File in files)
			{
				if(soundFile.isDirectory)
					continue
				val soundFilename :String = soundFile.name.lowercase()
				if(!soundFilename.endsWith("mp3"))
					continue
				var found :Boolean = false
				for(fileList in relevantReferences.values)
				{
					for(fileReference in fileList)
					{
						if(fileReference.folder == theFolder && fileReference.filename == soundFilename)
						{
							found = true
							break
						}
					}
					if(found)
						break
				}
				if(!found)
				{
					main.writeSoundLog("""Warning - $soundTypeName sound file "$soundFilename" is not used in $referencingFiles""")
					main.performRemovalInstructions("$folder/${soundFile.name}")
				}
			}
		}
	}

	private fun requiredMusicStates() :ArrayList<String>
	{
		val retur = ArrayList<String>()
		retur.add("music_battle_battle")
		retur.add("music_battle_mobilize")
		retur.add("music_battle_tension")
		retur.add("music_campaign_defeat")
		retur.add("music_campaign_loading")
		retur.add("music_campaign_victory")
		retur.add("music_credits1")
		retur.add("music_credits2")
		retur.add("music_campaign_victory")
		retur.add("music_frontend")
		retur.add("music_prebattle_scroll")
		retur.add("music_result_draw")
		retur.add("music_result_lose_average")
		retur.add("music_result_lose_close")
		retur.add("music_result_lose_crushing")
		retur.add("music_result_strat_draw")
		retur.add("music_result_strat_lose_average")
		retur.add("music_result_strat_lose_close")
		retur.add("music_result_strat_lose_crushing")
		retur.add("music_result_strat_win_average")
		retur.add("music_result_strat_win_close")
		retur.add("music_result_strat_win_crushing")
		retur.add("music_result_win_average")
		retur.add("music_result_win_close")
		retur.add("music_result_win_crushing")
		retur.add("music_stratmap_summer")
		retur.add("music_stratmap_winter")
		return retur
	}
}