package data.common

open class TrackedName(var name :String, var filename :String?, var lineNumber :Int?)
{
	override fun toString() :String
	{
		return "$name ($filename:$lineNumber)"
	}
}
