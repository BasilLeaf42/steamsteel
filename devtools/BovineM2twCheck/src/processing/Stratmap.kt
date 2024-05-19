package processing

import data.FactionEntry
import data.common.SimpleReferenceRecord
import data.common.FileReferenceRecord
import data.strat.FactionCharacterNames
import data.strat.MapCharacter
import data.strat.MapSettlement
import data.strat.building.BuildingEntry
import data.strat.building.BuildingLevelEntry
import data.strat.culture.CultureEntry
import data.strat.mission.*
import data.unit.EduEntry
import data.unit.ModelDbEntry
import data.unit.StratModelEntry
import main.BovineM2twCheck
import sources.stratmap.building.BuildingRequirementsHolder
import util.StringUtil
import util.Util

class Stratmap(private val main :BovineM2twCheck)
{
	private val validSettlementLevels by lazy { validSettlementLevels() }
	private val validAgents by lazy { validAgents() }
	private val validMissionConditions by lazy { validMissionConditions() }

	fun performChecks()
	{
		namesAndLabels()
		traitReferences()
		buildingReferences()
		stratmapModels()
		factionsAndCultures()
		characters()
		missions()
		missionPaybacks()
		settlements()
	}

	private fun characters()
	{
		//TODO more checks
		for(character in main.data.strat.mapCharacters)
		{
			if(character.battleModel.isNotEmpty())
			{
				val battleModel :ModelDbEntry? = main.data.unit.battleModels[character.battleModel, true]
				if(battleModel == null)
					main.writeStratmapLog(character.filename, character.lineNumber, """Reference to non-existent battle model "${character.battleModel}".""")
			}
			if(character.stratModel != null)
			{
				val stratModel = main.data.strat.stratModels[character.stratModel, true]
				if(stratModel == null)
					main.writeStratmapLog(character.filename, character.lineNumber, """Reference to non-existent strat model "${character.stratModel}".""")
			}
			if(character.subFaction != null && main.data.strat.factionEntries[character.subFaction!!] == null)
				main.writeStratmapLog(character.filename, character.lineNumber, "Character has sub faction ${character.subFaction} which does not exist.")
			if(main.data.unit.findCharacterType(character.ownerFaction, character.type) == null)
				main.writeStratmapLog(character.filename, character.lineNumber, "Character has unrecognized type ${character.type} for faction ${character.ownerFaction}.")
			if(!character.hasMatchingGender())
				main.writeStratmapLog(character.filename, character.lineNumber, "Character does not have gender matching its type.")

			if(character.isLeader)
			{
				for(other in main.data.strat.mapCharacters)
				{
					if(other.isLeader && other.ownerFaction == character.ownerFaction && character !== other)
						main.writeStratmapLog(character.filename, character.lineNumber, "Faction ${character.ownerFaction} has more than one leader, including ${character.name}.")
				}
			}
			if(character.isHeir)
			{
				for(other in main.data.strat.mapCharacters)
				{
					if(other.isHeir && other.ownerFaction == character.ownerFaction && character !== other)
						main.writeStratmapLog(character.filename, character.lineNumber, "Faction ${character.ownerFaction} has more than one heir, including ${character.name}.")
				}
			}
		}
		checkRelationships()
	}

	private fun checkRelationships()
	{
		for(relationship in main.data.strat.characterRelationships)
		{
			val character = main.data.strat.findCharacterOrRecord(relationship.characterName, relationship.faction)
			if(character == null)
				main.writeStratmapLog(relationship.filename, relationship.lineNumber, """Character relationship defined for character "${relationship.characterName}", but this character does not exist.""")
			else if(character.ownerFaction != relationship.faction)
				main.writeStratmapLog(relationship.filename, relationship.lineNumber, """Character relationship defined for character "${relationship.characterName}", but this character belongs to a different faction.""")
			for(relation in relationship.relations)
			{
				val relatedCharacter = main.data.strat.findCharacterOrRecord(relation, relationship.faction)
				if(relatedCharacter == null)
					main.writeStratmapLog(relationship.filename, relationship.lineNumber, """Character relationship defined for character "${relationship.characterName}" towards "$relation", but this related character does not exist.""")
				else if(relatedCharacter.ownerFaction != relationship.faction)
					main.writeStratmapLog(relationship.filename, relationship.lineNumber, """Character relationship defined for character "${relationship.characterName}" towards "$relation", but this related character belongs to a different faction.""")
			}
		}
	}

