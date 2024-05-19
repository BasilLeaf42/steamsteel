package processing

import data.common.DuplicateCount
import main.BovineM2twCheck
import util.Util

class TraitsAncillaries(private val main :BovineM2twCheck)
{
	private val validTriggerEvents by lazy { validTriggerEvents() }
	private val validAttributes by lazy { validAttributes() }
	private val validTraitCharacterTypes by lazy { validTraitCharacterTypes() }

	fun traitChecks()
	{
		for(dupe in main.data.text.traitDescriptions.getDuplicates())
			main.writeEdctLog("Trait text: Duplicate description ${dupe.name} (${dupe.count})")
		for(trait in main.data.code.traits.getAll())
		{
			if(trait.antiTraits.size > 0)
			{
				for(level in trait.traitLevels)
				{
					if(level.effects.size > 0)
					{
						main.writeEdctLog("Trait ${trait.name} has at least one antitrait and has effects. This will cause problems with effects sticking around when the trait gets reduced!")
						break
					}
				}
				for(anti in trait.antiTraits)
					checkTraitReference("EDCT", trait.lineNumber!!, anti, "Trait ${trait.name} has antitrait %TRAIT% which does not exist.", 1, false)
			}
			for(reference in trait.factionReferences)
			{
				val faction = main.data.strat.factionEntries[reference.reference]
				if(faction == null)
					main.writeEdctLog("${reference.filename} ${reference.lineNumber}: Trait ${trait.name} has combat effects versus faction ${reference.reference} which does not exist.")
			}
			for(reference in trait.religionReferences)
			{
				val religion = main.data.strat.religions[reference.reference, true]
				if(religion == null)
					main.writeEdctLog("${reference.filename} ${reference.lineNumber}: Trait ${trait.name} has combat effects versus religion ${reference.reference} which does not exist.")
			}
			for(reference in trait.excludedCultures)
			{
				val culture = main.data.strat.cultureEntries[reference.reference]
				if(culture == null)
					main.writeEdctLog("${reference.filename} ${reference.lineNumber}: Trait ${trait.name} excludes culture ${reference.reference} which does not exist.")
			}
			for(level in trait.traitLevels)
			{
				if(main.data.text.traitDescriptions[level.levelName, true] == null)
					main.writeEdctLog("""${trait.filename} ${trait.lineNumber} (${trait.name}): Trait level name "${level.levelName}" is not present in export_vnvs.txt""")
				if(main.data.text.traitDescriptions[level.description, true] == null)
					main.writeEdctLog("""${trait.filename} ${trait.lineNumber} (${trait.name}): Trait description "${level.description}" is not present in export_vnvs.txt""")
				if(main.data.text.traitDescriptions[level.effectsDescription, true] == null)
					main.writeEdctLog("""${trait.filename} ${trait.lineNumber} (${trait.name}): Trait effects description "${level.effectsDescription}" is not present in export_vnvs.txt""")
				if(level.gainMessage != null && main.data.text.traitDescriptions[level.gainMessage, true] == null)
					main.writeEdctLog("""${trait.filename} ${trait.lineNumber} (${trait.name}): Trait gain message "${level.gainMessage}" is not present in export_vnvs.txt""")
				if(level.loseMessage != null && main.data.text.traitDescriptions[level.loseMessage, true] == null)
					main.writeEdctLog("""${trait.filename} ${trait.lineNumber} (${trait.name}): Trait lose message "${level.loseMessage}" is not present in export_vnvs.txt""")
				if(level.epithetDescription != null && main.data.text.traitDescriptions[level.epithetDescription, true] == null)
					main.writeEdctLog("""${trait.filename} ${trait.lineNumber} (${trait.name}): Trait epithet description "${level.epithetDescription}" is not present in export_vnvs.txt""")
				for(effect in level.effects)
				{
					if(!validAttributes.contains(effect.reference))
						main.writeEdctLog("""${trait.filename} ${trait.lineNumber} (${trait.name} level ${level.levelName}): Trait effect "${effect.reference}" is not recognized. Typo or fault in the checker?""")
				}
			}
			for(i in trait.traitLevels.indices)
			{
				val testingLevel = trait.traitLevels[i]
				for(j in i + 1 until trait.traitLevels.size)
				{
					if(testingLevel.threshold == trait.traitLevels[j].threshold)
						main.writeEdctLog("${trait.filename} ${trait.lineNumber} (${trait.name}): Trait has multiple levels with threshold ${testingLevel.threshold}.")
				}
			}
			if(!main.runCfg.hiddenTraitsDescriptionSuppression)
			{
				for(level in trait.traitLevels)
				{
					if(trait.isHidden && !Util.equalsAny(level.description, "hidden_desc", "hidden_description_desc"))
						main.writeEdctLog("""Trait "${trait.name}" is hidden but has non-hidden description ${level.description} for level ${level.levelName}.""")
					if(trait.isHidden && level.effectsDescription != "hidden_effects_desc")
						main.writeEdctLog("""Trait "${trait.name}" is hidden but has non-hidden effects description ${level.effectsDescription} for level ${level.levelName}.""")
					if(!trait.isHidden && Util.equalsAny(level.description, "hidden_desc", "hidden_description_desc"))
						main.writeEdctLog("""Trait "${trait.name}" is not hidden but has "hidden" description for level ${level.levelName}.""")
					if(!trait.isHidden && level.effectsDescription == "hidden_effects_desc")
						main.writeEdctLog("""Trait "${trait.name}" is not hidden but has "hidden" effects description for level ${level.levelName}.""")
				}
			}
		}

		for(trait in main.data.code.traits.getAll())
		{
			for(target in trait.targetCharacterTypes)
			{
				if(!validTraitCharacterTypes.contains(target))
					main.writeEdctLog("${trait.filename} ${trait.lineNumber}: Target character type \"$target\" is not recognized. Typo?")
			}
		}
	}

