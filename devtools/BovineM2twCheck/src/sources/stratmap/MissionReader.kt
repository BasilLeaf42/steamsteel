package sources.stratmap

import data.common.SimpleReferenceRecord
import data.strat.mission.*
import main.BovineM2twCheck
import util.StringUtil
import util.Util
import java.io.BufferedReader
import java.io.FileNotFoundException
import java.io.FileReader

class MissionReader(private val main :BovineM2twCheck)
{
	private val ignoredMissionParameters by lazy { ignoredMissionParameters() }

	fun readAll()
	{
		val filename = "descr_missions.txt"
		var readLine :String? = null
		var lineNumber = 0
		try
		{
			main.writeOutput(filename)
			val reader = BufferedReader(FileReader(main.runCfg.dataFolder + filename))
			var activePayout :MissionPayout? = null
			var activeMission :MissionEntry? = null
			var activeRewardIsPenalty = false
			var openBracesCount :Int = 0
			var activeSubsection :String = ""
			while(run { readLine = reader.readLine(); readLine } != null)
			{
				var line :String = StringUtil.standardize(readLine!!)
				lineNumber++
				if(line == "")
					continue
				var tokens = StringUtil.split(line, " ")
				when(tokens[0])
				{
					"{" ->
					{
						openBracesCount++
						if(openBracesCount > 2)
							main.writeStratmapLog(filename, lineNumber, "More than two braces opened in mission or mission reward, don't know what to do with this.")
						line = StringUtil.after(line, "{").trim()
					}
					"}" ->
					{
						openBracesCount--
						if(openBracesCount < 0)
							main.writeStratmapLog(filename, lineNumber, "More closing braces than opening braces encountered, don't know what to do with this.")
						line = StringUtil.after(line, "}").trim()
						activeSubsection = ""
					}
				}
				if(line == "")
					continue

				tokens = StringUtil.split(line, " ")
				if(tokens[0] == "payback_list")
				{
					activePayout = MissionPayout(tokens[1], filename, lineNumber)
					main.data.strat.missionPayouts.add(activePayout)
					activeMission = null
					openBracesCount = 0
					continue
				}
				if(tokens[0] == "mission")
				{
					activePayout = null
					val type = tokens[1]
					var variant = tokens[1]
					if(tokens.size > 2)
						variant = tokens[2]
					activeMission = MissionEntry(type, filename, lineNumber, variant)
					main.data.strat.missions.add(activeMission)
					openBracesCount = 0
					continue
				}
				if(activePayout != null)
				{
					if(openBracesCount == 1)
					{
						when(tokens[0])
						{
							"reward" -> activeRewardIsPenalty = false
							"penalty" -> activeRewardIsPenalty = true
							else ->
								main.writeStratmapLog(filename, lineNumber, "Unrecognized element in payback_list: $line")
						}
						continue
					}
					if(openBracesCount == 2)
					{
						val reward = MissionReward()
						reward.thing = tokens[0]
						reward.amountOrModifier = tokens[1]
						if(activeRewardIsPenalty)
							activePayout.penalties.add(reward)
						else
							activePayout.rewards.add(reward)
						continue
					}
				}
				if(activeMission != null)
				{
					if(openBracesCount == 1)
					{
						when(tokens[0])
						{
							"image_path_issued" ->
								activeMission.issuedImage = tokens[1]
							"image_path_expired" ->
								activeMission.expiredImage = tokens[1]
							"image_path_success" ->
								activeMission.successImage = tokens[1]
							"image_path_failed" ->
								activeMission.failedImage = tokens[1]
							"settlement" ->
								activeMission.settlementOwnedCondition = tokens[1]
							"ancillary_type" ->
								activeMission.ancillaryTarget = tokens[1]
							"agent_type" ->
								activeMission.agentTarget = tokens[1]
							"resource_type" ->
								activeMission.resourceTarget = tokens[1]
							"factions" ->
							{
								if(line.indexOf("{") < 0 || line.indexOf("}") < 0)
								{
									main.writeSundryLog("$filename $lineNumber: Mission ${activeMission.name} has faction references without curly brackets {}, these are needed to parse the entry.")
									continue
								}
								line = StringUtil.between(line, "{", "}")!!.replace(",", " ")
								tokens = StringUtil.split(line, " ")
								for(i in 1 until tokens.size)
								{
									if (tokens[i] == "")
										continue
									activeMission.factions.add(tokens[i])
								}
							}
							"guild_handles" ->
							{
								for(i in 1 until tokens.size)
								{
									if(tokens[i] != "")
										activeMission.guildHandles.add(tokens[i])
								}
							}
							"buildings" ->
							{
								var buildingEnumerationString :String = StringUtil.between(line, "{", "}")!!
								buildingEnumerationString = buildingEnumerationString.replace(",", " ").replace("  ", " ")
								val buildingEnumeration :Array<String> = StringUtil.split(buildingEnumerationString.trim(), " ")
								activeMission.buildingTargets.addAll(buildingEnumeration)
							}
							"paybacks", "religion_modifiers", "eligible_religions" ->
								activeSubsection = tokens[0]
							else ->
							{
								when
								{
									ignoredMissionParameters.contains(tokens[0]) ->
										Util.noop()
									activeMission.parsedLines == 0 ->
									{
										activeMission.client = tokens[0]
										activeMission.parsedLines++
									}
									else ->
										main.writeSundryLog("$filename $lineNumber: Unrecognized mission parameter ${tokens[0]}")
								}
							}
						}
					}
					else
					{
						when(activeSubsection)
						{
							"paybacks" ->
								activeMission.paybacks.add(MissionPayback(line))
							"religion_modifiers" ->
								activeMission.religionModifiers.add(MissionReligionModifier(line, filename, lineNumber))
							"eligible_religions" ->
								activeMission.eligibleReligions.add(SimpleReferenceRecord(line, filename, lineNumber))
						}
					}
					activeMission.parsedLines++
				}
			}
			reader.close()
		}
		catch(e :FileNotFoundException)
		{
			main.writeOutput("Unable to find missions definition file ($filename). This will be a problem.")
		}
		catch(e :Exception)
		{
			main.fatalParsingError(lineNumber, readLine!!, e)
		}
	}