	private fun traitReferences()
	{
		for(reference in main.data.strat.traitReferences)
		{
			val trait = main.data.code.traits[reference.reference, false]
			if(trait == null)
				main.writeStratmapLog(reference.filename, reference.lineNumber, "Reference to nonexistent trait ${reference.reference}")
			else
			{
				if(reference.awardedAmount != null)
					trait.isAwarded = true
				if(reference.referencedLevel != -1)
				{
					trait.isTested = true
					if(reference.referencedLevel > trait.traitLevels.size)
						main.writeStratmapLog(reference.filename, reference.lineNumber, "Test for trait level ${reference.referencedLevel}, ${trait.name} has only ${trait.traitLevels.size} levels.")
				}
			}
		}
	}

	private fun buildingReferences()
	{
		checkBuildings()
		checkBuildingLevels()
		checkRequirements()
	}

	private fun checkBuildings()
	{
		for(building in main.data.strat.buildings.getAll())
		{
			if(building.convertTo != null)
			{
				val convertToBuilding = main.data.strat.buildings[building.convertTo, true]
				if(convertToBuilding == null)
					main.writeStratmapLog(building.filename, building.lineNumber, "Building ${building.name} converts to non-existent building ${building.convertTo}")
			}
			if(building.religion != null)
			{
				val religion = main.data.strat.religions[building.religion, true]
				if(religion == null)
					main.writeStratmapLog(building.filename, building.lineNumber, "Building ${building.name} relates to non-existent religion ${building.religion}")
			}
		}
		for(reference in main.data.strat.buildingReferences)
			main.data.strat.verifyBuildingReferenceExists(reference, "%FILE% %LINENUMBER%: Building \"%REF%\" does not exist.")
	}

	private fun checkBuildingLevels()
	{
		for(building in main.data.strat.buildings.getAll())
		{
			if(building.convertTo != null)
			{
				val convertToBuilding = main.data.strat.buildings[building.convertTo, true]
				if(convertToBuilding != null)
				{
					for(level in building.buildingLevels.getAll())
					{
						if(level.convertToLevel != null && level.convertToLevel!! > convertToBuilding.buildingLevels.count())
							main.writeStratmapLog(level.filename, level.lineNumber, "Building ${building.name} is convertible to level ${level.convertToLevel}, but ${convertToBuilding.name} has only ${convertToBuilding.buildingLevels.count()} levels.")
					}
				}
			}
			else
			{
				for(level in building.buildingLevels.getAll())
				{
					if(level.convertToLevel != null)
						main.writeStratmapLog(level.filename, level.lineNumber, "Building ${building.name} is not convertible but its level ${level.name} has convert_to reference.")
				}
			}
			for(level in building.buildingLevels.getAll())
			{
				if(level.settlementLevelRequirement != null && !validSettlementLevels.contains(level.settlementLevelRequirement!!))
					main.writeStratmapLog(level.filename, level.lineNumber, "Building level has an unrecognized minimum settlement level ${level.settlementLevelRequirement}. Recognized values include village, town, large_town, city, large_city and huge_city.")
				for(upgrade in level.upgrades)
				{
					if(building.buildingLevels[upgrade.name, true] == null)
						main.writeStratmapLog(upgrade.filename, upgrade.lineNumber, "Building ${building.name}'s level ${level.name} upgrades to non-existent level ${upgrade.name}")
				}
				for(capability in level.generalCapabilities)
				{
					if(capability.referredAgent != null && !validAgents.contains(capability.referredAgent!!))
						main.writeStratmapLog(capability.filename, capability.lineNumber, "Capability refers to invalid agent type ${capability.referredAgent}.")
				}
			}
			for(reference in main.data.strat.buildingLevelReferences)
				main.data.strat.verifyBuildingLevelOrBuildingExists(reference)
		}
	}

