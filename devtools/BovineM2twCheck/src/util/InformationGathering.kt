package util

import java.io.File
import java.io.IOException

object InformationGathering
{
	fun printVanillaAnimationList()
	{
		val rootPath = "C:/Spill/M2TWOtherMods/data"
		val currentPath = "animations"
		printVanillaAnimationFolder(rootPath, currentPath)
	}

	private fun printVanillaAnimationFolder(rootPath :String, currentPath :String)
	{
		val thisFolder = File("$rootPath/$currentPath")
		for(content in thisFolder.listFiles())
		{
			if(content.isDirectory)
				printVanillaAnimationFolder(rootPath, "$currentPath/${content.name}")
			else
				println("$currentPath/${content.name}")
		}
	}
}