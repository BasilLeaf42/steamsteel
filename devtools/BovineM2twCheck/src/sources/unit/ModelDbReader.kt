@file:Suppress("UNUSED_VARIABLE")

package sources.unit

import data.common.FileReferenceRecord
import data.unit.ModelDbEntry
import data.unit.ModelDbSegment
import main.BovineM2twCheck
import util.Queue
import util.StringUtil
import util.Util

import java.io.*
import java.util.ArrayList
import kotlin.*

class ModelDbReader(val main :BovineM2twCheck)
{
	private val filename = "battle_models.modeldb"
	private var currentModelDbLine :Int = -1
	private val unusedBits = Queue<Char>()
	private var currentLine :String? = null
	private var inputStream :FileInputStream? = null

	fun read()
	{
		try
		{
			syntaxCheck()
			parse()
		}
		catch(e :FileNotFoundException)
		{
			main.writeOutput("Cannot find the model DB file (${main.runCfg.dataFolder}$filename).")
			main.writeOutput("No checks have been performed on the model DB.")
			main.writeOutput("This is okay if you are ONLY using vanilla models, if not you may have entered your mod's data folder wrong.")
			return
		}
		catch(e :Exception)
		{
			var remainder :String? = currentLine
			if(remainder == null && inputStream != null)
			{
				val remainderReader = BufferedReader(InputStreamReader(inputStream!!))
				try
				{
					remainder = remainderReader.readLine()
					remainderReader.close()
				}
				catch(ex :IOException)
				{
					Util.noop()
				}
			}
			main.fatalParsingError(currentModelDbLine, remainder ?: "", e)
		}
	}

	private fun syntaxCheck()
	{
		main.writeOutput("unit_models/$filename (syntax check)")
		val inputDb = BufferedReader(FileReader("${main.runCfg.dataFolder}unit_models/$filename"))
		//Read the whole model DB into the string array
		val stringTempBuffer = ArrayList<String>()
		while(run { currentLine = inputDb.readLine(); currentLine } != null)
			stringTempBuffer.add(currentLine!!)

		val lines :Array<String> = Util.arrayListToArray(stringTempBuffer)
		for(i in lines.indices)
		{
			var trailingSpaceCounter = 0
			if(lines[i].contains("\t"))
			{
				main.writeUnitLog(filename, i + 1, null, "Line contains TAB character, should be SPACE or removed. Interpreting as space to allow parsing.")
				lines[i] = lines[i].replace("\t", " ")
			}
			while(lines[i].endsWith(" "))
			{
				trailingSpaceCounter++
				lines[i] = lines[i].substring(0, lines[i].length - 1)
			}
			if(trailingSpaceCounter != 1)
				main.writeUnitLog(filename, i + 1, null, "Trailing space count is wrong: $trailingSpaceCounter.")
		}
		inputDb.close()
	}

	private fun parse()
	{
		//Read the model DB again, parsing it into entries
		main.writeOutput("unit_models/$filename (parsing)")
		inputStream = FileInputStream("${main.runCfg.dataFolder}unit_models/$filename")

		currentModelDbLine = 1
		val entryNominalCount :Int = readEntryCount(inputStream!!)
		currentModelDbLine = 2
		var isFirstEntry = true
		while(inputStream!!.available() > 10)
		{
			val entryBeingRead :ModelDbEntry = readName(inputStream!!)
			main.data.unit.battleModels.add(entryBeingRead)
			//main.writeOutput(currentModelDbLine + " " + entryBeingRead.name)
			readModels(entryBeingRead, inputStream!!, isFirstEntry)
			readTextures(entryBeingRead, inputStream!!, isFirstEntry)
			readAttachments(entryBeingRead, inputStream!!)
			readSkeletons(entryBeingRead, inputStream!!, isFirstEntry)
			readTorch(entryBeingRead, inputStream!!, isFirstEntry)

			if(entryBeingRead.isMount)
				main.data.unit.mountModels.add(entryBeingRead)
			isFirstEntry = false
		}
		inputStream!!.close()

		if(entryNominalCount != main.data.unit.battleModels.count())
			main.writeUnitLog(filename, "", null, "Header says there are $entryNominalCount entries, while there are actually ${main.data.unit.battleModels.count()}")
	}