	fun traitTriggerChecks()
	{
		for(trigger in main.data.code.traitTriggers.getAll())
		{
			if(trigger.affects.size > 10)
				main.writeEdctLog("${trigger.filename} ${trigger.lineNumber}: Trigger ${trigger.name} has too many Affects clauses (${trigger.affects.size}), max is 10")
			for(affect in trigger.affects)
			{
				checkTraitReference(trigger.filename!!, trigger.lineNumber!!, affect.traitName, "Attempt to award non-existent trait \"%TRAIT%\"", 1, true)
				if(affect.chance < 1 || affect.chance > 100)
					main.writeEdctLog("${trigger.filename} ${trigger.lineNumber}: Affects clause with chance outside range 1-100")
			}
			for(reference in trigger.referredTraits)
				checkTraitReference(trigger.filename!!, trigger.lineNumber!!, reference.reference, "Attempt to check non-existent trait \"%TRAIT%\"", reference.referencedLevel, false)
			if(trigger.triggeringEvent == "becomesfactionleader")
				main.writeEdctLog("${trigger.filename} ${trigger.lineNumber}: Trigger \"${trigger.name}\" has WhenToTest BecameFactionLeader. This causes crashes when a faction leader dies in the battle when the last faction settlement falls! See https://www.twcenter.net/forums/showthread.php?788509-EDCT-WhenToTest-BecomesFactionLeader-causes-crashes for a workaround which preserves the functionality but prevents crashes.")
			else if(Util.equalsAny(trigger.triggeringEvent, "offeredformarriage", "offeredforadoption"))
			{
				if(trigger.isGeneralInvoked)
					main.writeEdctLog("${trigger.filename} ${trigger.lineNumber}: Trigger \"${trigger.name}\" has WhenToTest ${trigger.triggeringEvent}, and includes an IsGeneral condition. The test is both unnecessary and will fail - only named characters can be offered as such, and the character is not yet considered \"alive\" at the point of offering. He is considered alive when he's placed on the map if you accept.")
			}
			else if(!validTriggerEvents.contains(trigger.triggeringEvent))
				main.writeEdctLog("${trigger.filename} ${trigger.lineNumber}: Trigger \"${trigger.name}\" triggers on unrecognized event ${trigger.triggeringEvent}.")
			for(reference in trigger.referredFactions)
			{
				val faction = main.data.strat.factionEntries[reference.reference]
				if(faction == null)
					main.writeEdctLog("${reference.filename} ${reference.lineNumber}: Trigger \"${trigger.name}\" refers to non-existent faction ${reference.reference}.")
			}
			for(reference in trigger.referredReligions)
			{
				val religion = main.data.strat.religions[reference.reference, true]
				if(religion == null) main.writeEdctLog(reference.filename + " " + reference.lineNumber + ": Trigger \"" + trigger.name + "\" refers to non-existent religion " + reference.reference + ".")
			}
			for(reference in trigger.referredAttributes)
			{
				if(!validAttributes.contains(reference.reference))
					main.writeEdctLog("${reference.filename} ${reference.lineNumber}: Trigger \"${trigger.name}\" refers to unrecognized attribute ${reference.reference}.")
			}
			for(reference in trigger.referredCultures)
			{
				if(main.data.strat.cultureEntries[reference.reference] == null)
					main.writeEdctLog("${reference.filename} ${reference.lineNumber}: Trigger \"${trigger.name}\" refers to unrecognized culture ${reference.reference}.")
			}
		}
		for(dupe in main.data.code.traitTriggers.getDuplicates())
			main.writeEdctLog("There are ${dupe.count} triggers called \"${dupe.name}\".")
	}

