package main

import config.ConfigurationLists
import config.RunConfig
import data.DataRoot
import data.common.FileReferenceRecord
import processing.Code
import processing.FileReferences
import processing.Sound
import processing.Stratmap
import sources.M2twDataReader
import sources.shared.MapCharacterParsing
import util.CasUtil
import util.StringUtil
import util.Util
import java.io.BufferedWriter
import java.io.File
import java.io.FileWriter
import java.io.IOException
import java.util.*

fun main(args :Array<String>)
{
//	InformationGathering.printVanillaAnimationList();
	println("Starting the checker. This will show terse information about main stages starting.")
	println("You can see more verbose output by tailing \"checker.output.log\".")
	println()
	println("Initializing the tool.")
	try
	{
		val me :BovineM2twCheck = BovineM2twCheck(args[0])
		if(!me.runCfg.configOk)
		{
			println("Bailing from fatal fault in configuration.")
			if(System.console() != null)
			{
				println()
				println("(Halting the run because of the error, so you can see this message - press ENTER to dismiss it.)")
				System.console().readLine()
			}
		}
		else
			me.run()
	}
	catch(e :Exception)
	{
		println("Unsuccessful run. Post about it in the forum and I should be able to help.")
		println("Encountered error: ${e.message}")
		e.printStackTrace()
		if(System.console() != null)
		{
			println()
			println("(Halting the run because of the error, so you can see this message - press ENTER to dismiss it.)")
			System.console().readLine()
		}
	}
}

class BovineM2twCheck(configurationFile :String)
{
	private var runLog :BufferedWriter = BufferedWriter(FileWriter("checker.output.log"))

	var runCfg :RunConfig
	val lists :ConfigurationLists
	val data :DataRoot

	private val reader :M2twDataReader
	private val fileReferences :FileReferences
	private val unit :processing.Unit
	private val sound :Sound
	private val code :Code
	private val stratmap :Stratmap

	private var edaErrorLog :BufferedWriter
	private var edctErrorLog :BufferedWriter
	private var scriptErrorLog :BufferedWriter
	private var unitErrorLog :BufferedWriter
	private var soundErrorLog :BufferedWriter
	private var stratmapErrorLog :BufferedWriter
	private var fileReferenceLog :BufferedWriter
	private var sundryErrorLog :BufferedWriter
	private var soundErrorCount :Int = 0
	private var edaErrorCount :Int = 0
	private var edctErrorCount :Int = 0
	private var scriptErrorCount :Int = 0
	private var unitErrorCount :Int = 0
	private var stratmapErrorCount :Int = 0
	private var fileReferenceErrorCount :Int = 0
	private var sundryErrorCount :Int = 0

	init
	{
		if(System.getenv()["DATAFOLDER"] != null && System.getenv()["STRAT"] != null)
		{
			System.err.println("You have set the DATAFOLDER and STRAT environment variables. Chances are you followed outdated instructions to try to get the tool to work.")
			System.err.println("Please see https://www.twcenter.net/forums/showthread.php?788469-Bovine-M2TW-Checker (the first post) for how to do it post year 2018.")
			System.err.println("Specifically for this issue: Set those values in your configuration file instead!")
		}

		println("Looking for configuration file \"$configurationFile\".")
		data = DataRoot(this)
		try
		{
			runCfg = RunConfig(configurationFile)
		}
		catch(e :IOException)
		{
			try
			{
				System.err.println("Did not find the configuration file in the root folder of the tool. Looking for it under config instead.")
				runCfg = RunConfig("config/$configurationFile")
			}
			catch(ex :IOException)
			{
				System.err.println("Cannot find the supplied configuration file for your mod ($configurationFile). I cannot perform any checks without any configuration. Aborting.")
				throw IllegalArgumentException("Configuration file needed.")
			}
		}
		println("Configuration file found. Starting up.")

		if(!File(runCfg.dataFolder).exists())
		{
			System.err.println("Your configuration file sets the data folder to ${runCfg.dataFolder} (resolving to canonical path ${File(runCfg.dataFolder).canonicalPath}), which does not exist. You need to fix the value you set in $configurationFile.")
			runCfg.configOk = false
		}
		if(StringUtil.patternCountInString(runCfg.stratFolder, ":") > 1 || runCfg.stratFolder.indexOf(":") > 4)
			System.err.println("You appear to have provided an absolute path to your strat folder (${runCfg.stratFolder}). It should rather be the subfolder RELATIVE to your data folder (such as the default value \"world/maps/campaign/imperial_campaign\"). The following check for existence will probably fail.")
		if(!File(runCfg.stratFolder).exists())
		{
			System.err.println("Your configuration file sets the strat folder to ${runCfg.stratFolder} (resolving to canonical path ${File(runCfg.stratFolder).canonicalPath}), which does not exist. You need to fix the value you set in $configurationFile.")
			runCfg.configOk = false
		}

		lists = ConfigurationLists(this)

		writeOutput("${Date()}: Creating output files.")
		edaErrorLog = BufferedWriter(FileWriter("eda.error.log"))
		edctErrorLog = BufferedWriter(FileWriter("edct.error.log"))
		scriptErrorLog = BufferedWriter(FileWriter("script.error.log"))
		unitErrorLog = BufferedWriter(FileWriter("unit.error.log"))
		soundErrorLog = BufferedWriter(FileWriter("sounds.error.log"))
		stratmapErrorLog = BufferedWriter(FileWriter("stratmap.error.log"))
		fileReferenceLog = BufferedWriter(FileWriter("filereferences.error.log"))
		sundryErrorLog = BufferedWriter(FileWriter("sundry.error.log"))

		writeOutput("${Date()}: Initializing components.")
		CasUtil.dataFolder = runCfg.dataFolder
		MapCharacterParsing.init(this)
		reader = M2twDataReader(this)
		fileReferences = FileReferences(this)
		code = Code(this)
		unit = processing.Unit(this)
		sound = Sound(this)
		stratmap = Stratmap(this)
	}