	private fun checkRequirements()
	{
		for(building in main.data.strat.buildings.getAll())
		{
			for(level in building.buildingLevels.getAll())
			{
				checkBuildingRequirementsHolder(building, level, level, "")
				for(upgrade in level.upgrades)
					checkBuildingRequirementsHolder(building, level, upgrade, "upgrade ")
				for(capability in level.generalCapabilities)
					checkBuildingRequirementsHolder(building, level, capability, "capability ")
				for(capability in level.recruitmentCapabilities)
					checkBuildingRequirementsHolder(building, level, capability, "recruitment ")
			}
		}
	}

	private fun checkBuildingRequirementsHolder(building :BuildingEntry, level :BuildingLevelEntry, requirementsHolder :BuildingRequirementsHolder, locationName :String)
	{
		for(buildingReference in requirementsHolder.buildingReferences)
		{
			if(main.data.strat.buildings[buildingReference.reference, true] == null)
				main.writeStratmapLog(buildingReference.filename, buildingReference.lineNumber, "Building ${building.name}'s level ${level.name}'s $locationName requirements has reference to non-existent building ${buildingReference.reference}.")
		}
		for(levelReference in requirementsHolder.buildingLevelReferences)
		{
			var exists = false
			for(referencedBuilding in main.data.strat.buildings.getAll())
			{
				if(referencedBuilding.buildingLevels[levelReference.reference, true] != null)
				{
					exists = true
					break
				}
			}
			if(!exists)
				main.writeStratmapLog(levelReference.filename, levelReference.lineNumber, "Building ${building.name}'s level ${level.name}'s $locationName requirements has reference to non-existent building level ${levelReference.reference}.")
		}
		for(reference in requirementsHolder.factionRequirements)
		{
			if(Util.equalsAny(reference.reference, "all", ""))
				continue
			val faction = main.data.strat.factionEntries[reference.reference]
			if(faction == null)
			{
				//Probably a culture
				val culture = main.data.strat.cultureEntries[reference.reference]
				if(culture == null)
					main.writeStratmapLog(reference.filename, reference.lineNumber, "Reference to faction/culture ${reference.reference}, which does not exist.")
				else
				{
					val factionsInCulture = main.data.strat.getAllFactionNames(reference.reference)
					if(factionsInCulture.size == 0)
						main.writeStratmapLog(reference.filename, reference.lineNumber, "Reference to faction/culture ${reference.reference}, which has no member factions.")
				}
			}
		}
		for(reference in requirementsHolder.resourceRequirements)
		{
			val resource = main.data.strat.resources[reference.reference, true]
			if(resource == null)
				main.writeStratmapLog(reference.filename, reference.lineNumber, "Reference to non-existent campaign map resource ${reference.reference}")
			else if(reference.isForHiddenResource && !resource.isHidden)
				main.writeStratmapLog(reference.filename, reference.lineNumber, "Reference to hidden resource ${reference.reference}. It exists but is visible.")
			else if(!reference.isForHiddenResource && resource.isHidden)
				main.writeStratmapLog(reference.filename, reference.lineNumber, "Reference to visible resource ${reference.reference}. It exists, but is hidden.")
		}
		for(reference in requirementsHolder.religionReferences)
		{
			val religion = main.data.strat.religions[reference.reference, true]
			if(religion == null)
				main.writeStratmapLog(reference.filename, reference.lineNumber, "Reference to non-existent religion ${reference.reference}")
		}
	}

	private fun stratmapModels()
	{
		for(model in main.data.strat.stratModels.getAll())
		{
//			TemporaryClassCrossChecker.crosscheckFileReference(main, model.modelAssignment.modelFile, null, null, model.name, model.lineNumber, true);
//			TemporaryClassCrossChecker.crosscheckFileReference(main, model.modelAssignment.shadowModelFile, null, null, model.name, model.lineNumber, true);
			val skeleton = main.data.unit.skeletons[model.skeleton, true]
			if(skeleton == null) main.writeStratmapLog(model.filename, model.lineNumber, """Skeleton reference "${model.skeleton}" does not exist.""")
			for(texture in model.textureAssignments)
			{
				if(main.data.strat.factionEntries[texture.faction] == null)
					main.writeStratmapLog(model.filename, model.lineNumber, """${model.name}'s texture line refers to non-existent faction "${texture.faction}".""")
			}
		}
	}

