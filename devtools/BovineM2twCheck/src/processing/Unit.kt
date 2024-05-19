package processing

import data.TextureAssignmentError
import data.common.FileReferenceRecord
import data.unit.EduEntry
import data.unit.ModelDbEntry
import data.unit.SkeletonEntry
import main.BovineM2twCheck
import util.StringUtil
import util.Util
import java.io.BufferedReader
import java.io.File
import java.io.FileNotFoundException
import java.io.FileReader
import kotlin.math.max

class Unit(private val main :BovineM2twCheck)
{
	private val validEngineClasses by lazy { validEngineClasses() }
	private val validWaterTrailEffects by lazy { validWaterTrailEffects() }
	private val validMountClasses by lazy { validMountClasses() }
	private val validModelGroupNames by lazy { validModelGroupNames() }
	private val validLocomotionTables by lazy { validLocomotionTables() }

	private fun checkTextureAssignments(factionsToCheck :ArrayList<String>, eduEntry :EduEntry) :ArrayList<TextureAssignmentError>
	{
		val retur = ArrayList<TextureAssignmentError>()
		for(faction in factionsToCheck)
		{
			var found :Boolean
			val soldier :ModelDbEntry? = main.data.unit.battleModels[eduEntry.soldier!!, true]
			if(soldier == null)
			{
				retur.add(TextureAssignmentError(eduEntry.name, """Missing model: EDU entry "${eduEntry.name}" references nonexistent soldier model "${eduEntry.soldier}"."""))
				continue
			}
			for(officerName in eduEntry.officers)
			{
				found = false
				val officer :ModelDbEntry? = main.data.unit.battleModels[officerName, true]
				if(officer == null)
				{
					retur.add(TextureAssignmentError(eduEntry.name, """Missing model: EDU entry "${eduEntry.name}" references nonexistent officer model "$officerName"."""))
					continue
				}
				for(textureAssignment in officer.textureAssignments)
				{
					if(textureAssignment.faction == faction)
					{
						found = true
						break
					}
					else if(eduEntry.isMercenary() && textureAssignment.faction == "merc")
					{
						found = true
						break
					}
				}
				if(!found)
					retur.add(TextureAssignmentError(officer.name, """Silver surfer: EDU entry "${eduEntry.name}" requires officer texture assignments for faction $faction."""))
			}
			for(armourName in eduEntry.armourModels)
			{
				found = false
				val armour :ModelDbEntry? = main.data.unit.battleModels[armourName, true]
				if(armour == null)
				{
					retur.add(TextureAssignmentError(armourName, """Missing model: EDU entry "${eduEntry.name}" references nonexistent armour model "$armourName"."""))
					continue
				}
				for(textureAssignment in armour.textureAssignments)
				{
					if(textureAssignment.faction == faction)
					{
						found = true
						break
					}
					else if(eduEntry.isMercenary() && textureAssignment.faction == "merc")
					{
						found = true
						break
					}
				}
				if(!found)
					retur.add(TextureAssignmentError(armour.name, """Silver surfer: EDU entry "${eduEntry.name}" requires armour texture assignments for faction $faction."""))
			}
		}
		return retur
	}

