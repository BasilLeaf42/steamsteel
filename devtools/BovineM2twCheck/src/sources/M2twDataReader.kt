package sources

import main.BovineM2twCheck
import sources.code.CodeReader
import sources.sound.SoundReader
import sources.stratmap.StratMapReader
import sources.unit.UnitReader

class M2twDataReader(main :BovineM2twCheck)
{
	private val textReader = TextReader(main)
	private val codeReader = CodeReader(main)
	private val unitReader = UnitReader(main)
	private val soundReader = SoundReader(main)
	private val stratMapReader = StratMapReader(main)

	fun readItAll()
	{
		stratMapReader.readWhenever()
		soundReader.readWhenever()
		textReader.readWhenever()
		codeReader.readWhenever()
		unitReader.readWhenever()

		stratMapReader.readLast()
		codeReader.readLast()
	}
}