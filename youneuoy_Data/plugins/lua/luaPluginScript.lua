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
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/eopData/unitlimit/japan_test.txt", 1000);
	
	M2TWEOPDU.setEntryLocalizedName(1000, "Test Unit")
end