# rw-expedition-router
A tool for routing from one location to another in Rain World.

Currently expects to be placed in your `RainWorld_Data` directory.
Cannot presently read modify files (and therefore does not interpret MSC changes).
Currently requires shelter names to be exactly as they appear in the game's files.

Asks for a list of 'difficulty' values, one for each region, to weight decisions, and then asks for a starting and ending shelter name.
Then it outputs a list of shelters to pass by to get from the given starting shelter to the given ending shelter in the 'easiest' way.

Current 'to-be-implemented' features list:

- Asking for input on weights (and then normalising them before using them) [DONE]
- Reading the modify files that MSC uses to change existing regions
- Actually reading the filestructure as it is on an actual machine [DONE]
- Allowing a user to specify a name other than the exact room name of a given shelter as a start or end point
- Allowing the user to select which slugcat they are playing as and change the map accordingly
- Paying attention to one-way connections (This'll be a little bit tricky so don't your fingers too soon.)
- Having alternate, more descriptive names for shelters // shelter zones (like 'new player tutorial shelter' instead of 'SU_S01')
- A visual, rather than text-based interface
- Allowing a user to set by-subregion or by-shelter weights