	//The entry count is in position 8 in the model DB header.
	private fun readEntryCount(inputStream :FileInputStream) :Int
	{
		var retur = 0
		
		val headerTokens :ArrayList<String> = readHeaderTokens(inputStream)
		if(headerTokens.size >= 8)
			retur = headerTokens[7].toInt()
		return retur
	}
	
	private fun readName(inputStream :FileInputStream) :ModelDbEntry
	{
		val nameSegment :ModelDbSegment = readLengthNominatedSegment(inputStream)
		if(nameSegment.nominalContentLength > 0)
		{
			val retur = ModelDbEntry(StringUtil.standardize(nameSegment.content), currentModelDbLine)
			checkLengthMarker(nameSegment.nominalContentLength, retur.name, retur.name, "Name length marker says %NOMINAL_LENGTH%, but the entry name is %LENGTH% long.", currentModelDbLine)
			return retur
		}
		throw IOException("Model DB: Unable to read length nominated segment for model name, at line $currentModelDbLine")
	}
	
	private fun readModels(entry :ModelDbEntry, inputStream :FileInputStream, isFirstEntry :Boolean)
	{
		//Discard meaningless 1 or 1.12 segment
		val meaninglessSegment = readSingleToken(inputStream)
		
		if(isFirstEntry)
		{
			val dummyZero2 = readSingleToken(inputStream)
			val dummyZero3 = readSingleToken(inputStream)
			entry.nominalModelCount = Integer.parseInt(readSingleToken(inputStream))
			val dummyZero4 = readSingleToken(inputStream)
			val dummyZero5 = readSingleToken(inputStream)
		}
		else
		{
			val modelCountSegment :String = readSingleToken(inputStream)
			if(modelCountSegment == "0")
				return
			entry.nominalModelCount = Integer.parseInt(modelCountSegment)
		}
		
		if(entry.nominalModelCount > 0)
		{
			var stillReadingFileReferences = true
			do
			{
				val modelAssignment :ModelDbSegment = readLengthNominatedSegment(inputStream)
				if(modelAssignment.nominalContentLength == 0 && isFirstEntry && entry.modelAssignments.isEmpty())
				{
					val dummyZero6 = readSingleToken(inputStream)
					stillReadingFileReferences = false
					continue
				}
				val distanceToken :String = readSingleToken(inputStream)
				if(!modelAssignment.content.contains("unit_models") || !modelAssignment.content.contains(".mesh"))
				{
					prependToUnusedBits("${modelAssignment.nominalContentLength} ${modelAssignment.content} $distanceToken ")
					stillReadingFileReferences = false
				}
				else
				{
					val model = ModelDbEntry.ModelAssignment()
					model.lineNumber = currentModelDbLine
					model.fileName = StringUtil.standardize(modelAssignment.content)
					model.viewDistance = distanceToken
					entry.modelAssignments.add(model)
//					Util.addIfNotPresent(model.fileName, encounteredReferences)
					checkLengthMarker(modelAssignment.nominalContentLength, model.fileName!!, entry.name, "Line length marker says %NOMINAL_LENGTH%, but the model file is %LENGTH% long (${model.fileName}).", currentModelDbLine)
					main.data.fileReferencesForCrossCheck.add(FileReferenceRecord(filename, currentModelDbLine, entry.name, model.fileName!!))
				}
			}
			while(stillReadingFileReferences)
		}
	}
	