	private fun ignoredMissionParameters() :ArrayList<String>
	{
		val retur = ArrayList<String>()
		retur.add("duration")
		retur.add("exclude_duration")
		retur.add("max_duration_modifier")
		retur.add("num_turns_success")
		retur.add("min_turns_distance")
		retur.add("max_turns_distance")
		retur.add("max_search_turns")

		retur.add("turn_start")

		retur.add("difficulty_lower_pfp_bound")
		retur.add("difficulty_upper_pfp_bound")
		retur.add("difficulty_threshold")
		retur.add("lower_diff_threshold")
		retur.add("upper_diff_threshold")
		retur.add("min_strength_balance")

		retur.add("enemy_modifier")
		retur.add("neutral_modifier")
		retur.add("ally_modifier")

		retur.add("per_unit_modifier")
		retur.add("no_garrison_modifier")
		retur.add("garrison_strength")

		retur.add("num_reinforce_units")

		retur.add("max_agreements")

		retur.add("target_modifier")
		retur.add("trade_modifier")
		retur.add("ratio_modifier")
		retur.add("score_modifier")
		retur.add("settlement_score_offset")
		retur.add("army_score_offset")
		retur.add("own_region_army_score_offset")
		retur.add("own_region_modifier")
		retur.add("own_region_score_modifier")
		retur.add("military_access_score_offset")
		retur.add("navy_score_offset")
		retur.add("default_settlement_score_offset")
		retur.add("max_score")
		retur.add("max_loyalty")
		retur.add("max_target_percent_modifier")

		retur.add("settlement_agent_ratio")

		retur.add("min_treasury")
		retur.add("lower_boundary_income")
		retur.add("upper_boundary_income")

		retur.add("religion_thresh")
		retur.add("target_religion_base_offset")
		retur.add("settlement_priest_ratio")

		retur.add("ai_accept_base_chance")
		retur.add("ai_accept_fs_modifier")
		retur.add("ai_accept_gs_modifier")
		retur.add("ai_attacker_modifier")
		retur.add("ai_human_defender_modifier")
		retur.add("ai_papal_defender_modifier")
		retur.add("ai_min_settlements")
		retur.add("ai_sett_modifier")

		retur.add("num_active_missions_modifier")
		retur.add("target_mission_offset")

		retur.add("pfp_thresh")
		retur.add("pfp_lower_boundary")
		retur.add("pfp_upper_boundary")
		retur.add("diff_pfp_lower_bound")
		retur.add("diff_pfp_upper_bound")
		retur.add("target_pfp_score_threshold")
		retur.add("pfp_score_threshold")
		retur.add("leader_pfp_boundary")
		retur.add("heir_pfp_boundary")
		retur.add("papal_standing_boundary")
		retur.add("excommunicated_modifier")
		retur.add("exclude_sea_travel")

		return retur
	}
}