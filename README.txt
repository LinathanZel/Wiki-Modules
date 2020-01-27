##############
### README ###
##############

Important Files that you open:
1) Main_buffMultiGenerator.py
2) Main_buffSingleGenerator.py
3) Main_DBBGenerator.py

Important Files that you don't open:
1) buffGenerator.py
2) dbbGenerator.py

####################
### DESCRIPTIONS ###
####################

Note: All of the "Main_" files have an Update button, which will update the local datamine to the latest revision on Deathmax's GitHub.

1) Main_buffMultiGenerator.py

This program generates the entire page of the specified template.

For example, generating page with the Fire element, 5-star, and Super Brave Burst settings will output the entire page you copy-paste into "Template:BuffList SBB Fire 5"

2) Main_buffSingleGenerator.py

This program generates the UnitBuffList template of the unit inputted into the program.

Accepted inputs include the unit's ID and the full name. For example, "Spirit Conjurer Astrid" and "820438" are both acceptable inputs.

There is also a dropdown list including Brave Burst, Super Brave Burst, and Ultimate Brave Burst.

3) Main_DBBGenerator.py

This program generates the copy-pastable that is incorporated into the DBB wiki template. For an example on how the program's copy-pastable should be ported over, please take a look at Utheria and Gilgamesh's DBB (https://bravefrontierglobal.fandom.com/wiki/Absolute_Photon_Slash)

Accepted inputs include the unit's ID and the full name. For example, "Spirit Conjurer Astrid" and "820438" are both acceptable inputs.

4) buffGenerator.py

This is the library responsible for parsing buffs used by Main_buffSingleGenerator.py and Main_buffMultiGenerator.py. Do not touch this file.

5) dbbGenerator.py

This is the library responsible for parsing buffs used by Main_DBBGenerator. Do not touch this file.