	private fun readTextures(entry :ModelDbEntry, inputStream :FileInputStream, isFirstEntry :Boolean)
	{
		if(isFirstEntry)
		{
			val dummyZero1 = readSingleToken(inputStream)
			val dummyZero2 = readSingleToken(inputStream)
			entry.nominalTextureAssignmentCount = readSingleToken(inputStream).toInt()
			val dummyZero3 = readSingleToken(inputStream)
			val dummyZero4 = readSingleToken(inputStream)
		}
		else
			entry.nominalTextureAssignmentCount = readSingleToken(inputStream).toInt()
		if(entry.nominalTextureAssignmentCount > 0)
		{
			var factionSegment :ModelDbSegment = readLengthNominatedSegment(inputStream)
			var stillMoreTextureAssignments :Boolean = !StringUtil.isInteger(factionSegment.content)
			if(factionSegment.nominalContentLength == 0 && isFirstEntry && entry.textureAssignments.isEmpty())
				return

			while(stillMoreTextureAssignments)
			{
				val texture = ModelDbEntry.TextureAssignment()
				val faction :String = factionSegment.content
				if(!main.data.strat.getAllFactionNames(null).contains(faction))
					main.writeUnitLog(filename, currentModelDbLine, entry.name, """Reference to non-existent faction "$faction".""")
				checkLengthMarker(factionSegment.nominalContentLength, faction, entry.name, "Line length for faction $faction says it's %NOMINAL_LENGTH% long.", currentModelDbLine)
				texture.faction = faction
				texture.lineNumber = currentModelDbLine
				
				val textureSegment :ModelDbSegment = readLengthNominatedSegment(inputStream)
				texture.texture = StringUtil.standardize(textureSegment.content)
//				Util.addIfNotPresent(texture.texture, encounteredReferences)
				checkLengthMarker(textureSegment.nominalContentLength, texture.texture!!, entry.name, """Line length for faction $faction's texture "${texture.texture}" of length %LENGTH% says it's %NOMINAL_LENGTH% long.""", currentModelDbLine)
				main.data.fileReferencesForCrossCheck.add(FileReferenceRecord(filename, currentModelDbLine, entry.name, texture.texture!!))
				
				val normalTextureSegment :ModelDbSegment = readLengthNominatedSegment(inputStream)
				texture.normalTexture = StringUtil.standardize(normalTextureSegment.content)
//				Util.addIfNotPresent(texture.normalTexture, encounteredReferences)
				checkLengthMarker(normalTextureSegment.nominalContentLength, texture.normalTexture!!, entry.name, """Line length for faction $faction's normal texture "${texture.normalTexture}" of length %LENGTH% says it's %NOMINAL_LENGTH% long.""", currentModelDbLine)
				main.data.fileReferencesForCrossCheck.add(FileReferenceRecord(filename, currentModelDbLine, entry.name, texture.normalTexture!!))
				
				val spriteSegment :ModelDbSegment = readLengthNominatedSegment(inputStream)
				if(spriteSegment.nominalContentLength > 0)
				{
					texture.sprite = StringUtil.standardize(spriteSegment.content)
//					Util.addIfNotPresent(texture.sprite, encounteredReferences)
					checkLengthMarker(spriteSegment.nominalContentLength, texture.sprite!!, entry.name, "Line length for faction " + faction + "'s sprite \"" + texture.sprite + "\" of length %LENGTH% says it's %NOMINAL_LENGTH% long.", currentModelDbLine)
					main.data.fileReferencesForCrossCheck.add(FileReferenceRecord(filename, currentModelDbLine, entry.name, texture.sprite!!))
				}
				
				entry.textureAssignments.add(texture)
				factionSegment = readLengthNominatedSegment(inputStream)
				stillMoreTextureAssignments = factionSegment.nominalContentLength != 0 && !StringUtil.isInteger(factionSegment.content.substring(0, 1))
			}
			var myUnusedBits :String = "${factionSegment.nominalContentLength} "
			if(factionSegment.content != "")
				myUnusedBits += "${factionSegment.content} "
			prependToUnusedBits(myUnusedBits)
		}
	}
	
