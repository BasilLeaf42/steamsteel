package data.strat.mission

import data.common.SimpleReferenceRecord
import util.StringUtil

class MissionReligionModifier(line :String, filename :String, lineNumber :Int) :SimpleReferenceRecord("", filename, lineNumber)
{
	init
	{
		val tokens = StringUtil.split(line, " ")
		reference = tokens[0]
	}
}
