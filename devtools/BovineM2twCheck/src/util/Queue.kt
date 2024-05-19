package util

import java.util.*

class Queue<Gen>
{
	private var firstNode :QueueNode<Gen>? = null
	private var lastNode :QueueNode<Gen>? = null

	/**
	 * Gets the number of elements in the queue.
	 * @return Number of elements
	 */
	var size = 0
		private set

	/**
	 * Adds an item at the end of the Queue.
	 * @param   item   The item to put in
	 */
	fun add(item :Gen)
	{
		if(size == 0)
		{
			lastNode = QueueNode(item)
			firstNode = lastNode
		}
		else
		{
			lastNode!!.nextNode = QueueNode(item)
//			lastNode.nextNode.previousNode = lastNode;
			lastNode = lastNode!!.nextNode
		}
		size++
	}

	/**
	 * Gets and removes the first item from the queue.
	 * @return  The first item stored
	 */
	fun popFirst() :Gen?
	{
		if(size == 0)
			return null
		val retur = firstNode!!.content
		firstNode = firstNode!!.nextNode
		if(firstNode == null)
			lastNode = null
		size--
		return retur
	}

	/**
	 * Gets and removes the last item from the queue.
	 * @return  The last item stored
	 */
	fun popLast() :Gen?
	{
		if(size == 0)
			return null
		val retur = lastNode!!.content
		lastNode = getPreviousNode(lastNode)
		if(lastNode != null)
			lastNode!!.nextNode = null
		else
			firstNode = null
		size--
		return retur
	}

	private fun getPreviousNode(itsNextNode :QueueNode<Gen>?) :QueueNode<Gen>?
	{
		if(size <= 1)
			return null
		var node = firstNode
		while(node != null && node.nextNode != itsNextNode)
			node = node.nextNode
		return node
	}

	/**
	 * Gets all contents in the queue, without removing any from the queue.
	 */
	fun all() :ArrayList<Gen>
	{
		val retur = ArrayList<Gen>(size)
		var node = firstNode
		while(node != null)
		{
			retur.add(node.content)
			node = node.nextNode
		}
		return retur
	}

	/**
	 * Gets all contents in the queue, removing them from the queue in the process.
	 */
	fun removeAll() :ArrayList<Gen?>
	{
		val retur = ArrayList<Gen?>(size)
		while(size > 0)
			retur.add(popFirst())
		return retur
	}

	fun peekFirst() :Gen?
	{
		return if(firstNode == null)
			null
		else
			firstNode!!.content
	}

	fun peekLast() :Gen?
	{
		return if(firstNode == null)
			null
		else
			lastNode!!.content
	}

	override fun toString() :String
	{
		val retur = StringBuilder()
		var item :QueueNode<Gen>? = firstNode
		while(item != null)
		{
			if(retur.isNotEmpty())
				retur.append(", ")
			retur.append(item.content.toString())
			item = item.nextNode
		}
		return retur.toString()
	}
}