	private fun readAttachments(entry :ModelDbEntry, inputStream :FileInputStream)
	{
		entry.nominalAttachmentAssignmentCount = readSingleToken(inputStream).toInt()
		if(entry.nominalAttachmentAssignmentCount == 0)
		{
			entry.isMount = true
		}
		else
		{
			var factionSegment :ModelDbSegment = readLengthNominatedSegment(inputStream)
			var stillMoreAttachmentAssignments = !StringUtil.isInteger(factionSegment.content)
			while(stillMoreAttachmentAssignments)
			{
				val attachment = ModelDbEntry.AttachmentAssignment()
				attachment.faction = factionSegment.content
				if(!main.data.strat.getAllFactionNames(null).contains(attachment.faction!!))
					main.writeUnitLog(filename, currentModelDbLine, entry.name, """Reference to nonexistent faction "${attachment.faction}".""")
				checkLengthMarker(factionSegment.nominalContentLength, attachment.faction!!, entry.name, "Line length for faction ${attachment.faction} says it's %NOMINAL_LENGTH% long.", currentModelDbLine)
				attachment.lineNumber = currentModelDbLine
				
				val textureSegment :ModelDbSegment = readLengthNominatedSegment(inputStream)
				attachment.texture = StringUtil.standardize(textureSegment.content)
//				Util.addIfNotPresent(attachment.texture, encounteredReferences)
				checkLengthMarker(textureSegment.nominalContentLength, attachment.texture!!, entry.name, """Line length for faction ${attachment.faction}' attachment texture "${attachment.texture}" of length %LENGTH% says it's %NOMINAL_LENGTH% long.""", currentModelDbLine)
				main.data.fileReferencesForCrossCheck.add(FileReferenceRecord(filename, currentModelDbLine, entry.name, attachment.texture!!))
				
				val normalTextureSegment :ModelDbSegment = readLengthNominatedSegment(inputStream)
				attachment.normalTexture = StringUtil.standardize(normalTextureSegment.content)
//				Util.addIfNotPresent(attachment.normalTexture, encounteredReferences)
				checkLengthMarker(normalTextureSegment.nominalContentLength, attachment.normalTexture!!, entry.name, """Line length for faction ${attachment.faction}' attachment normal texture "${attachment.normalTexture}" of length %LENGTH% says it's %NOMINAL_LENGTH% long.""", currentModelDbLine)
				main.data.fileReferencesForCrossCheck.add(FileReferenceRecord(filename, currentModelDbLine, entry.name, attachment.normalTexture!!))
				
				val dummyZero = readSingleToken(inputStream)
				
				entry.attachmentAssignments.add(attachment)
				
				factionSegment = readLengthNominatedSegment(inputStream)
				stillMoreAttachmentAssignments = !StringUtil.isInteger("${factionSegment.content[0]}")
			}
			prependToUnusedBits("${factionSegment.nominalContentLength} ${factionSegment.content} ")
		}
	}
	
