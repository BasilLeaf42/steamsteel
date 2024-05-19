package processing

import main.BovineM2twCheck

class Code(main :BovineM2twCheck)
{
	private val tas = TraitsAncillaries(main)
	private val script = Script(main)

	fun performChecks()
	{
		script.checkAll()
		tas.traitChecks()
		tas.traitTriggerChecks()
		tas.ancillaryChecks()
		tas.checkTraitBuildingReferences()
	}

	fun listUnused()
	{
		tas.listUnused()
		script.listUnused()
	}
}