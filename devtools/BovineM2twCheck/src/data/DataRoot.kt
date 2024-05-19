package data

import main.BovineM2twCheck
import data.sound.SoundData
import data.unit.UnitData
import data.code.CodeData
import data.text.TextData
import data.strat.StratmapData
import data.common.FileReferenceCollection
import data.common.FileReferenceRecord
import java.util.ArrayList

class DataRoot(main :BovineM2twCheck)
{
	val sound = SoundData()
	val unit = UnitData()
	val code = CodeData()
	val text = TextData()
	val strat = StratmapData(main)
	val fileReferencesForCrossCheck = FileReferenceCollection<FileReferenceRecord>()
	val encounteredFileReferences = ArrayList<String>()
}