@file:Suppress("SameParameterValue")

package sources.code

import data.code.trait.*
import data.common.SimpleReferenceRecord
import main.BovineM2twCheck
import util.StringUtil
import java.io.*
import java.util.*

class TraitReader(private val main :BovineM2twCheck)
{
	private val filename = "export_descr_character_traits.txt"

	private val irrelevantTraitConditionTokens by lazy { irrelevantTraitConditionTokens() }
	private val irrelevantTraitConditionClauses by lazy { irrelevantTraitConditionClauses() }

	private var traitEntry = TraitEntry("dummy", -1)
	private var traitLevel = TraitLevel("dummy")
	private var triggerEntry = TraitTriggerEntry("dummy", filename, -1)

	fun readAll()
	{
//		readTraitDescriptions()
		readTraits()
	}

	private fun readTraits()
	{
		var readLine :String? = null
		var lineNumber = 0
		try
		{
			main.writeOutput(filename)
			val traitsFile = BufferedReader(FileReader(main.runCfg.dataFolder + filename))
			while(run { readLine = traitsFile.readLine(); readLine } != null)
			{
				lineNumber++
				//Ignore case, starting whitespace, multiple spaces and comments. Ignore comparison signs unless they separate tokens.
				var line :String = readLine!!
						.replace("=", " ")
						.replace(">", " ")
						.replace("<", " ")
						.replace("!", " ")
				line = StringUtil.standardize(line)
				if(line == "")
					continue
				val tokens = StringUtil.split(line.trim(), " ")

				if(!parseTraitLine(tokens, filename, lineNumber))
					parseTriggerLine(tokens, filename, lineNumber)
			}
			traitsFile.close()
		}
		catch(e :FileNotFoundException)
		{
			main.writeOutput("Cannot find the EDCT file (${main.runCfg.dataFolder}$filename)")
			main.writeOutput("No checks have been performed on the traits.")
			main.writeOutput("This is okay if you are ONLY using vanilla traits, if not you may have entered your mod's data folder wrong.")
		}
		catch(e :Exception)
		{
			main.fatalParsingError(lineNumber, readLine!!, e)
		}
	}

	private fun parseTraitLine(tokens :Array<String>, filename :String, lineNumber :Int) :Boolean
	{
		//Trait clauses
		when(tokens[0])
		{
			"trait" ->
			{
				traitEntry = TraitEntry(tokens[1], lineNumber)
				main.data.code.traits.add(traitEntry)
			}
			"characters" ->
			{
				for(i in 1 until tokens.size)
				{
					if(tokens[i] != "")
						traitEntry.targetCharacterTypes.add(StringUtil.before(tokens[i], ","))
				}
			}
			"hidden" ->
				traitEntry.isHidden = true
			"nogoingbacklevel" ->
				traitEntry.noGoingBackLevel = tokens[1].toInt()
			"antitraits" ->
			{
				for(i in 1 until tokens.size)
				{
					if(tokens[i] != "")
						traitEntry.antiTraits.add(StringUtil.before(tokens[i], ","))
				}
			}
			"excludecultures" ->
			{
				for(i in 1 until tokens.size)
				{
					val culture = StringUtil.before(tokens[i], ",")
					if(culture != "")
						traitEntry.excludedCultures.add(SimpleReferenceRecord(culture, filename, lineNumber))
				}
			}
			"level" ->
			{
				traitLevel = TraitLevel(tokens[1])
				traitEntry.traitLevels.add(traitLevel)
			}
			"description" ->
				traitLevel.description = tokens[1]
			"effectsdescription" ->
				traitLevel.effectsDescription = tokens[1]
			"epithet" ->
				traitLevel.epithetDescription = tokens[1]
			"gainmessage" ->
				traitLevel.gainMessage = tokens[1]
			"losemessage" ->
				traitLevel.loseMessage = tokens[1]
			"threshold" ->
				traitLevel.threshold = tokens[1].toInt()
			"effect" ->
			{
				var effectName = tokens[1]
				if(effectName.startsWith("combat_v_"))
				{
					effectName = StringUtil.after(effectName, "combat_v_")
					when
					{
						effectName.startsWith("faction_") ->
							traitEntry.factionReferences.add(SimpleReferenceRecord(StringUtil.after(effectName, "faction_"), filename, lineNumber))
						effectName.startsWith("religion_") ->
							traitEntry.religionReferences.add(SimpleReferenceRecord(StringUtil.after(effectName, "religion_"), filename, lineNumber))
						else ->
							traitLevel.effects.add(SimpleReferenceRecord(tokens[1], filename, lineNumber))
					}
				}
				else
					traitLevel.effects.add(SimpleReferenceRecord(tokens[1], filename, lineNumber))
			}
			else ->
				return false
		}
		return true
	}

