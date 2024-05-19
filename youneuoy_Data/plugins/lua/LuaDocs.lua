---@diagnostic disable: missing-return, lowercase-global
---Basic M2TWEOP table
---@class M2TWEOP
M2TWEOP = { 

}

--- Function to return the path to the mod folder, starts from the drive not the game folder.
---@return string mod path
function M2TWEOP.getModPath() end 

--- Open/close the lua console.
function M2TWEOP.toggleConsole() end 

--- Reload the lua script (without restarting the plugin itself, onPluginLoad doesn't fire).
function M2TWEOP.reloadScript() end 

--- Restart the lua plugin (onPluginLoad fires).
function M2TWEOP.restartLua() end 

--- Toggle developer mode.
function M2TWEOP.toggleDeveloperMode() end 

--- Save the game.
---@param path string (start from mods)
function M2TWEOP.saveGame(path) end 

--- Function to get the game version.
---@return integer gamever (1 = disk 2 = steam)
function M2TWEOP.getGameVersion() end 

--- Set perfect spy.
---@param set boolean 
function M2TWEOP.setPerfectSpy(set) end 

--- Get local faction ID.
---@return integer localFaction 
function M2TWEOP.getLocalFactionID() end 

--- Function to return the path to the plugin (location of your LUA files).
---@return string plugin path
function M2TWEOP.getPluginPath() end 

--- Load d3d texture
---@param path string full path to texture
---@return integer x size of the image
---@return integer y size of the image
---@return integer id of the image
function M2TWEOP.loadTexture(path) end 

--- Unload d3d texture
---@param id integer of the image
function M2TWEOP.unloadTexture(id) end 

--- Sets the limit of ancillaries per character on the stratmap.
---@param newLimit integer default: 8, maximum: 127
function M2TWEOP.setAncillariesLimit(newLimit) end 

--- Unlocks all console commands, also allows the use of the 'control' command to change factions in singleplayer campaigns.
function M2TWEOP.unlockGameConsoleCommands() end 

--- Sets the maximum amount of soldiers a general's bodyguard unit can replenish to. The value is multiplied by the unit size modifiers (e.g Huge = 2.5 multiplier)
---@param newSize integer 
function M2TWEOP.setMaxBgSize(newSize) end 

--- Toggle the highlighting of units on the tactical map.
function M2TWEOP.toggleUnitsBMapHighlight() end 

--- Get the current x, y and z coords of the battlemap camera
---@return battleCameraStruct Camera struct
function M2TWEOP.getBattleCamCoords() end 

--- Set the maximum number of religions in the mod (per descr\_religions.txt). Do not use religions > 10 in CombatVsReligion attributes!
---@param newLimit integer maximum: 127
function M2TWEOP.setReligionsLimit(newLimit) end 

--- Set the siege points required to make different siege equipment.
---@param equipmentType integer 0 = ram, 1 = ladder, 2 = siege tower
---@param newCost integer 
function M2TWEOP.setEquipmentCosts(equipmentType, newCost) end 

--- Checks if a tile is free.
---@param X integer coordinate of the tile.
---@param Y integer coordinate of the tile.
function M2TWEOP.isTileFree(X, Y) end 

--- Get the selected tile coords.
---@return integer x 
---@return integer y 
function M2TWEOP.getGameTileCoordsWithCursor() end 

--- Get the RegionID of a tile.
---@param x integer 
---@param y integer 
---@return integer regionID 
function M2TWEOP.getTileRegionID(x, y) end 

--- Get a specific tile's visibility according to faction (i.e can a faction see a tile) Note: Once the tile has been seen by a faction, it will always return true. e.g If you have spotted a settlement but it is now outside of the fog of war, it will still be classed as visible.
---@param faction factionStruct Faction to check
---@param xCoord integer x coord of the tile
---@param yCoord integer y coord of the tile
---@return boolean isVisible true = visible, false = not visible
function M2TWEOP.getTileVisibility(faction, xCoord, yCoord) end 

--- * Sets the minimum number of turns until the next guild offer after a rejection by the player.
---@param turns integer default: 10
function M2TWEOP.setGuildCooldown(turns) end 

--- Get the owner of a region by RegionID.
---@param regionID integer 
---@return factionStruct owner 
function M2TWEOP.getRegionOwner(regionID) end 

--- Sets the new maximum soldier count.
---@param minSize integer maximum: 300
---@param maxSize integer maximum: 300
function M2TWEOP.setEDUUnitsSize(minSize, maxSize) end 

--- * Sets the new maximum amount of building levels within a chain.
---@param limit integer default: 9, maximum: 57
function M2TWEOP.setBuildingChainLimit(limit) end 

--- Get religion name by index.
---@param index integer 
---@return string name 
function M2TWEOP.getReligionName(index) end 

--- Get the amount of religions.
---@return integer religionCount 
function M2TWEOP.getReligionCount() end 

--- Get religion ID by name.
---@param name string 
---@return integer index 
function M2TWEOP.getReligion(name) end 

--- Check game condition.
---@param condition string 
---@param eventData eventTrigger|nil? 
---@return boolean isTrue 
function M2TWEOP.condition(condition, eventData) end 

--- Get some game options.
---@return options1 options 
function M2TWEOP.getOptions1() end 

--- Get some game options.
---@return options2 options 
function M2TWEOP.getOptions2() end 

--- Get the campaign difficulty modifiers.
---@return campaignDifficulty1 options 
function M2TWEOP.getCampaignDifficulty1() end 

--- Get the campaign difficulty modifiers.
---@return campaignDifficulty2 options 
function M2TWEOP.getCampaignDifficulty2() end 

---Get information about the camera in a battle
---@class battleCameraStruct
battleCameraStruct = { 

    ---@type number
    xCoord = nil,

    ---@type number
    yCoord = nil,

    ---@type number
    zCoord = nil,

}

---Basic gameSTDUI table
---@class gameSTDUI
gameSTDUI = { 

}

--- Get a game UI element, element must be opened.
---@param elementName string 
---@return uiElementStruct element 
function gameSTDUI.getUiElement(elementName) end 

---Basic uiElementStruct table
---@class uiElementStruct
uiElementStruct = { 

    ---@type string
    elementName = nil,

    ---@type integer
    xSize = nil,

    ---@type integer
    ySize = nil,

    ---@type integer
    xPos = nil,

    ---@type integer
    yPos = nil,

    ---@type integer
    subElementsNum = nil,

}

--- Get a subelement of an UI element using the index.
---@param index integer Starts from 0.
---@return uiElementStruct subelement 
function uiElementStruct.getSubElement(index) end 

--- execute standard game UI element, use only for buttons
function uiElementStruct:execute() end 

---Basic stratmap.objects table
---@class stratmap.objects
stratmap.objects = { 

}

--- Add a new .cas campaign strategy model to the game with a unique ID. This should be called during onPluginLoad()
---@param path string Relative path from the modfolder (starting with "data/").
---@param modelId integer Unique ID to use the model later.
function stratmap.objects.addModelToGame(path, modelId) end 

--- Add a new .cas character strategy model to the game with a unique name. Only add it after loading to campaign map!
---@param skeleton string name of skeleton used.
---@param caspath string Relative path from the mods folder (starting with "mods/").
---@param shadowcaspath string Relative path from the mods folder (starting with "mods/").
---@param typename string Name of the new model used to assign.
---@param texturepath string Relative path from the mods folder (starting with "mods/").
---@param scale number 
function stratmap.objects.addCharacterCas(skeleton, caspath, shadowcaspath, typename, texturepath, scale) end 

--- Set the strategy model for object at specified coordinates, works only for supported object types
---@param xCoord integer 
---@param yCoord integer 
---@param modelId integer used for: watchtower, resource, settlement, fort, port
---@param modelId2 integer used for: fort wall (use fort coords), dock (use port coords)
function stratmap.objects.setModel(xCoord, yCoord, modelId, modelId2) end 

--- Replace a custom tile. Change the custom battlefield on the specified coordinates.
---@param label string Identifier.
---@param xCoord integer X coordinate of tile.
---@param yCoord integer Y coordinate of tile.
---@param filename string Just the name, not full path (.wfc)
---@param weather string Weather on the battle map.
---@param dayTime string Time of day.
function stratmap.objects.replaceTile(label, xCoord, yCoord, filename, weather, dayTime) end 

--- Start drawing .cas campaign strategy model with a unique ID in some coords. Can be used at any time.
---@param modelId integer Unique ID
---@param x integer 
---@param y integer 
---@param sizeMultiplier integer 1 is value with what it draw as same size as game objects
function stratmap.objects.startDrawModelAt(modelId, x, y, sizeMultiplier) end 

--- Stop drawing .cas campaign strategy model with a unique ID. Can be used at any time.
---@param modelId integer Unique ID
function stratmap.objects.stopDrawModel(modelId) end 

---Basic stratmap.camera table
---@class stratmap.camera
stratmap.camera = { 

}

--- Slowly move the camera to the specified tile.
---@param xCoord integer 
---@param yCoord integer 
function stratmap.camera.move(xCoord, yCoord) end 

--- Quickly move the camera to the specified tile.
---@param xCoord integer 
---@param yCoord integer 
function stratmap.camera.jump(xCoord, yCoord) end 

--- Set the zoom level of the camera.
---@param distance number 
function stratmap.camera.zoom(distance) end 

---Basic stratmap.game table
---@class stratmap.game
stratmap.game = { 

}

--- Get the amount of factions.
---@return integer facNumber Amount of factions
function stratmap.game.getFactionsCount() end 

--- Get a faction by the index, commonly used when iterating over all factions using getFactionsCount()
---@param Index integer of the faction.
---@return factionStruct faction 
function stratmap.game.getFaction(Index) end 

--- Create a new character at the specified coordinates.
---@param type string Character type, for example "named character".
---@param Faction factionStruct the new character belongs to.
---@param age integer The character's age
---@param name string The short name of the character.
---@param name2 string The full name of the character.
---@param subFaction integer Set to 31 to disable.
---@param portrait_custom string cannot be nil Name of the folder inside 'data/ui/custom_portraits folder. Can not be nil!
---@param xCoord integer X coordinate of the new character
---@param yCoord integer Y coordinate of the new character
---@return character newCharacter Returns a character class, not a named character class!
function stratmap.game.createCharacterByString(type, Faction, age, name, name2, subFaction, portrait_custom, xCoord, yCoord) end 

--- Create an army for a character. Commonly used after spawning a new character to set it's bodyguard unit.
---@param ourGeneral character Character class, not named character class!
---@return stackStruct army 
function stratmap.game.createArmy(ourGeneral) end 

--- Create an army in a settlement (don't need a character). Used to add units to an empty settlement.
---@param settlement settlementStruct 
---@return stackStruct army 
function stratmap.game.createArmyInSettlement(settlement) end 

--- Get a script counter value, works for counters and for event\_counters
---@param counterName string The name of the counter
---@return boolean isExist Returns true if the counter exists i.e it has been used at least once in any way in the campaign\_script
---@return integer counterValue Returns the value of the counter
function stratmap.game.getScriptCounter(counterName) end 

--- Set an event\_counter value, does not work for counters, only event\_counters.
---@param counterName string 
---@param value integer 
function stratmap.game.setScriptCounter(counterName, value) end 

--- Fire a game event message. Picture needs to be provided in the ui folders as default.
---@param eventName string 
---@param title string 
---@param body string 
function stratmap.game.historicEvent(eventName, title, body) end 

--- Fire any script command available from the game. It is always just 2 parameters in the function, the command name and all the arguments as 1 string in the second parameter.
-- Do not use inc_counter, set_counter, declare_counter! they crash!
---@param command string 
---@param args string? 
function stratmap.game.scriptCommand(command, args) end 

--- Execute a Medieval II console command.
---@param command string 
---@param args string? 
---@return string error Note: string can be empty but not nil
function stratmap.game.callConsole(command, args) end 

---Basic stratmap table
---@class stratmap
stratmap = { 

    ---@type stratmap.objects
    objects = nil,

    ---@type stratmap.camera
    camera = nil,

    ---@type stratmap.game
    game = nil,

}

---Unit table
---@class unit
unit = { 

    ---@type eduEntry
    eduEntry = nil,

    ---@type number
    movePoints = nil,

    ---0 means inactive, 1 means active, 2 means labelled unit (for Battle)
    ---@type integer
    aiActiveSet = nil,

    ---soldiers count. You can change it on stratmap and soldiers updated. Use @{setParams} if you need change several parameters at once.
    ---@type integer
    soldierCountStratMap = nil,

    ---soldiers expierence. You can change it on stratmap and soldiers updated. Use @{setParams} if you need change several parameters at once.
    ---@type integer
    exp = nil,

    ---soldiers armour. You can change it on stratmap and soldiers updated. Use @{setParams} if you need change several parameters at once.
    ---@type integer
    armourLVL = nil,

    ---soldiers weapon. You can change it on stratmap and soldiers updated. Use @{setParams} if you need change several parameters at once.
    ---@type integer
    weaponLVL = nil,

    ---Read only
    ---@type integer
    soldierCountStratMapMax = nil,

    ---Read only
    ---@type integer
    soldierCountBattleMap = nil,

    ---use moraleStatus enum
    ---@type integer
    moraleLevel = nil,

    ---@type integer
    isCloseFormation = nil,

    ---(battle)
    ---@type integer
    fatigue = nil,

    ---(battle)
    ---@type integer
    maxAmmo = nil,

    ---(battle)
    ---@type integer
    currentAmmo = nil,

    ---2d position on battlemap useful for getting distance etc (battle)
    ---@type number
    battlePosX = nil,

    ---2d position on battlemap useful for getting distance etc (battle)
    ---@type number
    battlePosY = nil,

    ---@type character
    character = nil,

    ---@type unitPositionData
    unitPositionData = nil,

    ---@type stackStruct
    army = nil,

    ---@type integer
    siegeEngineNum = nil,

    ---@type string
    alias = nil,

}

--- Kill this unit
function unit:kill() end 

---change soldierCountStratMap, exp, armourLVL, weaponLVL at one time. Set unit basic parameters
---@param exp integer Experience. Maximum: 9
---@param armor integer Armour level.
---@param weapon integer Weapon Upgrade. Maximum: 1
function unit:setParams(exp, armor, weapon) end 

---Check if unit has edu attribute. Check if unit has edu attribute.
function unit:hasAttribute() end 

--- Check if unit has guard mode, skirmish or fire at will on.
---@param property integer use enum: unitBattleProperties.guardMode, unitBattleProperties.skirmish, unitBattleProperties.fireAtWill
---@return boolean hasProperty 
function unit:hasBattleProperty(property) end 

--- Set a unit battle property (guard mode, skirmish or fire at will).
---@param property integer use enum: unitBattleProperties.guardMode, unitBattleProperties.skirmish, unitBattleProperties.fireAtWill
---@param value boolean 
function unit:setBattleProperty(property, value) end 

--- Get unit action status in battle ( idling, hiding, ready, reforming, moving, withdrawing, missiles\_firing, missiles\_reloading, charging, fighting, pursuing, routing, fighting\_backs\_to\_the\_walls, running\_amok, rallying, dead, leaving\_battle, entering\_battle, left\_battle, go\_berserk, taunting, bracing, infighting).
---@return string actionStatus 
function unit:getActionStatus() end 

--- Is unit set to run?
---@return boolean movingFastSet 
function unit:isMovingFastSet() end 

--- Toggle unit running.
---@param movingFastSet boolean 
function unit:setMovingFastSet(movingFastSet) end 

--- Is unit on walls?
---@return boolean isOnWalls 
function unit:isOnWalls() end 

--- Is unit engaged in melee?
---@return boolean isEngaged 
function unit:isEngaged() end 

--- Is unit under fire?
---@return boolean isUnderFire 
function unit:isUnderFire() end 

--- Get unit mount class.
---@return integer mountClass 
function unit:getMountClass() end 

---
---@class unitPositionData
unitPositionData = { 

    ---@type integer
    engagedUnitsNum = nil,

    ---@type unit
    unit = nil,

    ---(amount of walls
    ---@type integer
    isOnWallsCount = nil,

    ---(amount of towers)
    ---@type integer
    isInTowerCount = nil,

    ---(amount of gatehouses)
    ---@type integer
    isInGateHouseCount = nil,

    ---dont set
    ---@type integer
    targetsDone = nil,

    ---dont set
    ---@type integer
    additionalTargetsOverOne = nil,

    ---dont set
    ---@type integer
    targetsToGo = nil,

    ---dont set
    ---@type integer
    hasTargets = nil,

    ---@type integer
    isHalted = nil,

    ---use enum: combatStatus
    ---@type integer
    combatStatus = nil,

    ---dont set
    ---@type number
    lastTargetCoord1 = nil,

    ---dont set
    ---@type number
    lastTargetCoord2 = nil,

    ---@type integer
    towersUnderFireFromCount = nil,

    ---@type integer
    unitsUnderFireFromCount = nil,

}

--- Get unit that is firing at this unit.
---@param index integer 
---@return unit unit 
function unitPositionData:getUnitUnderFireFrom(index) end 

--- Get unit that is fighting this unit in melee.
---@param index integer 
---@return unit unit 
function unitPositionData:getEngagedUnit(index) end 

--- Get the unit this unit is currently targeting.
---@return unit unit 
function unitPositionData:getTargetUnit() end 

---Basic eduEntry table
---@class eduEntry
eduEntry = { 

    ---- Get only
    ---@type string
    eduType = nil,

    ---- Get only
    ---@type string
    soldier = nil,

    ---- Get only
    ---@type string
    unitCardTga = nil,

    ---- Get only
    ---@type string
    infoCardTga = nil,

    ---- Get only
    ---@type integer
    index = nil,

    ---- Get only
    ---@type integer
    unitCreatedCounter = nil,

    ---- Get only
    ---@type integer
    category = nil,

    ---- Get only
    ---@type integer
    class = nil,

    ---- Get only
    ---@type integer
    categoryClassCombo = nil,

    ---times 4
    ---@type integer
    recruitPriorityOffset = nil,

    ---@type integer
    crusadingUpkeepModifier = nil,

    ---@type number
    aiUnitValuePerSoldier = nil,

    ---@type number
    aiUnitValue = nil,

    ---@type integer
    soldierCount = nil,

    ---@type number
    mass = nil,

    ---@type number
    width = nil,

    ---@type number
    height = nil,

    ---@type boolean
    haveAttributeLegio = nil,

    ---@type number
    moveSpeedMod = nil,

    ---@type number
    unitSpacingFrontToBackClose = nil,

    ---@type number
    unitSpacingSideToSideClose = nil,

    ---@type number
    unitSpacingFrontToBackLoose = nil,

    ---@type number
    unitSpacingSideToSideLoose = nil,

    ---@type integer
    statHealth = nil,

    ---@type integer
    statHealthAnimal = nil,

    ---@type integer
    statHeat = nil,

    ---@type integer
    statScrub = nil,

    ---@type integer
    statSand = nil,

    ---@type integer
    statForest = nil,

    ---@type integer
    statSnow = nil,

    ---@type integer
    recruitTime = nil,

    ---@type integer
    recruitCost = nil,

    ---@type integer
    upkeepCost = nil,

    ---@type integer
    weaponCost = nil,

    ---@type integer
    armourCost = nil,

    ---@type integer
    customBattleCost = nil,

    ---@type integer
    customBattleIncrease = nil,

    ---@type integer
    customBattleLimit = nil,

    ---@type integer
    morale = nil,

    ---@type integer
    moraleLocked = nil,

    ---@type integer
    statFood1 = nil,

    ---@type integer
    statFood2 = nil,

    ---@type integer
    ammunition = nil,

}

---characters as they exist on the strategy map - dead characters, wives, children, and off-map characters do not have these fields.
---@class character
character = { 

    ---@type integer
    xCoord = nil,

    ---@type integer
    yCoord = nil,

    ---@type namedCharacter
    namedCharacter = nil,

    ---@type unit
    bodyguards = nil,

    ---@type stackStruct
    armyLeaded = nil,

    ---in the stack but not leading it
    ---@type stackStruct
    armyNotLeaded = nil,

    ---@type integer
    inEnemyZOC = nil,

    ---@type integer
    ambushState = nil,

    ---@type integer
    regionID = nil,

    ---can check if the character died before the game updates he is dead like post battle event
    ---@type integer
    isMarkedToKill = nil,

    ---@type integer
    doNotSpendMovePoints = nil,

    ---@type number
    movePointsCharacter = nil,

    ---@type number
    movePointsModifier = nil,

    ---@type number
    movePointsMaxCharacter = nil,

    ---@type number
    movePointsMaxArmy = nil,

    ---@type number
    movePointsArmy = nil,

    ---@type integer
    turnJoinedCrusade = nil,

    ---@type integer
    numTurnsIdle = nil,

    ---0 to 1
    ---@type number
    percentCharacterReligionInRegion = nil,

    ---@type number
    popConvertedThisTurn = nil,

    ---@type integer
    timeInRegion = nil,

    ---for auxiliary generals, not leading general
    ---@type integer
    timeWithArmy = nil,

    ---@type crusadeStruct
    crusade = nil,

    ---@type integer
    currentTurn = nil,

    ---@type number
    distanceToCrusadeTarget = nil,

    ---@type integer
    disbandProgress = nil,

    ---@type integer
    isCrusadeDisbandActive = nil,

    ---@type settlementStruct
    besiegingSettlement = nil,

    ---@type character
    besiegingCharacter = nil,

    ---see descr\_hero\_abilities.xml
    ---@type string
    ability = nil,

}

--- Get the character type. See hint below for the types.
-- 0-spy
-- 1-assassin
-- 2-diplomat
-- 3-admiral
-- 4-merchant
-- 5-priest
-- 6-general
-- 7-named character
-- 8-princess
-- 9-heretic
-- 10-witch
-- 11-inquisitor
-- 13-pope
---@return integer typeId 
function character:getTypeID() end 

--- Get the character type. See hint below for the types.
-- 0-spy
-- 1-assassin
-- 2-diplomat
-- 3-admiral
-- 4-merchant
-- 5-priest
-- 6-general
-- 7-named character
-- 8-princess
-- 9-heretic
-- 10-witch
-- 11-inquisitor
-- 13-pope
---@return string type 
function character:getTypeName() end 

--- Set the character type. See hint below for the types.
-- 0-spy
-- 1-assassin
-- 2-diplomat
-- 3-admiral
-- 4-merchant
-- 5-priest
-- 6-general
-- 7-named character
-- 8-princess
-- 9-heretic
-- 10-witch
-- 11-inquisitor
-- 13-pope
---@param typeId integer 
function character:setTypeID(typeId) end 

--- Issue regular move command, character must have movement points.
---@param xCoord integer 
---@param yCoord integer 
function character:moveToTile(xCoord, yCoord) end 

--- Instantly teleport character to the coordinates.
---@param xCoord integer 
---@param yCoord integer 
function character:reposition(xCoord, yCoord) end 

--- Delete this character
function character:kill() end 

--- Create a fort at the character's coordinates
function character:createFort() end 

--- Set bodyguard. Do this only for characters without it, such as immediately after creating a character.
---@param unit unit 
function character:setBodyguardUnit(unit) end 

--- Set a character's model to a new one.
---@param model string 
function character:setCharacterModel(model) end 

---Basic namedCharacter table. All named characters have these fields including dead characters, wives, children, and off-map characters.
---@class namedCharacter
namedCharacter = { 

    ---@type integer
    index = nil,

    ---@type character
    character = nil,

    ---Internal name.
    ---@type string
    shortName = nil,

    ---Internal name including surname.
    ---@type string
    fullName = nil,

    ---Display name, resets upon reloading a save.
    ---@type string
    localizedDisplayName = nil,

    ---@type string
    label = nil,

    ---Wives (who have never been princesses) and children do not have anything for this field. Path to 'young' portrait used starting from 'mods' folder. Resets upon reloading a save.
    ---@type string
    portrait = nil,

    ---Wives (who have never been princesses) and children do not have anything for this field. Path to 'old' portrait used starting from 'mods' folder. Resets upon reloading a save.
    ---@type string
    portrait2 = nil,

    ---Wives (who have never been princesses) and children do not have anything for this field. Folder name in ui/custom_portraits folder.
    ---@type string
    portrait_custom = nil,

    ---Battle model (needs battle_models.modeldb entry).
    ---@type string
    modelName = nil,

    ---5-leader,2 - heir, 0 - ordinary character, read only, do not set value
    ---@type integer
    status = nil,

    ---@type boolean
    isFamily = nil,

    ---@type boolean
    isMale = nil,

    ---@type integer
    age = nil,

    ---For example with 4 turns per year, the yearOfBirth could be 1840.25
    ---@type number
    yearOfBirth = nil,

    ---@type factionStruct
    faction = nil,

    ---@type integer
    subFaction = nil,

    ---@type namedCharacter
    parent = nil,

    ---@type namedCharacter
    spouse = nil,

    ---Maximum 4.
    ---@type table<integer, namedCharacter>
    childs = nil,

    ---@type integer
    ancNum = nil,

    ---@type integer
    level = nil,

    ---@type integer
    authority = nil,

    ---@type integer
    command = nil,

    ---positive = Chivalry, negative = Dread
    ---@type integer
    chivalryAndDread = nil,

    ---@type integer
    loyalty = nil,

    ---@type integer
    piety = nil,

    ---@type integer
    ambush = nil,

    ---@type integer
    artilleryCommand = nil,

    ---@type integer
    assassination = nil,

    ---@type integer
    attack = nil,

    ---@type integer
    battleSurgery = nil,

    ---@type integer
    bodyguardSize = nil,

    ---@type integer
    bodyguardValour = nil,

    ---@type integer
    boldness = nil,

    ---@type integer
    bribeResistance = nil,

    ---@type integer
    bribery = nil,

    ---@type integer
    cavalryCommand = nil,

    ---@type integer
    charm = nil,

    ---@type integer
    construction = nil,

    ---@type integer
    defence = nil,

    ---@type integer
    disposition = nil,

    ---@type integer
    electability = nil,

    ---@type integer
    eligibility = nil,

    ---@type integer
    farming = nil,

    ---@type integer
    fertility = nil,

    ---@type integer
    finance = nil,

    ---@type integer
    footInTheDoor = nil,

    ---@type integer
    generosity = nil,

    ---@type integer
    gunpowerCommand = nil,

    ---@type integer
    health = nil,

    ---@type integer
    heresyImmunity = nil,

    ---@type integer
    hitpoints = nil,

    ---@type integer
    infantryCommand = nil,

    ---@type integer
    influence = nil,

    ---@type integer
    law = nil,

    ---@type integer
    lineOfSight = nil,

    ---@type integer
    localPopularity = nil,

    ---@type integer
    looting = nil,

    ---@type integer
    magic = nil,

    ---@type integer
    management = nil,

    ---@type integer
    mining = nil,

    ---@type integer
    movementPointsBonus = nil,

    ---@type integer
    navalCommand = nil,

    ---@type integer
    nightBattle = nil,

    ---@type integer
    personalSecurity = nil,

    ---@type integer
    publicSecurity = nil,

    ---@type integer
    purity = nil,

    ---@type integer
    sabotage = nil,

    ---@type integer
    siegeAttack = nil,

    ---@type integer
    siegeDefense = nil,

    ---@type integer
    siegeEngineering = nil,

    ---@type integer
    squalor = nil,

    ---@type integer
    subterfuge = nil,

    ---@type integer
    taxCollection = nil,

    ---@type integer
    trading = nil,

    ---@type integer
    trainingAgents = nil,

    ---@type integer
    trainingAnimalUnits = nil,

    ---@type integer
    trainingUnits = nil,

    ---@type integer
    troopMorale = nil,

    ---@type integer
    unorthodoxy = nil,

    ---@type integer
    unrest = nil,

    ---@type integer
    violence = nil,

    ---Maximum 10. EVEN IF YOU SET RELIGION LIMIT.
    ---@type table<integer, integer>
    combatVsReligion = nil,

    ---Maximum 31.
    ---@type table<integer, integer>
    combatVsFaction = nil,

}

--- Sets the named character as the faction heir.
---@param onlyHeir boolean True = this character will be the only heir, false = add another heir (faction can appear to have multiple heirs but only one will become leader).
function namedCharacter:setAsHeir(onlyHeir) end 

--- Checks if character is alive, read only, do not set this value.
---@return boolean liveStatus true = alive, false = dead
function namedCharacter:isAlive() end 

--- Checks if character is off map, read only, do not set this value.
---@return boolean offMap 
function namedCharacter:isOffMap() end 

--- Checks if character is child, read only, do not set this value.
---@return boolean isChild 
function namedCharacter:isChild() end 

--- Get the pointer to the character's traits container.
---@return traitContainer The character's traits.
function namedCharacter:getTraits() end 

--- Add a trait to the character.
---@param traitName string Trait's internal name per export\_descr\_character\_traits.txt
---@param traitLevel integer Trait's level.
function namedCharacter:addTrait(traitName, traitLevel) end 

--- Remove a trait from the character.
---@param traitName string Trait's internal name per export\_descr\_character\_traits.txt
function namedCharacter:removeTrait(traitName) end 

--- Get the pointer to the ancillary using it's index. You can iterate over a character's ancillaries for example by going from index 0 to ancNum - 1.
---@param index integer 
---@return ancillary ancillary 
function namedCharacter:getAncillary(index) end 

--- Add an ancillary to the named character using the name per export\_descr\_ancillaries.txt.
---@param ancillaryName string 
function namedCharacter:addAncillary(ancillaryName) end 

--- Remove an ancillary from the named character using it's pointer. Use getAncillary function to get the specific ancillary.
---@param ancillary ancillary 
function namedCharacter:removeAncillary(ancillary) end 

---Basic capturedFactionInfo table.
---@class capturedFactionInfo
capturedFactionInfo = { 

    ---@type integer
    targetFactionID = nil,

    ---@type integer
    factionID = nil,

    ---@type namedCharacter
    namedChar = nil,

    ---@type namedCharacter
    targetCharacter = nil,

    ---@type integer
    capturedCharactersNum = nil,

    ---@type integer
    capturedUnitsNum = nil,

    ---@type integer
    ransomValue = nil,

}

--- Get a captured character by it's index.
---@param index integer 
---@return capturedCharacter capChar 
function capturedFactionInfo:getCapturedCharacter(index) end 

--- Get a captured unit by it's index.
---@param index integer 
---@return capturedUnit capUnit 
function capturedFactionInfo:getCapturedUnit(index) end 

---Basic capturedUnit table.
---@class capturedUnit
capturedUnit = { 

    ---@type unit
    unit = nil,

    ---@type integer
    capturedSoldiers = nil,

    ---@type integer
    capturedValue = nil,

}

---Basic capturedCharacter table.
---@class capturedCharacter
capturedCharacter = { 

    ---@type namedCharacter
    namedChar = nil,

    ---@type integer
    capturedValue = nil,

}

---Basic ancillary table
---@class ancillary
ancillary = { 

    ---@type integer
    index = nil,

    ---@type string
    name = nil,

    ---@type string
    imagePath = nil,

}

---Basic traits table
---@class traitContainer
traitContainer = { 

    ---@type integer
    level = nil,

    ---@type string
    name = nil,

    ---@type traitContainer
    nextTrait = nil,

    ---@type traitContainer
    prevTrait = nil,

    ---@type traitStruct
    traitInfo = nil,

}

---Basic trait table
---@class traitStruct
traitStruct = { 

    ---@type traitEntry
    traitEntry = nil,

    ---@type traitLevel
    levelEntry = nil,

    ---@type integer
    traitPoints = nil,

}

---Basic traitEntry table
---@class traitEntry
traitEntry = { 

    ---@type integer
    index = nil,

    ---@type string
    name = nil,

    ---Maximum: 10
    ---@type table<integer, traitLevel>
    levels = nil,

    ---@type integer
    levelCount = nil,

    ---Maximum: 20
    ---@type table<integer, traitEntry>
    antiTraits = nil,

    ---@type integer
    antiTraitCount = nil,

    ---@type integer
    noGoingBackLevel = nil,

    ---@type integer
    hidden = nil,

}

---Basic traitLevel table
---@class traitLevel
traitLevel = { 

    ---@type integer
    level = nil,

    ---@type integer
    threshold = nil,

    ---@type integer
    effectsCount = nil,

}

--- Get trait effect.
---@param index integer 
---@return traitEffect effect 
function traitLevel:getTraitEffect(index) end 

---Basic traitEffect table
---@class traitEffect
traitEffect = { 

    ---@type integer
    id = nil,

    ---@type integer
    value = nil,

}

---Basic factionStruct table
---@class factionStruct
factionStruct = { 

    ---@type integer
    factionID = nil,

    ---@type integer
    cultureID = nil,

    ---@type integer
    AIPersonalityType = nil,

    ---@type integer
    AIPersonalityName = nil,

    ---@type string
    ai_label = nil,

    ---@type string
    name = nil,

    ---@type string
    localizedName = nil,

    ---@type settlementStruct
    capital = nil,

    ---@type namedCharacter
    leader = nil,

    ---@type namedCharacter
    heir = nil,

    ---0=AI, 1=player
    ---@type integer
    isPlayerControlled = nil,

    ---@type integer
    neighBourFactionsBitmap = nil,

    ---@type integer
    religion = nil,

    ---@type integer
    isUndiscovered = nil,

    ---@type integer
    missionCount = nil,

    ---@type integer
    freezeFactionAI = nil,

    ---@type integer
    treasuryTurnStart = nil,

    ---@type integer
    incomeDoubled = nil,

    ---@type integer
    battlesWon = nil,

    ---@type integer
    battlesLost = nil,

    ---@type integer
    settlementsCaptured = nil,

    ---@type integer
    settlementsLost = nil,

    ---@type integer
    otherFactionCount = nil,

    ---@type integer
    money = nil,

    ---@type integer
    kingsPurse = nil,

    ---@type factionStratMapStruct
    facStrat = nil,

    ---includes literally all characters without distinction (so also wives, children, dead and those sent off map)
    ---@type integer
    numOfNamedCharacters = nil,

    ---includes all the characters present on the strat map
    ---@type integer
    numOfCharacters = nil,

    ---@type integer
    stacksNum = nil,

    ---@type integer
    settlementsNum = nil,

    ---@type integer
    fortsNum = nil,

    ---@type integer
    portsNum = nil,

    ---@type integer
    watchtowersNum = nil,

    ---@type integer
    neighBourRegionsNum = nil,

}

--- Get the faction's internal name
---@return string facName 
function factionStruct:getFactionName() end 

--- Get named character using it's index.
---@param number integer 
---@return namedCharacter retNamedCharacter 
function factionStruct:getNamedCharacter(number) end 

--- Get a character using it's index.
---@param number integer 
---@return character retCharacter 
function factionStruct:getCharacter(number) end 

--- Get an army using it's index.
---@param number integer 
---@return stackStruct army 
function factionStruct:getStack(number) end 

--- Get a settlement using it's index.
---@param number integer 
---@return settlementStruct settlement 
function factionStruct:getSettlement(number) end 

--- Get a fort using it's index.
---@param number integer 
---@return fortStruct fort 
function factionStruct:getFort(number) end 

--- Get a port using it's index.
---@param number integer 
---@return portStruct port 
function factionStruct:getPort(number) end 

--- Get a watchtower using it's index.
---@param number integer 
---@return watchtowerStruct watchtower 
function factionStruct:getWatchtower(number) end 

--- Delete a specific fort.
---@param fort fortStruct 
function factionStruct:deleteFort(fort) end 

--- Create a fort at the specified coordinates.
---@param X integer 
---@param Y integer 
function factionStruct:createFortXY(X, Y) end 

--- Check if a faction has military access to another faction.
---@param targetFaction factionStruct 
---@return boolean hasMilitaryAccess 
function factionStruct:hasMilitaryAccess(targetFaction) end 

--- Set if a faction has military access to another faction.
---@param targetFaction factionStruct 
---@param hasMilitaryAccess boolean 
function factionStruct:setMilitaryAccess(targetFaction, hasMilitaryAccess) end 

--- Get the faction standing between 2 factions (a faction with itself returns global standing).
---@param targetFaction factionStruct 
---@return number factionStanding 
function factionStruct:getFactionStanding(targetFaction) end 

--- Set the faction standing between 2 factions (a faction with itself sets global standing).
---@param targetFaction factionStruct 
---@param factionStanding number 
function factionStruct:setFactionStanding(targetFaction, factionStanding) end 

--- Get the faction ranking scores.
---@param turnNumber integer 
---@return factionRanking factionRanking 
function factionStruct:getFactionRanking(turnNumber) end 

--- Get the faction ecomomy table, specified number of turns ago (max 10).
---@param turnsAgo integer 
---@return factionEconomy factionEconomy 
function factionStruct:getFactionEconomy(turnsAgo) end 

--- Get a region ID of a neighbouring region by index.
---@param index integer 
---@return integer nRegionID 
function factionStruct:getNeighbourRegionID(index) end 

--- Get stats versus a specific other faction.
---@param targetFactionID integer 
---@return battleFactionCounter battleStats 
function factionStruct:getBattleVsFactionStats(targetFactionID) end 

---Basic aiFaction table
---@class aiFaction
aiFaction = { 

    ---@type factionStruct
    faction = nil,

    ---@type integer
    factionID = nil,

    ---@type aiLongTermGoalDirector
    LTGD = nil,

    ---@type aiPersonality
    aiPersonality = nil,

}

---Basic aiLongTermGoalDirector table
---@class aiLongTermGoalDirector
aiLongTermGoalDirector = { 

    ---@type factionStruct
    faction = nil,

    ---@type aiFaction
    aiFaction = nil,

    ---@type integer
    trustedAllyEnemiesBitfield = nil,

    ---@type integer
    freeStrengthEnemy = nil,

    ---@type integer
    freeStrengthEnemyBalance = nil,

    ---@type integer
    consideringNavalInvasion = nil,

    ---@type integer
    navalTargetRegionID = nil,

    ---@type integer
    navalTargetRegionPriority = nil,

}

--- Get long term goal director values versus a specific other faction.
---@param targetFactionID integer 
---@return decisionValuesLTGD longTermGoalValues 
function aiLongTermGoalDirector:getlongTermGoalValues(targetFactionID) end 

---Basic decisionValuesLTGD table
---@class decisionValuesLTGD
decisionValuesLTGD = { 

    ---@type integer
    defendType = nil,

    ---@type integer
    defendPriority = nil,

    ---@type integer
    invasionType = nil,

    ---@type integer
    invadePriority = nil,

    ---@type integer
    atWar = nil,

    ---@type integer
    wantPeace = nil,

    ---@type integer
    wantAlly = nil,

    ---@type integer
    wantBeProtect = nil,

    ---@type integer
    wantOfferProtect = nil,

    ---@type integer
    allianceAgainst = nil,

    ---@type integer
    ptsDesire = nil,

    ---@type integer
    ptsAlliance = nil,

    ---@type integer
    canForceInvade = nil,

}

---Basic aiFactionValues table
---@class aiFactionValues
aiFactionValues = { 

    ---@type integer
    totalPopulation = nil,

    ---@type integer
    tileCount = nil,

    ---@type integer
    averagePopulation = nil,

    ---@type integer
    productionValue = nil,

    ---@type integer
    nonAlliedBorderLength = nil,

    ---@type integer
    enemyBorderLength = nil,

    ---@type integer
    fleetCount = nil,

    ---@type integer
    navalPowerPerFleet = nil,

    ---@type integer
    navalStrength = nil,

    ---@type integer
    armyCount = nil,

    ---@type integer
    strengthPerArmy = nil,

    ---@type integer
    totalStrength = nil,

    ---@type integer
    freeStrength = nil,

    ---@type integer
    neighbourEnemyNum = nil,

    ---@type integer
    enemyStrength = nil,

    ---@type integer
    protectorateOf = nil,

}

---Basic interFactionLTGD table
---@class interFactionLTGD
interFactionLTGD = { 

    ---@type integer
    borderTiles = nil,

    ---@type integer
    frontLineBalance = nil,

    ---@type integer
    hasAllianceAgainst = nil,

    ---@type integer
    isStrongestNeighbour = nil,

    ---@type integer
    isWeakestNeighbour = nil,

}

---Basic aiPersonality table
---@class aiPersonality
aiPersonality = { 

    ---@type aiFaction
    aiFaction = nil,

    ---@type integer
    aiProductionControllersNum = nil,

    ---@type integer
    AIPersonalityType = nil,

    ---@type integer
    AIPersonalityName = nil,

    ---@type integer
    spyBias = nil,

    ---@type integer
    assassinBias = nil,

    ---@type integer
    diplomatBias = nil,

    ---@type integer
    admiralBias = nil,

    ---@type integer
    priestBias = nil,

    ---@type integer
    merchantBias = nil,

    ---@type integer
    balancedPolicyNum = nil,

    ---@type integer
    financialPolicyNum = nil,

    ---@type integer
    militaryPolicyNum = nil,

    ---@type integer
    growthPolicyNum = nil,

    ---@type integer
    culturalPolicyNum = nil,

}

--- Set bias value of the ai personality for a capability.
---@param type integer use building capabilities enum
---@param value integer 
function aiPersonality:setConstructionValue(type, value) end 

--- Set bias value of the ai personality for a recruitment class.
---@param type integer use unitCategoryClass enum
---@param value integer 
function aiPersonality:setRecruitmentValue(type, value) end 

--- Get bias value of the ai personality for a capability.
---@param type integer use building capabilities enum
---@return integer value 
function aiPersonality:getConstructionValue(type) end 

--- Get bias value of the ai personality for a recruitment class.
---@param type integer use unitCategoryClass enum
---@return integer value 
function aiPersonality:getRecruitmentValue(type) end 

--- Get a production controller by index.
---@param index integer 
---@return aiProductionController controller 
function aiPersonality:getProductionController(index) end 

---Basic aiProductionController table
---@class aiProductionController
aiProductionController = { 

    ---@type aiFaction
    aiFaction = nil,

    ---@type integer
    regionID = nil,

    ---@type settlementStruct
    settlement = nil,

    ---@type integer
    autoManagePolicy = nil,

    ---@type integer
    isAutoManaged = nil,

    ---@type integer
    isAutoManagedRecruitment = nil,

    ---@type integer
    isAutoManagedConstruction = nil,

    ---@type integer
    spyBias = nil,

    ---@type integer
    assassinBias = nil,

    ---@type integer
    diplomatBias = nil,

    ---@type integer
    admiralBias = nil,

    ---@type integer
    priestBias = nil,

    ---@type integer
    merchantBias = nil,

}

--- Set bias value of the ai personality for a capability.
---@param type integer use building capabilities enum
---@param value integer 
function aiProductionController:setConstructionValue(type, value) end 

--- Set bias value of the ai personality for a recruitment class.
---@param type integer use unitCategoryClass enum
---@param value integer 
function aiProductionController:setRecruitmentValue(type, value) end 

--- Get bias value of the ai personality for a capability.
---@param type integer use building capabilities enum
---@return integer value 
function aiProductionController:getConstructionValue(type) end 

--- Get bias value of the ai personality for a recruitment class.
---@param type integer use unitCategoryClass enum
---@return integer value 
function aiProductionController:getRecruitmentValue(type) end 

---Basic battleFactionCounter table
---@class battleFactionCounter
battleFactionCounter = { 

    ---@type integer
    battlesWon = nil,

    ---@type integer
    battlesLost = nil,

}

---Basic holdRegionsWinCondition table
---@class holdRegionsWinCondition
holdRegionsWinCondition = { 

    ---@type integer
    regionsToHoldCount = nil,

    ---@type integer
    numberOfRegions = nil,

}

--- Get the name of the region that has to be held to win the campaign.
---@param index integer 
---@return string regionName 
function holdRegionsWinCondition:getRegionToHoldName(index) end 

--- Get the number of turns the region has to be held to win the campaign.
---@param index integer 
---@return integer turnsToHold 
function holdRegionsWinCondition:getRegionToHoldLength(index) end 

---Basic factionEconomy table
---@class factionEconomy
factionEconomy = { 

    ---@type integer
    farmingIncome = nil,

    ---@type integer
    taxesIncome = nil,

    ---@type integer
    miningIncome = nil,

    ---@type integer
    tradeIncome = nil,

    ---@type integer
    merchantIncome = nil,

    ---@type integer
    constructionIncome = nil,

    ---@type integer
    otherIncome1 = nil,

    ---@type integer
    otherIncome2 = nil,

    ---@type integer
    diplomacyIncome = nil,

    ---@type integer
    tributesIncome = nil,

    ---@type integer
    adminIncome = nil,

    ---@type integer
    kingsPurseIncome = nil,

    ---@type integer
    wagesExpense = nil,

    ---@type integer
    upkeepExpense = nil,

    ---@type integer
    constructionExpenseBuildings = nil,

    ---@type integer
    constructionExpenseField = nil,

    ---@type integer
    recruitmentExpenseBuildings = nil,

    ---@type integer
    recruitmentExpenseMercs = nil,

    ---@type integer
    corruptionExpense = nil,

    ---@type integer
    diplomacyExpense = nil,

    ---@type integer
    tributesExpense = nil,

    ---@type integer
    otherExpense1 = nil,

    ---@type integer
    otherExpense2 = nil,

    ---@type integer
    devastationExpense = nil,

}

---Basic factionRanking table
---@class factionRanking
factionRanking = { 

    ---@type number
    totalRankingScore = nil,

    ---@type number
    militaryRankingScore = nil,

    ---@type number
    productionRankingScore = nil,

    ---@type number
    territoryRankingScore = nil,

    ---@type number
    financialRankingScore = nil,

    ---@type number
    populationRankingScore = nil,

}

---Basic factionStratMapStruct table
---@class factionStratMapStruct
factionStratMapStruct = { 

    ---Warning: resets on reload.
    ---@type integer
    primaryColorRed = nil,

    ---Warning: resets on reload.
    ---@type integer
    primaryColorGreen = nil,

    ---Warning: resets on reload.
    ---@type integer
    primaryColorBlue = nil,

    ---Warning: resets on reload.
    ---@type integer
    secondaryColorRed = nil,

    ---Warning: resets on reload.
    ---@type integer
    secondaryColorGreen = nil,

    ---Warning: resets on reload.
    ---@type integer
    secondaryColorBlue = nil,

    ---Usage unknown.
    ---@type integer
    triumphValue = nil,

    ---@type integer
    religionID = nil,

    ---Warning: resets on reload.
    ---@type integer
    standardIndex = nil,

    ---Warning: resets on reload.
    ---@type integer
    logoIndex = nil,

    ---Warning: resets on reload.
    ---@type integer
    smallLogoIndex = nil,

    ---@type integer
    customBattleAvailability = nil,

    ---@type integer
    periodsUnavailableInCustomBattle = nil,

    ---shouldnt do anything in med 2, but could potentially use flag to store some other info about this faction
    ---@type integer
    canSap = nil,

    ---@type integer
    prefersNavalInvasions = nil,

    ---@type integer
    canHavePrincess = nil,

    ---@type integer
    hasFamilyTree = nil,

    ---@type integer
    teutonic = nil,

    ---@type integer
    disbandToPools = nil,

    ---@type integer
    canBuildSiegeTowers = nil,

    ---@type integer
    canTransmitPlague = nil,

    ---@type integer
    shadowedByID = nil,

    ---@type integer
    shadowingID = nil,

    ---@type integer
    spawnsOnRevoltID = nil,

    ---@type integer
    roman = nil,

    ---@type integer
    barbarian = nil,

    ---@type integer
    eastern = nil,

    ---@type integer
    slave = nil,

    ---@type integer
    hordeMinUnits = nil,

    ---@type integer
    hordeMaxUnits = nil,

    ---@type integer
    reductionPerHorde = nil,

    ---@type integer
    hordeUnitPerSettlementPop = nil,

    ---@type integer
    hordeMinNamedCharacters = nil,

    ---@type integer
    hordeMaxPercentArmyStack = nil,

}

---Basic watchtowerStruct table
---@class watchtowerStruct
watchtowerStruct = { 

    ---@type integer
    xCoord = nil,

    ---@type integer
    yCoord = nil,

    ---@type integer
    factionID = nil,

    ---@type factionStruct
    faction = nil,

    ---@type settlementStruct
    settlement = nil,

    ---@type stackStruct
    blockingArmy = nil,

}

---Basic fortStruct table
---@class fortStruct
fortStruct = { 

    ---@type integer
    xCoord = nil,

    ---@type integer
    yCoord = nil,

    ---@type character
    governor = nil,

    ---@type stackStruct
    army = nil,

    ---@type factionStruct
    ownerFaction = nil,

    ---@type integer
    siegeNum = nil,

    ---@type integer
    siegeHoldoutTurns = nil,

    ---@type integer
    turnsSieged = nil,

    ---@type integer
    plagued = nil,

    ---@type integer
    subFactionID = nil,

    ---@type integer
    factionID = nil,

    ---@type integer
    cultureID = nil,

    ---@type integer
    fortFortificationLevel = nil,

}

--- Get a specific siege by it's index
---@param siegeIdx integer 
---@return siegeStruct siege 
function fortStruct:getSiege(siegeIdx) end 

---Basic portStruct table
---@class portStruct
portStruct = { 

    ---land tile, Note: setting this only moves port's strat model.
    ---@type integer
    xCoord = nil,

    ---land tile, Note: setting this only moves port's strat model.
    ---@type integer
    yCoord = nil,

    ---Note: port's ownership changes to blockading faction (army on port)
    ---@type factionStruct
    ownerFaction = nil,

    ---@type settlementStruct
    settlement = nil,

    ---Character standing on the port tile, only the first one, check for nil.
    ---@type character
    character = nil,

    ---Enemy army blockading the port, by standing on it's tile, check for nil.
    ---@type stackStruct
    blockadingArmy = nil,

    ---water tile, only upgraded ports have this, check for nil.
    ---@type dockStruct
    dock = nil,

}

---Basic dockStruct table
---@class dockStruct
dockStruct = { 

    ---water tile, Note: setting only moves dock strat model
    ---@type integer
    xCoord = nil,

    ---water tile, Note: setting only moves dock strat model
    ---@type integer
    yCoord = nil,

}

---Basic settlementStruct table
---@class settlementStruct
settlementStruct = { 

    ---@type integer
    xCoord = nil,

    ---@type integer
    yCoord = nil,

    ---@type character
    governor = nil,

    ---@type stackStruct
    army = nil,

    ---internal name of settlement
    ---@type string
    name = nil,

    ---@type string
    localizedName = nil,

    ---@type factionStruct
    ownerFaction = nil,

    ---@type integer
    fac_creatorNum = nil,

    ---@type integer
    regionID = nil,

    ---@type integer
    level = nil,

    ---@type integer
    isCastle = nil,

    ---@type integer
    siegeHoldoutTurns = nil,

    ---@type integer
    turnsSieged = nil,

    ---@type integer
    subFactionID = nil,

    ---@type integer
    yearFounded = nil,

    ---@type integer
    isCapital = nil,

    ---@type integer
    harvestSuccess = nil,

    ---@type integer
    baseFertility = nil,

    ---@type integer
    rebelFactionChance = nil,

    ---@type integer
    plagued = nil,

    ---@type integer
    plagueDeaths = nil,

    ---start at 10 for settlements owned at game start without specification in descr_strat
    ---@type integer
    turnsOwned = nil,

    ---@type integer
    populationSiegeStart = nil,

    ---@type integer
    settlementTaxLevel = nil,

    ---@type integer
    recruitmentPoolCount = nil,

    ---@type integer
    recruitmentCapabilityNum = nil,

    ---@type integer
    freezeRecruitmentPool = nil,

    ---@type integer
    spiesInRecruitmentQueue = nil,

    ---@type integer
    assassinsInRecruitmentQueue = nil,

    ---@type integer
    diplomatsInRecruitmentQueue = nil,

    ---@type integer
    admiralsInRecruitmentQueue = nil,

    ---@type integer
    merchantsInRecruitmentQueue = nil,

    ---@type integer
    priestsInRecruitmentQueue = nil,

    ---@type aiProductionController
    aiProductionController = nil,

    ---@type integer
    turmoil = nil,

    ---@type integer
    isProvokedRebellion = nil,

    ---@type integer
    populationSize = nil,

    ---@type integer
    buildingsNum = nil,

    ---@type buildingsQueue
    buildingsQueue = nil,

    ---@type integer
    resourcesNum = nil,

    ---@type settlementStats
    settlementStats = nil,

    ---@type settlementStats
    settlementStatsLastTurn = nil,

    ---@type integer
    siegesNum = nil,

}

--- Change owner faction of settlement. All agents, armies etc. leave the settlement.
---@param newOwner factionStruct Faction to change ownership to.
function settlementStruct:changeOwner(newOwner) end 

--- Get the settlement's specific regligion's value
---@param religionID integer In order of descr\_religions.txt, starting from 0
---@return number religionValue from 0 to 1
function settlementStruct:getReligion(religionID) end 

--- Set the settlement's specific religion's value, make sure the sum of all religion values does not exceed 1.0!
---@param religionID integer in order of descr\_religions.txt, starting from 0
---@param religionValue number from 0 to 1
function settlementStruct:setReligion(religionID, religionValue) end 

--- Get a settlement's standing points with a specific guild by ID
---@param guild_id integer 
function settlementStruct:getGuildStanding(guild_id) end 

--- Set the settlement's standing points with specific guild.
---@param guild_id integer 
---@param standing integer 
function settlementStruct:setGuildStanding(guild_id, standing) end 

--- Get a specific building by it's index.
---@param number integer 
---@return building build 
function settlementStruct:getBuilding(number) end 

--- Create a building in the settlement.
---@param building_level_id string 
function settlementStruct:createBuilding(building_level_id) end 

--- Destroy a building of a specified type in the settlement.
---@param typeName string Type of building.
---@param isReturnMoney boolean Should money be returned to the faction like with a manual desctruction.
function settlementStruct:destroyBuilding(typeName, isReturnMoney) end 

--- Get a specific resource by it's index.
---@param number integer 
---@return tradeResource resource 
function settlementStruct:getResource(number) end 

--- Get a specific siege by it's index
---@param siegeIdx integer 
---@return siegeStruct siege 
function settlementStruct:getSiege(siegeIdx) end 

--- Get a capability by capability type.
---@param capabilityType integer 
---@return settlementCapability capability 
function settlementStruct:getSettlementCapability(capabilityType) end 

--- Get an agent capability by agent type (only recruitable agents) 0 = spy, 1 = assassin, 2 = diplomat, 3 = princess, 4 = merchant, 5 = priest.
---@param agentType integer 
---@return settlementCapability capability 
function settlementStruct:getAgentCapability(agentType) end 

--- Get an agent limit capability by agent type (only recruitable agents) 0 = spy, 1 = assassin, 2 = diplomat, 3 = princess, 4 = merchant, 5 = priest.
---@param agentType integer 
---@return settlementCapability capability 
function settlementStruct:getAgentLimitCapability(agentType) end 

--- Get a recruitment capability by index (max 64!).
---@param index integer 
---@return recruitmentCapability capability 
function settlementStruct:getRecruitmentCapability(index) end 

--- Get a recruitment pool by index.
---@param index integer 
---@return settlementRecruitmentPool pool 
function settlementStruct:getSettlementRecruitmentPool(index) end 

---Basic settlementStats table
---@class settlementStats
settlementStats = { 

    ---- Get only
    ---@type integer
    PopGrowthBaseFarm = nil,

    ---@type integer
    population = nil,

    ---- Get only
    ---@type integer
    PopGrowthFarms = nil,

    ---- Get only
    ---@type integer
    PopGrowthHealth = nil,

    ---- Get only
    ---@type integer
    PopGrowthBuildings = nil,

    ---- Get only
    ---@type integer
    PopGrowthTaxBonus = nil,

    ---- Get only
    ---@type integer
    PopGrowthEntertainment = nil,

    ---- Get only
    ---@type integer
    PopGrowthTrade = nil,

    ---- Get only
    ---@type integer
    PopGrowthGovernorInfluence = nil,

    ---- Get only
    ---@type integer
    PopGrowthSqualor = nil,

    ---- Get only
    ---@type integer
    PopGrowthPlague = nil,

    ---- Get only
    ---@type integer
    PopGrowthTaxPenalty = nil,

    ---- Get only
    ---@type integer
    PublicOrderGarrison = nil,

    ---- Get only
    ---@type integer
    PublicOrderLaw = nil,

    ---- Get only
    ---@type integer
    PublicOrderBuildingsEntertainment = nil,

    ---- Get only
    ---@type integer
    PublicOrderGovernorInfluence = nil,

    ---- Get only
    ---@type integer
    PublicOrderTaxBonus = nil,

    ---- Get only
    ---@type integer
    PublicOrderTriumph = nil,

    ---- Get only
    ---@type integer
    PublicOrderPopulationBoom = nil,

    ---- Get only
    ---@type integer
    PublicOrderEntertainment = nil,

    ---- Get only
    ---@type integer
    PublicOrderHealth = nil,

    ---- Get only
    ---@type integer
    PublicOrderGarrisonTwo = nil,

    ---- Get only
    ---@type integer
    PublicOrderFear = nil,

    ---- Get only
    ---@type integer
    PublicOrderGlory = nil,

    ---- Get only
    ---@type integer
    PublicOrderSqualor = nil,

    ---- Get only
    ---@type integer
    PublicOrderDistanceToCapital = nil,

    ---- Get only
    ---@type integer
    PublicOrderNoGovernance = nil,

    ---- Get only
    ---@type integer
    PublicOrderTaxPenalty = nil,

    ---- Get only
    ---@type integer
    PublicOrderUnrest = nil,

    ---- Get only
    ---@type integer
    PublicOrderBesieged = nil,

    ---- Get only
    ---@type integer
    PublicOrderBlockaded = nil,

    ---- Get only
    ---@type integer
    PublicOrderCulturalUnrest = nil,

    ---- Get only
    ---@type integer
    PublicOrderExcommunication = nil,

    ---- Get only
    ---@type integer
    PublicOrder = nil,

    ---- Get only
    ---@type integer
    FarmsIncome = nil,

    ---- Get only
    ---@type integer
    TaxesIncome = nil,

    ---- Get only
    ---@type integer
    MiningIncome = nil,

    ---- Get only
    ---@type integer
    TradeIncome = nil,

    ---- Get only
    ---@type integer
    DiplomaticIncome = nil,

    ---- Get only
    ---@type integer
    DemolitionIncome = nil,

    ---- Get only
    ---@type integer
    LootingIncome = nil,

    ---- Get only
    ---@type integer
    BuildingsIncome = nil,

    ---- Get only
    ---@type integer
    AdminIncome = nil,

    ---- Get only
    ---@type integer
    ConstructionExpense = nil,

    ---- Get only
    ---@type integer
    RecruitmentExpense = nil,

    ---- Get only
    ---@type integer
    DiplomaticExpense = nil,

    ---- Get only
    ---@type integer
    CorruptionExpense = nil,

    ---- Get only
    ---@type integer
    EntertainmentExpense = nil,

    ---- Get only
    ---@type integer
    DevastationExpense = nil,

    ---- Get only
    ---@type integer
    TotalIncomeWithoutAdmin = nil,

    ---@type integer
    majorityReligionID = nil,

}

---Basic settlementCapability table
---@class settlementCapability
settlementCapability = { 

    ---@type integer
    value = nil,

    ---@type integer
    bonus = nil,

}

---Basic recruitmentCapability table
---@class recruitmentCapability
recruitmentCapability = { 

    ---@type integer
    eduIndex = nil,

    ---@type integer
    xp = nil,

    ---@type number
    initialSize = nil,

    ---@type number
    replenishRate = nil,

    ---@type number
    maxSize = nil,

}

---Basic settlementRecruitmentPool table
---@class settlementRecruitmentPool
settlementRecruitmentPool = { 

    ---@type integer
    eduIndex = nil,

    ---@type number
    availablePool = nil,

}

---Basic building table
---@class building
building = { 

    ---@type integer
    level = nil,

    ---@type integer
    hp = nil,

    ---@type settlementStruct
    settlement = nil,

    ---@type edbEntry
    edbEntry = nil,

}

--- Get the name of the building type (the building chain in export\_descr\_buildings.txt).
---@return string buildingType (building chain name)
function building:getType() end 

--- Get name of building level (as per export\_descr\_buildings.txt).
---@return string buildingName 
function building:getName() end 

---Basic buildingsQueue table
---@class buildingsQueue
buildingsQueue = { 

    ---position in queue of building currently under construction, usually 1
    ---@type integer
    currentlyBuilding = nil,

    ---maximum is 6
    ---@type integer
    numBuildingsInQueue = nil,

}

---by position in queue (1-6) Get building in queue by position
---@param position integer 
---@return buildingInQueue buildingInQueue 
function buildingsQueue:getBuildingInQueue(position) end 

---Basic buildingInQueue table
---@class buildingInQueue
buildingInQueue = { 

    ---Is nil if building doesn't exist yet.
    ---@type building
    building = nil,

    ---@type settlementStruct
    settlement = nil,

    ---@type integer
    currentLevel = nil,

    ---@type integer
    previousLevel = nil,

    ---@type integer
    buildCost = nil,

    ---@type integer
    buildTurnsPassed = nil,

    ---@type integer
    buildTurnsRemaining = nil,

    ---@type integer
    percentBuilt = nil,

}

--- Get name of building in queue type (chain)
---@return string buildingType (building chain name)
function buildingInQueue:getQueueBuildingType() end 

--- Get name of building in queue level
---@return string buildingName 
function buildingInQueue:getQueueBuildingName() end 

---Basic guild table
---@class guild
guild = { 

    ---@type string
    name = nil,

    ---@type integer
    id = nil,

    ---@type integer
    level1 = nil,

    ---@type integer
    level2 = nil,

    ---@type integer
    level3 = nil,

}

---Basic tradeResource table
---@class tradeResource
tradeResource = { 

    ---@type integer
    xCoord = nil,

    ---@type integer
    yCoord = nil,

    ---@type integer
    regionID = nil,

    ---@type settlementStruct
    settlement = nil,

}

--- Set the resource's strat model.
---@param modelId integer Added with stratmap.objects.addModelToGame
function tradeResource:setStratModel(modelId) end 

--- Get the resource's ID.
---@return integer ID 
function tradeResource:getResourceID() end 

--- Get the resource's trade value.
---@return integer value 
function tradeResource:getResourceValue() end 

--- Check if the resource has a mine.
---@return integer hasMine 0=no mine, 1=mine
function tradeResource:getResourceHasMine() end 

--- Get the resource's image (icon) relative path.
---@return string imagePath 
function tradeResource:getResourceImage() end 

---Basic stackStruct table
---@class stackStruct
stackStruct = { 

    ---@type factionStruct
    faction = nil,

    ---@type integer
    numOfUnits = nil,

    ---@type integer
    isBoarded = nil,

    ---@type integer
    ladders = nil,

    ---@type integer
    rams = nil,

    ---@type integer
    towers = nil,

    ---Includes Auxiliary generals and agents (i.e all characters excluding the leading general)
    ---@type integer
    numOfCharacters = nil,

    ---army embarked on this fleet stack
    ---@type stackStruct
    boardedArmy = nil,

    ---fleet that this army stack is embarked on
    ---@type stackStruct
    shipArmy = nil,

    ---@type portStruct
    blockedPort = nil,

    ---Returns nil if stack is inside residence (fleet, settlement, fort).
    ---@type character
    leader = nil,

    ---@type integer
    totalStrength = nil,

    ---X coordinate to which the retreating units will go.
    ---@type number
    reform_point_x = nil,

    ---Y coordinate to which the retreating units will go.
    ---@type number
    reform_point_y = nil,

    ---Current siege.
    ---@type siegeStruct
    siege = nil,

}

--- Get a unit by it's index.
---@param number integer 
---@return unit retUnit 
function stackStruct:getUnit(number) end 

--- Get a character (agent or non-leading named character) by it's index.
---@param number integer 
---@return character retCharacter 
function stackStruct:getCharacter(number) end 

--- Find the settlement in which the army is located. Returns nil if the army is not in a settlement.
-- Returns nil if the army is not in the settlement.
---@return settlementStruct settlement 
function stackStruct:findInSettlement() end 

--- Find the fort in which the army is located. Returns nil if the army is not in a fort.
-- Returns nil if the army is not in the fort.
---@return fortStruct fort 
function stackStruct:findInFort() end 

--- Create a unit in the army by index from M2TWEOP units DB (M2TWEOPDU).
---@param index integer 
---@param exp integer 
---@param armor integer 
---@param weapon integer 
---@return unit newUnit 
function stackStruct:createEOPUnit(index, exp, armor, weapon) end 

--- Create a unit in the army by type from export\_descr\_unit.txt
---@param type string 
---@param exp integer Experience. Maximum: 9.
---@param armor integer Armour level.
---@param weapon integer Weapon upgrade. Maximum: 1.
---@return unit newUnit 
function stackStruct:createUnit(type, exp, armor, weapon) end 

--- Sort units in a stack. Use the sortType enum to specify the sorting mode.
---@param sortMode integer 
---@param sortMode2 integer 
---@param sortMode3 integer 
function stackStruct:sortStack(sortMode, sortMode2, sortMode3) end 

--- Merge 2 armies on the strat map. Does nothing if the total size of the new army exceeds 20 units.
---@param targetArmy stackStruct 
function stackStruct:mergeArmies(targetArmy) end 

--- Create a unit in the army by index from export\_descr\_unit.txt
---@param index integer Index (order in export\_descr\_unit.txt)
---@param exp integer Experience. Maximum: 9.
---@param armor integer Armour level.
---@param weapon integer Weapon upgrade. Maximum: 1.
---@return unit newUnit 
function stackStruct:createUnitByIDX(index, exp, armor, weapon) end 

---Call it twice to initiate an assault. Besiege the specified settlement, or attack it if already besieging it. Requires movement points.
---@param settlement settlementStruct 
function stackStruct:siegeSettlement(settlement) end 

--- Attack another army. Requires movement points.
---@param defender stackStruct 
---@return integer Success 
function stackStruct:attackArmy(defender) end 

---Basic siegeStruct table
---@class siegeStruct
siegeStruct = { 

    ---@type stackStruct
    besieger = nil,

    ---@type settlementStruct
    besiegedSettlement = nil,

    ---@type fortStruct
    besiegedFort = nil,

    ---@type integer
    siegeTurns = nil,

    ---@type integer
    soldierCount = nil,

}

---Enum with a list of types of diplomatic relations.
---@enum dipRelType
dipRelType = { 

    ---@type integer
    war = nil,

    ---@type integer
    peace = nil,

    ---@type integer
    alliance = nil,

    ---@type integer
    suzerain = nil,

    ---(Doesn't work with trade rights agreements set at game start)
    ---@type integer
    trade = nil,

}

---Enum with a list of types of unit battle properties.
---@enum unitBattleProperties
unitBattleProperties = { 

    ---@type integer
    guardMode = nil,

    ---@type integer
    fireAtWill = nil,

    ---@type integer
    skirmish = nil,

}

---Enum with a list of types of building capabilities.
---@enum buildingCapability
buildingCapability = { 

    ---@type integer
    population_growth_bonus = 0,

    ---@type integer
    population_loyalty_bonus = 1,

    ---@type integer
    population_health_bonus = 2,

    ---@type integer
    trade_base_income_bonus = 3,

    ---@type integer
    trade_level_bonus = 4,

    ---@type integer
    trade_fleet = 5,

    ---@type integer
    taxable_income_bonus = 6,

    ---@type integer
    mine_resource = 7,

    ---@type integer
    farming_level = 8,

    ---@type integer
    road_level = 9,

    ---@type integer
    gate_strength = 10,

    ---@type integer
    gate_defences = 11,

    ---@type integer
    wall_level = 12,

    ---@type integer
    tower_level = 13,

    ---@type integer
    armour = 14,

    ---@type integer
    stage_games = 15,

    ---@type integer
    stage_races = 16,

    ---@type integer
    fire_risk = 17,

    ---@type integer
    weapon_melee_simple = 18,

    ---@type integer
    weapon_melee_blade = 19,

    ---@type integer
    weapon_missile_mechanical = 20,

    ---@type integer
    weapon_missile_gunpowder = 21,

    ---@type integer
    weapon_artillery_mechanical = 22,

    ---@type integer
    weapon_artillery_gunpowder = 23,

    ---@type integer
    weapon_naval_gunpowder = 24,

    ---@type integer
    upgrade_bodyguard = 25,

    ---@type integer
    recruits_morale_bonus = 26,

    ---@type integer
    recruits_exp_bonus = 27,

    ---@type integer
    happiness_bonus = 28,

    ---@type integer
    law_bonus = 29,

    ---@type integer
    construction_cost_bonus_military = 30,

    ---@type integer
    construction_cost_bonus_religious = 31,

    ---@type integer
    construction_cost_bonus_defensive = 32,

    ---@type integer
    construction_cost_bonus_other = 33,

    ---@type integer
    construction_time_bonus_military = 34,

    ---@type integer
    construction_time_bonus_religious = 35,

    ---@type integer
    construction_time_bonus_defensive = 36,

    ---@type integer
    construction_time_bonus_other = 37,

    ---@type integer
    construction_cost_bonus_wooden = 38,

    ---@type integer
    construction_cost_bonus_stone = 39,

    ---@type integer
    construction_time_bonus_wooden = 40,

    ---@type integer
    construction_time_bonus_stone = 41,

    ---@type integer
    free_upkeep = 42,

    ---@type integer
    pope_approval = 43,

    ---@type integer
    pope_disapproval = 44,

    ---@type integer
    religion_level = 45,

    ---@type integer
    amplify_religion_level = 46,

    ---@type integer
    archer_bonus = 47,

    ---@type integer
    cavalry_bonus = 48,

    ---@type integer
    heavy_cavalry_bonus = 49,

    ---@type integer
    gun_bonus = 50,

    ---@type integer
    navy_bonus = 51,

    ---@type integer
    recruitment_cost_bonus_naval = 52,

    ---@type integer
    retrain_cost_bonus = 53,

    ---@type integer
    weapon_projectile = 54,

    ---@type integer
    income_bonus = 55,

    ---@type integer
    recruitment_slots = 56,

}

---Enum with a list of character types.
---@enum characterType
characterType = { 

    ---@type integer
    spy = 0,

    ---@type integer
    assassin = 1,

    ---@type integer
    diplomat = 2,

    ---@type integer
    admiral = 3,

    ---@type integer
    merchant = 4,

    ---@type integer
    priest = 5,

    ---@type integer
    general = 6,

    ---@type integer
    named_character = 7,

    ---@type integer
    princess = 8,

    ---@type integer
    heretic = 9,

    ---@type integer
    witch = 10,

    ---@type integer
    inquisitor = 11,

    ---@type integer
    pope = 13,

}

---Enum with a list of army sort types.
---@enum sortType
sortType = { 

    ---@type integer
    eduType = 1,

    ---@type integer
    category = 2,

    ---@type integer
    class = 3,

    ---@type integer
    soldierCount = 4,

    ---@type integer
    experience = 5,

    ---@type integer
    categoryClass = 6,

    ---@type integer
    aiUnitValue = 7,

}

---Enum with a list of GTA AI plans.
---@enum aiPlan
aiPlan = { 

    ---@type integer
    doNothing = 0,

    ---@type integer
    attackAll = 1,

    ---@type integer
    defend = 2,

    ---@type integer
    defendFeature = 3,

    ---@type integer
    hide = 4,

    ---@type integer
    ambush = 5,

    ---@type integer
    scout = 6,

    ---@type integer
    withdraw = 7,

    ---@type integer
    attackSettlement = 8,

    ---@type integer
    defendSettlement = 9,

    ---@type integer
    sallyOut = 10,

}

---Enum with a list of GTA AI objectives.
---@enum aiObjective
aiObjective = { 

    ---@type integer
    invalid = 0,

    ---@type integer
    moveToPoint = 1,

    ---@type integer
    attackEnemyBattleGroup = 2,

    ---@type integer
    defendTerrainHill = 3,

    ---@type integer
    defendTerrainForest = 4,

    ---@type integer
    defendTerrainArea = 5,

    ---@type integer
    defendCrossing = 6,

    ---@type integer
    assaultCrossing = 7,

    ---@type integer
    defendLine = 8,

    ---@type integer
    scout = 9,

    ---@type integer
    withdraw = 10,

    ---@type integer
    defendSettlement = 11,

    ---@type integer
    supportDefendSettlement = 12,

    ---@type integer
    attackSettlement = 13,

    ---@type integer
    bombard = 15,

    ---@type integer
    attackModel = 16,

    ---@type integer
    sallyOut = 17,

    ---@type integer
    ambush = 18,

}

---Enum with a list of resources.
---@enum resourceType
resourceType = { 

    ---@type integer
    gold = 0,

    ---@type integer
    silver = 1,

    ---@type integer
    fish = 2,

    ---@type integer
    furs = 3,

    ---@type integer
    grain = 4,

    ---@type integer
    timber = 5,

    ---@type integer
    iron = 6,

    ---@type integer
    ivory = 7,

    ---@type integer
    wine = 8,

    ---@type integer
    slaves = 9,

    ---@type integer
    chocolate = 10,

    ---@type integer
    marble = 11,

    ---@type integer
    textiles = 12,

    ---@type integer
    dyes = 13,

    ---@type integer
    tobacco = 14,

    ---@type integer
    silk = 15,

    ---@type integer
    sugar = 16,

    ---@type integer
    sulfur = 17,

    ---@type integer
    tin = 18,

    ---@type integer
    spices = 19,

    ---@type integer
    cotton = 20,

    ---@type integer
    amber = 21,

    ---@type integer
    coal = 22,

    ---@type integer
    wool = 23,

    ---@type integer
    elephants = 24,

    ---@type integer
    camels = 25,

    ---@type integer
    dogs = 26,

    ---@type integer
    generic = 27,

}

---Enum of unit morale status.
---@enum moraleStatus
moraleStatus = { 

    ---@type integer
    berserk = 0,

    ---@type integer
    impetuous = 1,

    ---@type integer
    high = 2,

    ---@type integer
    firm = 3,

    ---@type integer
    shaken = 4,

    ---@type integer
    wavering = 5,

    ---@type integer
    routing = 6,

}

---Enum of unit combat status.
---@enum combatStatus
combatStatus = { 

    ---@type integer
    notInCombat = 0,

    ---@type integer
    victoryCertain = 1,

    ---@type integer
    victoryAlmostCertain = 2,

    ---@type integer
    victoryDistinct = 3,

    ---@type integer
    balanced = 4,

    ---@type integer
    defeatDistinct = 5,

    ---@type integer
    defeatAlmostCertain = 6,

    ---@type integer
    defeatCertain = 7,

}

---Enum of unit combat status.
---@enum battleSuccess
battleSuccess = { 

    ---@type integer
    close = 0,

    ---@type integer
    average = 1,

    ---@type integer
    clear = 2,

    ---@type integer
    crushing = 3,

}

---Enum of unit mount class.
---@enum mountClass
mountClass = { 

    ---@type integer
    horse = 0,

    ---@type integer
    camel = 1,

    ---@type integer
    elephant = 2,

    ---@type integer
    infantry = 3,

}

---Enum of battle types.
---@enum battleType
battleType = { 

    ---@type integer
    ambushSuccess = 0,

    ---@type integer
    ambushFail = 1,

    ---@type integer
    open = 2,

    ---@type integer
    siege = 3,

    ---@type integer
    sally = 4,

    ---@type integer
    naval = 5,

    ---@type integer
    withdrawal = 6,

    ---@type integer
    meetEnemy = 7,

}

---Enum of battle states.
---@enum battleState
battleState = { 

    ---@type integer
    notInBattle = 0,

    ---@type integer
    preBattle = 1,

    ---@type integer
    delay = 2,

    ---@type integer
    deployment = 3,

    ---@type integer
    deploymentPlayer2 = 4,

    ---@type integer
    conflict = 5,

    ---@type integer
    victoryScroll = 6,

    ---@type integer
    pursuit = 7,

}

---Enum of unit classes
---@enum unitClass
unitClass = { 

    ---@type integer
    heavy = 0,

    ---@type integer
    light = 1,

    ---@type integer
    skirmish = 2,

    ---@type integer
    spearmen = 3,

    ---@type integer
    missile = 4,

}

---Enum of unit categories
---@enum unitCategory
unitCategory = { 

    ---@type integer
    infantry = 0,

    ---@type integer
    cavalry = 1,

    ---@type integer
    siege = 2,

    ---@type integer
    non_combatant = 3,

    ---@type integer
    ship = 4,

    ---@type integer
    handler = 5,

}

---Enum of unit categories and class combo
---@enum unitCategoryClass
unitCategoryClass = { 

    ---@type integer
    nonCombatant = 0,

    ---@type integer
    lightInfantry = 1,

    ---@type integer
    heavyInfantry = 2,

    ---@type integer
    spearmenInfantry = 3,

    ---@type integer
    missileInfantry = 4,

    ---@type integer
    lightCavalry = 5,

    ---@type integer
    heavyCavalry = 6,

    ---@type integer
    missileCavalry = 7,

    ---@type integer
    siegeWeapon = 8,

    ---@type integer
    animalHandler = 9,

    ---@type integer
    battleShip = 10,

}

---Enum of automated settlement policy types
---@enum managePolicy
managePolicy = { 

    ---@type integer
    balanced = 0,

    ---@type integer
    financial = 1,

    ---@type integer
    military = 2,

    ---@type integer
    growth = 3,

    ---@type integer
    cultural = 4,

    ---@type integer
    noPolicy = 5,

}

---Basic options1 table
---@class options1
options1 = { 

    ---@type integer
    widescreen = nil,

    ---@type integer
    antiAliasMode = nil,

    ---@type integer
    subtitles = nil,

    ---@type integer
    english = nil,

    ---@type integer
    noBattleTimeLimit = nil,

    ---@type integer
    useNewCursorActions = nil,

    ---@type integer
    campaignNumTimesPlay = nil,

    ---@type integer
    uiWinConditions = nil,

    ---@type integer
    isScenario = nil,

    ---@type integer
    isHotseatEnabled = nil,

    ---@type integer
    hotseatAutosave = nil,

    ---@type integer
    email = nil,

    ---@type integer
    saveConfig = nil,

    ---@type integer
    closeAfterSave = nil,

    ---@type integer
    validateData = nil,

    ---@type integer
    campaignMapSpeedUp = nil,

    ---@type integer
    skipAiFactions = nil,

    ---@type integer
    labelCharacters = nil,

    ---@type integer
    noBackGroundFmv = nil,

    ---@type integer
    disableArrowMarkers = nil,

    ---@type integer
    arcadeBattles = nil,

    ---@type integer
    disableEvents = nil,

    ---@type integer
    isPrologue = nil,

    ---@type integer
    updateAiCamera = nil,

    ---@type integer
    hideCampaign = nil,

    ---@type integer
    unlimitedMenOnBattlefield = nil,

    ---@type integer
    tgaReserveSpace = nil,

    ---@type integer
    keysetUsed = nil,

    ---@type integer
    muteAdvisor = nil,

    ---@type integer
    advancedStatsAlways = nil,

    ---@type integer
    microManageAllSettlements = nil,

    ---@type integer
    blindAdvisor = nil,

    ---@type integer
    terrainQuality = nil,

    ---@type integer
    vegetationQuality = nil,

    ---@type integer
    useQuickChat = nil,

    ---@type integer
    graphicsAdaptor = nil,

    ---@type integer
    showDemeanour = nil,

    ---@type integer
    radar = nil,

    ---@type integer
    unitCards = nil,

    ---@type integer
    sa_cards = nil,

    ---@type integer
    buttons = nil,

    ---@type integer
    tutorialBattlePlayed = nil,

    ---@type integer
    disableVnVs = nil,

    ---@type integer
    allUsers = nil,

}

---Basic options2 table
---@class options2
options2 = { 

    ---@type integer
    campaignResolutionX = nil,

    ---@type integer
    campaignResolutionY = nil,

    ---@type integer
    battleResolutionX = nil,

    ---@type integer
    battleResolutionY = nil,

    ---@type integer
    vSync = nil,

    ---@type integer
    uiIconBarCheck = nil,

    ---@type integer
    uiRadarCheck = nil,

    ---@type integer
    useMorale = nil,

    ---@type integer
    uiAmmoCheck = nil,

    ---@type integer
    useFatigue = nil,

    ---@type integer
    uiSupplyCheck = nil,

    ---this does not toggle fow just remembers if it was on or off
    ---@type integer
    toggleFowState = nil,

    ---@type integer
    cameraRestrict = nil,

    ---@type integer
    eventCutscenes = nil,

    ---@type integer
    defaultCameraInBattle = nil,

    ---@type integer
    splashes = nil,

    ---@type integer
    stencilShadows = nil,

    ---@type integer
    audioEnable = nil,

    ---@type integer
    speechEnable = nil,

    ---@type integer
    firstTimePlay = nil,

    ---@type integer
    toggleAutoSave = nil,

    ---@type integer
    showBanners = nil,

    ---@type integer
    passwords = nil,

    ---@type integer
    hotseatTurns = nil,

    ---@type integer
    hotseatScroll = nil,

    ---@type integer
    allowValidationFeatures = nil,

    ---@type integer
    campaignSpeed = nil,

    ---@type integer
    labelSettlements = nil,

    ---@type integer
    disablePapalElections = nil,

    ---@type integer
    autoresolveAllBattles = nil,

    ---@type integer
    savePrefs = nil,

    ---@type integer
    disableConsole = nil,

    ---@type integer
    validateDiplomacy = nil,

    ---@type integer
    unitDetail = nil,

    ---@type integer
    buildingDetail = nil,

    ---if limited
    ---@type integer
    maxSoldiersOnBattlefield = nil,

    ---@type integer
    unitSize = nil,

    ---@type integer
    cameraRotateSpeed = nil,

    ---@type integer
    cameraMoveSpeed = nil,

    ---@type number
    cameraSmoothing = nil,

    ---@type integer
    masterVolume = nil,

    ---@type integer
    musicVolume = nil,

    ---@type integer
    speechVolume = nil,

    ---@type integer
    sfxVolume = nil,

    ---@type integer
    subFactionAccents = nil,

    ---@type integer
    tgaWidth = nil,

    ---@type number
    tgaAspect = nil,

    ---@type integer
    tgaInputScale = nil,

    ---@type integer
    scrollMinZoom = nil,

    ---@type integer
    scrollMaxZoom = nil,

    ---@type integer
    advisorVerbosity = nil,

    ---@type integer
    effectQuality = nil,

    ---@type integer
    EnableCameraCampaignSmoothing = nil,

    ---@type integer
    chatMsgDuration = nil,

    ---@type integer
    saveGameSpyPassword = nil,

    ---@type integer
    addDateToLogs = nil,

    ---@type integer
    showToolTips = nil,

    ---@type integer
    isNormalHud = nil,

    ---@type integer
    showPackageLitter = nil,

    ---@type number
    unitSizeMultiplierLow = nil,

    ---@type number
    unitSizeMultiplierMedium = nil,

    ---@type number
    unitSizeMultiplierLarge = nil,

}

---Basic campaignDifficulty1 table.
---@class campaignDifficulty1
campaignDifficulty1 = { 

    ---@type integer
    orderFromGrowth = nil,

    ---@type integer
    considerWarWithPlayer = nil,

    ---@type number
    brigandChanceAi = nil,

    ---@type number
    brigandChancePlayer = nil,

    ---@type integer
    forceAttackDelay = nil,

    ---@type number
    taxIncomeModifierPlayer = nil,

    ---@type number
    farmingIncomeModifierPlayer = nil,

    ---@type number
    incomeModifierAi = nil,

    ---@type number
    playerRegionValueModifier = nil,

}

---Basic campaignDifficulty2 table.
---@class campaignDifficulty2
campaignDifficulty2 = { 

    ---@type integer
    popGrowthBonusAi = nil,

    ---@type integer
    publicOrderBonusAi = nil,

    ---@type integer
    experienceBonusAi = nil,

    ---@type integer
    incomeBonusAi = nil,

    ---@type integer
    wantsTargetPlayer = nil,

    ---@type integer
    wantsTargetPlayerNaval = nil,

    ---@type integer
    autoAttackPlayerIfCrusadeTarget = nil,

}

---Basic eventTrigger table
---@class eventTrigger
eventTrigger = { 

    ---@type unit
    attackingUnit = nil,

    ---@type unit
    defendingUnit = nil,

    ---@type character
    stratCharacter = nil,

    ---@type namedCharacter
    character = nil,

    ---@type namedCharacter
    targetCharacter = nil,

    ---@type settlementStruct
    settlement = nil,

    ---@type settlementStruct
    targetSettlement = nil,

    ---@type fortStruct
    fort = nil,

    ---@type factionStruct
    faction = nil,

    ---@type factionStruct
    targetFaction = nil,

    ---@type stackStruct
    army = nil,

    ---@type integer
    regionID = nil,

    ---@type integer
    targetRegionID = nil,

    ---@type unit
    playerUnit = nil,

    ---@type unit
    enemyUnit = nil,

    ---@type buildingBattle
    battleBuilding = nil,

    ---@type buildingInQueue
    priorBuild = nil,

    ---@type string
    resourceDescription = nil,

    ---@type eduEntry
    eduEntry = nil,

    ---@type integer
    characterType = nil,

    ---@type integer
    targetCharacterType = nil,

    ---@type string
    disasterType = nil,

    ---@type string
    missionSuccessLevel = nil,

    ---@type integer
    missionProbability = nil,

    ---@type string
    missionDetails = nil,

    ---@type integer
    eventID = nil,

    ---@type guild
    guild = nil,

    ---@type string
    eventCounter = nil,

    ---@type coordPair
    coords = nil,

    ---@type integer
    religion = nil,

    ---@type integer
    targetReligion = nil,

    ---@type number
    amount = nil,

    ---@type crusadeStruct
    crusade = nil,

    ---@type capturedFactionInfo
    captureInfo = nil,

    ---@type string
    ransomType = nil,

    ---@type unit
    unit = nil,

}

---Basic uiCardManager table
---@class uiCardManager
uiCardManager = { 

    ---@type integer
    selectedUnitCardsCount = nil,

    ---@type integer
    unitCardsCount = nil,

    ---@type settlementStruct
    selectedSettlement = nil,

    ---@type character
    selectedCharacter = nil,

    ---@type fortStruct
    selectedFort = nil,

}

--- Get selected unit card by index.
---@param index integer 
---@return unit selectedUnit 
function uiCardManager:getSelectedUnitCard(index) end 

--- Get unit card by index (battle or strat).
---@param index integer 
---@return unit unit 
function uiCardManager:getUnitCard(index) end 

---Basic campaign table.
---@class campaignStruct
campaignStruct = { 

    ---@type integer
    playerFactionId = nil,

    ---Indexing starts at 1, so add 1 to faction ID. Maximum 31.
    ---@type table<integer, integer>
    campaignDifficultyFaction = nil,

    ---Indexing starts at 1, so add 1 to faction ID. Maximum 31.
    ---@type table<integer, integer>
    battleDifficultyFaction = nil,

    ---Table of factionStruct[31], indexing starts at 1. Maximum 31.
    ---@type table<integer, factionStruct>
    factionsSortedByDescrStrat = nil,

    ---Table of factionStruct[31], indexing starts at 1, so add 1 to faction ID. Maximum 31.
    ---@type table<integer, factionStruct>
    factionsSortedByID = nil,

    ---@type integer
    numberOfFactions = nil,

    ---Number of player-controlled factions.
    ---@type integer
    numberHumanFactions = nil,

    ---Faction whose turn it is at the moment, can be set.
    ---@type factionStruct
    currentFaction = nil,

    ---@type collegeOfCardinals
    collegeOfCardinals = nil,

    ---@type factionStruct
    papalFaction = nil,

    ---@type integer
    fogOfWar = nil,

    ---@type integer
    factionTurnID = nil,

    ---@type integer
    tickCount = nil,

    ---@type integer
    millisecondCount = nil,

    ---@type number
    secondCount = nil,

    ---@type integer
    passedTurnsNum = nil,

    ---Factor for number of turns per year, see descr\_strat.txt
    ---@type number
    timescale = nil,

    ---@type settlementStruct
    romeSettlement = nil,

    ---@type settlementStruct
    constantinopleSettlement = nil,

    ---@type crusadeStruct
    crusade = nil,

    ---@type jihadStruct
    jihad = nil,

    ---Lower values increase spawn rate.
    ---@type number
    BrigandSpawnValue = nil,

    ---Lower values increase spawn rate.
    ---@type number
    PirateSpawnValue = nil,

    ---@type integer
    restrictAutoResolve = nil,

    ---@type integer
    saveEnabled = nil,

    ---Number of units who get free upkeep in forts.
    ---@type integer
    FreeUpkeepForts = nil,

    ---@type number
    currentDate = nil,

    ---season (0=summer, 1=winter)
    ---@type integer
    currentseason = nil,

    ---@type number
    startDate = nil,

    ---season (0=summer, 1=winter)
    ---@type integer
    startSeason = nil,

    ---@type number
    endDate = nil,

    ---season (0=summer, 1=winter)
    ---@type integer
    endSeason = nil,

    ---@type integer
    daysInBattle = nil,

    ---24 max, so calculate as daysInBattle*24+currentTimeInBattle.
    ---@type number
    currentTimeInBattle = nil,

    ---@type integer
    fortsNum = nil,

    ---@type integer
    portsBuildingsNum = nil,

    ---@type integer
    watchTowerNum = nil,

}

--- Check if a diplomatic relation between two factions.
---@param checkType dipRelType Example: dipRelType.war
---@param fac1 factionStruct A faction.
---@param fac2 factionStruct Another faction.
---@return boolean checkResult 
function campaignStruct:checkDipStance(checkType, fac1, fac2) end 

--- Set a diplomatic relation between two factions.
---@param relType dipRelType Example: dipRelType.war
---@param fac1 factionStruct A faction.
---@param fac2 factionStruct Another faction.
function campaignStruct:setDipStance(relType, fac1, fac2) end 

--- Get size of unit(i.e. small or medium, etc). Numbers from 0 to 3
---@return integer unitSize 
function campaignStruct:GetUnitSize() end 

--- Get path to the current descr\_strat file used.
---@return string path 
function campaignStruct:getCampaignPath() end 

--- Get fort by index.
---@param index integer 
---@return fortStruct fort 
function campaignStruct:getFort(index) end 

--- Get port by index.
---@param index integer 
---@return portStruct port 
function campaignStruct:getPort(index) end 

--- Get watchtower by index.
---@param index integer 
---@return watchtowerStruct watchtower 
function campaignStruct:getWatchTower(index) end 

--- Get settlement by internal name.
---@param name string 
---@return settlementStruct settlement 
function campaignStruct:getSettlementByName(name) end 

---Basic College of Cardinals table.
---@class collegeOfCardinals
collegeOfCardinals = { 

    ---@type namedCharacter
    pope = nil,

    ---@type integer
    cardinalNum = nil,

}

--- Get a specific cardinal by index.
---@param index integer 
---@return character cardinal 
function collegeOfCardinals:getCardinal(index) end 

---Basic crusade table.
---@class crusadeStruct
crusadeStruct = { 

    ---@type integer
    startTurn = nil,

    ---@type integer
    endTurn = nil,

    ---@type settlementStruct
    targetSettlement = nil,

    ---@type integer
    length = nil,

    ---@type integer
    outcome = nil,

}

---Basic jihad table.
---@class jihadStruct
jihadStruct = { 

    ---@type integer
    startTurn = nil,

    ---@type integer
    endTurn = nil,

    ---@type settlementStruct
    targetSettlement = nil,

    ---@type integer
    length = nil,

    ---@type integer
    outcome = nil,

}

---Basic coordPair table.
---@class coordPair
coordPair = { 

    ---@type integer
    xCoord = nil,

    ---@type integer
    yCoord = nil,

}

---Basic strat map table.
---@class stratMap
stratMap = { 

    ---@type integer
    mapWidth = nil,

    ---@type integer
    mapHeight = nil,

    ---@type integer
    regionsNum = nil,

    ---@type integer
    volcanoesNum = nil,

    ---@type integer
    landConnectionsNum = nil,

    ---@type integer
    landMassNum = nil,

}

--- Get a specific region by index.
---@param index integer 
---@return regionStruct region 
function stratMap.getRegion(index) end 

--- Get a specific tile by it's coordinates.
---@param x integer 
---@param y integer 
---@return tileStruct tile 
function stratMap.getTile(x, y) end 

--- Get a volcano's coordinates.
---@param index integer 
---@return coordPair tile 
function stratMap:getVolcanoCoords(index) end 

--- Get a land connection's coordinates (the green arrows on the map that allow you to cross bodies of water).
---@param index integer 
---@return coordPair tile 
function stratMap:getLandConnection(index) end 

--- Get a landmass (collection of regions reachable by land, like a continent or island).
---@param index integer 
---@return landMass landMass 
function stratMap:getLandMass(index) end 

---Basic landMass table.
---@class landMass
landMass = { 

    ---@type integer
    index = nil,

    ---@type integer
    regionsNum = nil,

}

--- Get a region ID by index.
---@param index integer 
---@return integer regionID 
function landMass:getRegionID(index) end 

---Basic roadStruct table.
---@class roadStruct
roadStruct = { 

    ---@type integer
    coordsNum = nil,

    ---@type integer
    regionIdStart = nil,

    ---@type integer
    regionIdEnd = nil,

    -----only counts from 1 side (importer)
    ---@type integer
    tradeValue = nil,

}

--- Get a road coord by index.
---@param index integer 
---@return coordPair coords 
function roadStruct:getCoord(index) end 

---Basic tile table, not everything very known and understood yet, you can research with these fields.
---@class tileStruct
tileStruct = { 

    ---@type roadStruct
    road = nil,

    ---(1 = land, 0 = sea)
    ---@type integer
    isLand = nil,

    ---@type integer
    groundType = nil,

    ---@type integer
    regionID = nil,

    ---@type tradeResource|nil
    resource = nil,

    ---@type character|nil
    character = nil,

    ---@type settlementStruct|nil
    settlement = nil,

    ---@type fortStruct|nil
    fort = nil,

    ---@type portStruct|nil
    port = nil,

    ---@type watchtowerStruct|nil
    watchtower = nil,

    ---@type integer
    height = nil,

    ---@type integer
    climate = nil,

    ---@type integer
    heatValue = nil,

    ---@type integer
    factionID = nil,

    ---@type coordPair
    coords = nil,

    ---bitfield, from left to right: unknown, character, ship, watchtower, port, unknown, fort, settlement.
    ---@type integer
    objectTypes = nil,

    ---@type boolean
    hasRiver = nil,

    ---@type boolean
    hasCrossing = nil,

    ---@type boolean
    hasCharacter = nil,

    ---@type boolean
    hasShip = nil,

    ---@type boolean
    hasWatchtower = nil,

    ---@type boolean
    hasPort = nil,

    ---@type boolean
    hasFort = nil,

    ---@type boolean
    hasSettlement = nil,

    ---@type boolean
    isDevastated = nil,

    ---1 = bordering 2 = settlement.
    ---@type integer
    borderingSettlement = nil,

    ---1 = border, 2 = seaBorder, 3 = sea edge border (point where the region border both another land region and sea).
    ---@type integer
    border = nil,

    ---bitfield of faction id's (counts both tile and the 8 tiles around it, if you want only on tile combine with charactersOnTile).
    ---@type integer
    armiesNearTile = nil,

    ---bitfield of faction id's
    ---@type integer
    charactersOnTile = nil,

    ---@type number
    mpModifier = nil,

}

--- Check if a faction has an army near a tile.
---@param factionID integer 
---@return boolean hasArmyNearTile 
function tileStruct:factionHasArmyNearTile(factionID) end 

--- Check if a faction has a character on a tile.
---@param factionID integer 
---@return boolean hasCharacterOnTile 
function tileStruct:factionHasCharacterOnTile(factionID) end 

---Basic regionStruct table.
---@class regionStruct
regionStruct = { 

    ---@type string
    regionName = nil,

    ---@type string
    localizedName = nil,

    ---@type string
    settlementName = nil,

    ---@type string
    legioName = nil,

    ---@type integer
    regionID = nil,

    ---as set in descr_strat
    ---@type integer
    roadLevel = nil,

    ---as set in descr_strat
    ---@type integer
    farmingLevel = nil,

    ---@type integer
    famineThreat = nil,

    ---@type integer
    harvestSuccess = nil,

    ---@type integer
    totalSeaTradeValue = nil,

    ---@type integer
    stacksNum = nil,

    ---@type integer
    fortsNum = nil,

    ---@type integer
    watchtowersNum = nil,

    ---@type integer
    isSea = nil,

    ---(fully enclosed by region)
    ---@type integer
    hasLake = nil,

    ---@type landMass
    landMass = nil,

    ---@type roadStruct
    roadToPort = nil,

    ---@type integer
    seaConnectedRegionsCount = nil,

    ---@type integer
    loyaltyFactionID = nil,

    ---@type seaConnectedRegion
    seaExportRegion = nil,

    ---@type integer
    seaImportRegionsCount = nil,

    ---(point where the region border both another land region and sea).
    ---@type integer
    regionSeaEdgesCount = nil,

    ---@type integer
    tilesBorderingEdgeOfMapCount = nil,

    ---@type integer
    devastatedTilesCount = nil,

    ---@type settlementStruct
    settlement = nil,

    ---@type integer
    tileCount = nil,

    ---@type integer
    fertileTilesCount = nil,

    ---@type integer
    neighbourRegionsNum = nil,

    ---@type integer
    resourcesNum = nil,

    ---@type integer
    resourceTypesBitMap = nil,

    ---(bitmap with 32 first hidden resources), needs to be converted to binary and then use bitwise operators from lua.
    ---@type integer
    hiddenResources1 = nil,

    ---(bitmap last 32 first hidden resources), needs to be converted to binary and then use bitwise operators from lua.
    ---@type integer
    hiddenResources2 = nil,

    ---@type integer
    settlementXCoord = nil,

    ---@type integer
    settlementYCoord = nil,

    ---@type integer
    portEntranceXCoord = nil,

    ---@type integer
    portEntranceYCoord = nil,

    ---@type factionStruct
    faction = nil,

    ---@type mercPool
    mercPool = nil,

    ---@type string
    rebelType = nil,

    ---@type string
    localizedRebelsName = nil,

    ---@type integer
    triumphValue = nil,

}

--- Get an army by it's index.
---@param index integer 
---@return stackStruct army 
function regionStruct:getStack(index) end 

--- Get a fort by it's index.
---@param index integer 
---@return fortStruct fort 
function regionStruct:getFort(index) end 

--- Get a watchtower by it's index.
---@param index integer 
---@return watchtowerStruct watchtower 
function regionStruct:getWatchtower(index) end 

--- Get a resource by it's index.
---@param index integer 
---@return tradeResource resource 
function regionStruct:getResource(index) end 

--- Get a neighbour region by it's index.
---@param index integer 
---@return neighbourRegion nRegion 
function regionStruct:getNeighbour(index) end 

--- Check if a region has a hidden resource.
---@param index integer 
---@return boolean hr 
function regionStruct:getHiddenResource(index) end 

--- Set a region's hidden resource (reset on game restart).
---@param index integer 
---@param enable boolean 
function regionStruct:setHiddenResource(index, enable) end 

--- Get a region that is reachable from this region.
---@param index integer 
---@return seaConnectedRegion connectedRegion 
function regionStruct:getSeaConnectedRegion(index) end 

--- Get a region this region is importing trade goods from.
---@param index integer 
---@return seaConnectedRegion seaImportRegion 
function regionStruct:getSeaImportRegion(index) end 

--- Get a region sea edge (point where it borders both sea and another land region).
---@param index integer 
---@return tileStruct edge 
function regionStruct:getRegionSeaEdge(index) end 

--- Get religion amount from a set number of turns ago.
---@param religionID integer 
---@param turnsAgo integer (max 19)
---@return number religionAmount 
function regionStruct:getReligionHistory(religionID, turnsAgo) end 

--- Get a tile that borders the edge of the map.
---@param index integer 
---@return tileStruct edge 
function regionStruct:getTileBorderingEdgeOfMap(index) end 

--- Get a tile by index.
---@param index integer 
---@return tileStruct tile 
function regionStruct:getTile(index) end 

--- Get a fertile tile by index.
---@param index integer 
---@return tileStruct tile 
function regionStruct:getFertileTile(index) end 

--- Get a devastated tile.
---@param index integer 
---@return tileStruct tile 
function regionStruct:getDevastatedTile(index) end 

--- Get the strength total of all armies in this region that are hostile to a specific faction.
---@param factionID integer 
---@return integer totalStrength 
function regionStruct:getHostileArmiesStrength(factionID) end 

--- Check if region has a resource type.
---@param resourceID integer 
---@return boolean hasResource 
function regionStruct:hasResourceType(resourceID) end 

---Basic neighbourRegion table.
---@class neighbourRegion
neighbourRegion = { 

    ---@type integer
    regionID = nil,

    ---@type regionStruct
    region = nil,

    ---@type integer
    tradeValue = nil,

    ---@type integer
    alliedRegion = nil,

    ---@type integer
    borderTilesCount = nil,

    ---@type roadStruct
    connectingRoad = nil,

}

--- Get a border tile by index.
---@param index integer 
---@return tileStruct tile 
function neighbourRegion:getBorderTile(index) end 

---Basic seaConnectedRegion table.
---@class seaConnectedRegion
seaConnectedRegion = { 

    ---@type integer
    regionID = nil,

    ---@type integer
    seaExportValue = nil,

    ---@type integer
    seaImportValue = nil,

    ---@type integer
    tilesReachableCount = nil,

    ---@type integer
    seaTradeLanePathCount = nil,

}

--- Get a reachable tile by index.
---@param index integer 
---@return tileStruct tile 
function seaConnectedRegion:getReachableTile(index) end 

--- Get trade lane coords by index.
---@param index integer 
---@return coordPair coords 
function seaConnectedRegion:getTradeLaneCoord(index) end 

---Basic mercenary pool table.
---@class mercPool
mercPool = { 

    ---@type string
    name = nil,

}

--- Get amount of mercenary units a region has.
---@return integer mercUnitNum 
function mercPool:getMercUnitNum() end 

--- Add a new mercenary unit to a pool.
---@param idx integer EDU index, supports EOP units.
---@param exp integer Starting experience.
---@param cost integer 
---@param repmin number Minimum replenishment rate.
---@param repmax number Maximum replenishment rate.
---@param maxunits integer Maximum Pool.
---@param startpool number Starting pool.
---@param startyear integer (0 to disable) Use 0 if the startyear is before the year you introduce the merc, not an earlier startyear!
---@param endyear integer (0 to disable)
---@param crusading integer 
---@return mercPoolUnit mercunit 
function mercPool:addMercUnit(idx, exp, cost, repmin, repmax, maxunits, startpool, startyear, endyear, crusading) end 

--- Get a mercenary unit from a pool by index.
---@param idx integer 
---@return mercPoolUnit mercUnit 
function mercPool:getMercUnit(idx) end 

---Basic mercenary unit table.
---@class mercPoolUnit
mercPoolUnit = { 

    ---@type eduEntry
    eduEntry = nil,

    ---@type integer
    experience = nil,

    ---@type integer
    cost = nil,

    ---@type number
    replenishMin = nil,

    ---@type number
    replenishMax = nil,

    ---@type integer
    maxUnits = nil,

    ---@type number
    currentPool = nil,

    ---@type integer
    startYear = nil,

    ---@type integer
    endYear = nil,

    ---@type integer
    crusading = nil,

    ---@type integer
    poolIndex = nil,

    ---@type integer
    mercPoolUnitIndex = nil,

    ---@type mercPool
    mercPool = nil,

}

--- Set or remove a religion requirement for a mercenary unit.
---@param religion integer 
---@param set boolean True means enable this religion requirement, False means disable.
function mercPoolUnit:setMercReligion(religion, set) end 

---Basic gameDataAll table
---@class gameDataAll
gameDataAll = { 

    ---battle data
    ---@type battleStruct
    battleStruct = nil,

    ---campaign data
    ---@type campaignStruct
    campaignStruct = nil,

    ---ui and selected objects data
    ---@type uiCardManager
    uiCardManager = nil,

    ---data
    ---@type stratMap
    stratMap = nil,

}

--- Call at the start of the script, this is a static object and the pointer to it doesn't change.
---@return gameDataAll gameDataAll 
function gameDataAll.get() end 

---basic battleStruct table
---@class battleStruct
battleStruct = { 

    ---@type integer
    battleState = nil,

    ---@type integer
    battleType = nil,

    ---@type integer
    isNightBattle = nil,

    ---@type integer
    xCoord = nil,

    ---@type integer
    yCoord = nil,

    ---@type integer
    attackerXCoord = nil,

    ---@type integer
    attackerYCoord = nil,

    ---@type integer
    defenderXCoord = nil,

    ---@type integer
    defenderYCoord = nil,

    ---@type integer
    paused = nil,

    ---@type integer
    inBattle = nil,

    ---@type number
    battleSpeed = nil,

    ---@type number
    secondsPassed = nil,

    ---@type integer
    secondsSinceBattleLoaded = nil,

    ---@type integer
    hidingEnabledSet = nil,

    ---@type number
    mapWidthDoubled = nil,

    ---@type number
    mapHeightDoubled = nil,

    ---@type integer
    sidesNum = nil,

    ---Returns a battleSide[8]. Maximum: 8.
    ---@type table<integer, battleSide>
    sides = nil,

    ---faction alliance array, -1 if not in battle, start at 1 so faction ID + 1 Maximum 31.
    ---@type table<integer, integer>
    factionSide = nil,

}

--- Get table with certain info about the battle residence.
---@return battleResidence battleResidence 
function battleStruct.getBattleResidence() end 

---Basic battleSide table
---@class battleSide
battleSide = { 

    ---@type boolean
    isDefender = nil,

    ---@type boolean
    isCanDeploy = nil,

    ---0 = lose, 1 = draw, 2 = win
    ---@type integer
    wonBattle = nil,

    ---0 = close, 1 = average, 2 = clear, 3 = crushing
    ---@type integer
    battleSuccess = nil,

    ---Returns an int index of a wincondition. Maximum 4.
    ---@type table<integer, integer>
    winConditions = nil,

    ---@type integer
    armiesNum = nil,

    ---@type integer
    alliance = nil,

    ---@type integer
    soldierCount = nil,

    ---@type integer
    factionCount = nil,

    ---@type integer
    totalStrength = nil,

    ---@type number
    battleOdds = nil,

    ---@type integer
    totalValueStart = nil,

    ---@type battleAI
    battleAIPlan = nil,

    ---Returns a table of trackedPointerArmy. Maximum: 64.
    ---@type table<integer, trackedPointerArmy>
    armies = nil,

}

--- Get win condition string, for example: destroy\_or\_rout_enemy
---@param condition integer 
---@return string winCondition destroy\_or\_rout\_enemy, balance\_of\_strength\_percent, destroy\_enemy\_strength\_percent, capture\_location, destroy\_character, capture\_major\_settlement, capture\_army\_settlement, unknown\_condition
function battleSide.getWinConditionString(condition) end 

--- Get a battle army by it's index.
---@param index integer 
---@return battleArmy army 
function battleSide:getBattleArmy(index) end 

---Basic trackedPointerArmy table
---@class trackedPointerArmy
trackedPointerArmy = { 

    ---@type stackStruct
    army = nil,

    ---@type deploymentAreaS
    deploymentArea = nil,

}

---Basic trackedPointerArmy table
---@class deploymentAreaS
deploymentAreaS = { 

    ---@type integer
    coordsNum = nil,

}

--- Get pair of coords with index.
---@return number xCoord X coordinate of the area.
---@return number yCoord Y coordinate of the area.
function deploymentAreaS:getCoordPair() end 

---Basic Battle AI table
---@class battleAI
battleAI = { 

    ---@type integer
    gtaPlan = nil,

    ---@type integer
    unitCount = nil,

    ---@type integer
    enemyUnitCount = nil,

    ---@type integer
    addedObjectivesCount = nil,

}

--- Get a battle objective by it's index.
---@param index integer 
---@return battleObjective objective 
function battleAI:getObjective(index) end 

---Basic battleObjective table
---@class battleObjective
battleObjective = { 

    ---@type integer
    priority = nil,

    ---@type integer
    unitCount = nil,

}

--- Get a unit by it's index.
---@param index integer 
---@return unit unit 
function battleObjective:getUnit(index) end 

--- Get the type of objective.
---@return integer objectiveType 
function battleObjective:getType() end 

---Basic battleArmy table
---@class battleArmy
battleArmy = { 

    ---@type stackStruct
    army = nil,

    ---@type character
    character = nil,

    ---@type integer
    generalNumKillsBattle = nil,

    ---@type number
    totalValue = nil,

    ---@type number
    generalHPRatioLost = nil,

    ---@type integer
    numKilledGenerals = nil,

    ---@type integer
    unitCount = nil,

}

--- Get a battle unit by it's index.
---@param index integer 
---@return battleUnit unit 
function battleArmy:getBattleUnit(index) end 

---Basic battleUnit table
---@class battleUnit
battleUnit = { 

    ---@type unit
    unit = nil,

    ---@type number
    valuePerSoldier = nil,

    ---@type integer
    soldiersLost = nil,

    ---@type integer
    soldiersStart = nil,

    ---@type integer
    unitsRouted = nil,

    ---@type integer
    soldiersKilled = nil,

    ---@type integer
    takenPrisoner = nil,

    ---@type integer
    prisonersCaught = nil,

    ---@type integer
    soldiersHealed = nil,

    ---@type integer
    unitsRoutedEnd = nil,

    ---@type integer
    soldiersEnd = nil,

    ---@type integer
    friendlyFireCasualties = nil,

    ---@type integer
    expStart = nil,

    ---@type integer
    expGained = nil,

    ---@type integer
    isGeneral = nil,

    ---@type integer
    hasWithdrawn = nil,

}

---Basic battleResidence table
---@class battleResidence
battleResidence = { 

    ---@type settlementStruct
    settlement = nil,

    ---@type factionStruct
    faction = nil,

    ---@type integer
    isFortBattle = nil,

    ---@type battleBuildings
    battleBuildings = nil,

    ---@type integer
    settlementWallsBreached = nil,

    ---@type integer
    settlementGateDestroyed = nil,

}

---Basic buildingBattle table
---@class buildingBattle
buildingBattle = { 

    ---@type integer
    type = nil,

    ---@type integer
    endHealth = nil,

    ---@type integer
    currentHealth = nil,

    ---@type integer
    startHealth = nil,

    ---@type integer
    isDefenderControlled = nil,

    ---@type number
    posX = nil,

    ---@type number
    posZ = nil,

    ---@type number
    posY = nil,

}

---Basic battleBuildings table
---@class battleBuildings
battleBuildings = { 

    ---@type integer
    buildingCount = nil,

}

--- Get a battle building by it's index.
---@param index integer 
---@return buildingBattle building 
function battleBuildings:getBuilding(index) end 

---Enum with a list of attack attributes.
---@enum attackAttr
attackAttr = { 

    ---@type integer
    nothing = nil,

    ---@type integer
    spear = nil,

    ---@type integer
    light_spear = nil,

    ---@type integer
    prec = nil,

    ---@type integer
    ap = nil,

    ---@type integer
    bp = nil,

    ---@type integer
    area = nil,

    ---@type integer
    fire = nil,

    ---@type integer
    launching = nil,

    ---@type integer
    thrown = nil,

    ---@type integer
    short_pike = nil,

    ---@type integer
    long_pike = nil,

    ---@type integer
    spear_bonus_12 = nil,

    ---@type integer
    spear_bonus_10 = nil,

    ---@type integer
    spear_bonus_8 = nil,

    ---@type integer
    spear_bonus_6 = nil,

    ---@type integer
    spear_bonus_4 = nil,

}

---Enum with a list of stats.
---@enum eduStat
eduStat = { 

    ---@type integer
    none = nil,

    ---@type integer
    armour = nil,

    ---@type integer
    defense = nil,

    ---@type integer
    shield = nil,

    ---@type integer
    attack = nil,

    ---@type integer
    charge = nil,

}

---Basic M2TWEOPDU table. Contains descriptions of M2TWEOP unit types.
---@class M2TWEOPDU
M2TWEOPDU = { 

}

--- Create new M2TWEOPDU entry from a file describing it.
---@param filepath string path to file with unit type description(like in export\_descr\_unit.txt, but only with one record and without comments)
---@param eopEnryIndex integer Entry index, which will be assigned to a new record in DU (recommend starting from 1000, so that there is no confusion with records from EDU).
---@return eduEntry retEntry Usually you shouldn't use this value.
function M2TWEOPDU.addEopEduEntryFromFile(filepath, eopEnryIndex) end 

--- Create new M2TWEOPDU entry.
---@param baseEnryIndex integer Entry index number, which will be taken as the base for this DU record.
---@param eopEnryIndex integer Entry index, which will be assigned to a new record in DU (recommend starting from 1000, so that there is no confusion with records from EDU).
---@return eduEntry retEntry Usually you shouldn't use this value.
function M2TWEOPDU.addEopEduEntryFromEDUID(baseEnryIndex, eopEnryIndex) end 

---Needed for change many parameters of entry. Get eduEntry of a M2TWEOPDU entry. Needed to change many parameters of the entry.
---@param eopEnryIndex integer Entry index in M2TWEOPDU.
---@return eduEntry retEntry 
function M2TWEOPDU.getEopEduEntryByID(eopEnryIndex) end 

--- Get data of a M2TWEOPDU entry. You usually won't need this.
---@param eopEnryIndex integer Entry index in M2TWEOPDU.
---@return integer retEntry Usually you shouldn't use this value.
function M2TWEOPDU.getDataEopDu(eopEnryIndex) end 

--- Get eduEntry by index. Needed to change many parameters of the entry.
---@param EnryIndex integer Entry index (Values lower then 500 look for edu entry, values over 500 look for EOP edu entry).
---@return eduEntry retEntry 
function M2TWEOPDU.getEduEntry(EnryIndex) end 

--- Get eduEntry by edu type name. Needed to change many parameters of the entry.
---@param type string Unit type as in export_descr_unit.
---@return eduEntry retEntry 
function M2TWEOPDU.getEduEntryByType(type) end 

--- Get edu index by edu type name. Needed to use many edu functions.
---@param type string Unit type as in export_descr_unit.
---@return integer eduindex 
function M2TWEOPDU.getEduIndexByType(type) end 

---(only for eopdu units added by file!) Set unit card for a M2TWEOPDU entry. Requirements for the location and parameters of the image are unchanged in relation to the game (only for eopdu units added by file!).
---@param eopEnryIndex integer Entry index in M2TWEOPDU.
---@param newCardTga string 
function M2TWEOPDU.setEntryUnitCardTga(eopEnryIndex, newCardTga) end 

---(only for eopdu units added by file!) Set unit info card for M2TWEOPDU entry. Requirements for the location and parameters of the image are unchanged in relation to the game (only for eopdu units added by file!).
---@param eopEnryIndex integer Entry index in M2TWEOPDU.
---@param newInfoCardTga string 
function M2TWEOPDU.setEntryInfoCardTga(eopEnryIndex, newInfoCardTga) end 

--- Set unit info card for a M2TWEOPDU entry. Requirements for the location and parameters of the image are unchanged in relation to the game.
---@param eopEnryIndex integer Entry index in M2TWEOPDU.
---@param newSoldierModel string 
function M2TWEOPDU.setEntrySoldierModel(eopEnryIndex, newSoldierModel) end 

--- Get the amount of numbers in the armour_upg_levels line in export_descr_unit.
---@param index integer Entry index (Values lower then 500 look for edu entry, values over 500 look for EOP edu entry).
---@return integer ArmourUpgradeLevelsNum 
function M2TWEOPDU.getArmourUpgradeLevelsNum(index) end 

---(only for eopdu units added by file!) Set the amount of armour_upg_levels, if you increase the amount of levels the last number entry will be repeated (only for eopdu units added by file!).
---@param index integer Entry index (Values lower then 500 look for edu entry, values over 500 look for EOP edu entry).
---@param amount integer 
function M2TWEOPDU.setArmourUpgradeLevelsNum(index, amount) end 

--- Get armour upgrade level number at specified index.
---@param index integer Entry index (Values lower then 500 look for edu entry, values over 500 look for EOP edu entry).
---@param levelidx integer 
---@return integer level 
function M2TWEOPDU.getArmourUpgradeLevel(index, levelidx) end 

---(only for eopdu units added by file!) Set armour upgrade level number at specified index (only for eopdu units added by file!).
---@param index integer Entry index (Values lower then 500 look for edu entry, values over 500 look for EOP edu entry).
---@param levelidx integer 
---@param newlevel integer 
function M2TWEOPDU.setArmourUpgradeLevel(index, levelidx, newlevel) end 

--- Get the amount of models in the armour_upg_models line in export_descr_unit.
---@param index integer Entry index (Values lower then 500 look for edu entry, values over 500 look for EOP edu entry).
---@return integer ArmourUpgradeLevelsNum 
function M2TWEOPDU.getArmourUpgradeModelsNum(index) end 

---(only for eopdu units added by file!) Set the amount of armour_upg_levels, if you increase the amount of models the last model entry will be repeated (only for eopdu units added by file!).
---@param index integer Entry index (Values lower then 500 look for edu entry, values over 500 look for EOP edu entry).
---@param amount integer Maximum: 4
function M2TWEOPDU.setArmourUpgradeModelsNum(index, amount) end 

--- Get armour upgrade level number at specified index.
---@param index integer Entry index (Values lower then 500 look for edu entry, values over 500 look for EOP edu entry).
---@param levelidx integer 
---@return string modelName 
function M2TWEOPDU.getArmourUpgradeModel(index, levelidx) end 

---(only for eopdu units added by file!) Set the unit model at specified index (only for eopdu units added by file!).
---@param index integer Entry index (Values lower then 500 look for edu entry, values over 500 look for EOP edu entry).
---@param levelidx integer 
---@param modelName string 
function M2TWEOPDU.setArmourUpgradeModel(index, levelidx, modelName) end 

--- Set a primary or secondary attack attribute of an edu entry.
---@param index integer Entry index (Values lower then 500 look for edu entry, values over 500 look for EOP edu entry).
---@param attribute integer Use the attackAttr enum: attackAttr.spear, attackAttr.light\_spear, attackAttr.prec, attackAttr.ap, attackAttr.bp, attackAttr.area, attackAttr.fire, attackAttr.launching, attackAttr.thrown, attackAttr.short\_pike, attackAttr.long\_pike, attackAttr.spear\_bonus\_12, attackAttr.spear\_bonus\_10, attackAttr.spear\_bonus\_8, attackAttr.spear\_bonus\_6, attackAttr.spear\_bonus\_4.
---@param enable boolean 
---@param sec integer 1 = primary, 2 = secondary.
function M2TWEOPDU.setEntryAttackAttribute(index, attribute, enable, sec) end 

--- Get a primary or secondary attack attribute from an edu entry.
---@param index integer Entry index (Values lower then 500 look for edu entry, values over 500 look for EOP edu entry).
---@param attribute integer Use the attackAttr enum: attackAttr.spear, attackAttr.light\_spear, attackAttr.prec, attackAttr.ap, attackAttr.bp, attackAttr.area, attackAttr.fire, attackAttr.launching, attackAttr.thrown, attackAttr.short\_pike, attackAttr.long\_pike, attackAttr.spear\_bonus\_12, attackAttr.spear\_bonus\_10, attackAttr.spear\_bonus\_8, attackAttr.spear\_bonus\_6, attackAttr.spear\_bonus\_4.
---@param sec integer 1 = primary, 2 = secondary.
---@return boolean hasAttackAttribute 
function M2TWEOPDU.getEntryAttackAttribute(index, attribute, sec) end 

--- Set any of the basic unit stats of an edu entry.
---@param index integer Entry index (Values lower then 500 look for edu entry, values over 500 look for EOP edu entry).
---@param eduStat integer Use the eduStat enum: eduStat.armour, eduStat.defense, eduStat.shield, eduStat.attack, eduStat.charge.
---@param value integer 
---@param sec integer 1 = primary, 2 = secondary.
function M2TWEOPDU.setEntryStat(index, eduStat, value, sec) end 

--- Get any of the basic unit stats of an edu entry.
---@param index integer Entry index (Values lower then 500 look for edu entry, values over 500 look for EOP edu entry).
---@param eduStat integer Use the eduStat enum: eduStat.armour, eduStat.defense, eduStat.shield, eduStat.attack, eduStat.charge.
---@param sec integer 1 = primary, 2 = secondary.
---@return integer unitStat 
function M2TWEOPDU.getEntryStat(index, eduStat, sec) end 

--- Set localized name for a M2TWEOPDU entry. This does not require any entries in the text folder.
---@param eopEnryIndex integer Entry index in M2TWEOPDU.
---@param newLocalizedName string 
function M2TWEOPDU.setEntryLocalizedName(eopEnryIndex, newLocalizedName) end 

--- Set localized description for M2TWEOPDU entry. This does not require any entries in the text folder.
---@param eopEnryIndex integer Entry index in M2TWEOPDU.
---@param newLocalizedDescr string 
function M2TWEOPDU.setEntryLocalizedDescr(eopEnryIndex, newLocalizedDescr) end 

--- Set localized short description for M2TWEOPDU entry. This does not require any entries in the text folder.
---@param eopEnryIndex integer Entry index in M2TWEOPDU.
---@param newLocalizedShortDescr string 
function M2TWEOPDU.setEntryLocalizedShortDescr(eopEnryIndex, newLocalizedShortDescr) end 

---Basic edbEntry table.
---@class edbEntry
edbEntry = { 

    ---@type integer
    buildingID = nil,

    ---@type integer
    classification = nil,

    ---@type integer
    isCoreBuilding = nil,

    ---@type integer
    isPort = nil,

    ---@type integer
    isCoreBuilding2 = nil,

    ---@type integer
    hasReligion = nil,

    ---@type integer
    religionID = nil,

    ---@type integer
    isHinterland = nil,

    ---@type integer
    isFarm = nil,

    ---@type integer
    buildingLevelCount = nil,

}

---Basic capability table.
---@class capability
capability = { 

    ---@type integer
    capabilityType = nil,

    ---@type integer
    capabilityLvl = nil,

    ---@type integer
    bonus = nil,

    ---@type integer
    capabilityID = nil,

}

---Basic recruitpool table.
---@class recruitpool
recruitpool = { 

    ---@type integer
    capabilityType = nil,

    ---Difference is for agents
    ---@type integer
    capabilityLvlorExp = nil,

    ---@type integer
    unitID = nil,

    ---@type number
    initialSize = nil,

    ---@type number
    gainPerTurn = nil,

    ---@type number
    maxSize = nil,

}

---Basic EDB table.
---@class EDB
EDB = { 

}

--- Create new EOP Building entry
---@param edbEntry edbEntry Old entry.
---@param newIndex integer New index of new entry.
---@return edbEntry eopentry. 
function EDB.addEopBuildEntry(edbEntry, newIndex) end 

--- Get EOP Building entry. Returns vanilla build entry if you use a vanilla building index (< 128).
---@param index integer Index of eop entry.
---@return edbEntry eopentry. 
function EDB.getEopBuildEntry(index) end 

--- Set picture of building.
---@param edbEntry edbEntry Entry to set.
---@param newPic string Path to new pic.
---@param level integer Building level to set pic for.
---@param culture integer ID of the culture to set the pic for.
function EDB.setBuildingPic(edbEntry, newPic, level, culture) end 

--- Set constructed picture of building.
---@param edbEntry edbEntry Entry to set.
---@param newPic string Path to new pic.
---@param level integer Building level to set pic for.
---@param culture integer ID of the culture to set the pic for.
function EDB.setBuildingPicConstructed(edbEntry, newPic, level, culture) end 

--- Set construction picture of building.
---@param edbEntry edbEntry Entry to set.
---@param newPic string Path to new pic.
---@param level integer Building level to set pic for.
---@param culture integer ID of the culture to set the pic for.
function EDB.setBuildingPicConstruction(edbEntry, newPic, level, culture) end 

--- Set name of a building.
---@param edbEntry edbEntry Entry to set.
---@param newName string New name.
---@param level integer Building level.
---@param facnum integer Faction ID of the faction to set it for (dipNum).
function EDB.setBuildingLocalizedName(edbEntry, newName, level, facnum) end 

--- Set description of a building.
---@param edbEntry edbEntry Entry to set.
---@param newName string New description.
---@param level integer Building level.
---@param facnum integer Faction ID of the faction to set it for (dipNum).
function EDB.setBuildingLocalizedDescr(edbEntry, newName, level, facnum) end 

--- Set short description of a building.
---@param edbEntry edbEntry Entry to set.
---@param newName string New short description.
---@param level integer Building level.
---@param facnum integer Faction ID of the faction to set it for (dipNum).
function EDB.setBuildingLocalizedDescrShort(edbEntry, newName, level, facnum) end 

--- Add a capability to a building.
---@param edbEntry edbEntry Entry to set.
---@param level integer Building level.
---@param capability integer ID of capability to set.
---@param value integer Value to set.
---@param bonus boolean Is it bonus or not.
function EDB.addBuildingCapability(edbEntry, level, capability, value, bonus) end 

--- Remove a capability from a building.
---@param edbEntry edbEntry Entry to set.
---@param level integer Building level.
---@param index integer Which capability to remove (In order of iterating).
function EDB.removeBuildingCapability(edbEntry, level, index) end 

--- Get capability from a building at an index.
---@param edbEntry edbEntry Entry to set.
---@param level integer Building level.
---@param index integer 
---@return capability capability. 
function EDB.getBuildingCapability(edbEntry, level, index) end 

--- Get capability amount from a building.
---@param edbEntry edbEntry Entry to set.
---@param level integer Building level.
---@return integer capabilityNum. 
function EDB.getBuildingCapabilityNum(edbEntry, level) end 

--- Add a recruitment pool to a building.
---@param edbEntry edbEntry Entry to set.
---@param level integer Building level.
---@param eduIndex integer edu index of unit to add.
---@param initialSize number Initial pool.
---@param gainPerTurn number Replenishment per turn.
---@param maxSize number Maximum size.
---@param exp integer Initial experience.
---@param condition string Like in export_descr_buildings but without "requires".
function EDB.addBuildingPool(edbEntry, level, eduIndex, initialSize, gainPerTurn, maxSize, exp, condition) end 

--- Remove a recruitment pool from a building.
---@param edbEntry edbEntry Entry to set.
---@param level integer Building level.
---@param index integer Which pool to remove (In order of iterating).
function EDB.removeBuildingPool(edbEntry, level, index) end 

--- Get a recruitment pool from a building by index.
---@param edbEntry edbEntry Entry to set.
---@param level integer Building level.
---@param index integer Which pool to get (In order of iterating).
---@return recruitpool pool. 
function EDB.getBuildingPool(edbEntry, level, index) end 

--- Get a recruitment pool count.
---@param edbEntry edbEntry Entry to set.
---@param level integer Building level.
---@return integer poolNum. 
function EDB.getBuildingPoolNum(edbEntry, level) end 

--- Get a building edb entry by name.
---@param buildingname string 
---@return edbEntry entry 
function EDB.getBuildingByName(buildingname) end 

---Basic M2TWEOPSounds table. Contains descriptions of M2TWEOP sound features. Attention! You can use 256 sounds max. It supports the following audio formats: - WAV - OGG/Vorbis - FLAC You can play many sounds at the same time. It should be used for small sounds that can fit in memory. It's not recommended to use this for playing larger sounds like music.
---@class M2TWEOPSounds
M2TWEOPSounds = { 

}

--- Create (and load) a new sound.
---@param soundPath string Path to sound file
---@return integer soundID ID that will be used by this sound. Returns nil if the sound can't load..
function M2TWEOPSounds.createEOPSound(soundPath) end 

--- Delete a sound
---@param soundID integer ID of the sound that you want to delete.
function M2TWEOPSounds.deleteEOPSound(soundID) end 

--- Play a sound.
---@param soundID integer ID of the sound that you want to play.
function M2TWEOPSounds.playEOPSound(soundID) end 

--- Set a sound's playing offset. i.e Skip a certain number of milliseconds of the beginning of the sound.
---@param soundID integer ID of the sound.
---@param millisecondsOffset integer New playing position, from the beginning of the sound.
function M2TWEOPSounds.setEOPSoundOffset(soundID, millisecondsOffset) end 

--- Get a sound's playing offset.
---@param soundID integer ID of the sound.
---@return integer millisecondsOffset Playing position, from the beginning of the sound.
function M2TWEOPSounds.getEOPSoundOffset(soundID) end 

--- Pause a sound that is playing.
---@param soundID integer ID of the sound that you want to pause.
function M2TWEOPSounds.pauseEOPSound(soundID) end 

--- Stop a sound that is playing.
---@param soundID integer ID of the sound that you want to stop.
function M2TWEOPSounds.stopEOPSound(soundID) end 

---Basic M2TWEOPFBX table. Contains descriptions of m2tweop fbx feathures.
---@class M2TWEOPFBX
M2TWEOPFBX = { 

}

--- Load a new fbx model.
---@param modelPath string Path to .fbx file.
---@param texturePath string Path to .dds file
---@param modelID integer ID to be used for this model.
function M2TWEOPFBX.addFbxModel(modelPath, texturePath, modelID) end 

--- Delete a fbx model.
---@param modelID integer Model's ID that was specified when calling addFbxModel()
function M2TWEOPFBX.deleteFbxModel(modelID) end 

--- Get an added fbx model by it's ID.
---@param modelID integer Model's ID that was specified when calling addFbxModel()
---@return fbxModel fbx model, not it`s ID!
function M2TWEOPFBX.getFbxModel(modelID) end 

--- Create new fbx object with our previously loaded model. It can be placed on map, etc.
---@param modelID integer Model's ID that was specified when calling addFbxModel()
---@param objectID integer The ID that the object should use
---@return fbxObject The newly created FBX object (not it's ID)
function M2TWEOPFBX.addFbxObject(modelID, objectID) end 

--- Delete an fbx object.
---@param object fbxObject The created FBX object (not it's ID)
function M2TWEOPFBX.deleteFbxObject(object) end 

--- Get an fbx object by it's ID.
---@param int objectID The ID of the FBX object you wish to retrieve
---@return fbxObject The created FBX object (not it's ID)
function M2TWEOPFBX.getFbxObject(int) end 

--- Set an fbx object's coordinates.
---@param fbx fbxObject object
---@param x number coord
---@param y number coord
---@param z number coord
function M2TWEOPFBX.setFbxObjectCoords(fbx, x, y, z) end 

--- Get an fbx object's coordinates.
---@param fbx fbxObject object
---@return number x coord
---@return number y coord
---@return number z coord
function M2TWEOPFBX.getFbxObjectCoords(fbx) end 

--- Set an fbx object's size modifier.
---@param fbx fbxObject object
---@param sizeModifier number object size modifier
function M2TWEOPFBX.setFbxObjectSize(fbx, sizeModifier) end 

--- Get an fbx object's size modifier.
---@param fbx fbxObject object
---@return number sizeModifier object size modifier
function M2TWEOPFBX.getFbxObjectSize(fbx) end 

--- Set an fbx object's draw state.
---@param fbx fbxObject object
---@param is boolean draw needed
function M2TWEOPFBX.setFbxObjectDrawState(fbx, is) end 

--- Get an fbx object's draw state.
---@param fbx fbxObject object
---@return boolean is draw needed
function M2TWEOPFBX.getFbxObjectDrawState(fbx) end 

--- Set an fbx object's animation state.
---@param fbx fbxObject object
---@param is boolean animation needed
function M2TWEOPFBX.setFbxObjectAnimState(fbx, is) end 

--- Get an fbx object's animation state.
---@param fbx fbxObject object
---@return boolean is animation needed
function M2TWEOPFBX.getFbxObjectAnimState(fbx) end 

--- Set fbx object draw type, i.e. on what part of the game it is drawn.
-- Can be:
-- 1 - Strategy Map
-- 2 - Tactical/Battle Map
-- 0 - Both
-- Default value - 1
---@param fbx fbxObject object
---@param current integer draw type
function M2TWEOPFBX.setFbxObjectDrawType(fbx, current) end 

--- Get fbx object draw type, i.e. on what part of game it is drawn.
-- Can be:
-- 1 - Strategy Map
-- 2 - Tactical/Battle Map
-- 0 - Both
-- Default value - 1
---@param fbx fbxObject object
---@return integer current draw type
function M2TWEOPFBX.getFbxObjectDrawType(fbx) end 

---Events functions list. Just list, use it without EventsFunctionsList.!!!
---@class EventsFunctionsList
EventsFunctionsList = { 

}

--- Called at a character's turn start.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onCharacterTurnStart(eventData) end 

--- A captured character has been successfully ransomed back from the enemy.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onCapturedCharacterRansomed(eventData) end 

--- A captured character has been released by the enemy.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onCapturedCharacterReleased(eventData) end 

--- A character father died of natural causes.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onFatherDiesNatural(eventData) end 

--- When a battle is about to start but one of the armies withdraws.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onPreBattleWithdrawal(eventData) end 

--- When a battle has finished.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onPostBattle(eventData) end 

--- A General has hired some mercenaries.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onHireMercenaries(eventData) end 

--- A General has captured a residence such as a fort or watchtower.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onGeneralCaptureResidence(eventData) end 

--- A faction has been destroyed.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onLeaderDestroyedFaction(eventData) end 

--- An adoption has been proposed.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onOfferedForAdoption(eventData) end 

--- A lesser general adoption has been proposed (man of the hour event).
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onLesserGeneralOfferedForAdoption(eventData) end 

--- A marriage offer has been proposed.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onOfferedForMarriage(eventData) end 

--- A brother has been adopted.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onBrotherAdopted(eventData) end 

--- A child is born to the faction leader.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onBirth(eventData) end 

--- A character has come of age.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onCharacterComesOfAge(eventData) end 

--- A character has married.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onCharacterMarries(eventData) end 

--- A character has married a princess.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onCharacterMarriesPrincess(eventData) end 

--- A marriage alliance is possible.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onMarriageAlliancePossible(eventData) end 

--- A marriage alliance has been offered.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onMarriageAllianceOffered(eventData) end 

--- A priest has gone mad.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onPriestBecomesHeretic(eventData) end 

--- A character is adjacent to a heretic.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onCharacterNearHeretic(eventData) end 

--- A character is adjacent to a witch.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onCharacterNearWitch(eventData) end 

--- A character has been promoted to a cardinal.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onCardinalPromoted(eventData) end 

--- A character has become a father.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onCharacterBecomesAFather(eventData) end 

--- A General and his army has devastated an enemy's fertile land.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onGeneralDevastatesTile(eventData) end 

--- A spying mission has failed and the spy is executed by the target.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onExecutesASpyOnAMission(eventData) end 

--- An assassination mission has failed and the assassin is executed by the target.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onExecutesAnAssassinOnAMission(eventData) end 

--- Someone has had an attempt on their life.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onSufferAssassinationAttempt(eventData) end 

--- Someone has had an attempt on their assets.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onSufferAcquisitionAttempt(eventData) end 

--- Someone has had an attempt on their bachelorhood.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onSufferMarriageAttempt(eventData) end 

--- Someone has had a denouncement attempt.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onSufferDenouncementAttempt(eventData) end 

--- A Faction leader has ordered a sabotage mission.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onLeaderOrderedSabotage(eventData) end 

--- Someone has been bribed.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onAcceptBribe(eventData) end 

--- Someone has refused a bribe.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onRefuseBribe(eventData) end 

--- Insurgence has been provoked.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onInsurrection(eventData) end 

--- A Faction leader has ordered a diplomacy mission.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onLeaderOrderedDiplomacy(eventData) end 

--- A new admiral has been created for a new ship.
-- Exports: stratCharacter, character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onNewAdmiralCreated(eventData) end 

--- A building has been destroyed.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onGovernorBuildingDestroyed(eventData) end 

--- Games have been thrown.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onGovernorThrowGames(eventData) end 

--- Races have been thrown.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onGovernorThrowRaces(eventData) end 

--- The player has selected a character.
-- Exports: character, targetSettlement, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onCharacterSelected(eventData) end 

--- The player has selected an enemy character.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onEnemyCharacterSelected(eventData) end 

--- The player has selected a position beyond the character's extents.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onMultiTurnMove(eventData) end 

--- The player has opened the panel for the selected character.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onCharacterPanelOpen(eventData) end 

--- A mission has been completed.
-- Exports: character, faction, regionID, characterType, missionDetails, religion
---@param eventData eventTrigger 
function onLeaderMissionSuccess(eventData) end 

--- A mission has failed.
-- Exports: character, faction, regionID, characterType, missionDetails, religion
---@param eventData eventTrigger 
function onLeaderMissionFailed(eventData) end 

--- A General has been sent on Crusade/Jihad.
-- Exports: character, targetSettlement, faction, targetFaction, regionID, targetRegionID, characterType, religion, targetReligion, crusade
---@param eventData eventTrigger 
function onGeneralJoinCrusade(eventData) end 

--- A General has left a Crusade/Jihad.
-- Exports: character, targetSettlement, faction, targetFaction, regionID, targetRegionID, characterType, religion, targetReligion, crusade
---@param eventData eventTrigger 
function onGeneralAbandonCrusade(eventData) end 

--- A General has arrived in the Crusade/Jihad target region.
-- Exports: character, targetSettlement, faction, targetFaction, army, regionID, targetRegionID, characterType, religion, targetReligion, crusade
---@param eventData eventTrigger 
function onGeneralArrivesCrusadeTargetRegion(eventData) end 

--- A General has taken the Crusade/Jihad target settlement.
-- Exports: character, targetSettlement, faction, targetFaction, regionID, targetRegionID, characterType, religion, targetReligion, crusade
---@param eventData eventTrigger 
function onGeneralTakesCrusadeTarget(eventData) end 

--- A Character has finished its turn.
-- Exports: character, settlement, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onCharacterTurnEnd(eventData) end 

--- A Character has finished its turn in a settlement.
-- Exports: character, settlement, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onCharacterTurnEndInSettlement(eventData) end 

--- The character has been made the faction leader.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onBecomesFactionLeader(eventData) end 

--- The character is no longer faction leader.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onCeasedFactionLeader(eventData) end 

--- The character has been made a faction heir.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onBecomesFactionHeir(eventData) end 

--- The character is no longer faction heir.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onCeasedFactionHeir(eventData) end 

--- A character has been injured by a disaster.
-- Exports: character, faction, regionID, disasterType, characterType, religion
-- disasterTypes = earthquake, flood, horde, storm, volcano, dustbowl, locusts, famine, plague, riot, fire
---@param eventData eventTrigger 
function onCharacterDamagedByDisaster(eventData) end 

--- A General has captured a settlement.
-- Exports: character, settlement, targetSettlement, faction, targetFaction, regionID, characterType, religion
---@param eventData eventTrigger 
function onGeneralCaptureSettlement(eventData) end 

--- An assault has taken place. NOTE: settlement and fort are not in eventData! They are separate arguments!.
-- Exports: character, faction, targetFaction, regionID, targetRegionID, characterType, religion, targetReligion
---@param eventData eventTrigger 
---@param settlement settlementStruct|nil 
---@param fort fortStruct|nil 
function onGeneralAssaultsResidence(eventData, settlement, fort) end 

--- An assault has taken place.
-- Exports: character, targetCharacter, faction, targetFaction, regionID, characterType, targetCharacterType, religion, targetReligion
---@param eventData eventTrigger 
function onGeneralAssaultsGeneral(eventData) end 

--- A general on crusade/jihad has been attacked by other character (it includes crusading generals attacked in a residence or on navy and generals attacked by spotted and killed assassin).
-- Exports: character, targetCharacter, faction, targetFaction, regionID, characterType, targetCharacterType, religion, targetReligion
---@param eventData eventTrigger 
function onCharacterAttacksCrusadingGeneral(eventData) end 

--- A General of a captor faction has made a ransom decision.
-- Exports: character, faction, targetFaction, regionID, characterType, religion, targetReligion, captureInfo, ransomType
---@param eventData eventTrigger 
function onGeneralPrisonersRansomedCaptor(eventData) end 

--- A General of a captive faction has made a ransom decision.
-- Exports: character, faction, targetFaction, regionID, characterType, religion, targetReligion, captureInfo, ransomType
---@param eventData eventTrigger 
function onGeneralPrisonersRansomedCaptive(eventData) end 

--- A captor faction has made a ransom decision.
-- Exports: character, faction, targetFaction, regionID, characterType, religion, targetReligion, captureInfo, ransomType
---@param eventData eventTrigger 
function onFactionLeaderPrisonersRansomedCaptor(eventData) end 

--- A captive faction has made a ransom decision.
-- Exports: character, faction, targetFaction, regionID, characterType, religion, targetReligion, captureInfo, ransomType
---@param eventData eventTrigger 
function onFactionLeaderPrisonersRansomedCaptive(eventData) end 

--- A spy mission has completed. May also export fort or settlement if target was a garrison residence.
-- Exports: character, settlement, fort, faction, targetFaction, regionID, characterType, missionSuccessLevel, missionProbability, religion, targetReligion
---@param eventData eventTrigger 
function onSpyMission(eventData) end 

--- An assassination mission has completed.
-- Exports: character, faction, regionID, characterType, missionSuccessLevel, missionProbability, religion
---@param eventData eventTrigger 
function onAssassinationMission(eventData) end 

--- An acquisition mission has completed.
-- Exports: character, faction, regionID, characterType, missionSuccessLevel, missionProbability, religion
---@param eventData eventTrigger 
function onAcquisitionMission(eventData) end 

--- A marriage mission has completed.
-- Exports: character, faction, regionID, characterType, missionSuccessLevel, missionProbability, religion
---@param eventData eventTrigger 
function onMarriageMission(eventData) end 

--- A denouncement mission has completed.
-- Exports: character, faction, regionID, characterType, missionSuccessLevel, missionProbability, religion
---@param eventData eventTrigger 
function onDenouncementMission(eventData) end 

--- A sabotage mission has completed.
-- Exports: character, faction, regionID, characterType, missionSuccessLevel, missionProbability, religion
---@param eventData eventTrigger 
function onSabotageMission(eventData) end 

--- A bribery mission has completed.
-- Exports: character, faction, targetFaction, regionID, characterType, missionSuccessLevel, religion, targetReligion
---@param eventData eventTrigger 
function onBriberyMission(eventData) end 

--- A diplomacy mission has completed.
-- Exports: character, faction, targetFaction, regionID, characterType, missionSuccessLevel, religion, targetReligion
---@param eventData eventTrigger 
function onDiplomacyMission(eventData) end 

--- A Faction leader has ordered a spying mission.
-- Exports: character, settlement, fort, faction, targetFaction, regionID, characterType, missionSuccessLevel, religion, targetReligion
---@param eventData eventTrigger 
function onLeaderOrderedSpyingMission(eventData) end 

--- A Faction leader has ordered an assassination mission.
-- Exports: character, targetCharacter, faction, regionID, characterType, missionSuccessLevel, religion
---@param eventData eventTrigger 
function onLeaderOrderedAssassination(eventData) end 

--- A Faction leader has ordered a bribery mission.
-- Exports: character, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onLeaderOrderedBribery(eventData) end 

--- A settlement is being processed for the start of its faction's turn.
-- Exports: settlement, faction, regionID, religion
---@param eventData eventTrigger 
function onSettlementTurnStart(eventData) end 

--- A settlement is no longer garrisoned.
-- Exports: settlement, faction, regionID, religion
---@param eventData eventTrigger 
function onUngarrisonedSettlement(eventData) end 

--- A settlement has been upgraded.
-- Exports: settlement, faction, regionID, religion
---@param eventData eventTrigger 
function onSettlementUpgraded(eventData) end 

--- A settlement has been converted.
-- Exports: settlement, faction, regionID, religion
---@param eventData eventTrigger 
function onSettlementConverted(eventData) end 

--- Siege equipment has been completed by one of the besieging armies.
-- Exports: settlement, faction, regionID, religion
---@param eventData eventTrigger 
function onSiegeEquipmentCompleted(eventData) end 

--- A Settlement is being processed for the end of its faction's turn.
-- Exports: settlement, faction, regionID, religion
---@param eventData eventTrigger 
function onSettlementTurnEnd(eventData) end 

--- The player has selected a settlement.
-- Exports: settlement, faction, regionID, religion
---@param eventData eventTrigger 
function onSettlementSelected(eventData) end 

--- The player has opened the panel for the selected settlement.
-- Exports: settlement, faction, regionID, religion
---@param eventData eventTrigger 
function onSettlementPanelOpen(eventData) end 

--- The player has opened a recruitment panel.
-- Exports: settlement, faction, regionID, religion
---@param eventData eventTrigger 
function onRecruitmentPanelOpen(eventData) end 

--- The player has opened a construction panel.
-- Exports: settlement, faction, regionID, religion
---@param eventData eventTrigger 
function onConstructionPanelOpen(eventData) end 

--- The player has opened a trade panel.
-- Exports: settlement, faction, regionID, religion
---@param eventData eventTrigger 
function onTradePanelOpen(eventData) end 

--- The player has requested advice on the settlement scroll.
-- Exports: settlement, faction, regionID, resourceDescription, religion
---@param eventData eventTrigger 
function onSettlementScrollAdviceRequested(eventData) end 

--- A guild has been created/upgraded.
-- Exports: settlement, faction, regionID, resourceDescription, guild, religion
---@param eventData eventTrigger 
function onGuildUpgraded(eventData) end 

--- A guild has been destroyed.
-- Exports: settlement, faction, regionID, guild, religion
---@param eventData eventTrigger 
function onGuildDestroyed(eventData) end 

--- A settlement has been captured and occupied.
-- Exports: character, faction, targetFaction, regionID, characterType, religion, targetReligion
---@param eventData eventTrigger 
function onOccupySettlement(eventData) end 

--- A settlement has been captured and sacked.
-- Exports: character, faction, targetFaction, regionID, characterType, religion, targetReligion
---@param eventData eventTrigger 
function onSackSettlement(eventData) end 

--- A settlement has been captured and some of its population has been decimated.
-- Exports: character, faction, targetFaction, regionID, characterType, religion, targetReligion
---@param eventData eventTrigger 
function onExterminatePopulation(eventData) end 

--- A settlement has rioted.
-- Exports: settlement, faction, targetFaction, regionID, religion, targetReligion
---@param eventData eventTrigger 
function onCityRiots(eventData) end 

--- A settlement has been given to another faction.
-- Exports: settlement, faction, targetFaction, regionID, religion, targetReligion
---@param eventData eventTrigger 
function onGiveSettlement(eventData) end 

--- A settlement has rebelled.
-- Exports: settlement, faction, targetFaction, regionID, religion, targetReligion
---@param eventData eventTrigger 
function onCityRebels(eventData) end 

--- A settlement has been razed.
-- Exports: settlement, faction, targetFaction, regionID, religion, targetReligion
---@param eventData eventTrigger 
function onCitySacked(eventData) end 

--- A settlement has rioted.
-- Exports: character, settlement, faction, targetFaction, regionID, characterType, religion, targetReligion
---@param eventData eventTrigger 
function onGovernorCityRiots(eventData) end 

--- A settlement has rebelled.
-- Exports: character, settlement, faction, targetFaction, regionID, characterType, religion, targetReligion
---@param eventData eventTrigger 
function onGovernorCityRebels(eventData) end 

--- The player has abandoned a show me scipt.
---@param eventData eventTrigger 
function onAbandonShowMe(eventData) end 

--- A strat map game has been reloaded.
---@param eventData eventTrigger 
function onGameReloaded(eventData) end 

--- The plaza is being captured.
---@param eventData eventTrigger 
function onBattleWinningPlaza(eventData) end 

--- The plaza capture has been stopped.
---@param eventData eventTrigger 
function onBattleStopsWinningPlaza(eventData) end 

--- The enemy will have captured the plaza in 30s.
---@param eventData eventTrigger 
function onBattleDominatingPlaza(eventData) end 

--- A siege engine is now unmanned.
---@param eventData eventTrigger 
function onBattngineUnmanned(eventData) end 

--- Half of the player's army has been destroyed.
---@param eventData eventTrigger 
function onBattlePlayerArmyHalfDestroyed(eventData) end 

--- Half of the enemy's army has been destroyed.
---@param eventData eventTrigger 
function onBattnemyArmyHalfDestroyed(eventData) end 

--- The battle has finished.
---@param eventData eventTrigger 
function onBattleFinished(eventData) end 

--- Half of an army has been destroyed.
---@param eventData eventTrigger 
function onBattleArmyHalfDestroyed(eventData) end 

--- The escape key has been pressed. This trigger will only fire if the command StealEscKey has been used.
---@param eventData eventTrigger 
function onEscPressed(eventData) end 

--- The player has been issued with advice by a script.
---@param eventData eventTrigger 
function onScriptedAdvice(eventData) end 

--- The player has requested advice on the naval prebattle scroll.
---@param eventData eventTrigger 
function onNavalPreBattleScrollAdviceRequested(eventData) end 

--- The player has requested advice on the prebattle scroll.
---@param eventData eventTrigger 
function onPreBattleScrollAdviceRequested(eventData) end 

--- The player has opened the college of cardinals panel.
---@param eventData eventTrigger 
function onCollegeOfCardinalsPanelOpen(eventData) end 

--- The player has opened the diplomatic standing panel.
---@param eventData eventTrigger 
function onDiplomaticStandingPanelOpen(eventData) end 

--- An idle unit is under missile fire.
---@param eventData eventTrigger 
function onBattlePlayerUnderAttackIdle(eventData) end 

--- A team has gained the advantage in combat.
---@param eventData eventTrigger 
function onBattleWinningCombat(eventData) end 

--- The whole army is tired.
---@param eventData eventTrigger 
function onBattleArmyTired(eventData) end 

--- A spy has successfully opened the gates.
---@param eventData eventTrigger 
function onBattleSpySuccess(eventData) end 

--- A different team is now the strongest.
---@param eventData eventTrigger 
function onBattleTideofBattle(eventData) end 

--- A unit has gone berserk.
-- Exports: unit
---@param eventData eventTrigger 
function onBattleUnitGoesBerserk(eventData) end 

--- A siege engine has been destroyed.
-- Exports: unit
---@param eventData eventTrigger 
function onBattleSiegeEngineDestroyed(eventData) end 

--- A siege engine has docked with a wall.
-- Exports: unit
---@param eventData eventTrigger 
function onBattleSiegeEngineDocksWall(eventData) end 

--- An engine has started attacking a gate.
-- Exports: unit
---@param eventData eventTrigger 
function onBattleGatesAttackedByEngine(eventData) end 

--- An engine has destroyed a gate.
-- Exports: unit
---@param eventData eventTrigger 
function onBattleGatesDestroyedByEngine(eventData) end 

--- A siege engine has knocked down a wall.
-- Exports: unit
---@param eventData eventTrigger 
function onBattleWallsBreachedByEngine(eventData) end 

--- A wall has been captured.
-- Exports: unit
---@param eventData eventTrigger 
function onBattleWallsCaptured(eventData) end 

--- A unit has routed.
-- Exports: unit
---@param eventData eventTrigger 
function onBattleUnitRouts(eventData) end 

--- A unit has been disbanded.
-- Exports: faction, playerUnit, eduEntry, religion
---@param eventData eventTrigger 
function onUnitDisbanded(eventData) end 

--- A unit has been trained.
-- Exports: settlement, faction, playerUnit, eduEntry, religion
---@param eventData eventTrigger 
function onUnitTrained(eventData) end 

--- A unit has been trained.
-- Exports: character, settlement, faction, regionID, playerUnit, eduEntry, characterType, religion
---@param eventData eventTrigger 
function onGovernorUnitTrained(eventData) end 

--- A building has been completed.
-- Exports: character, settlement, faction, regionID, priorBuild, characterType, religion
---@param eventData eventTrigger 
function onGovernorBuildingCompleted(eventData) end 

--- An agent has been trained.
-- Exports: character, settlement, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onAgentCreated(eventData) end 

--- An agent has been trained.
-- Exports: character, settlement, faction, regionID, characterType, religion
---@param eventData eventTrigger 
function onGovernorAgentCreated(eventData) end 

--- A building has been destroyed.
-- Exports: settlement, faction, regionID, resourceDescription, religion
---@param eventData eventTrigger 
function onBuildingDestroyed(eventData) end 

--- A building has been added to the construction queue.
-- Exports: settlement, faction, regionID, resourceDescription, religion
---@param eventData eventTrigger 
function onAddedToBuildingQueue(eventData) end 

--- A building has been completed.
-- Exports: settlement, faction, priorBuild, religion
---@param eventData eventTrigger 
function onBuildingCompleted(eventData) end 

--- The player has requested building advice.
-- Exports: settlement, faction, regionID, religion
---@param eventData eventTrigger 
function onRequestBuildingAdvice(eventData) end 

--- The player has requested training advice.
-- Exports: settlement, faction, regionID, religion
---@param eventData eventTrigger 
function onRequestTrainingAdvice(eventData) end 

--- A unit has been added to the training queue.
-- Exports: settlement, faction, regionID, resourceDescription, religion
---@param eventData eventTrigger 
function onAddedToTrainingQueue(eventData) end 

--- An army has been entirely routed.
-- Exports: army
---@param eventData eventTrigger 
function onBattleArmyRouted(eventData) end 

--- A reinforcing army has arrived on the battlefield.
-- Exports: army
---@param eventData eventTrigger 
function onBattleReinforcementsArrive(eventData) end 

--- The player has requested mercenaries advice.
-- Exports: army
---@param eventData eventTrigger 
function onRequestMercenariesAdvice(eventData) end 

--- The player has clicked on a button.
-- Exports: resourceDescription
---@param eventData eventTrigger 
function onButtonPressed(eventData) end 

--- The player triggered a keyboard shortcut.
-- Exports: resourceDescription
---@param eventData eventTrigger 
function onShortcutTriggered(eventData) end 

--- A special UI Element is visible.
-- Exports: resourceDescription
---@param eventData eventTrigger 
function onUIElementVisible(eventData) end 

--- The player opened a scroll.
-- Exports: resourceDescription
---@param eventData string 
function onScrollOpened(eventData) end 

--- The player closed a scroll.
-- Exports: resourceDescription
---@param eventData eventTrigger 
function onScrollClosed(eventData) end 

--- The player has requested advice on a scroll.
-- Exports: resourceDescription
---@param eventData eventTrigger 
function onScrollAdviceRequested(eventData) end 

--- The player has suppressed a piece of advice.
-- Exports: resourceDescription
---@param eventData eventTrigger 
function onAdviceSupressed(eventData) end 

--- A general has been routed.
-- Exports: stratCharacter, character
---@param eventData eventTrigger 
function onBattleGeneralRouted(eventData) end 

--- A general has been killed.
-- Exports: stratCharacter
---@param eventData eventTrigger 
function onBattleGeneralKilled(eventData) end 

--- A Crusade/Jihad has been called.
-- Exports: targetSettlement, targetFaction, targetRegionID, targetReligion, crusade
---@param eventData eventTrigger 
function onCrusadeCalled(eventData) end 

--- The Pope has accepted the player's crusade target.
-- Exports: targetSettlement, targetFaction, targetRegionID, targetReligion, crusade
---@param eventData eventTrigger 
function onPopeAcceptsCrusadeTarget(eventData) end 

--- The Pope has rejected the player's crusade target.
-- Exports: targetSettlement, targetFaction, targetRegionID, targetReligion, crusade
---@param eventData eventTrigger 
function onPopeRejectsCrusadeTarget(eventData) end 

--- A Crusade/Jihad has ended.
-- Exports: targetSettlement, targetRegionID, crusade
---@param eventData eventTrigger 
function onCrusadeEnds(eventData) end 

--- Called before the faction's turn starts.
-- Exports: faction, religion
---@param eventData eventTrigger 
function onPreFactionTurnStart(eventData) end 

--- Called at a faction's turn start.
-- Exports: faction, religion
---@param eventData eventTrigger 
function onFactionTurnStart(eventData) end 

--- Called after faction changes to a new capital.
-- Exports: faction, religion
---@param eventData eventTrigger 
function onFactionNewCapital(eventData) end 

--- Called at a faction's turn end.
-- Exports: faction, religion
---@param eventData eventTrigger 
function onFactionTurnEnd(eventData) end 

--- A Faction has voted for the new pope.
-- Exports: faction, religion
---@param eventData eventTrigger 
function onVotedForPope(eventData) end 

--- A Faction has been excommunicated.
-- Exports: faction, religion
---@param eventData eventTrigger 
function onFactionExcommunicated(eventData) end 

--- A Faction has formed a horde.
-- Exports: faction, religion
---@param eventData eventTrigger 
function onHordeFormed(eventData) end 

--- A cardinal has been removed from the game.
-- Exports: faction, religion
---@param eventData eventTrigger 
function onCardinalRemoved(eventData) end 

--- An inquisitor has been dispatched to a region.
-- Exports: faction, religion
---@param eventData eventTrigger 
function onInquisitorAppointed(eventData) end 

--- An assassination mission against the pope has failed and the assassin is executed.
-- Exports: faction, religion
---@param eventData eventTrigger 
function onAssassinCaughtAttackingPope(eventData) end 

--- The player has opened his finances panel.
-- Exports: faction, religion
---@param eventData eventTrigger 
function onFinancesPanelOpen(eventData) end 

--- The player has opened the faction summary panel.
-- Exports: faction, religion
---@param eventData eventTrigger 
function onFactionSummaryPanelOpen(eventData) end 

--- The player has opened the family tree panel.
-- Exports: faction, religion
---@param eventData eventTrigger 
function onFamilyTreePanelOpen(eventData) end 

--- The player has opened the diplomatic standing panel.
-- Exports: faction, religion
---@param eventData eventTrigger 
function onDiplomacyPanelOpen(eventData) end 

--- The player has attacked an army or settlement. The decision panel is now open.
-- Exports: faction, religion
---@param eventData eventTrigger 
function onPreBattlePanelOpen(eventData) end 

--- A message has arrived for the player.
-- Exports: faction, eventID, religion
---@param eventData eventTrigger 
function onIncomingMessage(eventData) end 

--- The player has opened a message.
-- Exports: faction, eventID, religion
---@param eventData eventTrigger 
function onMessageOpen(eventData) end 

--- The player has closed a message.
-- Exports: eventID
---@param eventData eventTrigger 
function onMessageClosed(eventData) end 

--- The player has declined automated settlement management.
-- Exports: faction, religion
---@param eventData eventTrigger 
function onDeclineAutomatedSettlementManagement(eventData) end 

--- The battle AI has begun processing.
-- Exports: faction, religion
---@param eventData eventTrigger 
function onBattleAiCommenced(eventData) end 

--- The delay phase has begun.
-- Exports: faction, religion
---@param eventData eventTrigger 
function onBattleDelayPhaseCommenced(eventData) end 

--- The deployment phase has begun.
-- Exports: faction, religion
---@param eventData eventTrigger 
function onBattleDeploymentPhaseCommenced(eventData) end 

--- The conflict phase has begun.
-- Exports: faction, religion
---@param eventData eventTrigger 
function onBattleConflictPhaseCommenced(eventData) end 

--- Called after a faction declares a war.
-- Exports: faction, targetFaction, religion, targetReligion
---@param eventData eventTrigger 
function onFactionWarDeclared(eventData) end 

--- Called after a faction declares an alliance.
-- Exports: faction, targetFaction, religion, targetReligion
---@param eventData eventTrigger 
function onFactionAllianceDeclared(eventData) end 

--- A marriage has occured between two factions. gets fired for both factions involved.
-- Exports: faction, targetFaction, religion, targetReligion
---@param eventData eventTrigger 
function onInterFactionMarriage(eventData) end 

--- Called after a faction makes a trade agreement.
-- Exports: faction, targetFaction, religion, targetReligion
---@param eventData eventTrigger 
function onFactionTradeAgreementMade(eventData) end 

--- A new pope has been elected.
-- Exports: faction, targetFaction, religion, targetReligion
---@param eventData eventTrigger 
function onPopeElected(eventData) end 

--- Called after a faction breaks an alliance.
-- Exports: faction, targetFaction, religion, targetReligion
---@param eventData eventTrigger 
function onFactionBreakAlliance(eventData) end 

--- A faction to faction attitude update has occurred (once every round).
-- Exports: faction, targetFaction, religion
---@param eventData eventTrigger 
function onUpdateAttitude(eventData) end 

--- A demeanour response has occured in diplomacy talks.
-- Exports: faction, targetFaction, religion, targetReligion, amount
---@param eventData eventTrigger 
function onDemeanour(eventData) end 

--- Called after a faction gives money to another faction.
-- Exports: faction, targetFaction, religion, targetReligion, amount
---@param eventData eventTrigger 
function onGiveMoney(eventData) end 

--- A player unit has attacked one of the enemies units.
-- Exports: attackingUnit, defendingUnit, playerUnit, enemyUnit
---@param eventData eventTrigger 
function onBattlePlayerUnitAttacksEnemyUnit(eventData) end 

--- An enemy unit has attacked one of the players units.
-- Exports: attackingUnit, defendingUnit, playerUnit, enemyUnit
---@param eventData eventTrigger 
function onBattleEnemyUnitAttacksPlayerUnit(eventData) end 

--- One of the player's units has gone berserk.
-- Exports: playerUnit
---@param eventData eventTrigger 
function onBattlePlayerUnitGoesBerserk(eventData) end 

--- One of the player's units has routed.
-- Exports: playerUnit
---@param eventData eventTrigger 
function onBattlePlayerUnitRouts(eventData) end 

--- A siege engine belonging to the player has been destroyed.
-- Exports: playerUnit
---@param eventData eventTrigger 
function onBattlePlayerSiegeEngineDestroyed(eventData) end 

--- A player's engine has started attacking a gate.
-- Exports: playerUnit
---@param eventData eventTrigger 
function onBattleGatesAttackedByPlayerEngine(eventData) end 

--- One of the enemy's units has gone berserk.
-- Exports: enemyUnit
---@param eventData eventTrigger 
function onBattleEnemyUnitGoesBerserk(eventData) end 

--- One of the enemy's units has routed.
-- Exports: enemyUnit
---@param eventData eventTrigger 
function onBattnemyUnitRouts(eventData) end 

--- A siege engine belonging to the enemy has been destroyed.
-- Exports: enemyUnit
---@param eventData eventTrigger 
function onBattnemySiegeEngineDestroyed(eventData) end 

--- An enemy's engine has started attacking a gate.
-- Exports: enemyUnit
---@param eventData eventTrigger 
function onBattleGatesAttackedByEnemyEngine(eventData) end 

--- When a particular disaster has just happened.
-- Exports: resourceDescription
---@param eventData eventTrigger 
function onDisaster(eventData) end 

--- An event counter has changed it's value.
-- Exports: eventCounter
---@param eventData eventTrigger 
function onEventCounter(eventData) end 

--- The last unit has been removed from a fort, agents do not count.
-- Exports: fort, faction, regionID, religion
---@param eventData eventTrigger 
function onUngarrisonedFort(eventData) end 

--- An object of the target faction has been seen by the faction.
-- Exports: faction, targetFaction, regionID, coords, religion
---@param eventData eventTrigger 
function onObjSeen(eventData) end 

--- The tile has been seen by the faction.
-- Exports: faction, regionID, coords, religion
---@param eventData eventTrigger 
function onTileSeen(eventData) end 

--- A faction to faction transgression has occurred.
-- Exports: faction, targetFaction, resourceDescription, religion, targetReligion
-- transgressions: TC_THREATEN_WAR, TC_DECLARED_WAR, TC_MINOR_ASSASSINATION_ATTEMPT, TC_BROKE_TREATY_TERMS, TC_BROKE_ALLIANCE, TC_INVASION
---@param eventData eventTrigger 
function onTransgression(eventData) end 

--- A faction to faction forgiveness has occurred.
-- Exports: faction, targetFaction, resourceDescription, religion
-- forgiveness: FC_MILITARY_ASSISTANCE, FC_OBVIOUS_BRIBE
---@param eventData eventTrigger 
function onForgiveness(eventData) end 

--- An army has taken a crusade or jihad target settlement.
-- Exports: targetSettlement, faction, targetFaction, army, regionID, targetRegionID, coords, religion, targetReligion, crusade
---@param eventData eventTrigger 
function onArmyTakesCrusadeTarget(eventData) end 

--- Units have deserted a crusade or jihad.
-- Exports: targetSettlement, faction, targetFaction, targetRegionID, religion, targetReligion, crusade
---@param eventData eventTrigger 
function onUnitsDesertCrusade(eventData) end 

--- Called every time an image is rendered for display
---@param pDevice LPDIRECT3DDEVICE9 
function draw(pDevice) end 

--- Called when ImGui backend reload fonts
function onLoadingFonts() end 

--- Called when a new campaign is started from the menu.
function onNewGameStart() end 

--- Called after the game loads various db`s (edu, etc) at startup.
function onReadGameDbsAtStart() end 

--- Called after the game loads various db`s (edu, etc) at startup.
function onGameInit() end 

--- Called on ai initialized on turn start.
---@param aiFaction aiFaction 
function onAiTurn(aiFaction) end 

--- Called on clicking the stratmap.
---@param x integer 
---@param y integer 
function onClickAtTile(x, y) end 

--- Called after loading the campaign map
function onCampaignMapLoaded() end 

--- Called on creating a new save file.
function onCreateSaveFile() end 

--- Called on loading a save file.
function onLoadSaveFile() end 

--- Called at the start of a new turn.
---@param turnNumber integer 
function onChangeTurnNum(turnNumber) end 

--- Called on select worldpkgdesc for battlemap. See https://wiki.twcenter.net/index.php?title=.worldpkgdesc_-_M2TW. M2TWEOP will ignore the return value if its group does not match the required group!
---@param selectedRecordName string 
---@param selectedRecordGroup string 
---@return string newSelectedRecordName 
function onSelectWorldpkgdesc(selectedRecordName, selectedRecordGroup) end 

--- Called on specified fortificationlevel in a siege of a settlement.
---@param siegedSettlement settlementStruct 
---@return integer overridedFortificationlevel 
---@return boolean isCastle override settlement type (siege equipment is slightly different between cities and castles of the same level)
function onfortificationlevelS(siegedSettlement) end 

--- Called on the completion of the siege (in any way, with any outcome).
---@param xCoord integer x coordinate of siege(settlement or fort)
---@param yCoord integer y coordinate of siege(settlement or fort)
function onEndSiege(xCoord, yCoord) end 

--- Called on the starting of the siege (in any way, with any outcome).
---@param xCoord integer x coordinate of siege(settlement or fort)
---@param yCoord integer y coordinate of siege(settlement or fort)
function onStartSiege(xCoord, yCoord) end 

--- Called on plugin load (at game start).
function onPluginLoad() end 

