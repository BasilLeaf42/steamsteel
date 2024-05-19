package data.unit

import data.common.UsageTrackedName
import java.util.*

class ModelDbEntry(name :String?, lineNumber :Int) :UsageTrackedName(name!!, "battle_models.modeldb", lineNumber)
{
	var nominalModelCount = 0
	var modelAssignments = ArrayList<ModelAssignment>()
	var nominalTextureAssignmentCount = 0
	var textureAssignments = ArrayList<TextureAssignment>()
	var nominalAttachmentAssignmentCount = 0
	var attachmentAssignments = ArrayList<AttachmentAssignment>()
	var nominalSkeletonCount = 0
	var skeletons = ArrayList<ModelDbSkeleton>()
	var isMount = false

	class ModelDbSkeleton
	{
		var mount :String? = null
		var mountSkeleton :String? = null
		var primarySkeleton :String? = null
		var secondarySkeleton :String? = null
		var primaryAttachmentPrimary :String? = null
		var primaryAttachmentSecondary :String? = null
		var secondaryAttachmentPrimary :String? = null
		var secondaryAttachmentSecondary :String? = null
	}

	class TextureAssignment
	{
		var lineNumber :Int? = null
		var faction :String? = null
		var texture :String? = null
		var normalTexture :String? = null
		var sprite :String? = null
	}

	class AttachmentAssignment
	{
		var lineNumber :Int? = null
		var faction :String? = null
		var texture :String? = null
		var normalTexture :String? = null
	}

	class ModelAssignment
	{
		var lineNumber :Int? = null
		var fileName :String? = null
		var viewDistance :String? = null
	}

	override fun toString() :String
	{
		return name
	}
}