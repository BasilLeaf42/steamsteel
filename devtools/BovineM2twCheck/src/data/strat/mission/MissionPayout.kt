package data.strat.mission

import data.common.UsageTrackedName

class MissionPayout
	(name :String, occurringInFile :String, lineNumber :Int)
	: UsageTrackedName(name, occurringInFile, lineNumber)
{
	val rewards = ArrayList<MissionReward>()
	val penalties = ArrayList<MissionReward>()
}
