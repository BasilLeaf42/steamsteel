package data.unit

class UnitDescription(var name :String?, var shortDescription :String?, var longDescription :String?)
{
	var nameLineNumber = 0
	var shortLineNumber = 0
	var longLineNumber = 0
	var isDuplicate = false
	var nameIsVerifiedPresent = false
}