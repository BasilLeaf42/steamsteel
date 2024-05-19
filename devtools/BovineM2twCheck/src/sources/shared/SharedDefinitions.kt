package sources.shared

import java.util.*

object SharedDefinitions
{
	fun simpleScriptEventTypes() :ArrayList<String>
	{
		val eventTypes = ArrayList<String>()
		eventTypes.add("historic")
		eventTypes.add("volcano")
		eventTypes.add("earthquake")
		eventTypes.add("plague")
		eventTypes.add("fire")
		eventTypes.add("flood")
		eventTypes.add("storm")
		eventTypes.add("dustbowl")
		eventTypes.add("locusts")
		eventTypes.add("horde")
		eventTypes.add("counter")
		return eventTypes
	}
}