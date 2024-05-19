package util

class QueueNode<Gen>
(var content :Gen)
{
	var nextNode :QueueNode<Gen>? = null
}