	fun performChecks()
	{
		readCampaignScriptModelUse()
		characterReferences()
		unitChecks()
		engineUnitChecks()
		unitCardPicturesArePresent()
		for(entry :ModelDbEntry in main.data.unit.battleModels.getAll())
		{
			if(entry.modelAssignments.size == 0)
				continue
			for(skeleton in entry.skeletons)
			{
				if(skeleton.primarySkeleton != null && main.data.unit.skeletons[skeleton.primarySkeleton, true] == null && !main.lists.acceptedMissingSkeletons.contains(skeleton.primarySkeleton!!))
					main.writeUnitLog(entry.filename, entry.lineNumber, entry.name, "Assigned non-existent primary skeleton ${skeleton.primarySkeleton}")
				if(skeleton.secondarySkeleton != null && main.data.unit.skeletons[skeleton.secondarySkeleton, true] == null && !main.lists.acceptedMissingSkeletons.contains(skeleton.secondarySkeleton!!))
					main.writeUnitLog(entry.filename, entry.lineNumber, entry.name, "Assigned non-existent secondary skeleton ${skeleton.secondarySkeleton}")
				if(skeleton.mountSkeleton != null && main.data.unit.skeletons[skeleton.mountSkeleton, true] == null && !main.lists.acceptedMissingSkeletons.contains(skeleton.mountSkeleton!!))
					main.writeUnitLog(entry.filename, entry.lineNumber, entry.name, "Assigned non-existent mount skeleton ${skeleton.mountSkeleton}")
				if(skeleton.primaryAttachmentPrimary != null && main.data.unit.skeletons[skeleton.primaryAttachmentPrimary, true] == null && !main.lists.acceptedMissingSkeletons.contains(skeleton.primaryAttachmentPrimary!!))
					main.writeUnitLog(entry.filename, entry.lineNumber, entry.name, "Assigned non-existent main weapon skeleton ${skeleton.primaryAttachmentPrimary}")
				if(skeleton.primaryAttachmentSecondary != null && main.data.unit.skeletons[skeleton.primaryAttachmentSecondary, true] == null && !main.lists.acceptedMissingSkeletons.contains(skeleton.primaryAttachmentSecondary!!))
					main.writeUnitLog(entry.filename, entry.lineNumber, entry.name, "Assigned non-existent offhand weapon skeleton ${skeleton.primaryAttachmentSecondary}")
				if(skeleton.secondaryAttachmentPrimary != null && main.data.unit.skeletons[skeleton.secondaryAttachmentPrimary, true] == null && !main.lists.acceptedMissingSkeletons.contains(skeleton.secondaryAttachmentPrimary!!))
					main.writeUnitLog(entry.filename, entry.lineNumber, entry.name, "Assigned non-existent secondary weapon skeleton ${skeleton.secondaryAttachmentPrimary}")
				if(skeleton.secondaryAttachmentSecondary != null && main.data.unit.skeletons[skeleton.secondaryAttachmentSecondary, true] == null && !main.lists.acceptedMissingSkeletons.contains(skeleton.secondaryAttachmentSecondary!!))
					main.writeUnitLog(entry.filename, entry.lineNumber, entry.name, "Assigned non-existent offhand weapon skeleton ${skeleton.secondaryAttachmentSecondary}")
			}

			//Check for different faction assignments of unit textures
			//and attachment textures, unless mount (will have no attachments).
			if(entry.attachmentAssignments.size > 0)
			{
				for(att in entry.attachmentAssignments)
				{
					var isAlsoUnitTextured = false
					for(tex in entry.textureAssignments)
					{
						if(tex.faction == att.faction)
						{
							isAlsoUnitTextured = true
							break
						}
					}
					if(!isAlsoUnitTextured)
						main.writeUnitLog(entry.filename, entry.lineNumber, entry.name, "Attachment texture assignment for faction ${att.faction} is not accompanied by unit texture assignment.")
				}
				for(tex in entry.textureAssignments)
				{
					var isAlsoAttachmentTextured = false
					for(att in entry.attachmentAssignments)
					{
						if(tex.faction == att.faction)
						{
							isAlsoAttachmentTextured = true
							break
						}
					}
					if(!isAlsoAttachmentTextured)
						main.writeUnitLog(entry.filename, entry.lineNumber, entry.name, "Unit texture assignment for faction ${tex.faction} is not accompanied by attachment texture assignment.")
				}
			}
		}

		for(reference in main.data.strat.resourceReferences)
		{
			val resource = main.data.strat.resources[reference.reference, true]
			when
			{
				resource == null ->
					main.writeUnitLog(reference.filename, reference.lineNumber, null, "Reference to non-existent campaign map resource ${reference.reference}.")
				reference.isForHiddenResource && !resource.isHidden ->
					main.writeUnitLog(reference.filename, reference.lineNumber, null, "Reference to hidden resource ${reference.reference}, but this is not a hidden resource.")
				!reference.isForHiddenResource && resource.isHidden ->
					main.writeUnitLog(reference.filename, reference.lineNumber, null, "Reference to resource ${reference.reference}, but this is a hidden resource.")
			}
		}
		checkAnimationUsage("animations")

		//Verify mount class
		for(entry :ModelDbEntry in main.data.unit.battleModels.getAll())
		{
			for(skeleton in entry.skeletons)
			{
				if(skeleton.mount != null)
				{
					if(!validMountClasses.contains(skeleton.mount!!))
						main.writeUnitLog(entry.filename, entry.lineNumber, entry.name, """Model uses mount class "${skeleton.mount}". Allowed values only include Horse, None, Camel and Elephant.""")
				}
			}
		}

		//Verify rider/soldier locomotion
		for(skeleton :SkeletonEntry in main.data.unit.skeletons.getAll())
		{
			if(skeleton.locomotionTable != null && !validLocomotionTables.contains(skeleton.locomotionTable!!))
				main.writeUnitLog(skeleton.filename, skeleton.lineNumber, skeleton.name, "Unrecognized locomotion table value: ${skeleton.locomotionTable}")
			if(skeleton.noDeltas && skeleton.locomotionTable != null)
				main.writeUnitLog(skeleton.filename, skeleton.lineNumber, skeleton.name, "Skeleton uses both locomotion_table and no_deltas. This should be just one or the other - locomotion_table for independently moving units and no_deltas for stationary riders.")
		}
		for(eduEntry :EduEntry in main.data.unit.eduEntries.values)
		{
			if(eduEntry.mount != null)
			{
				var modelDbEntry :ModelDbEntry? = main.data.unit.battleModels[eduEntry.soldier!!, true]
				if(modelDbEntry != null)
				{
					for(skeletonAssignment :ModelDbEntry.ModelDbSkeleton in modelDbEntry.skeletons)
					{
						for(unmarked :String in getUnmarkedWithNoDeltas(skeletonAssignment))
							main.writeUnitLog(eduEntry.filename, eduEntry.lineNumber, "${eduEntry.name}'s soldier ${eduEntry.soldier}", "Rider soldier includes a skeleton assignment not marked with no_deltas: $unmarked.")
					}
				}
				for(officerName :String in eduEntry.officers)
				{
					modelDbEntry = main.data.unit.battleModels[officerName, true]
					if(modelDbEntry != null)
					{
						for(skeletonAssignment :ModelDbEntry.ModelDbSkeleton in modelDbEntry.skeletons)
						{
							for(unmarked :String in getUnmarkedWithNoDeltas(skeletonAssignment))
								main.writeUnitLog(eduEntry.filename, eduEntry.lineNumber, "${eduEntry.name}'s officer $officerName", "Rider officer includes a skeleton assignment not marked with no_deltas: $unmarked.")
						}
					}
				}
			}
		}

		for(m in main.data.unit.mounts.getAll())
		{
			if(m.isVanillaRepresentation)
				break
			val model = main.data.unit.mountModels[m.model, true]
			if(model == null)
				main.writeUnitLog(m.filename, m.lineNumber, m.name, "Referenced mount model ${m.model} does not exist.")
			else if(!model.isMount)
				main.writeUnitLog(m.filename, m.lineNumber, m.name, "Referenced mount model ${m.model} is a soldier model instead.")
			if(m.riderCount != m.riderOffsets.size)
				main.writeUnitLog(m.filename, m.lineNumber, m.name, "Rider count is set as ${m.riderCount}, but there are ${m.riderOffsets} rider offsets.")
			for(i in 0 until m.riderOffsets.size)
			{
				for(j in i + 1 until m.riderOffsets.size)
				{
					if(m.riderOffsets[i] == m.riderOffsets[j])
						main.writeUnitLog(m.filename, m.lineNumber, m.name, "Identical rider offsets: ${m.riderOffsets[i]}")
				}
			}
			if(m.waterTrailEffect == "")
				main.writeUnitLog(m.filename, m.lineNumber, m.name, "Water trail effect is missing.")
			else if(!validWaterTrailEffects.contains(m.waterTrailEffect))
				main.writeUnitLog(m.filename, m.lineNumber, m.name, "Unrecognized water trail effect: ${m.waterTrailEffect}.")
			if(m.mountClass == "elephant" && m.riderCount < 2)
				main.writeUnitLog(m.filename, m.lineNumber, m.name, "Mount class elephant requires at least two riders (on pain of CTD), this has ${m.riderCount}.")
			if(!validMountClasses().contains(m.mountClass))
				main.writeUnitLog(m.filename, m.lineNumber, m.name, "Unrecognized mount class ${m.mountClass}")
		}
		for(skeleton in main.data.unit.skeletons.getAll())
		{
			if(skeleton.parent != null && main.data.unit.skeletons[skeleton.parent, true] == null)
				main.writeUnitLog(skeleton.filename, skeleton.lineNumber, skeleton.name, "Parent skeleton missing: ${skeleton.parent}")
		}

		//Verify usage of mounts
		for(eduEntry in main.data.unit.eduEntries.values)
		{
			if(eduEntry.mount == null)
				continue
			val mount = main.data.unit.mounts[eduEntry.mount!!, true]
			if(mount == null)
				main.writeUnitLog(eduEntry.filename, eduEntry.lineNumber, eduEntry.name, """Unit uses mount "${eduEntry.mount}" which does not exist.""")
		}

		//Verify usage of engines
		for(eduEntry in main.data.unit.eduEntries.values)
		{
			if(eduEntry.engine != null)
			{
				val engine = main.data.unit.engines[eduEntry.engine, true]
				if(engine == null)
					main.writeUnitLog(eduEntry.filename, eduEntry.lineNumber, eduEntry.name, """Unit uses engine "${eduEntry.engine}" which does not exist.""")
			}
		}
		for(eduEntry in main.data.unit.eduEntries.values)
		{
			if(eduEntry.mountedEngine != null)
			{
				val engine = main.data.unit.engines[eduEntry.mountedEngine, true]
				if(engine == null)
					main.writeUnitLog(eduEntry.filename, eduEntry.lineNumber, eduEntry.name, """Unit uses mounted engine "${eduEntry.mountedEngine}" which does not exist.""")
			}
		}

		//Verify ownership integrity
		for(eduEntry in main.data.unit.eduEntries.values)
		{
			if(eduEntry.category != "ship")
			{
				val errors = checkTextureAssignments(eduEntry.uniqueOwnerships(), eduEntry)
				for(error in errors)
					main.writeUnitLog(eduEntry.filename, eduEntry.lineNumber, error.entryName, error.errorMessage)
			}
		}

		//Verify number of armour levels
		for(eduEntry in main.data.unit.eduEntries.values)
		{
			if(eduEntry.armourLevels.size != eduEntry.armourModels.size)
				main.writeUnitLog(eduEntry.filename, eduEntry.lineNumber, eduEntry.name, "Unit is set up with ${eduEntry.armourLevels.size} armour levels, but ${eduEntry.armourModels.size} armour models. These should match.")
		}
	}