	private fun factionsAndCultures()
	{
		var papacy :FactionEntry? = null
		var slave :FactionEntry? = null
		for(faction in main.data.strat.factionEntries.values)
		{
			if(main.data.strat.cultureEntries[faction.culture] == null && faction.name != "merc")
				main.writeStratmapLog("""Faction "${faction.name}" has culture ${faction.culture} which does not exist""")
		}
		for(faction in main.data.strat.factionEntries.values)
		{
 			if(faction.isHorde() && faction.hordeUnits.size == 0)
				main.writeStratmapLog("""Faction "${faction.name}" has at least one horde attribute but no horde units defined. Either define horde units or remove any of these attributes: horde_min_units, horde_max_units, horde_max_units_reduction_every_horde, horde_unit_per_settlement_population, horde_min_named_characters, horde_max_percent_army_stack, horde_disband_percent_on_settlement_capture.""")
			for(i in 0 until faction.hordeUnits.size)
			{
				val hordeUnit :EduEntry? = main.data.unit.eduEntries[faction.hordeUnits[i]]
				if(hordeUnit == null)
					main.writeStratmapLog("Faction ${faction.name} uses horde unit ${faction.hordeUnits[i]} which does not exist.")
			}
		}
		for(faction in main.data.strat.factionEntries.values)
		{
			if(main.data.strat.cultureEntries[faction.culture] == null && faction.name != "merc")
				main.writeStratmapLog("""Faction "${faction.name}" has culture ${faction.culture} which does not exist""")
		}
		for(faction in main.data.strat.factionEntries.values)
		{
			if(faction.isPapacy)
			{
				if(papacy != null)
					main.writeStratmapLog("There are more than one papacy factions, including ${faction.name}")
				papacy = faction
			}
			if(faction.isSlave)
			{
				if(slave != null)
					main.writeStratmapLog("There are more than one slave factions, including ${faction.name}")
				slave = faction
			}
		}
		if(slave == null)
			main.writeStratmapLog("Your mod does not have any slave faction!")

		for(culture in main.data.strat.cultureEntries.values)
		{
			val factions = main.data.strat.getAllFactionNames(culture.name)
			if(factions.size == 0)
				main.writeStratmapLog("Culture ${culture.name} has no member factions!")
			for(faction in factions)
			{
				for(agentFileReference in culture.agentFileReferences)
				{
					val fileLocation = "ui/units/$faction/${agentFileReference.reference}"
					main.checkFileReference(FileReferenceRecord(agentFileReference.filename, agentFileReference.lineNumber, "Culture ${culture.name}'s agent files for faction $faction", fileLocation))
				}
				for(agentFileReference in culture.agentInfoCards)
				{
					val fileLocation = "ui/unit_info/$faction/${agentFileReference.reference}"
					main.checkFileReference(FileReferenceRecord(agentFileReference.filename, agentFileReference.lineNumber, "Culture ${culture.name}'s agent files for faction $faction", fileLocation))
				}
			}
		}
	}

