package util

import java.io.BufferedReader
import java.io.FileNotFoundException
import java.io.FileReader
import java.util.*
import kotlin.collections.ArrayList

object CasUtil
{
	private val storedQueries = HashMap<String, ArrayList<String>>()
	var dataFolder :String = ""

	fun getCasFileTextures(filename :String, applyRelativeCasPathToTextures :Boolean) :ArrayList<String>
	{
		var foundTextures :ArrayList<String>? = storedQueries[filename]
		if(foundTextures != null)
			return foundTextures
		foundTextures = ArrayList<String>()

		val partOfTexturePathRegex :Regex = "^[a-zA-Z0-9#_\\/\\\\\\. ]$".toRegex()
//		val partOfTexturePathRegex :Regex = "^[a-zA-Z0-9#_/\\\\.]$".toRegex()
		var relativePath :String = ""
		if(filename.contains("/"))
			relativePath = filename.substring(0, filename.lastIndexOf("/"))
		if(filename.contains("\\"))
			relativePath = filename.substring(0, filename.lastIndexOf("\\"))
		if(relativePath.isNotEmpty())
			relativePath += "/"
		try
		{
			val casReader :BufferedReader = BufferedReader(FileReader(dataFolder + filename))
			var readLine :String?
			while(run { readLine = casReader.readLine(); readLine } != null)
			{
				var line :String = readLine!!
				var textureLocation :Int = line.indexOf("textures")
				while(textureLocation >= 0)
				{
					while(line.substring(textureLocation, textureLocation + 1).matches(partOfTexturePathRegex))
						textureLocation--
					line = line.substring(textureLocation + 1)
					var endOfTexture :Int = 0
					while(line.substring(endOfTexture, endOfTexture + 1).matches(partOfTexturePathRegex))
						endOfTexture++
					var texture :String = line.substring(0, endOfTexture).lowercase()
					while(texture.indexOf(".texture") > 0 && !texture.endsWith(".texture"))
						texture = texture.substring(0, texture.length - 1)
					if(!texture.endsWith(".texture") && !texture.endsWith(".tga"))
						texture += ".dds"
					texture = texture.replace("\\", "/")
					if(texture.startsWith("/"))
						texture = texture.substring(1)
					if(applyRelativeCasPathToTextures)
						foundTextures.add(relativePath + texture)
					else foundTextures.add(texture)
					line = line.substring(texture.length)
					textureLocation = line.indexOf("texture")
				}
			}
			casReader.close()
		}
		catch(e :FileNotFoundException)
		{
			Util.noop()
		}
		storedQueries[filename] = foundTextures
		return foundTextures
	}
}