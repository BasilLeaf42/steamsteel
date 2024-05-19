package util

import java.util.*

object Util
{
	fun addIfNotPresent(string :String, array :ArrayList<String>)
	{
		for(presentString in array)
			if(presentString == string)
				return
		array.add(string)
	}

	fun equalsAny(test :String?, comparison1 :String, comparison2 :String) :Boolean
	{
		if(test == null)
			return false
		return test == comparison1 || test == comparison2
	}

	fun equalsAny(test :String?, comparison1 :String, comparison2 :String, comparison3 :String) :Boolean
	{
		if(test == null)
			return false
		return equalsAny(test, comparison1, comparison2) || test == comparison3
	}

	fun equalsAny(test :String?, comparison1 :String, comparison2 :String, comparison3 :String, comparison4 :String) :Boolean
	{
		if(test == null)
			return false
		return equalsAny(test, comparison1, comparison2, comparison3) || test == comparison4
	}

	fun equalsAny(test :String?, comparison1 :String, comparison2 :String, comparison3 :String, comparison4 :String, comparison5 :String) :Boolean
	{
		if(test == null)
			return false
		return equalsAny(test, comparison1, comparison2, comparison3, comparison4) || test == comparison5
	}

	fun noop() {}

	fun arrayListToArray(source :ArrayList<String>) :Array<String>
	{
		val retur = Array<String>(source.size) { "" }
		source.toArray(retur)
		return retur
	}
}