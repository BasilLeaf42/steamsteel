package data.common

class IntegerValuedReferenceRecord(reference :String, filename :String, lineNumber :Int, val value :String)
	:SimpleReferenceRecord(reference, filename, lineNumber)
