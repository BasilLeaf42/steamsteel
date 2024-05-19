package data.common;

open class UsageTrackedName(name :String, filename :String?, lineNumber :Int?) :TrackedName(name, filename, lineNumber)
{
	var isUsed = false
}