	fun run()
	{
		println("Starting reading process.")
		writeOutput("${Date()}: Constructor finished. Starting reading process.")
		read()
		writeOutput("${Date()}: Reading finished. Starting checking process.")
		if(totalReports() > 0)
			writeOutput("(There are however already reported ${totalReports()} issues, probably because of issues encountered when parsing the files)")
		println("Starting processing of checks.")
		performChecks()
		val totalReports :Int = totalReports()
		writeOutput("${Date()}: Finished checking process without any crash. Yay!")
		writeOutput("There are $totalReports issues reported.")
		if(totalReports == 0)
			writeOutput("Yay again!")
		println("Successful run.")
		finish()
	}

	private fun totalReports() :Int
	{
		return edaErrorCount + edctErrorCount + scriptErrorCount + stratmapErrorCount + unitErrorCount + soundErrorCount + fileReferenceErrorCount + sundryErrorCount
	}

	private fun read()
	{
		lists.readConfig()
		writeOutput(Date().toString() + ": Configuration files reading complete. Starting reading game files.")
		reader.readItAll()
	}

	private fun performChecks()
	{
		writeOutput("Code related")
		code.performChecks()
		writeOutput("Sound related")
		sound.soundChecks()
		writeOutput("Stratmap related")
		stratmap.performChecks()
		writeOutput("File references")
		fileReferences.checkFileReferences()
		writeOutput("Unit related")
		unit.performChecks()

		writeOutput("Listing unused elements")
		code.listUnused()
		stratmap.listUnused()
		fileReferences.listUnused()
		unit.listUnused()
		sound.listUnused()
	}

	fun writeEdaLog(message :String)
	{
		edaErrorCount++
		edaErrorLog.write(message)
		edaErrorLog.newLine()
		if(edaErrorCount % 25 == 0)
			edaErrorLog.flush()
	}

	fun writeEdctLog(message :String)
	{
		edctErrorCount++
		edctErrorLog.write(message)
		edctErrorLog.newLine()
		if(edctErrorCount % 25 == 0)
			edctErrorLog.flush()
	}

	fun writeScriptLog(file :String?, lineNumber :Int?, message :String)
	{
		writeScriptLog("$file $lineNumber: $message")
	}

	fun writeScriptLog(message :String)
	{
		scriptErrorCount++
		scriptErrorLog.write(message)
		scriptErrorLog.newLine()
		if(scriptErrorCount % 25 == 0)
			scriptErrorLog.flush()
	}

	fun writeStratmapLog(file :String?, lineNumber :Int?, message :String)
	{
		writeStratmapLog("$file $lineNumber: $message")
	}

	fun writeStratmapLog(message :String)
	{
		stratmapErrorCount++
		stratmapErrorLog.write(message)
		stratmapErrorLog.newLine()
		if(stratmapErrorCount % 25 == 0)
			stratmapErrorLog.flush()
	}

	fun writeFileReferenceLog(reference :FileReferenceRecord)
	{
		var message :String = ""
		if(reference.file != "")
			message += reference.file
		if(reference.lineNumber != null && reference.lineNumber > 0)
			message += " " + reference.lineNumber
		if(reference.referringEntryName != null)
			message += " (" + reference.referringEntryName + ")"
		if(message != "")
			message += ":"
		message += " " + reference.referencedFile + " under folder " + reference.referencedFolder + " does not exist."
		writeFileReferenceLog(message)
	}

	fun writeFileReferenceLog(message :String)
	{
		fileReferenceErrorCount++
		fileReferenceLog.write(message)
		fileReferenceLog.newLine()
		if(fileReferenceErrorCount % 25 == 0)
			fileReferenceLog.flush()
	}

	fun writeUnitLog(file :String?, lineNumber :Int?, entry :String?, message :String)
	{
		writeUnitLog(file, "$lineNumber", entry, message)
	}

