Total War Name Verifier 

by TornNight (Ely Soto)


Requires Java 1.6 or greater



What it does:
  
1. Ensures all names in descr_names.txt are also in names.txt.
  
2. Ensures all names in names.txt are also in descr_names_lookup.txt.
  3. Ensures character names in descr_strat.txt are included in descr_names.txt for the correct faction
  
4. Ensures surnames in descr_strat.txt are included in descr_names.txt for the correct faction
  
5. Ensures female names in descr_strat.txt are included in descr_names.txt for the correct faction
  
6. Checks for duplicate names in descr_strat.txt
  
7. Checks for names in names.txt not in descr_names.txt
  
8. Checks for non-standard characters in names



How to Use:
  
Put the following files in the same directory as name_verifier.exe

: 
- descr_names.txt
  
- names.txt
  
- descr_names_lookup.txt
  
- descr_strat.txt

  
Execute.



Version 1.6
	
- Corrected checks of sub_faction named characters

Version 1.5
	
- Checks for non-standard character names under Warnings.

Version 1.4
  
- Fixed issue with first names that had spaces
  
- Added check for duplicate names in descr_strat.txt
  
- Addec check for names in names.txt not in descr_names.txt

Version 1.3
  
- Corrected ignoring comments near names
  
- Increased upper limit on names to 20000 

Version 1.2
  
- Corrected Reading in UTF-16LE encoded names.txt

Version 1.1
  
- Added Verification for Surnames and Female names in names.txt
  
- Added Generation of Lookup File

Version 1.0
  Initial Release



License: Free
