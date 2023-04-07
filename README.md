# rw-expedition-router
A tool for routing from one location to another in Rain World.

Currently expects all `world_[region abbreviation].txt` files to be in the same directory as main.py.
Cannot presently read modify files (and therefore does not interpret MSC changes).
Currently uses a pre-set list of weights.

Current 'to-be-implemented' features list:
-Asking for input on weights (and then normalising them before using them)
-Reading the modify files that MSC uses to change existing regions
-Actually reading the filestructure as it is on an actual machine
-Allowing a user to specify a name other than the exact room name of a given shelter as a start or end point
-Allowing the user to select which slugcat they are playing as and change the map accordingly
-Paying attention to one-way connections (This'll be a little bit tricky so don't your fingers too soon.)
-Having alternate, more descriptive names for shelters // shelter zones (like 'new player tutorial shelter' instead of 'SU_S01')
-A visual, rather than text-based interface
-Allowing a user to set by-subregion or by-shelter weights
