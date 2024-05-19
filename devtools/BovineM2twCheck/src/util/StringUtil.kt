package util

object StringUtil
{
	//Ignore case, comments, starting whitespace and multiple spaces
	fun standardize(input :String) :String
	{
		var retur :String = input.replace("\t", " ")
		while(retur.contains("  "))
			retur = retur.replace("  ", " ")
		while(retur.startsWith(" "))
			retur = retur.substring(1)
		retur = retur.lowercase()
		if(retur.contains(";"))
			retur = retur.substring(0, retur.indexOf(";"))
		return retur
	}

	fun isInteger(test :String) :Boolean
	{
		return test.toIntOrNull() != null
	}

	/**
	 * Gets the substring before a given pattern. If not present, returns the full string.
	 */
	fun before(str :String, pattern :String) :String
	{
		val position :Int = str.indexOf(pattern)
		if(position >= 0)
			return str.substring(0, position)
		return str
	}

	/**
	 * Gets the substring after a given pattern. If not present, returns the full string.
	 */
	fun after(str :String, pattern :String) :String
	{
		val position :Int = str.indexOf(pattern)
		if(position >= 0)
			return str.substring(position + pattern.length)
		return str
	}

	/**
	 * Gets the substring before a given pattern, searched from the end. If not present, returns the full string.
	 */
	fun beforeLast(str :String, pattern :String) :String
	{
		val position :Int = str.lastIndexOf(pattern)
		if(position >= 0)
			return str.substring(0, position)
		return str
	}

	/**
	 * Gets the substring between two given patterns.
	 */
	fun between(str :String?, firstPattern :String, lastPattern :String) :String?
	{
		return between(str, firstPattern, lastPattern, 0)
	}

	/**
	 * Gets the substring between two given patterns,
	 * starting the search for the first pattern at the begin index.
	 */
	fun between(str :String?, firstPattern :String, lastPattern :String, beginIndex :Int) :String?
	{
		if(str == null)
			return null
		var retur :String? = null
		var pos :Int = str.indexOf(firstPattern, beginIndex)
		if(pos >= 0)
		{
			pos += firstPattern.length
			val endPos :Int = str.indexOf(lastPattern, pos)
			if(endPos >= 0)
				retur = str.substring(pos, endPos)
		}
		return retur
	}

	/**
	 * Counts the number of occurrences of a string inside another string
	 */
	fun patternCountInString(source :String, pattern :String?) :Int
	{
		var retur :Int = 0
		var startPosition :Int = 0
		while(source.indexOf(pattern!!, startPosition) >= 0 && startPosition < source.length)
		{
			val index :Int = source.indexOf(pattern, startPosition)
			retur++
			startPosition = index + 1
		}
		return retur
	}

	fun ensureEndsWith(test :String, requiredEnding :String) :String
	{
		if(!test.endsWith(requiredEnding))
			return test + requiredEnding
		return test
	}

	fun exceptBefore(str :String, pattern :String) :String
	{
		val before :String = before(str, pattern)
		if(before == str)
			return ""
		return after(str, pattern)
	}

	fun split(source :String, pattern :String) :Array<String>
	{
		val regex :Regex = pattern.toRegex()
		return source.split(regex).toTypedArray()
	}
}