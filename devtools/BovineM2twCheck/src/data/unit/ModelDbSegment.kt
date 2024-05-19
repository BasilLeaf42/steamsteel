package data.unit

class ModelDbSegment(var nominalContentLength :Int, var content :String)
{
	override fun toString() :String
	{
		return "$nominalContentLength $content"
	}
}