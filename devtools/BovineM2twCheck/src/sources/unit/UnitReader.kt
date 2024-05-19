package sources.unit

import data.unit.EduEntry
import main.BovineM2twCheck
import util.StringUtil
import util.Util
import java.io.BufferedReader
import java.io.FileNotFoundException
import java.io.FileReader

class UnitReader(private val main :BovineM2twCheck)
{
	private val mountReader = MountReader(main)
	private val modelDbReader = ModelDbReader(main)
	private val skeletonReader = SkeletonReader(main)
	private val engineReader = EngineReader(main)
	private val charactersReader = CharactersReader(main)

	private val ignoredDirectives :ArrayList<String> by lazy { ignoredDirectives() }

	fun readWhenever()
	{
		engineReader.readEngines()
		modelDbReader.read()
		mountReader.readMounts()
		skeletonReader.readAll()
		charactersReader.readCharacterTypes()
		readEdu()
	}

	private fun readEdu()
	{
		val filename = "export_descr_unit.txt"
		var readLine :String? = null
		var lineNumber = 0
		try
		{
			main.writeOutput(filename)
			val eduFile = BufferedReader(FileReader(main.runCfg.dataFolder + filename))
			var entry = EduEntry("dummy", "", -1)
			while(run { readLine = eduFile.readLine(); readLine } != null)
			{
				lineNumber++
				var line :String = StringUtil.standardize(readLine!!)
				while(line.endsWith(" "))
					line = line.substring(0, line.length - 1)
				if(line.isEmpty())
					continue
				val tokens :Array<String> = StringUtil.split(line, " ")
				when(tokens[0])
				{
					"type" ->
					{
						entry = EduEntry(StringUtil.after(line, " "), filename, lineNumber)
						main.data.unit.eduEntries[entry.name] = entry
					}
					"dictionary" ->
						entry.dictionaryName = tokens[1]
					"category" ->
						entry.category = tokens[1]
					"voice_type" ->
						entry.voice = tokens[1]
					"accent" ->
						entry.accent = tokens[1]
					"soldier" ->
						entry.soldier = StringUtil.between(line, " ", ",")
					"officer" ->
						entry.officers.add(tokens[1])
					"engine" ->
						entry.engine = tokens[1]
					"mounted_engine" ->
						entry.mountedEngine = tokens[1]
					"mount" ->
						entry.mount = StringUtil.after(line, " ").trim()
					"armour_ug_levels" ->
					{
						for(i in 1 until tokens.size)
							entry.armourLevels.add(tokens[i].replace(",", "").toInt())
					}
					"armour_ug_models" ->
					{
						for(i in 1 until tokens.size)
							entry.armourModels.add(tokens[i].replace(",", ""))
					}
					"attributes" ->
					{
						for(i in 1 until tokens.size)
							entry.attributes.add(tokens[i].replace(",", ""))
					}
					"stat_pri_attr" ->
					{
						for(i in 1 until tokens.size)
							entry.primaryWeaponAttributes.add(tokens[i].replace(",", ""))
					}
					"stat_sec_attr" ->
					{
						for(i in 1 until tokens.size)
							entry.secondaryWeaponAttributes.add(tokens[i].replace(",", ""))
					}
					"stat_ter_attr" ->
					{
						for(i in 1 until tokens.size)
							entry.tertiaryWeaponAttributes.add(tokens[i].replace(",", ""))
					}
					"ownership", "era" ->
					{
						var firstOwnerIndex = 1
						if(tokens[0] == "era")
							firstOwnerIndex = 2
						for(i in firstOwnerIndex until tokens.size)
						{
							val owner :String = tokens[i].replace(",", "")
							when
							{
								owner.isEmpty() ->
									Util.noop()
								owner == "all" ->
								{
									entry.ownership.addAll(main.data.strat.getAllFactionNames(null))
									entry.ownership.remove("merc")
								}
								main.data.strat.factionEntries[owner] != null ->
									entry.ownership.add(owner)
								else ->
								{
									val factionsInCulture = main.data.strat.getAllFactionNames(owner)
									if(factionsInCulture.size > 0)
										entry.ownership.addAll(factionsInCulture)
									else
										entry.ownership.add(owner)
								}
							}
						}
					}
					"banner" ->
					{
						when(tokens[1])
						{
							"faction" ->
								entry.factionBanner = tokens[2]
							"holy" ->
								entry.crusadeBanner = tokens[2]
							"unit" ->
								entry.unitBanner = tokens[2]
							else ->
								main.writeSundryLog("$filename $lineNumber: Unrecognized directive on line: $line")
						}
					}
					"info_pic_dir" ->
						entry.infoPictureDirectory = tokens[1]
					"card_pic_dir" ->
						entry.cardPictureDirectory = tokens[1]
					else ->
					{
						if(!ignoredDirectives.contains(tokens[0]))
							main.writeSundryLog("$filename $lineNumber: Unrecognized directive on line: $line")
					}
				}
			}
			eduFile.close()
		}
		catch(e :FileNotFoundException)
		{
			main.writeOutput("Cannot find $filename. This will probably produce additional false errors in output.")
		}
		catch(e :Exception)
		{
			main.fatalParsingError(lineNumber, readLine!!, e)
		}
	}

	private fun ignoredDirectives() :ArrayList<String>
	{
		//TODO Some of these are probably useful to check somehow
		val retur = ArrayList<String>()
		retur.add("class")
		retur.add("ship")
		retur.add("formation")
		retur.add("stat_health")
		retur.add("stat_pri")
		retur.add("stat_pri_armour")
		retur.add("stat_sec")
		retur.add("stat_sec_armour")
		retur.add("stat_heat")
		retur.add("stat_ground")
		retur.add("stat_mental")
		retur.add("stat_charge_dist")
		retur.add("stat_fire_delay")
		retur.add("stat_food")
		retur.add("stat_cost")
		retur.add("stat_stl")
		retur.add("stat_ter")
		retur.add("recruit_priority_offset")
		retur.add("mount_effect")
		retur.add("move_speed_mod")
		return retur
	}
}