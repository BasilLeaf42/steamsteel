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

    ---Called after the game loads to menu.
-- function onGameInit()
    -- modPath=M2TWEOP.getModPath();
-- end

-- Add new units here!
function onReadGameDbsAtStart()
	-- log_always("--- onReadGameDbsAtStart ---");
	modPath = M2TWEOP.getModPath();

	-- Japan (Mercenaries)
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Heimin_Mob.txt", 1000);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Heimin_Partisans.txt", 1001);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Heimin_Partisans_Geberu.txt", 1002);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Heimin_Partisans_Minieru.txt", 1003);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Teppotai_Merc.txt", 1004);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Shizoku.txt", 1005);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Ainu_Archers.txt", 1006);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Ainu_Teppo.txt", 1007);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Ainu_Geberu.txt", 1008);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Ainu_Minieru.txt", 1009);
	
	-- Japan (1860s)
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Shogitai.txt", 1010);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Byakkotai.txt", 1011);
		
	-- Japan (1870s)
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Battotai.txt", 1012);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Keishitai_1870.txt", 1013);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Shinsenryodan.txt", 1014);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Suzakutai_1870.txt", 1015);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Rikuguntai_1870.txt", 1016);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Rikusentai_1870.txt", 1017);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Kaiso_Shinsengumi.txt", 1018);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Goshimpei_1870.txt", 1019);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Denshutai_1870.txt", 1020);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Tondenhei_1870.txt", 1021);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Hoppo_Keibitai_1870.txt", 1022);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Goshimpei_Hohei_1870.txt", 1023);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Ryukihei_1870.txt", 1024);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Ryukihei_Shogun_1870.txt", 1025);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Goshimpei_Kihei_1870.txt", 1026);
	
	-- Japan (1880s)
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Rikuguntai_1880.txt", 1027);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Ezo_Rikuguntai_1880.txt", 1028);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Denshutai_1880.txt", 1029);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Goshimpei_1880.txt", 1030);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Tondenhei_1880.txt", 1031);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Goshimpei_Hohei_1880.txt", 1032);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Hoppo_Keibitai_1880.txt", 1033);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Ryukihei_1880.txt", 1034);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Goshimpei_Kihei_1880.txt", 1035);
	
	-- Japan (1890s)
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Rikuguntai_1890.txt", 1036);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Ezo_Rikuguntai_1890.txt", 1037);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Goshimpei_1890.txt", 1038);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Hokuchin_Butai_1890.txt", 1039);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Ryukihei_1890.txt", 1040);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Goshimpei_Kihei_1890.txt", 1041);
	
	-- Japan (1900s)
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Rikuguntai_1900.txt", 1050);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Rikuguntai_1905.txt", 1051);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Ezo_Rikuguntai_1900.txt", 1052);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Ezo_Rikuguntai_1905.txt", 1053);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Goshimpei_1900.txt", 1054);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Goshimpei_1905.txt", 1055);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Hokuchin_Butai_1900.txt", 1056);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Hokuchin_Butai_1905.txt", 1057);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Ryukihei_1900.txt", 1058);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Ryukihei_1905.txt", 1059);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Goshimpei_Kihei_1900.txt", 1060);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Goshimpei_Kihei_1905.txt", 1061);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Koheitai_1900.txt", 1062);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Koheitai_1905.txt", 1063);
	
	-- Japan (Unique generals)
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Tokugawa_Yoshinobu.txt", 1080);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Kondo_Isami.txt", 1081);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Hijikata_Toshizo.txt", 1082);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Matsudaira_Katamori.txt", 1083);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Saigo_Takamori_1860.txt", 1084);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Itagaki_Taisuke.txt", 1085);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/japan/Japan_Sakamoto_Ryoma.txt", 1086);
	
	-- Qing
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/qing/Qing_Tiger_Warriors.txt", 1100);
	
	-- Korea / Joseon (1860s to 1870s)
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/korea/Korean_Pikemen.txt", 1101);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/korea/Korean_Musketeers.txt", 1102);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/korea/Korean_Gimagungsu.txt", 1103);
	
	-- Korea / Joseon (1880s)
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/korea/Korean_Byeolgigun.txt", 1104);
	
	-- Korea / Empire of Korea (1890s to 1900s)
	
	-- Ethiopia / Sudan
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/africa/Ethiopia_Sudanese_Warriors.txt", 1200);
	M2TWEOPDU.addEopEduEntryFromFile(modPath.."/data/unit_limit/africa/Ethiopia_Sudanese_Musketeers.txt", 1201);
	
	
end