	private fun unitCardPicturesArePresent()
	{
		//Unit info (details page) picture
		var folderTemplate :String = "ui/unit_info/%FACTION_FOLDER%"
		for(unit :EduEntry in main.data.unit.eduEntries.values)
		{
			var checkedFolder :String
			when
			{
				unit.isMercenary() ->
				{
					checkedFolder = folderTemplate.replace("%FACTION_FOLDER%", "merc")
					main.checkFileReference(FileReferenceRecord(unit.filename, unit.lineNumber, "${unit.name} - mercenary", "${main.runCfg.dataFolder}$checkedFolder/${unit.dictionaryName}_info.tga"))
				}
				unit.infoPictureDirectory.isNotEmpty() ->
				{
					checkedFolder = folderTemplate.replace("%FACTION_FOLDER%", unit.infoPictureDirectory)
					main.checkFileReference(FileReferenceRecord(unit.filename, unit.lineNumber, "${unit.name} - common folder provided with info_pic_dir", "${main.runCfg.dataFolder}$checkedFolder/${unit.dictionaryName}_info.tga"))
				}
				else ->
				{
					for(owner :String in unit.uniqueOwnerships())
					{
						checkedFolder = folderTemplate.replace("%FACTION_FOLDER%", owner)
						main.checkFileReference(FileReferenceRecord(unit.filename, unit.lineNumber, "${unit.name} - Faction $owner", "${main.runCfg.dataFolder}$checkedFolder/${unit.dictionaryName}_info.tga"))
					}
				}
			}
		}

		//Unit card (army composition panel) picture
		folderTemplate = "ui/units/%FACTION_FOLDER%"
		for(unit :EduEntry in main.data.unit.eduEntries.values)
		{
			var checkedFolder :String
			when
			{
				unit.isMercenary() ->
				{
					checkedFolder = folderTemplate.replace("%FACTION_FOLDER%", "mercs")
					main.checkFileReference(FileReferenceRecord(unit.filename, unit.lineNumber, "${unit.name} - mercenary", "${main.runCfg.dataFolder}$checkedFolder/#${unit.dictionaryName}.tga"))
				}
				unit.cardPictureDirectory.isNotEmpty() ->
				{
					checkedFolder = folderTemplate.replace("%FACTION_FOLDER%", unit.cardPictureDirectory)
					main.checkFileReference(FileReferenceRecord(unit.filename, unit.lineNumber, "${unit.name} - common folder provided with card_pic_dir", "${main.runCfg.dataFolder}$checkedFolder/#${unit.dictionaryName}.tga"))
				}
				else ->
				{
					for(owner :String in unit.uniqueOwnerships())
					{
						checkedFolder = folderTemplate.replace("%FACTION_FOLDER%", owner)
						main.checkFileReference(FileReferenceRecord(unit.filename, unit.lineNumber, "${unit.name} - Faction $owner", "${main.runCfg.dataFolder}$checkedFolder/#${unit.dictionaryName}.tga"))
					}
				}
			}
		}
	}

