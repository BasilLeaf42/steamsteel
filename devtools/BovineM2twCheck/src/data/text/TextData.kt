package data.text

import data.common.UsageTrackedCollection
import data.common.UsageTrackedName

class TextData
{
	val expandedText = UsageTrackedCollection<UsageTrackedName>()
	val ancillaryDescriptions = UsageTrackedCollection<UsageTrackedName>()
	val traitDescriptions = UsageTrackedCollection<UsageTrackedName>()
	val historicEventNames = UsageTrackedCollection<UsageTrackedName>()
	val historicEventDescriptions = UsageTrackedCollection<UsageTrackedName>()
}