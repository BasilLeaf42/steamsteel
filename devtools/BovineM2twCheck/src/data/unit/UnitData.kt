package data.unit

import data.CharacterEntry
import data.common.UsageTrackedCollection
import java.util.*

class UnitData
{
	val battleModels = UsageTrackedCollection<ModelDbEntry>()
	val mountModels = UsageTrackedCollection<ModelDbEntry>()
	val skeletons = UsageTrackedCollection<SkeletonEntry>()
	val characterTypes = ArrayList<CharacterEntry>()
	val engines = UsageTrackedCollection<EngineEntry>()
	val mounts = UsageTrackedCollection<MountEntry>()
	val unitDescriptions = ArrayList<UnitDescription>()
	val eduEntries = HashMap<String, EduEntry>()
	val usedAnimationFiles = ArrayList<String>()
	fun findUnitDescription(name :String) :UnitDescription?
	{
		for(descr in unitDescriptions)
		{
			if(name == descr.name)
				return descr
		}
		return null
	}

	fun findCharacterType(faction :String, type :String) :CharacterEntry?
	{
		for(characterType in characterTypes)
		{
			if(characterType.faction == faction && characterType.name == type)
				return characterType
		}
		return null
	}
}