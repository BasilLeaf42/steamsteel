package data.code.trait

class AffectClause(tokens :Array<String>)
{
	//Trait exists check at TraitsAncillariesScript.traitChecks
	var traitName :String = tokens[1]

	//Not checked
	var magnitude :Int = tokens[2].toInt()

	//Range 1-100 check at TraitsAncillariesScript.traitChecks
	var chance :Int = tokens[4].toInt()

}