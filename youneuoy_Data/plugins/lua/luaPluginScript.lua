require('myconfigs')

-- Helper for managing persistence of tables across save/load
require('helpers/tableSave')

-- Uncomment to use EOP Helper functions
-- require('helpers/EopLuaHelpers')

-- Uncomment to use external debugger
-- require('helpers/mobdebug').start()

-- Our campaign config table.
campaignConfig = { ["someConfigValue"] = 5 };

-- Fires when loading a save file
function onLoadSaveFile(paths)
    campaignPopup = true;

    for index, path in pairs(paths) do
        if (string.find(path, "configTable.lua"))
        then
            -- Function from helper, load saved table
            campaignConfig = persistence.load(path);
        end
    end
end

-- Fires when creating a save file
-- Returns a list of M2TWEOP save files
function onCreateSaveFile()
    local savefiles = {};
    currentPath = M2TWEOP.getPluginPath();

    -- Function from helper, save our table
    persistence.store(currentPath .. "configTable.lua", campaignConfig);

    savefiles[1] = currentPath .. "configTable.lua";
    return savefiles;
end

-- Fires when the plugin is first loaded at game start or reloded with CTRL+9+1
function onPluginLoad()
    M2TWEOP.unlockGameConsoleCommands();
    -- M2TWEOP.setAncillariesLimit(8);
    -- M2TWEOP.setMaxBgSize(100);
    -- M2TWEOP.setReligionsLimit(50);
    -- M2TWEOP.setBuildingChainLimit(40);
    -- M2TWEOP.setGuildCooldown(3);
end

local maintenanceDrawCfg=
    {
        isDrawNeeded=false,
        lastCheckTime=0,
        checkInterval=1.0
    }

function onCharacterSelected(eventData)
    local selectedChar = eventData.character
	
	if distanceFromPoint(selectedChar, 4,	188) < 4 then
	    local xChar, yChar = selectedChar.character.xCoord, selectedChar.character.yCoord;
			
		selectedChar.character:reposition(505,189);
		end
		
	if distanceFromPoint(selectedChar, 4,	256) < 4 then
	    local xChar, yChar = selectedChar.character.xCoord, selectedChar.character.yCoord;
			
		selectedChar.character:reposition(505,256);
		end

	if distanceFromPoint(selectedChar, 4,	307) < 4 then
	    local xChar, yChar = selectedChar.character.xCoord, selectedChar.character.yCoord;
			
		selectedChar.character:reposition(494,304);
		end

	if distanceFromPoint(selectedChar, 506,	304) < 4 then
	    local xChar, yChar = selectedChar.character.xCoord, selectedChar.character.yCoord;
			
		selectedChar.character:reposition(15,308);
		end

	if distanceFromPoint(selectedChar, 505,	218) < 4 then
	    local xChar, yChar = selectedChar.character.xCoord, selectedChar.character.yCoord;
			
		selectedChar.character:reposition(4,218);
	end

	if distanceFromPoint(selectedChar, 505,	100) < 4 then
	    local xChar, yChar = selectedChar.character.xCoord, selectedChar.character.yCoord;
			
		selectedChar.character:reposition(4,101);
		end

	end


function distanceFromPoint(character, x, y)
  local xChar, yChar = character.character.xCoord, character.character.yCoord
  local xMax, xMin, yMax, yMin = math.max(xChar, x), math.min(xChar, x), math.max(yChar, y), math.min(yChar, y)
  local xSegment, ySegment = xMax - xMin, yMax - yMin
  local hypotenuse = math.sqrt(xSegment^2 + ySegment^2)
  return hypotenuse        
end

    ---Called after the game loads to menu. New Units
function onGameInit()
    modPath=M2TWEOP.getModPath();
	
	-- Japan (Mercenaries)
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Heimin_Mob.txt", 1000);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Heimin_Partisans.txt", 1001);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Teppotai_Merc.txt", 1002);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Shizoku.txt", 1003);
	
	-- Japan (1870s)
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Keishitai_1870.txt", 1004);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Shinsenryodan.txt", 1005);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Suzakutai_1870.txt", 1006);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Battotai.txt", 1007);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Rikuguntai_1870.txt", 1008);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Goshimpei_1870.txt", 1009);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Tondenhei_1870.txt", 1010);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Ryukihei_1870.txt", 1011);
	
	-- Miscellaneous
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/oroe/Korean_Pikemen.txt", 1012);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/oroe/Korean_Musketeers.txt", 1013);
	
	-- Japan (Mercenaries)
	M2TWEOPDU.setEntryLocalizedName(1000, "Heimin Mob")
	M2TWEOPDU.setEntryLocalizedName(1001, "Heimin Partisans")
	M2TWEOPDU.setEntryLocalizedName(1002, "Teppō Auxiliaries")
	M2TWEOPDU.setEntryLocalizedName(1003, "Shizoku")
	
	-- Japan (1870s)
	M2TWEOPDU.setEntryLocalizedName(1004, "Keishitai (1870s)")
	M2TWEOPDU.setEntryLocalizedName(1005, "Shinsenryodan")
	M2TWEOPDU.setEntryLocalizedName(1006, "Suzakutai (1870s)")
	M2TWEOPDU.setEntryLocalizedName(1007, "Battōtai")
	M2TWEOPDU.setEntryLocalizedName(1008, "Rikuguntai (1870s)")
	M2TWEOPDU.setEntryLocalizedName(1009, "Goshimpei (1870s)")
	M2TWEOPDU.setEntryLocalizedName(1010, "Tondenhei (1870s)")
	M2TWEOPDU.setEntryLocalizedName(1011, "Ryūkihei (1870s)")
	
	-- Miscellaneous
	M2TWEOPDU.setEntryLocalizedName(1012, "Joseon Pikemen")
	M2TWEOPDU.setEntryLocalizedName(1013, "Joseon Musketeers")
end