	private fun readSkeletons(entry :ModelDbEntry, inputStream :FileInputStream, isFirstEntry :Boolean)
	{
		if(isFirstEntry)
		{
			val dummyZero1 = readSingleToken(inputStream)
			val dummyZero2 = readSingleToken(inputStream)
			entry.nominalSkeletonCount = Integer.parseInt(readSingleToken(inputStream))
			val dummyZero4 = readSingleToken(inputStream)
			val dummyZero5 = readSingleToken(inputStream)
			if(entry.modelAssignments.isEmpty())
			{
				entry.nominalSkeletonCount = Integer.parseInt(readSingleToken(inputStream))
				val dummyZero7 = readSingleToken(inputStream)
				val dummyZero8 = readSingleToken(inputStream)
			}
		}
		else
			entry.nominalSkeletonCount = Integer.parseInt(readSingleToken(inputStream))
		
		if(entry.nominalSkeletonCount == 0 && !entry.isMount)
			main.writeUnitLog(filename, currentModelDbLine, entry.name, "No skeletons defined for a non-mount model.")
		for(i in 0 until entry.nominalSkeletonCount)
		{
			val skeleton = ModelDbEntry.ModelDbSkeleton()
			val mountSegment :ModelDbSegment = readLengthNominatedSegment(inputStream)
			if(mountSegment.nominalContentLength > 0)
			{
				skeleton.mount = StringUtil.standardize(mountSegment.content)
				checkLengthMarker(mountSegment.nominalContentLength, skeleton.mount!!, entry.name, """Line length for mount "${skeleton.mount}" of length %LENGTH% says it's %NOMINAL_LENGTH% long.""", currentModelDbLine)
			}
			
			if(entry.isMount)
			{
				val mountSkeletonSegment :ModelDbSegment = readLengthNominatedSegment(inputStream)
				if(mountSkeletonSegment.nominalContentLength > 0)
				{
					skeleton.mountSkeleton = StringUtil.standardize(mountSkeletonSegment.content)
					checkLengthMarker(mountSkeletonSegment.nominalContentLength, skeleton.mountSkeleton!!, entry.name, "Line length for mount skeleton ${skeleton.mountSkeleton} says it's %NOMINAL_LENGTH% long.", currentModelDbLine)
				}
				val dummyZero1 = readSingleToken(inputStream)
				val dummyZero2 = readSingleToken(inputStream)
				val dummyZero3 = readSingleToken(inputStream)
			}
			else
			{
				if(main.data.unit.mountModels[skeleton.mount, true] == null && !main.lists.acceptedMissingMounts.contains(skeleton.mount))
					main.writeUnitLog(filename, currentModelDbLine, entry.name, "Mount model ${skeleton.mount} does not exist.")
				val primarySkeletonSegment :ModelDbSegment = readLengthNominatedSegment(inputStream)
				skeleton.primarySkeleton = StringUtil.standardize(primarySkeletonSegment.content)
				checkLengthMarker(primarySkeletonSegment.nominalContentLength, skeleton.primarySkeleton!!, entry.name, "Line length for primary skeleton ${skeleton.primarySkeleton} says it's %NOMINAL_LENGTH% long.", currentModelDbLine)
				
				val secondarySkeletonSegment :ModelDbSegment = readLengthNominatedSegment(inputStream)
				if(secondarySkeletonSegment.nominalContentLength != 0)
				{
					skeleton.secondarySkeleton = StringUtil.standardize(secondarySkeletonSegment.content)
					checkLengthMarker(secondarySkeletonSegment.nominalContentLength, skeleton.secondarySkeleton!!, entry.name, "Line length for secondary skeleton ${skeleton.secondarySkeleton} says it's %NOMINAL_LENGTH% long.", currentModelDbLine)
				}
				
				val weaponCount :Int = readSingleToken(inputStream).toInt()
				if(weaponCount != 0)
				{
					val primaryWeaponSegment :ModelDbSegment = readLengthNominatedSegment(inputStream)
					skeleton.primaryAttachmentPrimary = StringUtil.standardize(primaryWeaponSegment.content)
					checkLengthMarker(primaryWeaponSegment.nominalContentLength, skeleton.primaryAttachmentPrimary!!, entry.name, "Line length for primary weapon ${skeleton.primaryAttachmentPrimary} says it's %NOMINAL_LENGTH% long.", currentModelDbLine)
					if(weaponCount > 1)
					{
						val primaryOffhandSegment :ModelDbSegment = readLengthNominatedSegment(inputStream)
						skeleton.primaryAttachmentSecondary = StringUtil.standardize(primaryOffhandSegment.content)
						checkLengthMarker(primaryOffhandSegment.nominalContentLength, skeleton.primaryAttachmentSecondary!!, entry.name, "Line length for primary offhand ${skeleton.primaryAttachmentSecondary} says it's %NOMINAL_LENGTH% long.", currentModelDbLine)
					}
					val secondaryWeaponCount :Int = readSingleToken(inputStream).toInt()
					if(secondaryWeaponCount > 0)
					{
						val secondaryWeaponSegment :ModelDbSegment = readLengthNominatedSegment(inputStream)
						skeleton.secondaryAttachmentPrimary = StringUtil.standardize(secondaryWeaponSegment.content)
						checkLengthMarker(secondaryWeaponSegment.nominalContentLength, skeleton.secondaryAttachmentPrimary!!, entry.name, "Line length for secondary weapon ${skeleton.secondaryAttachmentPrimary} says it's %NOMINAL_LENGTH% long.", currentModelDbLine)
						if(secondaryWeaponCount > 1)
						{
							val secondaryOffhandSegment :ModelDbSegment = readLengthNominatedSegment(inputStream)
							skeleton.secondaryAttachmentSecondary = StringUtil.standardize(secondaryOffhandSegment.content)
							checkLengthMarker(secondaryOffhandSegment.nominalContentLength, skeleton.secondaryAttachmentSecondary!!, entry.name, "Line length for secondary offhand ${skeleton.secondaryAttachmentSecondary} says it's %NOMINAL_LENGTH% long.", currentModelDbLine)
						}
					}
				}
				else
					readSingleToken(inputStream)
			}
			entry.skeletons.add(skeleton)
		}
	}
	
