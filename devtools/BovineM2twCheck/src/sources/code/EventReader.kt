package sources.code

import data.common.SimpleReferenceRecord
import data.code.script.EventCounterEntry
import main.BovineM2twCheck
import sources.shared.SharedDefinitions.simpleScriptEventTypes
import util.StringUtil
import java.io.*

class EventReader(private val main :BovineM2twCheck)
{
	fun readAll()
	{
		readPredefinedHistoricEvents()
	}

	private fun readPredefinedHistoricEvents()
	{
		val filename = "descr_events.txt"
		var readLine :String? = null
		var lineNumber = 0
		try
		{
			main.writeOutput(filename)
			val predefinedHistoricEventFile = BufferedReader(FileReader(main.runCfg.stratFolder + filename))
			val simpleEventTypes = simpleScriptEventTypes()
			var event :EventCounterEntry? = EventCounterEntry("dummy")
			while(run { readLine = predefinedHistoricEventFile.readLine(); readLine } != null)
			{
				lineNumber++
				//Ignore case, starting whitespace, multiple spaces and comments
				val line :String = StringUtil.standardize(readLine!!)
				val tokens = StringUtil.split(line, " ")
				if(tokens[0] == "event")
				{
					if(simpleEventTypes.contains(tokens[1]) && tokens.size > 2)
					{
						event = main.data.code.eventCounters[tokens[2], false]
						if(event == null)
						{
							event = EventCounterEntry(tokens[2], filename, lineNumber)
							main.data.code.eventCounters.add(event)
						}
						event.isUsed = true
						event.isHistoric = true
					}
					if(tokens[1] == "emergent_faction")
					{
						val fullEventName = "the_" + tokens[2] + "_emerge"
						event = EventCounterEntry(fullEventName, filename, lineNumber)
						event.isUsed = true
						event.isHistoric = true
						main.data.code.eventCounters.add(event)
					}
				}
				else if(tokens[0] == "date")
					event!!.setLocations.add(SimpleReferenceRecord(event.name, filename, lineNumber))
			}
			predefinedHistoricEventFile.close()
		}
		catch(e :FileNotFoundException)
		{
			main.writeOutput("Cannot find $filename. Are you sure you provided the correct location for the data folder?")
		}
		catch(e :Exception)
		{
			main.fatalParsingError(lineNumber, readLine!!, e)
		}
	}
}