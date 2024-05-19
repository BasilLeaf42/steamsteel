package data.strat.mission

import util.StringUtil

class MissionPayback(line :String)
{
	val conditions = ArrayList<MissionPaybackCondition>()
	val payoutId :String

	init
	{
		val tokens = StringUtil.split(line, " ")
		var idMarkerIndex :Int = 0
		for(i in tokens.indices)
		{
			if(tokens[i] == "payback_id")
			{
				idMarkerIndex = i
				break
			}
		}
		payoutId = tokens[idMarkerIndex + 1]
		for(i in 0 until idMarkerIndex)
		{
			if(i % 2 == 1)
				continue
			conditions.add(MissionPaybackCondition(tokens[i], tokens[i + 1]))
		}
	}
}
