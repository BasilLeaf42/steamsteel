package sources.code

import main.BovineM2twCheck

class CodeReader(main :BovineM2twCheck)
{
	private val traitReader = TraitReader(main)
	private val eventReader = EventReader(main)
	private val scriptReader = ScriptReader(main)
	private val adviceReader = AdviceReader(main)
	private val ancillaryReader = AncillaryReader(main)

	fun readWhenever()
	{
		traitReader.readAll()
		eventReader.readAll()
		scriptReader.loadScripts()
		adviceReader.readAdvice()
	}

	fun readLast()
	{
		scriptReader.loadCustomScripts()
		ancillaryReader.readAll()
	}
}