	fun listUnused()
	{
		for(trait in main.data.code.traits.getAll())
		{
			if(!trait.isTested && !trait.isAwarded)
				main.writeEdctLog("Trait \"${trait.name}\" is never tested, and never awarded in export_descr_character_traits, export_descr_ancillaries, descr_strat or campaign_script.")
			else if(!trait.isAwarded)
				main.writeEdctLog("Trait \"" + trait.name + "\" is tested, but never awarded in export_descr_character_traits, export_descr_ancillaries, descr_strat or campaign_script.")
		}
		for(unusedAncillaryDescription in main.data.text.ancillaryDescriptions.getUnused())
			main.writeEdaLog("Ancillary description \"${unusedAncillaryDescription.name}\" is not used on any ancillary")
		for(unusedTraitDescription in main.data.text.traitDescriptions.getUnused())
			main.writeEdctLog("${unusedTraitDescription.lineNumber}: Trait description \"${unusedTraitDescription.name}\" is not used on any trait")
	}

	fun checkTraitBuildingReferences()
	{
		for(reference in main.data.code.buildingLevelReferences)
			main.data.strat.verifyBuildingLevelOrBuildingExists(reference)
		for(trigger in main.data.code.traitTriggers.getAll())
		{
			for(reference in trigger.referredBuildings)
				main.data.strat.verifyBuildingLevelOrBuildingExists(reference)
		}
	}

	fun ancillaryChecks()
	{
		for(dupe :DuplicateCount in main.data.text.ancillaryDescriptions.getDuplicates())
			main.writeEdaLog("Ancillary description \"${dupe.name}\" is duplicated (${dupe.count} times)")

		for(reference in main.data.code.edaTraitReferences)
		{
			val trait = main.data.code.traits[reference.reference, false]
			if(trait == null)
				main.writeEdaLog("${reference.filename} ${reference.lineNumber}: Reference to nonexistent trait ${reference.reference}")
			else
			{
				if(reference.awardedAmount != null)
					trait.isAwarded = true
				if(reference.referencedLevel != -1)
				{
					trait.isTested = true
					if(reference.referencedLevel > trait.traitLevels.size)
						main.writeEdaLog("${reference.filename} ${reference.lineNumber}: Test for trait level ${reference.referencedLevel}, ${trait.name} has only ${trait.traitLevels.size} levels.")
				}
			}
		}
	}

	private fun checkTraitReference(referencingFile :String, lineNumber :Int, referencedTrait :String, messageIfNonexistent :String, referencedLevel :Int, referenceIsAwarding :Boolean)
	{
		val trait = main.data.code.traits[referencedTrait, false]
		if(trait == null)
			main.writeEdctLog("$referencingFile $lineNumber: ${messageIfNonexistent.replace("%TRAIT%", referencedTrait)}")
		else
		{
			if(referenceIsAwarding)
				trait.isAwarded = true
			else
				trait.isTested = true
			if(referencedLevel > trait.traitLevels.size)
				main.writeEdctLog("$referencingFile $lineNumber: Test for trait level $referencedLevel, $referencedTrait has only ${trait.traitLevels.size} levels.")
		}
	}

	private fun validTraitCharacterTypes() :ArrayList<String>
	{
		val retur = ArrayList<String>()
		retur.add("all")
		retur.add("family")
		retur.add("diplomat")
		retur.add("spy")
		retur.add("assassin")
		retur.add("admiral")
		retur.add("merchant")
		retur.add("priest")
		retur.add("princess")
		retur.add("inquisitor")
		retur.add("heretic")
		retur.add("witch")
		return retur
	}

