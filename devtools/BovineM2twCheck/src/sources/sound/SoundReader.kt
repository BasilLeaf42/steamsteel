package sources.sound

import data.common.SimpleReferenceRecord
import data.common.FileReferenceCollection
import data.common.FileReferenceRecord
import data.common.UsageTrackedName
import data.sound.MusicEventOrState
import data.sound.VoiceFileReference
import main.BovineM2twCheck
import util.StringUtil
import util.Util
import java.io.*

class SoundReader(private val main :BovineM2twCheck)
{
	fun readWhenever()
	{
		readSounds()
		readAccents()
		readDiplomacySpeech()
		readMusic()
	}

	private fun readAccents()
	{
		val filename = "descr_sounds_accents.txt"
		var readLine :String? = null
		var lineNumber = 0
		var currentAccent :String = ""
		var foundAccentFactions = 0
		try
		{
			main.writeOutput(filename)
			val accentFile :BufferedReader = BufferedReader(InputStreamReader(FileInputStream(main.runCfg.dataFolder + filename)))
			while(run { readLine = accentFile.readLine(); readLine } != null)
			{
				val line :String = StringUtil.standardize(readLine!!).trim()
				lineNumber++
				if(line == "")
					continue
				val tokens :Array<String> = StringUtil.split(line, " ")
				if(line.startsWith("accent "))
				{
					currentAccent = tokens[1]
					main.data.sound.accentFactions[currentAccent] = ArrayList<String>()
				}
				else if(line.startsWith("factions"))
				{
					for(i in 1 until tokens.size)
					{
						if(tokens[1] != "")
						{
							foundAccentFactions++
							main.data.sound.accentFactions[currentAccent]!!.add(tokens[i].replace(",", ""))
						}
					}
				}
			}
			accentFile.close()
			main.writeOutput("Read ${main.data.sound.accentFactions.size} accents for ${foundAccentFactions} factions.")
		}
		catch(e :FileNotFoundException)
		{
			main.writeOutput("Cannot find $filename. Checking for valid accent assignment by faction is impossible.")
		}
		catch(e :Exception)
		{
			main.fatalParsingError(lineNumber, readLine!!, e)
		}
	}

	private fun readSounds()
	{
		readSoundBank("descr_sounds_events.txt", "type", main.data.sound.effects, "effect", "FileReferenceRecord")
		readSoundBank("descr_sounds_units_anims.txt", "bank:", main.data.sound.effects, "effect", "FileReferenceRecord")
		readSoundEffects("descr_event_effects.txt", main.data.sound.effects)
		readSoundEffects("descr_structure_effects.txt", main.data.sound.effects)
		readSoundBank("descr_sounds_generic.txt", "event", main.data.sound.effects, "effect", "FileReferenceRecord")
		readVoiceBank("export_descr_sounds_stratmap_voice.txt", "type", main.data.sound.campMapVoiceReferences, "stratmap voice")
		readVoiceBank("export_descr_sounds_units_voice.txt", "class", main.data.sound.battleMapVoiceReferences, "battle voice")
		readVoiceBank("export_descr_sounds_soldier_voice.txt", "class", main.data.sound.battleMapVoiceReferences, "battle voice")
		readVoiceBank("export_descr_sounds_narration.txt", "event", main.data.sound.narrationVoiceReferences, "narration voice")
		readVoiceBank("export_descr_sounds_advice.txt", "text", main.data.sound.adviceVoiceReferences, "advice voice")

		readEffectEvents()
	}

	private fun readDiplomacySpeech()
	{
		val filename = "text/diplomacy_speech.txt"
		var readLine :String? = null
		var lineNumber = 0
		try
		{
			main.writeOutput(filename)
			val diplomacySpeechTextFile = BufferedReader(InputStreamReader(FileInputStream(main.runCfg.dataFolder + filename), "UTF-16"))
			while(run { readLine = diplomacySpeechTextFile.readLine(); readLine } != null)
			{
				val line :String = readLine!!
				lineNumber++
				if(line.startsWith("{"))
				{
					var name = line.substring(1, line.indexOf("}"))
					name = StringUtil.standardize(name)
					main.data.sound.diplomacySpeechHeaders.add(UsageTrackedName(name, "diplomacy_speech", lineNumber))
				}
			}
			diplomacySpeechTextFile.close()
			main.writeOutput("Read " + main.data.sound.diplomacySpeechHeaders.count() + " entries.")
		}
		catch(e :FileNotFoundException)
		{
			main.writeOutput("Cannot find text/diplomacy_speech.txt. Cannot check diplomacy sound integrity.")
			main.runCfg.diplomacySpeechIsAvailable = false
		}
		catch(e :Exception)
		{
			main.fatalParsingError(lineNumber, readLine!!, e)
		}
	}