	private fun namesAndLabels()
	{
		for(faction in main.data.strat.names.keys)
		{
			val names = main.data.strat.names[faction]
/*			ArrayList<String> list = names.getWomenNames();
			int listSize = list.size();
			for(int i = 0; i < listSize; i++)
			{
				for(int j = i + 1; j < listSize; j++)
				{
					if(list.get(i).equals(list.get(j)))
						main.writeStratmapLog("Faction " + faction + " uses first name " + list.get(i) + " more than once for women.");
				}
			}
			list = names.getCharacterNames();
			listSize = list.size();
			for(int i = 0; i < listSize; i++)
			{
				for(int j = i + 1; j < listSize; j++)
				{
					if(list.get(i).equals(list.get(j)))
						main.writeStratmapLog("Faction " + faction + " uses first name " + list.get(i) + " more than once for men.");
				}
			}
			list = names.getWomenNames();
			listSize = list.size();
			for(int i = 0; i < listSize; i++)
			{
				for(int j = i + 1; j < listSize; j++)
				{
					if(list.get(i).equals(list.get(j)))
						main.writeStratmapLog("Faction " + faction + " uses surname " + list.get(i) + " more than once.");
				}
			}
*/
			for(name in names!!.womenNames)
			{
				for(translation in main.data.strat.nameText.keys)
				{
					if(!main.data.strat.nameText[translation]!!.containsKey(name))
						main.writeStratmapLog("Faction $faction defines woman name $name in descr_names.txt. Translation $translation does not provide any display text for this name.")
				}
			}
			for(name in names.characterNames)
			{
				for(translation in main.data.strat.nameText.keys)
				{
					if(!main.data.strat.nameText[translation]!!.containsKey(name))
						main.writeStratmapLog("Faction $faction defines male first name $name in descr_names.txt. Translation $translation does not provide any display text for this name.")
				}
			}
			for(name in names.characterSurnames)
			{
				for(translation in main.data.strat.nameText.keys)
				{
					if(!main.data.strat.nameText[translation]!!.containsKey(name))
						main.writeStratmapLog("Faction $faction defines surname $name in descr_names.txt. Translation $translation does not provide any display text for this name.")
				}
			}
		}
		for(translation in main.data.strat.nameText.keys)
		{
			for(name in main.data.strat.nameText[translation]!!.keys)
			{
				var found = false
				for(faction in main.data.strat.names.keys)
				{
					val factionNames = main.data.strat.names[faction]
					found = factionNames!!.characterSurnames.contains(name) || factionNames.characterNames.contains(name) || factionNames.womenNames.contains(name)
					if(found)
						break
				}
				if(!found)
					main.writeStratmapLog("Translation $translation includes name text for name code $name, but this name code is not used by any faction for neither surname, male first name nor female first name.")
			}
		}

		for(character :MapCharacter in main.data.strat.mapCharacters)
		{
			val tokens = StringUtil.split(character.name, " ")
			var relevantFaction = character.ownerFaction
			if(character.subFaction != null)
				relevantFaction = character.subFaction!!
			val factionNames :FactionCharacterNames = main.data.strat.names[relevantFaction]!!
			if(character.isFemale && !factionNames.womenNames.contains(tokens[0]))
				main.writeStratmapLog(character.filename, character.lineNumber, "Map character (${character.type}) uses first name ${tokens[0]}, which is not a female name for faction ${relevantFaction}.")
			if(!character.isFemale && !factionNames.characterNames.contains(tokens[0]))
				main.writeStratmapLog(character.filename, character.lineNumber, "Map character (${character.type}) uses first name ${tokens[0]}, which is not a male name for faction ${relevantFaction}.")
			if(tokens.size > 1 && !factionNames.characterSurnames.contains(tokens[1]))
				main.writeStratmapLog(character.filename, character.lineNumber, "Map character uses surname ${tokens[1]}, which is not defined for faction ${relevantFaction}.")
		}
	}

