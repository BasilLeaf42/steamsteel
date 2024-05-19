package data.sound

import data.common.*
import kotlin.collections.ArrayList
import kotlin.collections.HashMap

class SoundData
{
	//TODO check assignments
	val accentFactions = HashMap<String, ArrayList<String>>()
	val diplomacySpeechHeaders = UsageTrackedCollection<UsageTrackedName>()
	val diplomacySoundReferences = ArrayList<SimpleReferenceRecord>()

	val genericMusic = ArrayList<MusicEventOrState>()
	val musicTypeFactionAssignments = HashMap<String, ArrayList<String>>()
	val musicStates = HashMap<String, ArrayList<MusicEventOrState>>()

	val campMapVoiceReferences = FileReferenceCollection<VoiceFileReference>()
	val battleMapVoiceReferences = FileReferenceCollection<VoiceFileReference>()
	val narrationVoiceReferences = FileReferenceCollection<VoiceFileReference>()
	val adviceVoiceReferences = FileReferenceCollection<VoiceFileReference>()

	val effects = FileReferenceCollection<FileReferenceRecord>()
	val effectReferences = ArrayList<SimpleReferenceRecord>()
}