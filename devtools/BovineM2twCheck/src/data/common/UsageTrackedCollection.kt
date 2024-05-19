package data.common

import java.util.ArrayList
import java.util.HashMap

class UsageTrackedCollection<Gen :UsageTrackedName>
{
	private val contents = ArrayList<Gen>()
	
	fun add(name :Gen)
	{
		contents.add(name)
	}
	
	operator fun get(name :String?, markUsed :Boolean) :Gen?
	{
		for(entry :Gen in contents)
		{
			if(entry.name == name)
			{
				if(markUsed)
					entry.isUsed = true
				return entry
			}
		}
		return null
	}
	
	fun getDuplicates() :ArrayList<DuplicateCount>
	{
		val counts = HashMap<String, DuplicateCount>()
		for(name :Gen in contents)
		{
			val dupe :DuplicateCount? = counts[name.name]
			if(dupe == null)
				counts[name.name] = DuplicateCount(name.name)
			else
				dupe.increaseCount()
		}
		val retur = ArrayList<DuplicateCount>()
		for(dupe :DuplicateCount in counts.values)
		{
			if(dupe.count > 1)
				retur.add(dupe)
		}
		return retur
	}
	
	fun getUnused() :ArrayList<Gen>
	{
		val retur = ArrayList<Gen>()
		for(name :Gen in contents)
		{
			if(!name.isUsed)
				retur.add(name)
		}
		return retur
	}
	
	fun count() :Int
	{
		return contents.size
	}

	fun getAll() :ArrayList<Gen>
	{
		return contents
	}
}