	fun listUnused()
	{
		for(mount in main.data.unit.mounts.getUnused())
		{
			if(mount.isVanillaRepresentation)
				break
			if(!main.lists.acceptedUnusedMounts.contains(mount.name))
				main.writeUnitLog(mount.filename, mount.lineNumber, null, """Mount "${mount.name}" is never used by units in export_descr_unit.""")
		}
		for(mount in main.data.unit.mountModels.getUnused())
		{
			if(!main.lists.acceptedUnusedBattleModels.contains(mount.name))
				main.writeUnitLog(mount.filename, mount.lineNumber, mount.name, "Mount model is never used by registered mounts.")
		}
		for(skeleton in main.data.unit.skeletons.getAll())
		{
			if(!main.runCfg.vanillaSkeletonsOnly && !skeleton.isUsed && !main.lists.acceptedUnusedSkeletons.contains(skeleton.name))
			{
				val reportMessage = """Skeleton is never used by model DB entries."""
				main.writeUnitLog(skeleton.filename, skeleton.lineNumber, skeleton.name, reportMessage)
			}
		}
		for(engine in main.data.unit.engines.getUnused())
		{
			if(!main.lists.acceptedUnusedEngines.contains(engine.name))
				main.writeUnitLog(engine.filename, engine.lineNumber, engine.name, """Engine is never used by units in export_descr_unit.""")
		}

		//Report unused models
		for(model :ModelDbEntry in main.data.unit.battleModels.getUnused())
		{
			if(!main.lists.acceptedUnusedBattleModels.contains(model.name))
				main.writeUnitLog(model.filename, model.lineNumber, model.name, "Battle model is never used by EDU entries, strat characters or scripted characters.")
		}
	}

