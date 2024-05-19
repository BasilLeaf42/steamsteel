package data.unit

import data.common.UsageTrackedName
import java.util.*

class SkeletonEntry(name :String?, occurringInFile :String?, lineNumber :Int) :UsageTrackedName(name!!, occurringInFile, lineNumber)
{
	var isEngine = false
	var parent :String? = null
	var referencePoints :String? = null
	var scale = 1.0f
	var animations = ArrayList<SkeletonAnimation>()
	var strikeDistances :String? = null
	var inAwareness :Float? = null
	var inZone :Float? = null
	var inCentre :Float? = null
	var forceHitPositionsToCylinder = false
	var removeAttackAnimations = false
	var suppressRefPointsWarning = false

	//Locomotion table is used when a soldier is supposed to move independently, no deltas when it's stationary and riding a mount
	var locomotionTable :String? = null
	var noDeltas = false
}