	private fun missions()
	{
		//Paybacks and their conditions
		for(mission :MissionEntry in main.data.strat.missions)
		{
			var unconditionalFoundIndex :Int? = null
			for(i in 0 until mission.paybacks.size)
			{
				val payback :MissionPayback = mission.paybacks[i]
				val payout :MissionPayout? = main.data.strat.missionPayouts[payback.payoutId, true]
				if(payout == null)
					main.writeStratmapLog(mission.filename, mission.lineNumber, "Mission ${mission.name} uses payout ${payback.payoutId} which does not exist.")
				if(payback.conditions.size == 0 && unconditionalFoundIndex == null)
					unconditionalFoundIndex = i
				for(condition :MissionPaybackCondition in payback.conditions)
				{
					if(!validMissionConditions.contains(condition.name))
						main.writeStratmapLog(mission.filename, mission.lineNumber, "Unrecognized payout condition ${condition.name}.")
					when(condition.name)
					{
						"cash" ->
						{
							try { condition.value.toInt() }
							catch(e :NumberFormatException) { main.writeStratmapLog(mission.filename, mission.lineNumber, "Payout condition cash has non-integer value: ${condition.value}") }
						}
						"papal_standing", "difficulty" ->
						{
							try { condition.value.toDouble() }
							catch(e :NumberFormatException) { main.writeStratmapLog(mission.filename, mission.lineNumber, "Payout condition ${condition.name} has non-float value: ${condition.value}") }
						}
						"random" ->
						{
							try
							{
								val doubleValue :Double = condition.value.toDouble()
								if(doubleValue > 1)
									main.writeStratmapLog(mission.filename, mission.lineNumber, "Payout condition random exceeds 1 (more than 100% chance).")
								if(doubleValue < 0)
									main.writeStratmapLog(mission.filename, mission.lineNumber, "Payout condition random below 0 (less than 0% chance).")
							}
							catch(e :NumberFormatException)
							{
								main.writeStratmapLog(mission.filename, mission.lineNumber, "Payout condition random has non-float value: ${condition.value}")
							}
						}
					}
				}
			}
			if(unconditionalFoundIndex == null)
				main.writeStratmapLog(mission.filename, mission.lineNumber, "Mission ${mission.name} lacks an unconditional (default) payout.")
			else if(unconditionalFoundIndex < mission.paybacks.size - 1)
				main.writeStratmapLog(mission.filename, mission.lineNumber, "Mission ${mission.name} has an unconditional (default) payout before others, making the subsequent ones unreachable.")
		}

		//References
		for(mission :MissionEntry in main.data.strat.missions)
		{
			for(religion :SimpleReferenceRecord in mission.eligibleReligions)
			{
				if(main.data.strat.religions[religion.reference, false] == null)
					main.writeStratmapLog(mission.filename, mission.lineNumber, "Mission refers to non-existent religion ${religion.reference}")
			}
			for(religion :SimpleReferenceRecord in mission.religionModifiers)
			{
				if(main.data.strat.religions[religion.reference, false] == null)
					main.writeStratmapLog(mission.filename, mission.lineNumber, "Mission refers to non-existent religion ${religion.reference}")
			}
			if(mission.resourceTarget != null && main.data.strat.resources[mission.resourceTarget, true] == null)
				main.writeStratmapLog(mission.filename, mission.lineNumber, "Mission refers to non-existent resource ${mission.resourceTarget} as required content for its target province")

			for(buildingLevel :String in mission.buildingTargets)
			{
				var found = false
				for(building :BuildingEntry in main.data.strat.buildings.getAll())
				{
					if(building.buildingLevels[buildingLevel, true] != null)
						found = true
				}
				if(!found)
					main.writeStratmapLog(mission.filename, mission.lineNumber, "Mission refers to non-existent building level $buildingLevel")
			}

			for(faction :String in mission.factions)
			{
				if(main.data.strat.factionEntries[faction] == null)
					main.writeStratmapLog(mission.filename, mission.lineNumber, "Mission refers to non-existent faction $faction")
			}
		}

		//Image files
		val popeMissionCultures = HashMap<String, CultureEntry>()
		for(faction :FactionEntry in main.data.strat.factionEntries.values)
		{
			if(faction.isEligibleForPopeMissions && popeMissionCultures[faction.culture] == null)
				popeMissionCultures[faction.culture] = main.data.strat.cultureEntries[faction.culture]!!
		}
		for(mission :MissionEntry in main.data.strat.missions)
		{
			if(mission.client == "pope_mission")
			{
				for(culture :CultureEntry in popeMissionCultures.values)
					checkMissionImages(mission, culture)
			}
			else
			{
				for(culture :CultureEntry in main.data.strat.cultureEntries.values)
					checkMissionImages(mission, culture)
			}
		}
		for(mission :MissionEntry in main.data.strat.missions)
		{
			if(mission.client == "")
				continue
			if(main.data.text.expandedText["${mission.client}_source", true] == null && mission.client != "faction_mission")
				main.writeStratmapLog(mission.filename, mission.lineNumber, "Missing client text ${mission.client}_source in text/expanded.txt")
			if(main.data.text.expandedText["${mission.client}_expire", true] == null)
				main.writeStratmapLog(mission.filename, mission.lineNumber, "Missing client text ${mission.client}_expire in text/expanded.txt")
			if(main.data.text.expandedText["${mission.client}_fail", true] == null)
				main.writeStratmapLog(mission.filename, mission.lineNumber, "Missing client text ${mission.client}_fail in text/expanded.txt")
			if(main.data.text.expandedText["${mission.client}_given", true] == null)
				main.writeStratmapLog(mission.filename, mission.lineNumber, "Missing client text ${mission.client}_given in text/expanded.txt")
			if(main.data.text.expandedText["${mission.client}_success", true] == null)
				main.writeStratmapLog(mission.filename, mission.lineNumber, "Missing client text ${mission.client}_success in text/expanded.txt")
		}

		for(i in 0 until main.data.strat.missions.size)
		{
			val test :MissionEntry = main.data.strat.missions[i]
			for(j in i + 1 until main.data.strat.missions.size)
			{
				val comparison :MissionEntry = main.data.strat.missions[j]
				if(test.name == comparison.name && test.variant == comparison.variant)
					main.writeStratmapLog(test.filename, test.lineNumber, "mission ${test.name} (variant ${test.variant}) is duplicated at ${comparison.filename}:${comparison.lineNumber}. One of them should change variant name.")
			}
		}
	}