	@Suppress("UNCHECKED_CAST")
	private fun readVoiceBank(sourceFile :String, entryNameIdentifier :String, targetCollection :FileReferenceCollection<VoiceFileReference>, targetCollectionName :String)
	{
		readSoundBank(sourceFile, entryNameIdentifier, targetCollection as FileReferenceCollection<FileReferenceRecord>, targetCollectionName, "VoiceFileReference")
	}

	private fun readSoundBank(sourceFile :String, entryNameIdentifier :String, targetCollection :FileReferenceCollection<FileReferenceRecord>, targetCollectionName :String, targetObjectType :String)
	{
		var readLine :String? = null
		var lineNumber = 0
		var accent = ""
		var entryName = ""
		var vocal = ""
		var folder = ""
		var fileListingActive = false
		try
		{
			main.writeOutput(sourceFile)
			val inputFile = BufferedReader(FileReader(main.runCfg.dataFolder + sourceFile))
			while(run { readLine = inputFile.readLine(); readLine } != null)
			{
				lineNumber++
				val line :String = StringUtil.standardize(readLine!!).trim()
				if(line == "")
					continue
				val tokens :Array<String> = StringUtil.split(line, " ")
				var fileListingJustActivated = false
				when(tokens[0])
				{
					"accent" ->
						accent = tokens[1]
					entryNameIdentifier ->
						entryName = tokens[1]
					"vocal" ->
						vocal = tokens[1]
					"folder" ->
					{
						folder = line.substring("folder data/".length).lowercase()
						if(!folder.endsWith("/"))
							folder = "$folder/"
						fileListingActive = true
						fileListingJustActivated = true
					}
				}
				if(fileListingActive && !fileListingJustActivated)
				{
					if(line == "end")
						fileListingActive = false
					else
					{
						var filename :String = tokens[0]
						if(!filename.contains("."))
							filename = "$filename.wav"
						var soundName = filename
						if(soundName.endsWith(".mp3"))
							soundName = soundName.substring(0, filename.indexOf(".mp3"))
						if(soundName.endsWith(".wav"))
							soundName = soundName.substring(0, filename.indexOf(".wav"))
						if(main.runCfg.diplomacySpeechIsAvailable)
						{
							if(entryName == "diplomat" || entryName == "princess")
							{
								main.data.sound.diplomacySoundReferences.add(SimpleReferenceRecord(soundName, sourceFile, lineNumber))
								main.data.sound.diplomacySpeechHeaders[soundName, true]
							}
						}
						var reference :FileReferenceRecord
						if(targetObjectType == "VoiceFileReference")
						{
							reference = VoiceFileReference(sourceFile, lineNumber, entryName, filename, folder, true)
							reference.soundName = soundName
							reference.vocal = vocal
							reference.accent = accent
						}
						else
							reference = FileReferenceRecord(sourceFile, lineNumber, entryName, filename, folder)
						targetCollection.add(reference)
						if(!main.runCfg.soundFileIntegritySuppression)
							main.data.fileReferencesForCrossCheck.add(reference)
					}
				}
			}
			inputFile.close()
			main.writeOutput("The target collection now numbers ${targetCollection.contents.size} $targetCollectionName references.")
		}
		catch(e :FileNotFoundException)
		{
			main.writeOutput("Cannot find the sound linking file (" + main.runCfg.dataFolder + sourceFile + ")")
			main.writeOutput("No checks have been performed on this part of sounds integrity.")
			main.writeOutput("This is okay if you are ONLY using vanilla factions and sounds. You may have entered your mod's data folder wrong.")
		}
		catch(e :Exception)
		{
			main.fatalParsingError(lineNumber, readLine!!, e)
		}
	}

