@ECHO OFF
SET MTW= "data"
SET M2TW= "data\text"
SET MTW3= "data\menu\symbols"
SET M4TW= "data\ui"
SET M7TW= "data\world\maps"
xcopy %MTW%\tow_steamsteel %MTW%\ /r /y /q
xcopy %MTW%\menu\menu_steamsteel %MTW%\menu /r /y /q
xcopy %MTW%\loading_screen\load_steamsteel %MTW%\loading_screen /r /y /q
xcopy %MTW%\banners\textures\banners_steamsteel %MTW%\banners\textures /r /y /q
xcopy %MTW3%\fe_buttons_24_steamsteel %MTW3%\fe_buttons_24 /r /y /q
xcopy %MTW3%\fe_buttons_48_steamsteel %MTW3%\fe_buttons_48 /r /y /q
xcopy %MTW3%\fe_faction_units_steamsteel %MTW3%\fe_faction_units /r /y /q
xcopy %M4TW%\faction_symbols\faction_symbols_steamsteel %M4TW%\faction_symbols /r /y /q
xcopy %M2TW%\text_steamsteel %M2TW%\ /r /y /q
xcopy %M7TW%\map_steamsteel %M7TW%\base /r /y /q
xcopy %M7TW%\campaign\camp_steamsteel %M7TW%\campaign\imperial_campaign /r /y /q
ECHO Launching
"M2TWEOP GUI.exe"
