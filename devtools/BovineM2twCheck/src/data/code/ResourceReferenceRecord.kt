package data.code

import data.common.SimpleReferenceRecord

class ResourceReferenceRecord(reference :String, occurringInFile :String, lineNumber :Int, var isForHiddenResource :Boolean)
	:SimpleReferenceRecord(reference, occurringInFile, lineNumber)
