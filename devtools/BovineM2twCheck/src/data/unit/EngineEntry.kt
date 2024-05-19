package data.unit

import data.common.UsageTrackedName
import java.util.*

class EngineEntry(name :String?, occurringInFile :String?, lineNumber :Int) :UsageTrackedName(name!!, occurringInFile, lineNumber)
{
	//Checked for valid culture at Unit.unitChecks
	var cultures = ArrayList<String>()

	//TODO lots of checks, I'm sure!
	//Checked for valid values
	var engineClass :String? = null

	//Checked file reference
	var pathfinding :String? = null

	//Checked file reference
	var referencePoints :String? = null
	var modelGroups = ArrayList<EngineModelGroup>()

	//TODO what is this?
	var shadow :String? = null

	//Section below not checked
	var radius :Float? = null
	var visualRadius :Float? = null
	var length :Float? = null
	var width :Float? = null
	var height :Float? = null
	var mass :Float? = null
	var dockDistance :Float? = null
	var mobDistance :Float? = null
	var flammable = false
	var ignition :Float? = null
	var frontAttacked = false
	var saRange :Float? = null
	var saFriendlyRange :Float? = null
	var obstacleShape :String? = null
	var obstacleXRadius :Float? = null
	var obstacleYRadius :Float? = null

	//TODO find and check reference
	var fireEffect :String? = null

	//TODO find and check reference
	var spo :String? = null
	var pushPoints = ArrayList<String>()
	var station :String? = null
	var health :Int? = null
	var missilePosition :String? = null
	var normalShots :Int? = null
	var specialShots :Int? = null
	var shotDelay :Int? = null
	var shotPfxFront :String? = null
	var shotPfxBack :String? = null
	var shotSfx :String? = null
	var formation :String? = null
	var areaEffect :String? = null
	var surfaceOccupants :Int? = null
	var variant :String? = null

	//TODO check valid values
	var attackStats :String? = null

	//TODO check valid values
	var attackAttributes :String? = null
	var arrowGenerator :String? = null
	var aimDirection :String? = null
	var aimArc :Float? = null
	var fireInterval :Float? = null

	//TODO find and check references
	var crewAnimations = ArrayList<EngineCrewAnimation>()
}