	private fun parseTriggerLine(tokens :Array<String>, filename :String, lineNumber :Int) :Boolean
	{
		var parsed = true
		//Keywords
		when(tokens[0])
		{
			"trigger" ->
			{
				if(tokens.size < 2)
				{
					main.writeSundryLog("$filename $lineNumber: Unnamed trigger. All trait triggers should have names.")
					triggerEntry = TraitTriggerEntry("(Unnamed)", filename, lineNumber)
				}
				else
					triggerEntry = TraitTriggerEntry(tokens[1], filename, lineNumber)
				main.data.code.traitTriggers.add(triggerEntry)
			}
			"whentotest" ->
				triggerEntry.triggeringEvent = tokens[1]
			"affects" ->
				triggerEntry.affects.add(AffectClause(tokens))
			else ->
				parsed = false
		}
		//Condition details
		if(!parsed)
		{
			for(i in tokens.indices)
			{
				if(irrelevantTraitConditionClauses.contains(tokens[i]))
					break
				if(irrelevantTraitConditionTokens.contains(tokens[i]))
					continue
				when(tokens[i])
				{
					"isgeneral" ->
						triggerEntry.isGeneralInvoked = true
					"i_eventcounter" ->
						main.data.code.addCheckedEventCounterLocation(SimpleReferenceRecord(tokens[i + 1], filename, lineNumber))
					"i_settlementowner" ->
					{
						triggerEntry.referredSettlements.add(SimpleReferenceRecord(tokens[i + 1], filename, lineNumber))
						triggerEntry.referredFactions.add(SimpleReferenceRecord(tokens[i + 2], filename, lineNumber))
					}
					"settlementname" ->
						triggerEntry.referredSettlements.add(SimpleReferenceRecord(tokens[i + 1], filename, lineNumber))
					"attribute", "fatherattribute", "factionleaderattribute", "spouseattribute", "highestattadjacentchar" ->
						triggerEntry.referredAttributes.add(SimpleReferenceRecord(tokens[i + 1], filename, lineNumber))
					"i_factionleaderattribute" ->
					{
						triggerEntry.referredFactions.add(SimpleReferenceRecord(tokens[i + 1], filename, lineNumber))
						triggerEntry.referredAttributes.add(SimpleReferenceRecord(tokens[i + 2], filename, lineNumber))
					}
					"percentageunitattribute" ->
						triggerEntry.referredUnitAttributes.add(SimpleReferenceRecord(tokens[i + 1], filename, lineNumber))
					"culturetype", "generalfoughtculture", "targetfactionculturetype" ->
						triggerEntry.referredCultures.add(SimpleReferenceRecord(tokens[i + 1], filename, lineNumber))
					"trait", "fathertrait", "factionleadertrait", "spousetrait" ->
						triggerEntry.referredTraits.add(TraitReferenceRecord(filename, lineNumber, tokens[i + 1], tokens[i + 2]))
					"i_factionleadertrait" ->
					{
						triggerEntry.referredFactions.add(SimpleReferenceRecord(tokens[i + 1], filename, lineNumber))
						triggerEntry.referredTraits.add(TraitReferenceRecord(filename, lineNumber, tokens[i + 2], tokens[i + 3]))
					}
					"factiontype", "targetfactiontype", "generalfoughtfaction", "diplomaticstancefromfaction", "i_isfactionaicontrolled", "originalfactiontype", "i_numberofsettlements", "i_charactertypeneartile", "charfactiontype", "i_numberofheirs" ->
						triggerEntry.referredFactions.add(SimpleReferenceRecord(tokens[i + 1], filename, lineNumber))
					"diplomaticstancefromcharacter" ->
					{
						triggerEntry.referredFactions.add(SimpleReferenceRecord(tokens[i + 1], filename, lineNumber))
						triggerEntry.referredDiplomaticStances.add(SimpleReferenceRecord(tokens[i + 2], filename, lineNumber))
					}
					"diplomaticstancefactions" ->
						triggerEntry.referredDiplomaticStances.add(SimpleReferenceRecord(tokens[i + 1], filename, lineNumber))
					"advisebuild", "settlementbuildingexists", "settlementbuildingfinished", "buildingfinishedbygovernor", "governorbuildingexists", "numbuildingscompletedfaction", "factionbuildingexists" ->
						triggerEntry.referredBuildings.add(SimpleReferenceRecord(tokens[i + 1], filename, lineNumber))
					"characterreligion", "religious_belief", "religious_order", "factionreligion", "neighbourreligion", "religion", "targetreligion" ->
						triggerEntry.referredReligions.add(SimpleReferenceRecord(tokens[i + 1], filename, lineNumber))
					"hasanctype" ->
						triggerEntry.referredAncillaries.add(SimpleReferenceRecord(tokens[i + 1], filename, lineNumber))
					"missionid" ->
						triggerEntry.referredMissions.add(SimpleReferenceRecord(tokens[i + 1], filename, lineNumber))
					"paybackid" ->
						triggerEntry.referredMissionPaybacks.add(SimpleReferenceRecord(tokens[i + 1], filename, lineNumber))
					"settlementloyaltylevel" ->
						triggerEntry.referredSettlementLoyaltyLevels.add(SimpleReferenceRecord(tokens[i + 1], filename, lineNumber))
					"factionscorerank" ->
						if(tokens.size < i + 3)
						{
							main.writeEdctLog("$filename $lineNumber: Unexpected number of tokens after FactionScoreRank")
							return false
						}
					else ->
					{
						main.writeSundryLog("Unrecognized token in EDCT $lineNumber: ${tokens[i]}. Typo in EDCT or fault in the checker?")
						return false
					}
				}
				break
			}
		}
		return true
	}
	
