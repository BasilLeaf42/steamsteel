package sources.unit

import data.common.FileReferenceRecord
import data.unit.SkeletonAnimation
import data.unit.SkeletonEntry
import main.BovineM2twCheck
import util.StringUtil
import util.Util
import java.io.BufferedReader
import java.io.FileNotFoundException
import java.io.FileReader

class SkeletonReader(private val main :BovineM2twCheck)
{
	fun readAll()
	{
		readSkeletonFile("descr_skeleton.txt", false)
		readSkeletonFile("descr_engine_skeleton.txt", true)
	}

	private fun readSkeletonFile(filename :String, isEngine :Boolean)
	{
		var readLine :String? = null
		var lineNumber = 0
		try
		{
			main.writeOutput(filename)
			val skeletonReader = BufferedReader(FileReader(main.runCfg.dataFolder + filename))
			var entry = SkeletonEntry("dummy", null, -1)
			while(run { readLine = skeletonReader.readLine() ; readLine } != null)
			{
				lineNumber++
				val line :String = StringUtil.standardize(readLine!!)
				if(line.isEmpty())
					continue
				if(line.startsWith("version"))
					continue
				val tokens = StringUtil.split(line, " ")
				when
				{
					line.startsWith("type") ->
					{
						entry = SkeletonEntry(tokens[1], filename, lineNumber)
						entry.isEngine = isEngine
						main.data.unit.skeletons.add(entry)
					}
					line.startsWith("anim") ->
					{
						val animation = SkeletonAnimation()
						entry.animations.add(animation)
						animation.name = tokens[1]
						var casFile = StringUtil.between(line, "data/", ".cas")
						if(casFile != null)
						{
							casFile = "$casFile.cas"
							animation.casFile = casFile
							Util.addIfNotPresent(casFile, main.data.unit.usedAnimationFiles)
							main.data.fileReferencesForCrossCheck.add(FileReferenceRecord(filename, lineNumber, "${entry.name}'s animation ${animation.name}", casFile, null, null, ".cmi", !main.runCfg.vanillaAnimationsRequired))
						}
						var evtFile = StringUtil.between(line, "evt:data/", ".evt")
						if(evtFile != null)
						{
							evtFile = "$evtFile.evt"
							animation.casFile = evtFile
							Util.addIfNotPresent(evtFile, main.data.unit.usedAnimationFiles)
							main.data.fileReferencesForCrossCheck.add(FileReferenceRecord(filename, lineNumber, "${entry.name}'s animation ${animation.name}", evtFile, null, null, null, !main.runCfg.vanillaAnimationsRequired))
						}
					}
					line.startsWith("parent") ->
						entry.parent = tokens[1]
					line.startsWith("strike_distances ") ->
						entry.strikeDistances = line.substring("strike_distances ".length)
					line.startsWith("no_deltas") ->
						entry.noDeltas = true
					line.startsWith("suppress_refpoints_warning") ->
						entry.suppressRefPointsWarning = true
					line.startsWith("remove_attack_anims") ->
						entry.removeAttackAnimations = true
					line.startsWith("force_hit_positions_to_cylinder") ->
						entry.forceHitPositionsToCylinder = true
					line.startsWith("scale") ->
						entry.scale = tokens[1].toFloat()
					line.startsWith("in_awareness") ->
						entry.inAwareness = tokens[1].toFloat()
					line.startsWith("in_zone") ->
						entry.inZone = tokens[1].toFloat()
					line.startsWith("in_centre") ->
						entry.inCentre = tokens[1].toFloat()
					line.startsWith("locomotion_table") ->
						entry.locomotionTable = tokens[1]
					line.startsWith("reference_points") ->
					{
						entry.referencePoints = tokens[1]
						main.data.fileReferencesForCrossCheck.add(FileReferenceRecord(filename, lineNumber, entry.name, entry.referencePoints!!))
					}
					else ->
						main.writeUnitLog(filename, lineNumber, entry.name, "Line in descr_skeleton contains unknown command \"$line\"")
				}
			}
			skeletonReader.close()
		}
		catch(e :FileNotFoundException)
		{
			main.writeOutput("Unable to find list of skeletons/animations ($filename). This is okay only if you are using only vanilla models, else you may have given a wrong path to your mod's datafolder. Will use the vanilla list for references.")
			main.lists.readVanillaSkeletons()
		}
		catch(e :Exception)
		{
			main.fatalParsingError(lineNumber, readLine!!, e)
		}
	}
}