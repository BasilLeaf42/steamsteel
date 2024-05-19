package data.code.trait

import data.common.SimpleReferenceRecord

class TraitReferenceRecord(occurringInFile :String, lineNumber :Int, reference :String, referencedLevel :Int?, awardedAmount :Int? = null)
	:SimpleReferenceRecord(reference, occurringInFile, lineNumber)
{
	//Checked for level existence at TraitsAncillariesScript.traitChecks => checkTraitReference
	var referencedLevel = -1
	var awardedAmount :Int? = null

	constructor(occurringInFile :String, lineNumber :Int, reference :String, referencedLevel :String)
			:this(occurringInFile, lineNumber, reference, referencedLevel.toInt())

	constructor(occurringInFile :String, lineNumber :Int, reference :String, referencedLevel :Int?, awardedAmount :String)
			:this(occurringInFile, lineNumber, reference, referencedLevel, awardedAmount.toInt())

	init
	{
		this.referencedLevel = referencedLevel ?: -1
		this.awardedAmount = awardedAmount
	}
}