	fun writeUnitLog(file :String?, lineNumber :String?, entry :String?, message :String)
	{
		unitErrorCount++
		var resultingMessage :String = ""
		if(file != null)
		{
			resultingMessage += file
			if(!lineNumber.isNullOrEmpty() && lineNumber != "0")
				resultingMessage += " $lineNumber"
			resultingMessage += ": "
		}
		if(entry != null)
			resultingMessage += "(Entry $entry) "
		resultingMessage += message
		unitErrorLog.write(resultingMessage)
		unitErrorLog.newLine()
		unitErrorLog.flush()
	}

	fun writeSoundLog(message :String)
	{
		soundErrorCount++
		soundErrorLog.write(message)
		soundErrorLog.newLine()
		if(soundErrorCount % 25 == 0)
			soundErrorLog.flush()
	}

	fun writeOutput(message :String)
	{
		runLog.write(message)
		runLog.newLine()
		runLog.flush()
	}

	fun writeSundryLog(message :String)
	{
		sundryErrorCount++
		sundryErrorLog.write(message)
		sundryErrorLog.newLine()
		if(sundryErrorCount % 25 == 0)
			sundryErrorLog.flush()
	}

	fun fatalParsingError(lineNumber :Int, lineContent :String, encounteredException :Exception)
	{
		writeOutput("Unhandled parsing error on line $lineNumber, contents (possibly partial) are: \"$lineContent\"")
		writeOutput("You can expect a lot of wrong reports while parsing this file fails (false positives AND missing actual issues).")
		writeOutput("Encountered error is: ${encounteredException.javaClass.name}: \"${encounteredException.message}\"")
		flushLogs()
	}

	private fun finish()
	{
		if(edaErrorCount == 0)
			writeEdaLog("No errors detected.")
		if(edctErrorCount == 0)
			writeEdctLog("No errors detected.")
		if(scriptErrorCount == 0)
			writeScriptLog("No errors detected.")
		if(stratmapErrorCount == 0)
			writeStratmapLog("No errors detected.")
		if(unitErrorCount == 0)
			writeUnitLog(null, null as String?, null, "No errors detected.")
		if(soundErrorCount == 0)
			writeSoundLog("No errors detected.")
		if(fileReferenceErrorCount == 0)
			writeFileReferenceLog("No errors detected.")
		if(sundryErrorCount == 0)
			writeSundryLog("No errors detected.")

		edaErrorLog.close()
		edctErrorLog.close()
		scriptErrorLog.close()
		stratmapErrorLog.close()
		unitErrorLog.close()
		soundErrorLog.close()
		fileReferenceLog.close()
		sundryErrorLog.close()
		runLog.close()
	}

	fun flushLogs()
	{
		edaErrorLog.flush()
		edctErrorLog.flush()
		scriptErrorLog.flush()
		stratmapErrorLog.flush()
		unitErrorLog.flush()
		fileReferenceLog.flush()
		soundErrorLog.flush()
		sundryErrorLog.flush()
		runLog.flush()
	}

	fun checkFileReference(reference :FileReferenceRecord)
	{
		fileReferences.checkFileReference(reference)
	}

	fun performRemovalInstructions(filename :String)
	{
		val fullName :String = filename.replace("/", File.separator).replace("\\", File.separator)
		val folderSplitPosition :Int = fullName.lastIndexOf(File.separator)
		val folder :String = fullName.substring(0, folderSplitPosition)
		val name = fullName.substring(folderSplitPosition + 1)

		for(command :String in runCfg.unusedRemovalCommands)
		{
			when
			{
				command.startsWith("COPY_TO") ->
				{
					val targetFolder = StringUtil.after(command, "COPY_TO ")
					val fullSourceFolder :String = "${runCfg.dataFolder}$folder"
					val fullTargetFolder :String = "${runCfg.dataFolder}$targetFolder/$folder"
					File(fullTargetFolder).mkdirs()
					try
					{
						File("$fullSourceFolder/$name").copyTo(File("$fullTargetFolder/$name"))
					}
					catch(e :FileAlreadyExistsException) { Util.noop() }
				}
				command.startsWith("CONSOLE_COMMAND") ->
				{
					var consoleCommand :String = StringUtil.after(command, "CONSOLE_COMMAND ")
					consoleCommand = consoleCommand.replace("%FILENAME%", filename).replace("%DATAFOLDER%", runCfg.dataFolder)
					consoleCommand = consoleCommand.replace("/", File.separator)
					consoleCommand = consoleCommand.replace("\\", File.separator)
					consoleCommand = consoleCommand.replace("${File.separator}${File.separator}", File.separator)
					consoleCommand = consoleCommand.replace("cmd \\c", "cmd /c")
					Runtime.getRuntime().exec(consoleCommand)
				}
				else ->
					writeSundryLog("Unrecognized command for unused file: $command")
			}
		}
	}
}