	private fun validAttributes() :ArrayList<String>
	{
		val retur = ArrayList<String>()
		//General traits
		retur.add("fertility")
		retur.add("personalsecurity")
		retur.add("briberesistance")
		retur.add("authority")
		retur.add("loyalty")
		retur.add("movementpoints")
		retur.add("lineofsight")
		retur.add("hitpoints")
		retur.add("chivalry")
		retur.add("electability")
		retur.add("boldness")

		//Governor
		retur.add("siegeengineering")
		retur.add("localpopularity")
		retur.add("publicsecurity")
		retur.add("construction")
		retur.add("taxcollection")
		retur.add("trading")
		retur.add("law")
		retur.add("health")
		retur.add("unrest")
		retur.add("squalor")
		retur.add("farming")
		retur.add("mining")
		retur.add("looting")
		retur.add("management")
		retur.add("trainingagents")
		retur.add("trainingunits")
		retur.add("traininganimalunits")

		//Battle
		retur.add("battlesurgery")
		retur.add("bodyguardsize")
		retur.add("bodyguardvalour")
		retur.add("command")
		retur.add("artillerycommand")
		retur.add("gunpowdercommand")
		retur.add("infantrycommand")
		retur.add("cavalrycommand")
		retur.add("navalcommand")
		retur.add("troopmorale")
		retur.add("level")
		retur.add("defence")
		retur.add("attack")
		retur.add("siegeattack")
		retur.add("siegedefence")
		retur.add("ambush")
		retur.add("nightbattle")

		//Diplomatic
		retur.add("charm")
		retur.add("influence")
		retur.add("bribery")

		//Spy
		retur.add("subterfuge")
		retur.add("sabotage")

		//Merchant
		retur.add("finance")

		//Religious agents
		retur.add("piety")
		retur.add("violence")
		retur.add("unorthodoxy")
		retur.add("magic")
		retur.add("heresyimmunity")
		retur.add("eligibility")
		retur.add("purity")

		return retur
	}

	private fun validTriggerEvents() :ArrayList<String>
	{
		val retur = ArrayList<String>()
		//Not really valid, but reported more specifically
		retur.add("becomesfactionleader")

		//Agents and their actions
		retur.add("acceptbribe")
		retur.add("acquisitionmission")
		retur.add("assassinationmission")
		retur.add("briberymission")
		retur.add("cardinalpromoted")
		retur.add("characternearheretic")
		retur.add("characternearwitch")
		retur.add("denouncementmission")
		retur.add("diplomacymission")
		retur.add("executesanassassinonamission")
		retur.add("executesaspyonamission")
		retur.add("priestbecomesheretic")
		retur.add("refusebribe")
		retur.add("sabotagemission")
		retur.add("spymission")
		retur.add("sufferacquisitionattempt")
		retur.add("sufferassassinationattempt")
		retur.add("sufferdenouncementattempt")

		//Character creation and life events
		retur.add("becomesfactionheir")
		retur.add("brotheradopted")
		retur.add("characterbecomesafather")
		retur.add("charactercomesofage")
		retur.add("characterdamagedbydisaster")
		retur.add("charactermarries")
		retur.add("ceasedfactionheir")
		retur.add("ceasedfactionleader")
		retur.add("lessergeneralofferedforadoption")
		retur.add("offeredforadoption")
		retur.add("offeredformarriage")
		retur.add("charactermarriesprincess")
		retur.add("newadmiralcreated")
		retur.add("fatherdiesnatural")

		//Recurring
		retur.add("characterturnendinsettlement")
		retur.add("characterturnend")
		retur.add("characterturnstart")

		//Battle
		retur.add("battlegeneralrouted")
		retur.add("capturedcharacterreleased")
		retur.add("capturedcharacterransomed")
		retur.add("exterminatepopulation")
		retur.add("factionleaderprisonersransomedcaptive")
		retur.add("factionleaderprisonersransomedcaptor")
		retur.add("generalcapturesettlement")
		retur.add("generalassaultsgeneral")
		retur.add("generalprisonersransomedcaptive")
		retur.add("generalprisonersransomedcaptor")
		retur.add("generaltakescrusadetarget")
		retur.add("occupysettlement")
		retur.add("postbattle")
		retur.add("prebattlewithdrawal")
		retur.add("sacksettlement")

		//Actions
		retur.add("agentcreated")
		retur.add("generalabandoncrusade")
		retur.add("generalarrivescrusadetargetregion")
		retur.add("generalassaultsresidence")
		retur.add("generaldevastatestile")
		retur.add("generaljoincrusade")
		retur.add("governoragentcreated")
		retur.add("governorbuildingcompleted")
		retur.add("governorbuildingdestroyed")
		retur.add("governorthrowgames")
		retur.add("governorthrowraces")
		retur.add("governorunittrained")
		retur.add("hiremercenaries")
		retur.add("leaderdestroyedfaction")
		retur.add("leaderorderedassassination")
		retur.add("leaderorderedbribery")
		retur.add("leaderordereddiplomacy")
		retur.add("leaderorderedsabotage")
		retur.add("leaderorderedspyingmission")

		//Happenings
		retur.add("characterselected")
		retur.add("governorcityrebels")
		retur.add("governorcityriots")
		retur.add("insurrection")

		//Missions
		retur.add("leadermissionfailed")
		retur.add("leadermissionsuccess")
		return retur
	}
}