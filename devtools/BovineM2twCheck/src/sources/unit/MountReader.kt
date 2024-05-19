package sources.unit

import data.unit.MountEntry
import main.BovineM2twCheck
import util.StringUtil
import java.io.BufferedReader
import java.io.FileNotFoundException
import java.io.FileReader

class MountReader(private val main :BovineM2twCheck)
{
	fun readMounts()
	{
		val filename = "descr_mount.txt"
		var readLine :String? = null
		var lineNumber = 0
		try
		{
			main.writeOutput(filename)
			val mountsReader = BufferedReader(FileReader(main.runCfg.dataFolder + filename))
			var entry = MountEntry("dummy", -1)
			while(run { readLine = mountsReader.readLine(); readLine } != null)
			{
				lineNumber++
				val line :String = StringUtil.standardize(readLine!!)
				val tokens :Array<String> = StringUtil.split(line, " ")
				when(tokens[0])
				{
					"type" ->
					{
						val name = StringUtil.after(line, " ").trim()
						entry = MountEntry(name, lineNumber)
						main.data.unit.mounts.add(entry)
					}
					"class" ->
						entry.mountClass = tokens[1]
					"model" ->
						entry.model = tokens[1]
					"water_trail_effect" ->
						entry.waterTrailEffect = tokens[1]
					"riders" ->
						entry.riderCount = tokens[1].toInt()
					"rider_offset" ->
						entry.riderOffsets.add(StringUtil.after(line, " "))
				}
			}
			mountsReader.close()
		}
		catch(e :FileNotFoundException)
		{
			main.writeOutput("Unable to find mounts ($filename), this may cause a lot of false errors detected. Assuming you are using the vanilla mounts only.")
			addVanillaMounts()
		}
		catch(e :Exception)
		{
			main.fatalParsingError(lineNumber, readLine!!, e)
		}
	}

	private fun addVanillaMounts()
	{
		val dummyMount = MountEntry("dummy", -1)
		main.data.unit.mounts.add(dummyMount.createVanillaMountRepresentation("pony"))
		main.data.unit.mounts.add(dummyMount.createVanillaMountRepresentation("fast pony"))
		main.data.unit.mounts.add(dummyMount.createVanillaMountRepresentation("heavy horse"))
		main.data.unit.mounts.add(dummyMount.createVanillaMountRepresentation("mailed horse"))
		main.data.unit.mounts.add(dummyMount.createVanillaMountRepresentation("barded horse"))
		main.data.unit.mounts.add(dummyMount.createVanillaMountRepresentation("armoured horse"))
		main.data.unit.mounts.add(dummyMount.createVanillaMountRepresentation("eastern armoured horse"))
		main.data.unit.mounts.add(dummyMount.createVanillaMountRepresentation("elephant"))
		main.data.unit.mounts.add(dummyMount.createVanillaMountRepresentation("elephant_cannon"))
		main.data.unit.mounts.add(dummyMount.createVanillaMountRepresentation("elephant_rocket"))
		main.data.unit.mounts.add(dummyMount.createVanillaMountRepresentation("camel"))
	}
}