	@Suppress("UNUSED_PARAMETER")
	private fun readTorch(entry :ModelDbEntry, inputStream :FileInputStream, isFirstEntry :Boolean)
	{
		if(isFirstEntry)
		{
			val dummyFirstValue1 = readSingleToken(inputStream)
			val dummyFirstValue2 = readSingleToken(inputStream)
			val dummyFirstValue3 = readSingleToken(inputStream)
			val dummyFirstValue4 = readSingleToken(inputStream)
		}
		//Just discard, we're not checking anything here.
		val dummyValue1 = readSingleToken(inputStream)
		val dummyValue2 = readSingleToken(inputStream)
		val dummyValue3 = readSingleToken(inputStream)
		val dummyValue4 = readSingleToken(inputStream)
		val dummyValue5 = readSingleToken(inputStream)
		val dummyValue6 = readSingleToken(inputStream)
		val dummyValue7 = readSingleToken(inputStream)
//		String[] tokens = splitLine()
//		entry.torchSettings = new double[tokens.length]
//		for(int i = 0; i < tokens.length; i++)
//			entry.torchSettings[i] = Double.parseDouble(tokens[i])
//		nextLine()
	}
	
	private fun checkLengthMarker(length :Int, string :String, entryName :String, message :String, lineNumber :Int)
	{
		if(length != string.length)
			main.writeUnitLog(filename, lineNumber, entryName, message.replace("%LENGTH%", "${string.length}").replace("%NOMINAL_LENGTH%", "$length"))
	}
	
	private fun readHeaderTokens(input :FileInputStream) :ArrayList<String>
	{
		val tokens = ArrayList<String>()
		for(i in 0 until 10)
			tokens.add(readSingleToken(input))
		return tokens
	}
	
	private fun readLengthNominatedSegment(inputStream :FileInputStream) :ModelDbSegment
	{
		var segmentLength = 0
		var segmentLengthDetermined = false
		var content = ""
		val currentToken = StringBuilder()
		var previousCharacter :Char? = null
		var keepReading = true
		while(keepReading)
		{
			var character :Char?
			if(unusedBits.size > 0)
				character = unusedBits.popFirst()
			else
				character = inputStream.read().toChar()
			
			if(character == '\t')
				character = ' '
			if(character == '\n')
			{
				currentModelDbLine++
				//Try to handle a missing trailing space at end of line
				if(previousCharacter != null && previousCharacter != ' ')
					character = ' '
			}
			if(character == '\r')
				Util.noop()
			else if(character == ' ' && currentToken.length >= segmentLength)
			{
				if(!segmentLengthDetermined)
				{
					if(currentToken.isNotEmpty())
					{
						segmentLength = Integer.parseInt(currentToken.toString())
						segmentLengthDetermined = true
						if(segmentLength == 0)
							return ModelDbSegment(0, "")
					}
				}
				else
				{
					content = currentToken.toString()
					keepReading = false
				}
				currentToken.delete(0, currentToken.length)
			}
			else if(character != '\n')
			{
				if(character != ' ' || currentToken.isNotEmpty())
					currentToken.append(character)
			}
			previousCharacter = character
		}
		return ModelDbSegment(segmentLength, content)
	}

	private fun readSingleToken(inputStream :FileInputStream) :String
	{
		var content = ""
		val currentToken = StringBuilder()
		var keepReading = true
		var segmentLengthDetermined = false
		var previousCharacter :Char? = null
		while(keepReading)
		{
			var character :Char?
			if(unusedBits.size > 0)
				character = unusedBits.popFirst()
			else
				character = inputStream.read().toChar()
			if(character == '\r')
				continue
			if(character == '\n')
			{
				currentModelDbLine++
				//Try to handle a missing trailing space at end of line
				if(previousCharacter != null && previousCharacter != ' ')
					character = ' '
				else
					continue
			}
			if(character == ' ')
			{
				if(currentToken.isNotEmpty())
				{
					content = currentToken.toString()
					keepReading = false
				}
			}
			else
			{
				currentToken.append(character)
				previousCharacter = character
			}
		}
		return content
	}
	
	private fun prependToUnusedBits(content :String)
	{
		val alreadyUnusedBits = StringBuilder()
		while(unusedBits.size > 0)
			alreadyUnusedBits.append(unusedBits.popFirst())
		for(character in content.toCharArray())
			unusedBits.add(character)
		for(character in alreadyUnusedBits.asIterable())
			unusedBits.add(character)
	}
}