	private fun engineUnitChecks()
	{
		for(engine in main.data.unit.engines.getAll())
		{
			var cultures = Util.arrayListToArray(engine.cultures)
			for(culture in cultures)
			{
				if(culture == "all")
				{
					engine.cultures.remove(culture)
					for(cultureGroupMember in main.data.strat.cultureEntries.values)
						engine.cultures.add(cultureGroupMember.name)
				}
			}
			cultures = Util.arrayListToArray(engine.cultures)
			for(culture in cultures)
			{
				if(main.data.strat.cultureEntries[culture] == null)
					main.writeUnitLog(engine.filename, engine.lineNumber, engine.name, "Engine is available for culture $culture which does not exist.")
			}
			for(i in cultures.indices)
			{
				for(j in i + 1 until cultures.size)
				{
					if(cultures[i] == cultures[j])
						main.writeUnitLog(engine.filename, engine.lineNumber, engine.name, "Engine is available for culture ${cultures[i]} more than once.")
				}
			}
			if(!validEngineClasses.contains(engine.engineClass))
				main.writeUnitLog(engine.filename, engine.lineNumber, engine.name, "Unrecognized engine class ${engine.engineClass}.")
			for(modelGroup in engine.modelGroups)
			{
				for(name in modelGroup.names)
				{
					if(!validModelGroupNames.contains(name))
						main.writeUnitLog(engine.filename, engine.lineNumber, engine.name, """Unrecognized engine model group "$name", recognized model group names are: normal, dying, dead.""")
				}
				if(modelGroup.skeleton != null)
				{
					val skeleton = main.data.unit.skeletons[modelGroup.skeleton, true]
					if(skeleton == null)
						main.writeUnitLog(engine.filename, engine.lineNumber, engine.name, """Model group "${modelGroup.name()}" references nonexistent skeleton "${modelGroup.skeleton}".""")
				}
			}
			for(animation in engine.crewAnimations)
			{
				var found = false
				for(modelGroup in engine.modelGroups)
				{
					val skeleton :SkeletonEntry? = main.data.unit.skeletons[modelGroup.skeleton, true]
					if(skeleton != null)
					{
						for(skeletonAnimation in skeleton.animations)
						{
							if(skeletonAnimation.name == animation.name)
							{
								found = true
								break
							}
						}
					}
					if(found)
						break
				}
				if(!found)
					main.writeUnitLog(engine.filename, engine.lineNumber, engine.name, """Engine refers to crew animation "${animation.name}" which is not contained in any of its model groups' skeletons.""")
			}
		}
	}

