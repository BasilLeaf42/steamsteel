package sources.code

import data.common.SimpleReferenceRecord
import data.common.UsageTrackedName
import main.BovineM2twCheck
import util.StringUtil
import util.Util
import java.io.BufferedReader
import java.io.FileNotFoundException
import java.io.FileReader

class AdviceReader(private var main :BovineM2twCheck)
{
	fun readAdvice()
	{
		val filename = "export_descr_advice.txt"
		var lineNumber = 0
		var readLine :String? = null
		try
		{
			main.writeOutput(filename)
			val adviceFile = BufferedReader(FileReader(main.runCfg.dataFolder + filename))
			var triggersReached = false
			while(run { readLine = adviceFile.readLine(); readLine} != null)
			{
				lineNumber++
				//Ignore case, starting whitespace, multiple spaces and comments
				val line = StringUtil.standardize(readLine!!)
				val tokens = line.split(" ".toRegex()).toTypedArray()
				if(tokens[0] == "script")
					Util.addIfNotPresent(tokens[1], main.data.code.customScripts)
				else if(tokens[0] == "on_display")
					Util.addIfNotPresent(tokens[1], main.data.code.customScripts)
				else if(tokens[0] == "advicethread")
				{
					if(!triggersReached)
						main.data.code.adviceThreads.add(UsageTrackedName(tokens[1], filename, lineNumber))
					else
					{
						if(main.data.code.adviceThreads[tokens[1], true] == null)
							main.writeScriptLog(filename + " " + lineNumber + ": Invocation of nonexistent advice thread " + tokens[1])
					}
				}
				else if(tokens[0] == "trigger") triggersReached = true
				for(i in tokens.indices)
				{
					if(tokens[i] == "i_eventcounter")
						main.data.code.addCheckedEventCounterLocation(SimpleReferenceRecord(tokens[i + 1], filename, lineNumber))
					if(tokens[i] == "i_threadcount")
					{
						val threadName = tokens[i + 1]
						if(main.data.code.adviceThreads[threadName, false] == null)
							main.writeScriptLog("$filename $lineNumber: Checking thread count for nonexistent advice thread $threadName")
					}
				}
			}
			adviceFile.close()
		}
		catch(e :FileNotFoundException)
		{
			main.writeOutput("Cannot find export_descr_advice.txt. Will not be loading any scripts other than campaign_script.txt.")
		}
		catch(e :Exception)
		{
			main.fatalParsingError(lineNumber, readLine!!, e)
		}
	}
}