	private var effect = ""
	private var effectSet = ""
	private var effectActive = false
	private var effectSetActive = false
	private var lineNumber = 0
	private fun readSoundEffects(sourceFile :String, targetCollection :FileReferenceCollection<FileReferenceRecord>)
	{
		var readLine :String? = null
		lineNumber = 0
		val encounteredEffects = ArrayList<String>()
		var openBracesCount = 0
		try
		{
			main.writeOutput(sourceFile)
			val inputFile = BufferedReader(FileReader(main.runCfg.dataFolder + sourceFile))
			while(run { readLine = inputFile.readLine(); readLine } != null)
			{
				lineNumber++
				val line :String = StringUtil.standardize(readLine!!).trim()
				if(line == "")
					continue
				val tokens :Array<String> = StringUtil.split(line, " ")
				if(line == "{")
				{
					openBracesCount++
					continue
				}
				if(line == "}")
				{
					openBracesCount--
					continue
				}
				when(openBracesCount)
				{
					0 -> noOpenBraces(sourceFile, tokens, encounteredEffects)
					1 -> oneOpenBraces(sourceFile, tokens)
					2 -> twoOpenBraces(sourceFile, tokens, encounteredEffects, targetCollection)
				}
			}
			inputFile.close()
			main.writeOutput("The target collection now numbers ${targetCollection.contents.size} sound effect references.")
		}
		catch(e :FileNotFoundException)
		{
			main.writeOutput("Cannot find the sound linking file (" + main.runCfg.dataFolder + sourceFile + ")")
			main.writeOutput("No checks have been performed on this part of sounds integrity.")
			main.writeOutput("This is okay if you are ONLY using vanilla factions and sounds. You may have entered your mod's data folder wrong.")
		}
		catch(e :Exception)
		{
			main.fatalParsingError(lineNumber, readLine!!, e)
		}
	}

	private fun noOpenBraces(sourceFile :String, tokens :Array<String>, encounteredEffects :java.util.ArrayList<String>)
	{
		when(tokens[0])
		{
			"effect" ->
			{
				effect = tokens[1]
				if(encounteredEffects.contains(effect))
					main.writeSoundLog("$sourceFile $lineNumber: Duplicate effect name ${tokens[1]}")
				else
					encounteredEffects.add(effect)
				effectActive = true
				effectSetActive = false
			}
			"effect_set" ->
			{
				effectSet = tokens[1]
				effectActive = false
				effectSetActive = true
			}
			else ->
				main.writeSundryLog("$sourceFile $lineNumber: Unrecognized directive ${tokens[0]}")
		}

	}

	private fun oneOpenBraces(sourceFile :String, tokens :Array<String>)
	{
		when(tokens[0])
		{
			"type" ->
			{
				if(tokens[1] != "sound")
					main.writeSundryLog("$sourceFile $lineNumber: Unrecognized effect type ${tokens[1]}")
			}
			"lod", "time_of_day" ->
				Util.noop()
			else ->
				main.writeSundryLog("$sourceFile $lineNumber: Unrecognized directive ${tokens[0]}")
		}
	}

	private fun twoOpenBraces(sourceFile :String, tokens :Array<String>, encounteredEffects :java.util.ArrayList<String>, targetCollection :FileReferenceCollection<FileReferenceRecord>)
	{
		when
		{
			effectActive && tokens[0] == "evt_file" ->
			{
				val record = FileReferenceRecord(sourceFile, lineNumber, effect, tokens[1])
				targetCollection.add(record)
				main.data.fileReferencesForCrossCheck.add(record)
			}
			effectSetActive ->
			{
				if(!encounteredEffects.contains(tokens[0]))
					main.writeSoundLog("$sourceFile $lineNumber: Effect set $effectSet contains undefined effect named ${tokens[0]}")
			}
			Util.equalsAny(tokens[0], "random_one_shot", "shockwave_mass", "time_between_shots") ->
				Util.noop()
			else ->
				main.writeSundryLog("$sourceFile $lineNumber: Unrecognized directive ${tokens[0]}")
		}
	}