	private fun readCampaignScriptModelUse()
	{
		val filename = "campaign_script.txt"
		var readLine :String? = null
		var lineNumber = 0
		try
		{
			main.writeOutput("$filename (for battle model usage)")
			val scriptReader = BufferedReader(FileReader(main.runCfg.stratFolder + filename))
			while(run { readLine = scriptReader.readLine(); readLine } != null)
			{
				lineNumber++
				val line :String = StringUtil.standardize(readLine!!)
				if(line.isEmpty())
					continue
				val tokens = StringUtil.split(line, " ")
				if(line.startsWith("character"))
				{
					for(i in tokens.indices)
					{
						var foundBattleModel :String? = null
						if(tokens[i] == "battle_model")
							foundBattleModel = tokens[i + 1].replace(",", "")
						if(foundBattleModel != null)
						{
							//TODO move to tests
							if(main.data.unit.battleModels[foundBattleModel, true] == null)
								main.writeUnitLog("campaign_script.txt", lineNumber, "", """CS references nonexistent battle model "$foundBattleModel".""")
						}
					}
				}
				if(line.startsWith("change_battle_model"))
				{
					val foundBattleModel = tokens[3]
					//TODO move to tests
					if(main.data.unit.battleModels[foundBattleModel, true] == null)
						main.writeUnitLog("campaign_script.txt", lineNumber, "", """CS references nonexistent battle model "$foundBattleModel".""")
				}
			}
			scriptReader.close()
		}
		catch(e :FileNotFoundException)
		{
			main.writeOutput("Unable to find campaign_script.txt for reading custom battle models. You may have given a wrong path to your mod's strat folder.")
		}
		catch(e :Exception)
		{
			main.fatalParsingError(lineNumber, readLine!!, e)
		}
	}