	private fun checkMissionImages(mission :MissionEntry, culture :CultureEntry)
	{
		if(mission.issuedImage != "")
			main.checkFileReference(FileReferenceRecord(mission.filename, mission.lineNumber, mission.name, "ui/${culture.name}/eventpics/${mission.issuedImage}.tga"))
		if(mission.expiredImage != "")
			main.checkFileReference(FileReferenceRecord(mission.filename, mission.lineNumber, mission.name, "ui/${culture.name}/eventpics/${mission.expiredImage}.tga"))
		if(mission.failedImage != "")
			main.checkFileReference(FileReferenceRecord(mission.filename, mission.lineNumber, mission.name, "ui/${culture.name}/eventpics/${mission.failedImage}.tga"))
		if(mission.successImage != "")
			main.checkFileReference(FileReferenceRecord(mission.filename, mission.lineNumber, mission.name, "ui/${culture.name}/eventpics/${mission.successImage}.tga"))
	}

	private fun missionPaybacks()
	{
		for(payout :MissionPayout in main.data.strat.missionPayouts.getAll())
		{
			for(reward :MissionReward in payout.rewards)
			{
				if(reward.thing == "null_payback")
				{
					if(main.data.text.expandedText["${reward.amountOrModifier}_pre_descr", true] == null)
						main.writeStratmapLog(payout.filename, payout.lineNumber, "Payout ${payout.name} has null_payback reward ${reward.amountOrModifier}, its issued description ${reward.amountOrModifier}_pre_descr is missing in expanded.txt")
					if(main.data.text.expandedText["${reward.amountOrModifier}_descr", true] == null)
						main.writeStratmapLog(payout.filename, payout.lineNumber, "Payout ${payout.name} has null_payback reward ${reward.amountOrModifier}, its fulfilled description ${reward.amountOrModifier}_descr is missing in expanded.txt")
				}
			}
			for(reward :MissionReward in payout.penalties)
			{
				if(reward.thing == "null_payback")
				{
					if(main.data.text.expandedText["${reward.amountOrModifier}_pre_descr", true] == null)
						main.writeStratmapLog(payout.filename, payout.lineNumber, "Payout ${payout.name} has null_payback penalty ${reward.amountOrModifier}, its threat description ${reward.amountOrModifier}_pre_descr is missing in expanded.txt")
					if(main.data.text.expandedText["${reward.amountOrModifier}_descr", true] == null)
						main.writeStratmapLog(payout.filename, payout.lineNumber, "Payout ${payout.name} has null_payback penalty ${reward.amountOrModifier}, its punishment description ${reward.amountOrModifier}_descr is missing in expanded.txt")
				}
			}
		}
	}

