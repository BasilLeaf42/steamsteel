package data

import data.common.SimpleReferenceRecord

class CharacterNameReferenceRecord(
		reference :String
		,filename :String
		,lineNumber :Int
		,var faction :String?
		,var subFaction :String?)
	:SimpleReferenceRecord(reference, filename, lineNumber)
