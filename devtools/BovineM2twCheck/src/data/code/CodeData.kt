package data.code

import data.CharacterNameReferenceRecord
import data.common.SimpleReferenceRecord
import data.code.script.DeclaredCounterEntry
import data.code.script.EventCounterEntry
import data.code.trait.TraitEntry
import data.code.trait.TraitReferenceRecord
import data.code.trait.TraitTriggerEntry
import data.common.IntegerValuedReferenceRecord
import data.common.UsageTrackedCollection
import data.common.UsageTrackedName
import data.strat.MapCharacter
import java.util.*
import kotlin.collections.ArrayList

class CodeData
{
	val customScripts = ArrayList<String>()
	val adviceThreads = UsageTrackedCollection<UsageTrackedName>()
	val scriptInvokedAdvice = ArrayList<String>()
	val ancillaryNames = ArrayList<String>()
	val edaTriggers = ArrayList<String>()
	val traits = UsageTrackedCollection<TraitEntry>()
	val traitTriggers = UsageTrackedCollection<TraitTriggerEntry>()
	val declaredCounters = UsageTrackedCollection<DeclaredCounterEntry>()
	val eventCounters = UsageTrackedCollection<EventCounterEntry>()
	val buildingLevelReferences = ArrayList<SimpleReferenceRecord>()
	val edaTraitReferences = ArrayList<TraitReferenceRecord>()
	val scriptTraitReferences = ArrayList<TraitReferenceRecord>()
	val unitReferences = ArrayList<SimpleReferenceRecord>()
	val characterNameReferences = ArrayList<CharacterNameReferenceRecord>()
	val labelReferences = ArrayList<SimpleReferenceRecord>()
	val factionReferences = ArrayList<SimpleReferenceRecord>()

	val scriptedCharacters = ArrayList<MapCharacter>()

	fun addSetEventCounterLocation(record :SimpleReferenceRecord)
	{
		var referencedEvent = record.reference
		var newEntryIsDecision = false
		var entry = eventCounters[referencedEvent, false]
		if(entry == null && referencedEvent.endsWith("_accepted") || referencedEvent.endsWith("_declined"))
		{
			referencedEvent = referencedEvent.replace("_accepted", "").replace("_declined", "")
			newEntryIsDecision = true
			entry = eventCounters[referencedEvent, false]
		}
		if(entry == null)
		{
			entry = EventCounterEntry(record.reference, record.filename, record.lineNumber)
			entry.isDecision = newEntryIsDecision
			entry.isHistoric = newEntryIsDecision
			eventCounters.add(entry)
		}
		entry.setLocations.add(record)
		if(entry.filename == null)
		{
			entry.filename = record.filename
			entry.lineNumber = record.lineNumber
		}
	}

	fun addCheckedEventCounterLocation(record :SimpleReferenceRecord)
	{
		var referencedEvent = record.reference
		var newEntryIsDecision = false
		var entry = eventCounters[referencedEvent, false]
		if(entry == null && referencedEvent.endsWith("_accepted") || referencedEvent.endsWith("_declined"))
		{
			referencedEvent = referencedEvent.replace("_accepted", "").replace("_declined", "")
			newEntryIsDecision = true
			entry = eventCounters[referencedEvent, false]
		}
		if(entry == null)
		{
			entry = EventCounterEntry(referencedEvent)
			entry.isDecision = newEntryIsDecision
			entry.isHistoric = newEntryIsDecision
			eventCounters.add(entry)
		}
		entry.checkedLocations.add(record)
	}

	fun getHistoricEvents() :ArrayList<EventCounterEntry>
	{
		val retur = ArrayList<EventCounterEntry>()
		for(event in eventCounters.getAll())
		{
			if(event.isHistoric)
				retur.add(event)
		}
		return retur
	}

	fun addCheckedDeclaredCounterLocation(location :SimpleReferenceRecord)
	{
		var declaredCounter = declaredCounters[location.reference, false]
		if(declaredCounter == null)
		{
			declaredCounter = DeclaredCounterEntry(location.reference, location.filename, location.lineNumber)
			declaredCounters.add(declaredCounter)
		}
		declaredCounter.checkedLocations.add(location)
	}

	fun addSetDeclaredCounterLocation(location :IntegerValuedReferenceRecord)
	{
		var declaredCounter = declaredCounters[location.reference, false]
		if(declaredCounter == null)
		{
			declaredCounter = DeclaredCounterEntry(location.reference, location.filename, location.lineNumber)
			declaredCounters.add(declaredCounter)
		}
		declaredCounter.setLocations.add(location)
	}

	fun addDeclaredCounter(counter :SimpleReferenceRecord)
	{
		var declaredCounter = declaredCounters[counter.reference, false]
		if(declaredCounter == null)
		{
			declaredCounter = DeclaredCounterEntry(counter.reference, counter.filename, counter.lineNumber)
			declaredCounters.add(declaredCounter)
		}
		declaredCounter.declaredLocations.add(counter)
	}
}