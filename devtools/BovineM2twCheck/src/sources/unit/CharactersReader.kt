package sources.unit

import data.CharacterEntry
import main.BovineM2twCheck
import util.StringUtil
import java.io.BufferedReader
import java.io.FileNotFoundException
import java.io.FileReader

class CharactersReader(val main :BovineM2twCheck)
{
	fun readCharacterTypes()
	{
		val filename = "descr_character.txt"
		var readLine :String? = null
		var lineNumber = 0
		var currentCharacter = CharacterEntry("dummy", null, -1)
		try
		{
			main.writeOutput(filename)
			val characterReader = BufferedReader(FileReader(main.runCfg.dataFolder + filename))
			while(run { readLine = characterReader.readLine(); readLine } != null)
			{
				lineNumber++
				val line :String = StringUtil.standardize(readLine!!)
				val tokens = StringUtil.split(line, " ")
				if(line.isEmpty())
					continue
				when(tokens[0])
				{
					"type" ->
					{
						currentCharacter = CharacterEntry(StringUtil.after(line, "type").trim().lowercase(), filename, lineNumber)
						main.data.unit.characterTypes.add(currentCharacter)
					}
					"actions" ->
					{
						for(i in 1 until tokens.size)
							currentCharacter.actions.add(tokens[i].replace(",", ""))
					}
					"wage_base" ->
						currentCharacter.wageBase = tokens[1].toInt()
					"starting_action_points" ->
						currentCharacter.startingActionPoints = tokens[1].toInt()
					"faction" ->
					{
						if(currentCharacter.faction != null)
						{
							currentCharacter = CharacterEntry(currentCharacter, lineNumber)
							main.data.unit.characterTypes.add(currentCharacter)
						}
						currentCharacter.faction = tokens[1].lowercase()
					}
					"dictionary" ->
						currentCharacter.dictionary = tokens[1].toInt()
					"strat_model" ->
						currentCharacter.stratModelNames.add(tokens[1])
					"battle_model" ->
					{
						val modelName = tokens[1]
						currentCharacter.battleModelNames.add(modelName)
					}
					"battle_equip" ->
						currentCharacter.battleEquip = StringUtil.after(line, "battle_equip").trim()
				}
			}
			characterReader.close()
		}
		catch(e :FileNotFoundException)
		{
			main.writeOutput("Unable to find file listing characters ($filename). You may have given a wrong path to your mod's datafolder.")
		}
		catch(e :Exception)
		{
			main.fatalParsingError(lineNumber, readLine!!, e)
		}
	}
}