	private fun readMusic()
	{
		var readLine :String? = null
		var lineNumber = 0
		var filename :String = "world/maps/base/descr_sounds_music_types.txt"
		var currentMusicType :String = ""
		try
		{
			main.writeOutput(filename)
			val inputFile = BufferedReader(FileReader(main.runCfg.dataFolder + filename))
			while(run { readLine = inputFile.readLine(); readLine } != null)
			{
				lineNumber++
				val line :String = StringUtil.standardize(readLine!!).trim()
				if(line == "")
					continue
				val tokens :Array<String> = StringUtil.split(line, " ")
				if(line.startsWith("music_type"))
				{
					currentMusicType = tokens[1]
					main.data.sound.musicTypeFactionAssignments[currentMusicType] = ArrayList<String>()
				}
				else if(line.startsWith("factions"))
				{
					for(i in 1 until tokens.size)
						main.data.sound.musicTypeFactionAssignments[currentMusicType]!!.add(tokens[i])
				}
			}
			inputFile.close()
		}
		catch(e :FileNotFoundException)
		{
			main.writeOutput("Cannot find the music types definition file (" + main.runCfg.dataFolder + filename + ")")
			main.writeOutput("No checks have been performed on this part of sounds integrity.")
			main.writeOutput("This is okay if you are ONLY using vanilla factions and music. You may have entered your mod's data folder wrong.")
		}
		catch(e :Exception)
		{
			main.fatalParsingError(lineNumber, readLine!!, e)
		}

		filename = "descr_sounds_music.txt"
		lineNumber = 0
		var activeGenericMusic :MusicEventOrState = MusicEventOrState("dummy")
		val activeMusicTypes = ArrayList<String>()
		var state :String? = null
		var folder :String = ""
		var fileListingActive = false
		try
		{
			main.writeOutput(filename)
			val inputFile = BufferedReader(FileReader(main.runCfg.dataFolder + filename))
			while(run { readLine = inputFile.readLine(); readLine } != null)
			{
				lineNumber++
				val line :String = StringUtil.standardize(readLine!!).trim()
				if(line == "")
					continue
				val tokens :Array<String> = StringUtil.split(line, " ")
				when
				{
					tokens[0] == "music_type" ->
					{
						activeMusicTypes.clear()
						for(i in 1 until tokens.size)
							activeMusicTypes.add(tokens[i].replace(",", ""))
					}
					tokens[0] == "state" ->
						state = tokens[1]
					tokens[0] == "event" && activeMusicTypes.size == 0 ->
					{
						activeGenericMusic = MusicEventOrState(tokens[1])
						main.data.sound.genericMusic.add(activeGenericMusic)
					}
					tokens[0] == "folder" ->
					{
						folder = line.substring("folder data/".length).lowercase().trim()
						if(!folder.endsWith("/"))
							folder = "$folder/"
						fileListingActive = true
					}
					tokens[0] == "end" ->
						fileListingActive = false
					fileListingActive ->
					{
						val soundFilename :String = line
						if(state == null)
						{
							activeGenericMusic.folder = folder
							activeGenericMusic.filename = soundFilename
							if(!main.runCfg.soundFileIntegritySuppression)
								main.data.fileReferencesForCrossCheck.add(FileReferenceRecord(filename, lineNumber, null, activeGenericMusic.filename!!, activeGenericMusic.folder))
						}
						else
						{
							val reference = MusicEventOrState(state)
							reference.folder = folder
							reference.filename = soundFilename
							for(musicType :String in activeMusicTypes)
							{
								if(main.data.sound.musicStates[musicType] == null)
									main.data.sound.musicStates[musicType] = ArrayList<MusicEventOrState>()
								main.data.sound.musicStates[musicType]!!.add(reference)
							}
							if(!main.runCfg.soundFileIntegritySuppression)
								main.data.fileReferencesForCrossCheck.add(FileReferenceRecord(filename, lineNumber, null, reference.filename!!, reference.folder))
						}
					}
				}
			}
			inputFile.close()
		}
		catch(e :FileNotFoundException)
		{
			main.writeOutput("Cannot find the music definition file (" + main.runCfg.dataFolder + filename + ")")
			main.writeOutput("No checks have been performed on this part of sounds integrity.")
			main.writeOutput("This is okay if you are ONLY using vanilla factions and music. You may have entered your mod's data folder wrong.")
		}
		catch(e :Exception)
		{
			main.fatalParsingError(lineNumber, readLine!!, e)
		}
	}

	private fun readEffectEvents()
	{
		var readLine :String?
		val files :Array<File>? = File("${main.runCfg.dataFolder}sounds/effect_evt").listFiles()
		if(files != null)
		{
			for(file :File in files)
			{
				var lineNumber = 0
				val reader = BufferedReader(FileReader(file))
				main.writeOutput("sounds/effect_evt/${file.name}")
				while(run { readLine = reader.readLine(); readLine } != null)
				{
					lineNumber++
					val line :String = StringUtil.standardize(readLine!!)
					val tokens :Array<String> = StringUtil.split(line, " ")
					if(tokens[0] == "event" && tokens[1] == "sound")
					{
						main.data.sound.effectReferences.add(SimpleReferenceRecord(tokens[2], "sounds/effect_evt/${file.name}", lineNumber))
					}
				}
			}
		}
	}
}