package sources

import data.common.UsageTrackedCollection
import data.common.UsageTrackedName
import data.unit.UnitDescription
import main.BovineM2twCheck
import util.StringUtil
import java.io.*

class TextReader(val main :BovineM2twCheck)
{
	fun readWhenever()
	{
		readTextNames("text/export_ancillaries.txt", main.data.text.ancillaryDescriptions)
		readTextNames("text/export_vnvs.txt", main.data.text.traitDescriptions)
		readTextNames("text/historic_events.txt", main.data.text.historicEventNames, "_title", true)
		readTextNames("text/historic_events.txt", main.data.text.historicEventDescriptions, "_body", true)
		readTextNames("text/expanded.txt", main.data.text.expandedText)
		readUnitDescriptions()
	}

	private fun readTextNames(filename :String, targetCollection :UsageTrackedCollection<UsageTrackedName>, suffixFilter :String? = null, removeSuffix :Boolean = false)
	{
		var readLine :String? = null
		var lineNumber = 0
		try
		{
			if(suffixFilter != null)
				main.writeOutput("$filename (suffix filter $suffixFilter)")
			else
				main.writeOutput(filename)
			val textFile = BufferedReader(InputStreamReader(FileInputStream(main.runCfg.dataFolder + filename), "UTF-16"))
			while(run { readLine = textFile.readLine(); readLine } != null)
			{
				//Ignore case, starting whitespace, multiple spaces and comments
				val line :String = StringUtil.standardize(readLine!!)
				lineNumber++
				if(line.startsWith("{"))
				{
					var name :String = StringUtil.between(line, "{", "}")!!
					if(suffixFilter != null)
					{
						if(!name.endsWith(suffixFilter))
							continue
						if(removeSuffix)
							name = name.substring(0, name.length - suffixFilter.length)
					}

					if(name.contains(" "))
					{
						main.writeSundryLog("""$filename $lineNumber: Text code name "$name" cannot include spaces.""")
						name = name.replace(" ", "_")
					}
					targetCollection.add(UsageTrackedName(name, filename, lineNumber))
				}
			}
			textFile.close()
		}
		catch(e :FileNotFoundException)
		{
			main.writeOutput("Cannot find text file $filename. Are you sure you provided the correct location for the data folder?")
		}
		catch(e :Exception)
		{
			main.fatalParsingError(lineNumber, readLine!!, e)
		}
	}

	private fun readUnitDescriptions()
	{
		val filename = "text/export_units.txt"
		var readLine :String? = null
		var lineNumber = 0
		try
		{
			main.writeOutput(filename)
			val unitDescriptionReader = BufferedReader(InputStreamReader(FileInputStream(main.runCfg.dataFolder + filename), "UTF-16"))
			while(run { readLine = unitDescriptionReader.readLine(); readLine } != null)
			{
				lineNumber++
				val line :String = StringUtil.standardize(readLine!!)
				if(line.startsWith("{"))
				{
					var name :String
					val label :String = StringUtil.between(line, "{", "}")!!
					when
					{
						label.endsWith("_descr_short") ->
						{
							name = StringUtil.beforeLast(label, "_descr_short")
							var description :UnitDescription? = main.data.unit.findUnitDescription(name)
							when
							{
								description == null ->
								{
									description = UnitDescription(name, label, null)
									description.nameLineNumber = lineNumber
									main.data.unit.unitDescriptions.add(description)
								}
								description.shortDescription == null ->
									description.shortDescription = label
								else ->
								{
									description = UnitDescription(null, label, null)
									description.isDuplicate = true
									main.data.unit.unitDescriptions.add(description)
								}
							}
							description.shortLineNumber = lineNumber
						}
						label.endsWith("_descr") ->
						{
							name = StringUtil.beforeLast(label, "_descr")
							var description :UnitDescription? = main.data.unit.findUnitDescription(name)
							when
							{
								description == null ->
								{
									description = UnitDescription(name, null, label)
									description.nameLineNumber = lineNumber
									main.data.unit.unitDescriptions.add(description)
								}
								description.longDescription == null ->
									description.longDescription = label
								else ->
								{
									description = UnitDescription(null, null, label)
									description.isDuplicate = true
									main.data.unit.unitDescriptions.add(description)
								}
							}
							description.longLineNumber = lineNumber
						}
						else ->
						{
							name = label
							var description = main.data.unit.findUnitDescription(name)
							if(description == null)
							{
								description = UnitDescription(name, null, null)
								description.nameIsVerifiedPresent = true
								main.data.unit.unitDescriptions.add(description)
							}
							else if(!description.nameIsVerifiedPresent)
								description.nameIsVerifiedPresent = true
							else
							{
								description = UnitDescription(name, null, null)
								description.isDuplicate = true
								main.data.unit.unitDescriptions.add(description)
							}
							description.nameLineNumber = lineNumber
						}
					}
				}
			}
			unitDescriptionReader.close()
		}
		catch(e :FileNotFoundException)
		{
			main.writeOutput("Unable to find unit description file ($filename), this may result in a lot of false errors.")
		}
		catch(e :Exception)
		{
			main.fatalParsingError(lineNumber, readLine!!, e)
		}
	}
}