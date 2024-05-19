package sources.unit

import data.common.FileReferenceRecord
import data.unit.EngineCrewAnimation
import data.unit.EngineEntry
import data.unit.EngineMesh
import data.unit.EngineModelGroup
import main.BovineM2twCheck
import util.CasUtil
import util.StringUtil
import java.io.BufferedReader
import java.io.File
import java.io.FileNotFoundException
import java.io.FileReader

class EngineReader(private val main :BovineM2twCheck)
{
	fun readEngines()
	{
		val filename = "descr_engines.txt"
		var readLine :String? = null
		var lineNumber = 0
		var crewAnimationsActive = false
		try
		{
			main.writeOutput(filename)
			val engineReader = BufferedReader(FileReader(main.runCfg.dataFolder + filename))
			var engine = EngineEntry("dummy", null, -1)
			var modelGroup = EngineModelGroup()
			while(run { readLine = engineReader.readLine(); readLine } != null)
			{
				val line :String = StringUtil.standardize(readLine!!)
				lineNumber++
				if(line == "")
					continue
				val tokens = StringUtil.split(line, " ")
				when
				{
					tokens[0] == "crew_animations" ->
					{
						if(crewAnimationsActive)
							main.writeUnitLog(filename, lineNumber, engine.name, "Parsing error: Crew animations is already active. Did you forget to end the previous engine's section?")
						crewAnimationsActive = true
					}
					crewAnimationsActive && tokens[0] == "end" ->
						crewAnimationsActive = false
					crewAnimationsActive ->
					{
						val animation = EngineCrewAnimation()
						animation.name = tokens[0]
						for(i in 1 until tokens.size)
							animation.animationSections.add(tokens[i].replace(",", ""))
						engine.crewAnimations.add(animation)
					}
					tokens[0] == "type" ->
					{
						engine = EngineEntry(tokens[1], filename, lineNumber)
						main.data.unit.engines.add(engine)
					}
					tokens[0] == "culture" ->
					{
						for(i in 1 until tokens.size)
						{
							var culture = tokens[i]
							if(culture.endsWith(","))
								culture = culture.substring(0, culture.length - 1)
							engine.cultures.add(culture)
						}
					}
					tokens[0] == "class" ->
						engine.engineClass = tokens[1]
					tokens[0] == "pathfinding_data" ->
					{
						engine.pathfinding = tokens[1]
						if(engine.pathfinding != "none")
							main.data.fileReferencesForCrossCheck.add(FileReferenceRecord(filename, lineNumber, engine.name, engine.pathfinding!!))
					}
					tokens[0] == "reference_points" ->
					{
						engine.referencePoints = tokens[1]
						main.data.fileReferencesForCrossCheck.add(FileReferenceRecord(filename, lineNumber, engine.name, engine.referencePoints!!))
					}
					tokens[0] == "engine_model_group" ->
					{
						modelGroup = EngineModelGroup()
						engine.modelGroups.add(modelGroup)
						for(i in 1 until tokens.size)
							modelGroup.names.add(tokens[i].replace(",", ""))
					}
					tokens[0] == "engine_skeleton" ->
						modelGroup.skeleton = tokens[1]
					tokens[0] == "engine_bone_map" ->
					{
						modelGroup.boneMap = tokens[1]
						main.data.fileReferencesForCrossCheck.add(FileReferenceRecord(filename, lineNumber, "${engine.name}'s model group ${modelGroup.name()}", modelGroup.boneMap!!))
					}
					tokens[0] == "engine_collision" ->
					{
						modelGroup.collision = tokens[1]
						main.data.fileReferencesForCrossCheck.add(FileReferenceRecord(filename, lineNumber, "${engine.name}'s model group ${modelGroup.name()}", modelGroup.collision!!, null, null, ".cmi", true))
					}
					tokens[0] == "engine_mesh" ->
					{
						val mesh = EngineMesh()
						mesh.filename = tokens[1]
						if(mesh.filename!!.endsWith(","))
							mesh.filename = mesh.filename!!.substring(0, mesh.filename!!.length - 1)
						modelGroup.meshes.add(mesh)
						main.data.fileReferencesForCrossCheck.add(FileReferenceRecord(filename, lineNumber, "${engine.name}'s model group ${modelGroup.name()}", mesh.filename!!))
						val textures = CasUtil.getCasFileTextures(mesh.filename!!, false)
						if(textures.size == 0 && !main.lists.vanillaFiles.contains(mesh.filename!!))
						{
							if(File("${main.runCfg.dataFolder}${mesh.filename}").exists())
								main.writeOutput("Found no textures in engine mesh ${mesh.filename}. This means the checker probably is lacking code to recognize its textures.")
						}
						if(textures.size > 0)
						{
							mesh.texture = textures[0]
							main.data.fileReferencesForCrossCheck.add(FileReferenceRecord(filename, lineNumber, """${engine.name}'s model group "${modelGroup.name()}"""", mesh.texture!!))
						}
						if(textures.size > 1)
						{
							mesh.normalTexture = textures[1]
							main.data.fileReferencesForCrossCheck.add(FileReferenceRecord(filename, lineNumber, """${engine.name}'s model group "${modelGroup.name()}"""", mesh.normalTexture!!))
						}
						if(textures.size > 2)
						{
							mesh.overlayTexture = textures[2]
							main.data.fileReferencesForCrossCheck.add(FileReferenceRecord(filename, lineNumber, """${engine.name}'s model group "${modelGroup.name()}"""", mesh.overlayTexture!!))
						}
					}
					tokens[0] == "engine_shadow" ->
						engine.shadow = tokens[1]
					tokens[0] == "engine_radius" ->
						engine.radius = tokens[1].toFloat()
					tokens[0] == "engine_visual_radius" ->
						engine.visualRadius = tokens[1].toFloat()
					tokens[0] == "engine_length" ->
						engine.length = tokens[1].toFloat()
					tokens[0] == "engine_width" ->
						engine.width = tokens[1].toFloat()
					tokens[0] == "engine_height" ->
						engine.height = tokens[1].toFloat()
					tokens[0] == "engine_mass" ->
					{
						//Need to handle alphanumeric, as the great bombard from vanilla has "5q"
						try { engine.mass = tokens[1].toFloat() }
						catch(e :NumberFormatException) { main.writeUnitLog(filename, lineNumber, engine.name, """Siege engine's mass should be numeric, rather than "${tokens[1]}"""") }
					}
					tokens[0] == "engine_dock_dist" ->
						engine.dockDistance = tokens[1].toFloat()
					tokens[0] == "engine_mob_dist" ->
						engine.mobDistance = tokens[1].toFloat()
					tokens[0] == "engine_flammable" ->
						engine.flammable = tokens[1] == "true"
					tokens[0] == "engine_ignition" ->
						engine.ignition = tokens[1].toFloat()
					tokens[0] == "fire_effect" ->
						engine.fireEffect = tokens[1]
					tokens[0] == "engine_front_attacked" ->
						engine.frontAttacked = tokens[1] == "true"
					tokens[0] == "sa_range" ->
						engine.saRange = tokens[1].toFloat()
					tokens[0] == "sa_friendly_range" ->
						engine.saFriendlyRange = tokens[1].toFloat()
					tokens[0] == "obstacle_shape" ->
						engine.obstacleShape = tokens[1]
					tokens[0] == "obstacle_x_radius" ->
						engine.obstacleXRadius = tokens[1].toFloat()
					tokens[0] == "obstacle_y_radius" ->
						engine.obstacleYRadius = tokens[1].toFloat()
					tokens[0] == "engine_spo" ->
						engine.spo = tokens[1]
					tokens[0] == "engine_push_point" ->
						engine.pushPoints.add(line.substring("engine_push_point ".length))
					tokens[0] == "engine_station" ->
						engine.station = line.substring("engine_station ".length)
					tokens[0] == "engine_health" ->
						engine.health = tokens[1].toInt()
					tokens[0] == "missile_pos" ->
						engine.missilePosition = line.substring("missile_pos ".length)
					tokens[0] == "normal_shots" ->
						engine.normalShots = tokens[1].toInt()
					tokens[0] == "special_shots" ->
						engine.specialShots = tokens[1].toInt()
					tokens[0] == "shot_delay" ->
						engine.shotDelay = tokens[1].toInt()
					tokens[0] == "shot_pfx_front" ->
						engine.shotPfxFront = tokens[1]
					tokens[0] == "shot_pfx_back" ->
						engine.shotPfxBack = tokens[1]
					tokens[0] == "shot_sfx" ->
						engine.shotSfx = tokens[1]
					tokens[0] == "engine_formation" ->
						engine.formation = line.substring("engine_formation ".length)
					tokens[0] == "area_effect" ->
						engine.areaEffect = line.substring("area_effect ".length)
					tokens[0] == "surface_occupants" ->
						engine.surfaceOccupants = tokens[1].toInt()
					tokens[0] == "variant" ->
						engine.variant = tokens[1]
					tokens[0] == "attack_stat" ->
						engine.attackStats = line.substring("attack_stat ".length)
					tokens[0] == "attack_stat_attr" ->
						engine.attackAttributes = line.substring("attack_stat_attr ".length)
					tokens[0] == "arrow_generator" ->
						engine.arrowGenerator = line.substring("arrow_generator ".length)
					tokens[0] == "aim_dir" ->
						engine.attackAttributes = line.substring("aim_dir ".length)
					tokens[0] == "aim_arc" ->
						engine.aimArc = tokens[1].toFloat()
					tokens[0] == "fire_interval" ->
						engine.fireInterval = tokens[1].toFloat()
					else ->
						main.writeOutput("$filename $lineNumber: Unrecognized directive on line: $line")
				}
			}
			engineReader.close()
		}
		catch(e :FileNotFoundException)
		{
			main.writeOutput("Unable to find list of engine models ($filename). This may cause false reports.")
		}
		catch(e :Exception)
		{
			main.fatalParsingError(lineNumber, readLine!!, e)
		}
	}
}