	private fun checkAnimationUsage(path :String)
	{
		if(main.runCfg.vanillaSkeletonsOnly)
		{
			main.writeOutput("As the vanilla skeletons are in use absent descr_skeleton.txt, whether animation files are actually in use is impossible to check. Skipping these reports.")
			return
		}
		val folder = File("${main.runCfg.dataFolder}/$path")
		val contents = folder.listFiles()
		if(contents != null)
		{
			for(content in contents)
			{
				val referenceName = ("$path/${content.name}").lowercase()
				if(content.name != ".svn")
				{
					if(content.isDirectory)
					{
						checkAnimationUsage(referenceName)
					}
					else
					{
						if(!main.data.unit.usedAnimationFiles.contains(referenceName) && !main.lists.acceptedNonreferencedFiles.contains(referenceName))
						{
							main.writeUnitLog(null, "", null, """Animation file "$referenceName" is not referenced in descr_skeleton or descr_engine_skeleton.""")
							main.performRemovalInstructions(referenceName)
						}
					}
				}
			}
		}
	}

	private fun characterReferences()
	{
		for(characterType in main.data.unit.characterTypes)
		{
			for(modelName in characterType.battleModelNames)
			{
				val battleModel :ModelDbEntry? = main.data.unit.battleModels[modelName, true]
				if(battleModel == null)
					main.writeUnitLog(characterType.filename, characterType.lineNumber, modelName, """Character type "${characterType.name}" for faction ${characterType.faction} in descr_character refers to nonexistent battle model $modelName.""")
			}
			for(modelName in characterType.stratModelNames)
			{
				val stratModel = main.data.strat.stratModels[modelName, true]
				if(stratModel == null)
					main.writeUnitLog(characterType.filename, characterType.lineNumber, modelName, """Character type "${characterType.name}" for faction ${characterType.faction} in descr_character refers to nonexistent strat model $modelName""")
			}
			if(!Util.equalsAny(characterType.name, "named character", "general") && characterType.battleModelNames.size > 0)
				main.writeUnitLog(characterType.filename, characterType.lineNumber, null, """Character type "${characterType.name}" for faction ${characterType.faction} refers to battle model, but only "named character" and "general" should use this clause.""")
			else if(Util.equalsAny(characterType.name, "named character", "general") && characterType.battleModelNames.size == 0)
				main.writeUnitLog(characterType.filename, characterType.lineNumber, null, """Character type "${characterType.name}" for faction ${characterType.faction} needs a battle model.""")
			else if(Util.equalsAny(characterType.name, "named character", "general"))
			{
				//TODO Add checking of faction texture assignments
				Util.noop()
			}
		}
	}

	private fun unitChecks()
	{
		for(eduEntry in main.data.unit.eduEntries.values)
		{
			val description = main.data.unit.findUnitDescription(eduEntry.dictionaryName)
			if(description == null)
				main.writeUnitLog(eduEntry.filename, eduEntry.lineNumber, eduEntry.name, """Unit description "${eduEntry.dictionaryName}" is missing in export_units.txt.""")
		}
		for(description in main.data.unit.unitDescriptions)
		{
			if(description.name == null)
			{
				if(description.longDescription != null)
				{
					if(description.isDuplicate)
						main.writeUnitLog("export_units.txt", description.longLineNumber, null, """Duplicate long description labelled "${description.longDescription}".""")
					else
						main.writeUnitLog("export_units.txt", description.longLineNumber, null, """Long description labelled "${description.longDescription}" has no corresponding entry for its unit name.""")
				}
				if(description.shortDescription != null)
				{
					if(description.isDuplicate)
						main.writeUnitLog("export_units.txt", description.shortLineNumber, null, """Duplicate short description labelled "${description.shortDescription}".""")
					else
						main.writeUnitLog("export_units.txt", description.shortLineNumber, null, """Short description labelled "${description.shortDescription}" has no corresponding entry for its unit name.""")
				}
			}
			else
			{
				if(description.isDuplicate)
					main.writeUnitLog("export_units.txt", description.nameLineNumber, null, """Duplicate unit name labelled "${description.name}".""")
				else if(!description.nameIsVerifiedPresent)
					main.writeUnitLog("export_units.txt", max(description.shortLineNumber, description.longLineNumber), null, """Unit name "${description.name}" is missing but short and/or long description exists.""")
				else
				{
					if(description.longDescription == null)
						main.writeUnitLog("export_units.txt", description.nameLineNumber, description.name, """Unit description "${description.name}" is missing its long description.""")
					if(description.shortDescription == null)
						main.writeUnitLog("export_units.txt", description.nameLineNumber, description.name, """Unit description "${description.name}" is missing its short description.""")
				}
			}
			var nameIsUsed = false
			for(eduEntry in main.data.unit.eduEntries.values)
			{
				if(eduEntry.dictionaryName == description.name)
				{
					nameIsUsed = true
					break
				}
			}
			if(!nameIsUsed && description.name != null)
				main.writeUnitLog("export_units.txt", description.nameLineNumber, description.name, "Unit description is not used by any unit.")
		}
	}

