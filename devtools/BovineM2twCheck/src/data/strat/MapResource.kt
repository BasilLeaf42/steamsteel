package data.strat

class MapResource(resourceName :String, x :String, y :String)
{
	var name :String
	var x :Int
	var y :Int

	init
	{
		name = resourceName.replace(",", "")
		this.x = x.replace(",", "").toInt()
		this.y = y.replace(",", "").toInt()
	}
}