	private fun irrelevantTraitConditionTokens() :ArrayList<String>
	{
		val tokens = ArrayList<String>()
		tokens.add("condition")
		tokens.add("and")
		tokens.add("not")
		return tokens
	}

	private fun irrelevantTraitConditionClauses() :ArrayList<String>
	{
		val clauses = ArrayList<String>()
		clauses.add("characterislocal")
		clauses.add("settlementislocal")
		clauses.add("isfactionaicontrolled")
		clauses.add("isfactionleader")
		clauses.add("isfactionheir")
		clauses.add("i_turnnumber")
		clauses.add("factionincome")
		clauses.add("agenttype")
		clauses.add("isadmiral")
		clauses.add("ransomamount")
		clauses.add("missionsuccesslevel")
		clauses.add("characterage")
		clauses.add("governorloyaltylevel")
		clauses.add("characternumturnsidle")
		clauses.add("ransomtype")
		clauses.add("distancecapital")
		clauses.add("noactionthisturn")
		clauses.add("timewitharmy")
		clauses.add("ismarried")
		clauses.add("endedinsettlement")
		clauses.add("randompercent")
		clauses.add("wonbattle")
		clauses.add("wasattacker")
		clauses.add("battlesuccess")
		clauses.add("generalfoughtincombat")
		clauses.add("numfriendsinbattle")
		clauses.add("numcapturedcharacters")
		clauses.add("treasury")
		clauses.add("timeinregion")
		clauses.add("inenemylands")
		clauses.add("buildingqueueidledespitecash")
		clauses.add("trainingqueueidledespitecash")
		clauses.add("governortaxlevel")
		clauses.add("governorinresidence")
		clauses.add("atsea")
		clauses.add("battleodds")
		clauses.add("percentageenemykilled")
		clauses.add("remainingmppercentage")
		clauses.add("percentageunitcategory")
		clauses.add("i_conflicttype")
		clauses.add("endedinenemyzoc")
		clauses.add("isbesieging")
		clauses.add("isundersiege")
		clauses.add("i_withdrawsbeforebattle")
		clauses.add("percentagebodyguardkilled")
		clauses.add("ally_routs")
		clauses.add("routs")
		clauses.add("generalnumkillsinbattle")
		clauses.add("healthpercentage")
		clauses.add("numcapturedsoldiers")
		clauses.add("numkilledgenerals")
		clauses.add("isnightbattle")
		clauses.add("totalsiegeweapons")
		clauses.add("percentageofarmykilled")
		clauses.add("percentageroutedofffield")
		clauses.add("onawarfooting")
		clauses.add("settlementtaxlevel")
		clauses.add("settlementtype")
		clauses.add("generalhplostratioinbattle")
		clauses.add("i_battleenemyarmynumberofunits")
		clauses.add("populationownreligion")
		clauses.add("percentageofpopulationingarrison")
		clauses.add("isregiononeof")
		clauses.add("missionsucceeded")
		clauses.add("probabilitysuccess")
		clauses.add("campaigndifficulty")
		clauses.add("factionislocal")
		clauses.add("factionhasallies")
		clauses.add("inbarbarianlands")
		clauses.add("tradingmonopoly")
		clauses.add("tradingexotic")
		clauses.add("onresource")
		clauses.add("populationheretic")
		clauses.add("timesinceheresy")
		clauses.add("timesincereligion")
		clauses.add("religionshift")
		clauses.add("iscrusade")
		clauses.add("isoncrusade")
		clauses.add("isjihad")
		clauses.add("isonjihad")
		clauses.add("isregionjihadtarget")
		clauses.add("iscrusadetarget")
		clauses.add("isjihadtarget")
		clauses.add("factionexcommunicated")
		clauses.add("isregioncrusadetarget")
		clauses.add("settlementhasplague")
		clauses.add("settlementpopulationmaxedout")
		clauses.add("settlementstaken")
		clauses.add("i_battlesettlementfortificationlevel")
		clauses.add("inuncivilisedlands")
		return clauses
	}
}