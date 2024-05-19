package data

import data.common.TrackedName
import java.util.*

class CharacterEntry :TrackedName
{
	var actions = ArrayList<String>()
	var wageBase = 0
	var startingActionPoints = 0
	var faction :String? = null
	var dictionary = 0
	var stratModelNames = ArrayList<String>()
	var battleModelNames = ArrayList<String>()
	var battleEquip :String? = null

	constructor(type :String?, filename :String?, lineNumber :Int)
			:super(type!!, filename, lineNumber)

	constructor(copySource :CharacterEntry, lineNumber :Int)
			:super(copySource.name, copySource.filename, lineNumber)
	{
		actions = copySource.actions
		wageBase = copySource.wageBase
		startingActionPoints = copySource.startingActionPoints
		faction = null
		dictionary = 0
		battleEquip = null
	}
}