	private fun settlements()
	{
		for(settlement :MapSettlement in main.data.strat.mapSettlements)
		{
			val ownerFactionEntry :FactionEntry? = main.data.strat.factionEntries[settlement.ownerFaction]
			if(ownerFactionEntry == null)
				main.writeStratmapLog(settlement.filename, settlement.lineNumber, "Settlement in region ${settlement.region} is owned by faction ${settlement.ownerFaction} which does not exist.")

			if(settlement.creatorFaction == null)
				main.writeStratmapLog(settlement.filename, settlement.lineNumber, "Settlement in region ${settlement.region} has no creator faction.")
			else
			{
				val creatorFactionEntry :FactionEntry? = main.data.strat.factionEntries[settlement.creatorFaction]
				if(creatorFactionEntry == null)
					main.writeStratmapLog(settlement.filename, settlement.lineNumber, "Settlement in region ${settlement.region} has creator faction ${settlement.creatorFaction} which does not exist.")
			}

			for(building :String in settlement.buildingsPresent)
			{
				val buildingSplit :List<String> = building.split(" ".toRegex())
				val buildingName = buildingSplit[0]
				val buildingLevelName = buildingSplit[1]
				val buildingEntry = main.data.strat.buildings[buildingName, true]
				if(buildingEntry == null)
				{
					main.writeStratmapLog(settlement.filename, settlement.lineNumber, "Settlement in region ${settlement.region} includes a building $buildingName which does not exist.")
					continue
				}
				val buildingLevelEntry = buildingEntry.buildingLevels[buildingLevelName, true]
				if(buildingLevelEntry == null)
				{
					main.writeStratmapLog(settlement.filename, settlement.lineNumber, "Settlement in region ${settlement.region} includes a building $buildingName whose level ${buildingLevelName} does not exist.")
					continue
				}
				if(settlement.isCity && buildingLevelEntry.cityCastleRequirement == "castle")
					main.writeStratmapLog(settlement.filename, settlement.lineNumber, "Settlement in region ${settlement.region} includes a building $buildingName, which is marked as belonging to CASTLE provinces, but this settlement is a CITY.")
				if(!settlement.isCity && buildingLevelEntry.cityCastleRequirement == "city")
					main.writeStratmapLog(settlement.filename, settlement.lineNumber, "Settlement in region ${settlement.region} includes a building $buildingName, which is marked as belonging to CITY provinces, but this settlement is a CASTLE.")
			}
		}
	}

	fun listUnused()
	{
		for(model :StratModelEntry in main.data.strat.stratModels.getUnused())
		{
			if(!main.lists.acceptedUnusedStratModels.contains(model.name))
				main.writeStratmapLog(model.filename, model.lineNumber, """Strat model "${model.name}" is never used by strat characters.""")
		}
		for(payout :MissionPayout in main.data.strat.missionPayouts.getUnused())
		{
			main.writeStratmapLog(payout.filename, payout.lineNumber, """Mission payout "${payout.name}" is not used by any missions.""")
		}
	}

	private fun validSettlementLevels() :ArrayList<String>
	{
		val retur = ArrayList<String>()
		retur.add("village")
		retur.add("town")
		retur.add("large_town")
		retur.add("city")
		retur.add("large_city")
		retur.add("huge_city")
		return retur
	}

	private fun validAgents() :ArrayList<String>
	{
		val retur = ArrayList<String>()
		retur.add("spy")
		retur.add("merchant")
		retur.add("diplomat")
		retur.add("assassin")
		retur.add("priest")
		return retur
	}

	private fun validMissionConditions() :ArrayList<String>
	{
		val retur = ArrayList<String>()
		retur.add("random")
		retur.add("papal_standing")
		retur.add("difficulty")
		retur.add("cash")
		return retur
	}
}