ECHO OFF
CLS
COLOR 0
:LOOP
ECHO        --- Steam and Steel Menu ---
ECHO   Type letter of the campaign you want to play
ECHO -----------------------------------
ECHO World Campaign 
ECHO  A = Steam and Steel Main Campaign
ECHO  B = Clockwork Empires                                   
ECHO -----------------------------------
ECHO Central Asia Campaign 
ECHO  C = The Great Game
ECHO -----------------------------------
ECHO South America Campaign 
ECHO  D = Future of Our Liberty
ECHO -----------------------------------
ECHO North America Campaign 
ECHO  E = Civil War
ECHO -----------------------------------
ECHO Africa Campaign 
ECHO  F = The Scramble for Africa
ECHO -----------------------------------
ECHO Europe Campaign 
ECHO  G = European Steel
ECHO -----------------------------------
ECHO South East Asia Campaign 
ECHO  H = Oriental Empires
ECHO -----------------------------------
ECHO  0 = Continue Campaign
:: SET /P prompts for input and sets the variable
:: to whatever the user types
SET MTW= "data"
SET M2TW= "data\text"
SET MTW3= "data\menu\symbols"
SET M4TW= "data\ui"
SET M7TW= "data\world\maps"
SET Choice=
SET /P Choice=Type campaign Number or Letter and press 'Enter'  
:: The syntax in the next line extracts the substring
:: starting at 0 (the beginning) and 1 character long
IF NOT '%Choice%'=='' SET Choice=%Choice:~0,1%
ECHO.
:: /I makes the IF comparison case-insensitive
IF /I '%Choice%'=='A' GOTO Item1
IF /I '%Choice%'=='B' GOTO Item2
IF /I '%Choice%'=='C' GOTO Item3
IF /I '%Choice%'=='D' GOTO Item4
IF /I '%Choice%'=='E' GOTO Item5
IF /I '%Choice%'=='F' GOTO Item6
IF /I '%Choice%'=='G' GOTO Item7
IF /I '%Choice%'=='H' GOTO Item8
IF /I '%Choice%'=='0' GOTO Start
ECHO "%Choice%" is not valid. Please try again.
ECHO.
GOTO Loop
:Item1
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
GOTO Start
:Item2
xcopy %MTW%\tow_althis %MTW%\ /r /y /q
xcopy %MTW%\menu\menu_althis %MTW%\menu /r /y /q
xcopy %MTW%\loading_screen\load_steamsteel %MTW%\loading_screen /r /y /q
xcopy %MTW%\banners\banners_steamsteel %MTW%\banners /r /y /q
xcopy %MTW3%\fe_buttons_24_steamsteel %MTW3%\fe_buttons_24 /r /y /q
xcopy %MTW3%\fe_buttons_48_steamsteel %MTW3%\fe_buttons_48 /r /y /q
xcopy %MTW3%\fe_faction_units_steamsteel %MTW3%\fe_faction_units /r /y /q
xcopy %M4TW%\faction_symbols\faction_symbols_steamsteel %M4TW%\faction_symbols /r /y /q
xcopy %M2TW%\text_althis %M2TW%\ /r /y /q
xcopy %M7TW%\map_steamsteel %M7TW%\base /r /y /q
xcopy %M7TW%\campaign\camp_steamsteel %M7TW%\campaign\imperial_campaign /r /y /q
GOTO Start
:Item3
xcopy %MTW%\menu\menu_greatgame %MTW%\menu /r /y /q
xcopy %MTW%\loading_screen\load_greatgame %MTW%\loading_screen /r /y /q
xcopy %MTW%\banners\banners_greatgame %MTW%\banners /r /y /q
xcopy %MTW%\tow_greatgame %MTW%\ /r /y /q
xcopy %MTW3%\fe_buttons_24_greatgame %MTW3%\fe_buttons_24 /r /y /q
xcopy %MTW3%\fe_buttons_48_greatgame %MTW3%\fe_buttons_48 /r /y /q
xcopy %MTW3%\fe_faction_units_greatgame %MTW3%\fe_faction_units /r /y /q
xcopy %M4TW%\faction_symbols\faction_symbols_greatgame %M4TW%\faction_symbols /r /y /q
xcopy %M2TW%\text_greatgame %M2TW%\ /r /y /q
xcopy %M7TW%\map_greatgame %M7TW%\base /r /y /q
xcopy %M7TW%\campaign\camp_greatgame %M7TW%\campaign\imperial_campaign /r /y /q
GOTO Start
:Item4
xcopy %MTW%\menu\menu_samerica %MTW%\menu /r /y /q
xcopy %MTW%\loading_screen\load_samerica %MTW%\loading_screen /r /y /q
xcopy %MTW%\banners\banners_samerica %MTW%\banners /r /y /q
xcopy %MTW%\tow_samerica %MTW%\ /r /y /q
xcopy %MTW3%\fe_buttons_24_samerica %MTW3%\fe_buttons_24 /r /y /q
xcopy %MTW3%\fe_buttons_48_samerica %MTW3%\fe_buttons_48 /r /y /q
xcopy %MTW3%\fe_faction_units_samerica %MTW3%\fe_faction_units /r /y /q
xcopy %M4TW%\faction_symbols\faction_symbols_samerica %M4TW%\faction_symbols /r /y /q
xcopy %M2TW%\text_samerica %M2TW%\ /r /y /q
xcopy %M7TW%\map_samerica %M7TW%\base /r /y /q
xcopy %M7TW%\campaign\camp_samerica %M7TW%\campaign\imperial_campaign /r /y /q
GOTO Start
:Item5
xcopy %MTW%\menu\menu_civilwar %MTW%\menu /r /y /q
xcopy %MTW%\loading_screen\load_civilwar %MTW%\loading_screen /r /y /q
xcopy %MTW%\banners\banners_civilwar %MTW%\banners /r /y /q
xcopy %MTW%\tow_civilwar %MTW%\ /r /y /q
xcopy %MTW3%\fe_buttons_24_civilwar %MTW3%\fe_buttons_24 /r /y /q
xcopy %MTW3%\fe_buttons_48_civilwar %MTW3%\fe_buttons_48 /r /y /q
xcopy %MTW3%\fe_faction_units_civilwar %MTW3%\fe_faction_units /r /y /q
xcopy %M4TW%\faction_symbols\faction_symbols_civilwar %M4TW%\faction_symbols /r /y /q
xcopy %M2TW%\text_civilwar %M2TW%\ /r /y /q
xcopy %M7TW%\map_civilwar %M7TW%\base /r /y /q
xcopy %M7TW%\campaign\camp_civilwar %M7TW%\campaign\imperial_campaign /r /y /q
GOTO Start
:Item6
xcopy %MTW%\menu\menu_scramble %MTW%\menu /r /y /q
xcopy %MTW%\loading_screen\load_scramble %MTW%\loading_screen /r /y /q
xcopy %MTW%\banners\banners_scramble %MTW%\banners /r /y /q
xcopy %MTW%\tow_scramble %MTW%\ /r /y /q
xcopy %MTW3%\fe_buttons_24_scramble %MTW3%\fe_buttons_24 /r /y /q
xcopy %MTW3%\fe_buttons_48_scramble %MTW3%\fe_buttons_48 /r /y /q
xcopy %MTW3%\fe_faction_units_scramble %MTW3%\fe_faction_units /r /y /q
xcopy %M4TW%\faction_symbols\faction_symbols_scramble %M4TW%\faction_symbols /r /y /q
xcopy %M2TW%\text_scramble %M2TW%\ /r /y /q
xcopy %M7TW%\map_scramble %M7TW%\base /r /y /q
xcopy %M7TW%\campaign\camp_scramble %M7TW%\campaign\imperial_campaign /r /y /q
GOTO Start
:Item7
xcopy %MTW%\menu\menu_europe %MTW%\menu /r /y /q
xcopy %MTW%\loading_screen\load_europe %MTW%\loading_screen /r /y /q
xcopy %MTW%\banners\textures\banners_europe %MTW%\banners\textures /r /y /q
xcopy %MTW%\tow_europe %MTW%\ /r /y /q
xcopy %MTW3%\fe_buttons_24_europe %MTW3%\fe_buttons_24 /r /y /q
xcopy %MTW3%\fe_buttons_48_europe %MTW3%\fe_buttons_48 /r /y /q
xcopy %MTW3%\fe_faction_units_europe %MTW3%\fe_faction_units /r /y /q
xcopy %M4TW%\faction_symbols\faction_symbols_europe %M4TW%\faction_symbols /r /y /q
xcopy %M2TW%\text_europe %M2TW%\ /r /y /q
xcopy %M7TW%\map_europe %M7TW%\base /r /y /q
xcopy %M7TW%\campaign\camp_europe %M7TW%\campaign\imperial_campaign /r /y /q
GOTO Start
:Item8
xcopy %MTW%\menu\menu_sea %MTW%\menu /r /y /q
xcopy %MTW%\loading_screen\load_sea %MTW%\loading_screen /r /y /q
xcopy %MTW%\banners\banners_sea %MTW%\banners /r /y /q
xcopy %MTW%\tow_sea %MTW%\ /r /y /q
xcopy %MTW3%\fe_buttons_24_sea %MTW3%\fe_buttons_24 /r /y /q
xcopy %MTW3%\fe_buttons_48_sea %MTW3%\fe_buttons_48 /r /y /q
xcopy %MTW3%\fe_faction_units_sea %MTW3%\fe_faction_units /r /y /q
xcopy %M4TW%\faction_symbols\faction_symbols_sea %M4TW%\faction_symbols /r /y /q
xcopy %M2TW%\text_sea %M2TW%\ /r /y /q
xcopy %M7TW%\map_sea %M7TW%\base /r /y /q
xcopy %M7TW%\campaign\camp_sea %M7TW%\campaign\imperial_campaign /r /y /q
GOTO Start
:Start
cd ..\..
IF EXIST kingdoms.exe (start kingdoms.exe @%0\..\steamsteel.cfg) ELSE (
IF EXIST medieval2.exe (
start medieval2.exe @%0\..\steamsteel.cfg) ELSE (
    echo ERROR: Cannot find the M2TW or Kingdoms executable.
    echo Steam and Steel may be installed into the wrong folder.
  )
)
--io.file_first
:End
exit