	private fun getUnmarkedWithNoDeltas(assignment :ModelDbEntry.ModelDbSkeleton) :ArrayList<String>
	{
		val retur = ArrayList<String>()
		if(assignment.mount == "none")
			return retur
		if(assignment.mountSkeleton != null)
		{
			val skeleton :SkeletonEntry? = main.data.unit.skeletons[assignment.mountSkeleton, true]
			if(skeleton != null && !isMarkedWithNoDeltas(skeleton))
				retur.add(assignment.mountSkeleton!!)
		}
		if(assignment.primarySkeleton != null)
		{
			val skeleton :SkeletonEntry? = main.data.unit.skeletons[assignment.primarySkeleton, true]
			if(skeleton != null && !isMarkedWithNoDeltas(skeleton))
				retur.add(assignment.primarySkeleton!!)
		}
		if(assignment.secondarySkeleton != null)
		{
			val skeleton :SkeletonEntry? = main.data.unit.skeletons[assignment.secondarySkeleton, true]
			if(skeleton != null && !isMarkedWithNoDeltas(skeleton))
				retur.add(assignment.secondarySkeleton!!)
		}
		return retur
	}

	private fun isMarkedWithNoDeltas(skeleton :SkeletonEntry?) :Boolean
	{
		if(skeleton == null)
			return false
		if(skeleton.noDeltas)
			return true
		if(skeleton.parent != null)
		{
			val parent :SkeletonEntry? = main.data.unit.skeletons[skeleton.parent, true]
			return isMarkedWithNoDeltas(parent)
		}
		return false
	}

	private fun validEngineClasses() :ArrayList<String>
	{
		val retur = ArrayList<String>()
		retur.add("tower")
		retur.add("ladder")
		retur.add("ram")
		retur.add("catapult")
		retur.add("rocket_launcher")
		retur.add("culverin")
		retur.add("serpentine")
		retur.add("bombard")
		retur.add("huge_bombard")
		retur.add("grand_bombard")
		retur.add("mortar")
		retur.add("basilisk")
		retur.add("ballista")
		retur.add("trebuchet")
		retur.add("cannon")
		retur.add("ribault")
		retur.add("holy_cart")
		return retur
	}

	private fun validWaterTrailEffects() :ArrayList<String>
	{
		val retur = ArrayList<String>()
		retur.add("horse_water_trail")
		retur.add("elephant_water_trail")
		retur.add("camel_water_trail")
		return retur
	}

	private fun validMountClasses() :ArrayList<String>
	{
		val retur = ArrayList<String>()
		retur.add("horse")
		retur.add("none")
		retur.add("elephant")
		retur.add("camel")
		return retur
	}

	private fun validModelGroupNames() :ArrayList<String>
	{
		val retur = ArrayList<String>()
		retur.add("normal")
		retur.add("dying")
		retur.add("dead")
		return retur
	}

	private fun validLocomotionTables() :ArrayList<String>
	{
		val retur = ArrayList<String>()
		retur.add("soldier")
		retur.add("elephant")
		return retur

	}
}