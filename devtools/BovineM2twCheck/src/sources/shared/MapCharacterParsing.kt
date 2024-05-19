package sources.shared

import data.common.FileReferenceRecord
import data.common.SimpleReferenceRecord
import data.strat.MapCharacter
import main.BovineM2twCheck
import util.StringUtil
import util.Util

object MapCharacterParsing
{
	var main :BovineM2twCheck? = null
	fun init(main :BovineM2twCheck)
	{
		this.main = main
	}

	fun createCharacter(faction :String, filename :String, lineNumber :Int, line :String, isScripted :Boolean) :MapCharacter
	{
		var remainingLine = line
		var name = StringUtil.before(remainingLine, ",")
		var subFaction :String? = null
		if(name.startsWith("sub_faction "))
		{
			subFaction = StringUtil.after(name, " ")
			if(isScripted)
				main!!.data.code.factionReferences.add(SimpleReferenceRecord(subFaction, filename, lineNumber))
			else
				main!!.data.strat.factionReferences.add(SimpleReferenceRecord(subFaction, filename, lineNumber))
			remainingLine = StringUtil.after(remainingLine, ",")
			name = StringUtil.before(remainingLine, ",").trim()
		}
		val character = MapCharacter(faction, filename, lineNumber, name)
		character.subFaction = subFaction
		readCharacterDetails(filename, lineNumber, character, StringUtil.after(remainingLine, ","))
		return character
	}

	private fun readCharacterDetails(filename :String, lineNumber :Int, character :MapCharacter, line :String)
	{
		character.type = StringUtil.before(line, ",").trim()
		if(Util.equalsAny(character.type, "princess", "witch"))
			character.isFemale = true
		var details = StringUtil.after(line, ",")
		details = details.replace(",", " ").replace("  ", " ").replace("  ", " ").trim()
		val tokens = StringUtil.split(details, " ")
		var skips = 0
		for(i in 0 until tokens.indices.count())
		{
			if(skips > 0)
			{
				skips--
				continue
			}
			skips = readCharacterDetail(filename, lineNumber, character, tokens, i)
		}
	}

	private fun readCharacterDetail(filename :String, lineNumber :Int, character :MapCharacter, tokens :Array<String>, startIndex :Int) :Int
	{
		val main = this.main!!
		val detail = tokens[startIndex]
		var value :String? = null
		if(startIndex < tokens.size - 1)
			value = tokens[startIndex + 1]
		var skips = 1
		when(detail)
		{
			"male", "female" ->
			{
				character.isFemale = detail == "female"
				skips = 0
			}
			"family" ->
			{
				character.isFamilyMember = true
				skips = 0
			}
			"leader" ->
			{
				character.isLeader = true
				skips = 0
			}
			"heir" ->
			{
				character.isHeir = true
				skips = 0
			}
			"strat_model" ->
				character.stratModel = value
			"battle_model" ->
				character.battleModel = value!!
			"age" ->
				character.age = value!!.toInt()
			"x" ->
				character.x = value!!.toInt()
			"y" ->
				character.y = value!!.toInt()
			"portrait" ->
			{
				character.portrait = value!!
				main.data.fileReferencesForCrossCheck.add(FileReferenceRecord(filename, lineNumber, character.name, "ui/custom_portraits/$value/portrait_dead.tga"))
				main.data.fileReferencesForCrossCheck.add(FileReferenceRecord(filename, lineNumber, character.name, "ui/custom_portraits/$value/portrait_old.tga"))
				main.data.fileReferencesForCrossCheck.add(FileReferenceRecord(filename, lineNumber, character.name, "ui/custom_portraits/$value/portrait_young.tga"))
			}
			"label" ->
				character.label = value!!
			"hero_ability" ->
				character.ability = value
			"direction" ->
				character.direction = value!!
			"" ->
				Util.noop()
			else ->
				main.writeSundryLog("""$filename $lineNumber: Encountered unrecognized character attribute "$detail"""")
		}
		return skips
	}
}