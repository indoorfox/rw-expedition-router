import re
import os
rw_data = input("Input the path to your RainWorld_Data directory (including the folder itself) : ")
reg_world = os.path.join(rw_data, "StreamingAssets", "world")
msc_world = os.path.join(rw_data, "StreamingAssets", "mods", "moreslugcats", "world")
msc_modify = os.path.join(rw_data, "StreamingAssets", "mods", "moreslugcats", "modify", "world")
world = []
size = True #Should the program take number of rooms into account when pathing?

def parseroom(room, shelters, aliases): #interprets room input as a shelter
  if 'start' in room.lower():
    room = conditional
  if 'moon' in room.lower() or 'lttm' in room.lower():
    if conditional=="Spear":
      room = "spearmoon"
    else:
      room = "moon"
  if 'pebbles' in room.lower() or 'fp' in room.lower():
    if conditional=="Saint":
      room = "saintpebbles"
    else:
      room = "pebbles"
  for name in aliases[4]:
    if name[0].lower()==room.lower():
      room = name[1]
      break
  for name in aliases[3]:
    if name[0].lower()==room.lower():
      room = name[1]
      break
  for shelter in shelters:
    for contained in shelter[3]:
      if contained==room:
        return shelter[1]
  return("NOT FOUND")

def slugcatpicker(slugcat): #takes in user input and outpits slugcat-relevant variables [list of regions, slugcat in-file name]
  weights = [["SU"], ["HI"], ["CC"], ["SI"], ["LF"], ["SB"], ["GW"], ["VS"]]
  if "surv" in slugcat.lower():
    weights += [["OE"], ["MS"], ["UW"], ["SS"], ["SH"], ["DS"], ["SL"]]
    conditional = "White"
  elif "monk" in slugcat.lower():
    weights += [["OE"], ["MS"], ["UW"], ["SS"], ["SH"], ["DS"], ["SL"]]
    conditional = "Yellow"
  elif "hunt" in slugcat.lower():
    weights += [["MS"], ["UW"], ["SS"], ["SH"], ["DS"], ["SL"]]
    conditional = "Red"
  elif "gour" in slugcat.lower():
    weights += [["OE"], ["MS"], ["UW"], ["SS"], ["SH"], ["DS"], ["SL"]]
    conditional = "Gourmand"
  elif "arti" in slugcat.lower():
    weights += [["LC"], ["LM"], ["UW"], ["SS"], ["SH"], ["DS"]]
    conditional = "Artificer"
  elif "riv" in slugcat.lower():
    weights += [["MS"], ["UW"], ["RM"], ["SH"], ["DS"], ["SL"]]
    conditional = "Rivulet"
  elif "spear" in slugcat.lower():
    weights += [["DM"], ["UW"], ["SS"], ["SH"], ["DS"], ["LM"]]
    conditional = "Spear"
  elif "saint" in slugcat.lower():
    weights += [["MS"], ["CL"], ["UG"], ["SL"], ["HR"]]
    conditional = "Saint"
  elif ("inv" in slugcat.lower()) or ("enot" in slugcat.lower()) or ("?" in slugcat.lower()):
    weights += [["OE"], ["MS"], ["UW"], ["SS"], ["SH"], ["DS"], ["SL"]]
    conditional = "Inv"
  else:
    return [[],"UNRECOGNIZED"]
  return [weights,conditional]
    
def loadregion(abbr): #loads the rooms in a region, and then compacts them into shelter zones. Returns a list of shelters.
  worldlocation = os.path.join(reg_world, abbr.lower(), "world_"+abbr.lower()+".txt")
  modify = False
  if os.path.exists(worldlocation):
    modify = True
  else:
    worldlocation = os.path.join(msc_world, abbr.lower(), "world_"+abbr.lower()+".txt")
  worldfile = open(worldlocation, 'r')
  region = []
  shelters = []
  while True:
    line = worldfile.readline()
    line = re.split('\n', line)[0]
    if(line == "END ROOMS"): #'END ROOMS' is, as expected, the end of the list of rooms. We don't want to read more data after this point in the file.
      break
    linesplit = re.split(' : ', line)
    if(len(linesplit)>=2):
      linesplit[1] = list(filter(None, re.split(', |DISCONNECTED', linesplit[1])))
      if(len(linesplit)==2):
        linesplit.append("NORMAL")
      elif(linesplit[2]=="ANCIENTSHELTER" or linesplit[2]=="SHELTER"):
        linesplit[2] = "SHELTER"
        shelter = [abbr, linesplit[0], linesplit[1], [linesplit[0]], []]
        shelters.append(shelter)
      elif(linesplit[2]=="GATE"):
        linesplit[2] = "GATE" #This is a specific case in case I need to do something with these later.
      else:
        linesplit[2] = "NORMAL"
      region.append(linesplit)
  worldfile.close() #Don't need this still in memory!
  if modify: #regions that are in the base game have a 'modify' file we'll need to interpret to get their MSC changes.
    modfile = open(os.path.join(msc_modify, abbr.lower(), "world_"+abbr.lower()+".txt"))
    test = True
    while True:
      line = re.split('\n', modfile.readline())[0]
      if test:
        if line=="ROOMS":
          test = False
          continue
        elif line == "[ENDMERGE]":
          break
        else:
          continue
      if(line == "END ROOMS"): 
        break
      linesplit = re.split(' : ', line)
      if(len(linesplit)>=2):
        linesplit[1] = list(filter(None, re.split(', |DISCONNECTED', linesplit[1])))
        if(len(linesplit)==2):
          linesplit.append("NORMAL")
        elif(linesplit[2]=="ANCIENTSHELTER" or linesplit[2]=="SHELTER"):
          linesplit[2] = "SHELTER"
          shelter = [abbr, linesplit[0], linesplit[1], [linesplit[0]], []]
          temp = False
          for room in shelters:
            if room[1]==linesplit[0]:
              room[2] = linesplit[1]
              temp = True
          if not temp:  
            shelters.append(shelter)
        elif(linesplit[2]=="GATE"):
          linesplit[2] = "GATE" 
        else:
          linesplit[2] = "NORMAL"
        for room in region: #if we already have the room, that means the modify file is just here to change its properties. Apply those.
          if room[0]==linesplit[0]:
            room[1] = linesplit[1]
            room[2] = linesplit[2]
            continue
        region.append(linesplit) #if we don't already have it, add it in.
  if modify:
    conditionalinterpret(shelters, region, os.path.join(msc_modify, abbr.lower(), "world_"+abbr.lower()+".txt"))
  else:
    conditionalinterpret(shelters, region, os.path.join(msc_world, abbr.lower(), "world_"+abbr.lower()+".txt"))
  while expand(shelters, region): 
    pass
  return(shelters)

def loadaliases(): #loads the aliases file into memory.
  aliasfile = open("names.txt", 'r')
  step = ""
  REGIONS = []
  SAINTREGIONS = []
  INVREGIONS = []
  SHELTERS = []
  ROOMS = []
  while True:
    line = re.split('\n', aliasfile.readline())[0]
    if step=="":
      step = re.split(':', line)[0]
      continue
    if step=="END NAMES":
      break
    if line=="":
      step = line
      continue
    linesplit = re.split(' - ', line)
    locals()[step].append(linesplit)
  return[REGIONS, SAINTREGIONS, INVREGIONS, SHELTERS, ROOMS]
      

def conditionalinterpret(shelters, region, fileloc): #interprets the 'conditional links' section of the MSC files.
  file = open(fileloc, mode='r')
  test = True
  while True:
    line = re.split('\n', file.readline())[0]
    if test:
      if line=="CONDITIONAL LINKS":
        test= False
        continue
      elif line=="[ENDMERGE]" or line=="CREATURES":
        break
      else:
        continue
    if line=="END CONDITIONAL LINKS":
      break
    linesplit = re.split(' : ',line)
    if len(linesplit) >= 2:
      if linesplit[1]=="EXCLUSIVEROOM":
        if not conditional==linesplit[0]:
          for shelter in shelters:
            if shelter[1]==linesplit[2]:
              shelters.remove(shelter)
          for room in region:
            if room[0]==linesplit[2]:
              region.remove(room)
      if linesplit[0]==conditional:
        if linesplit[1]=="HIDEROOM":
          for shelter in shelters:
            if shelter[1]==linesplit[2]:
              shelters.remove(shelter)
          for room in region:
            if room[0]==linesplit[2]:
              region.remove(room)
        else:
          if linesplit[2].isnumeric():
            for room in region:
              if room[0]==linesplit[1]:
                room[1].append(linesplit[3])
          else:
            for room in region:
              if room[0]==linesplit[1]:
                for connection in room[1]:
                  if connection==linesplit[2]:
                    room[1].remove(linesplit[2])
                if not linesplit[3]=="DISCONNECTED":
                  room[1].append(linesplit[3])
  return

def expand(shelters, region): #expands the search boundary for each shelter zone. Returns false once no more shelters have room to expand.
  numsearching = 0
  for shelter in shelters:
    shelter[3] += shelter[2] #rooms on the periphery get contained *first*, so that if they're next to eachother they don't cause any weirdness.
    newboundary = []
    for room in shelter[2]: 
      for x in region:
        if x[0] == room:
          if x[2] == "GATE": #We have to keep track of the gates so we can stitch together the regions later.
            gatefound = False #We don't want to mark the same gate twice, though.
            for test in shelter[4]:
              if test == room:
                gatefound = True
                break
            if not gatefound:
              shelter[4].append(room)
          for connection in x[1]: 
            found = False
            for adjacency in shelters:
              for contained in adjacency[3]:
                if contained == connection: 
                  if adjacency != shelter: #we don't want to have shelter zones considering themselves self-connected, that'll make our pathing gross later.
                    for test in shelter[4]:
                      if test == adjacency[1]: #we also don't want duplicate connections now, that'll make things *super* gross.
                        found = True
                        break
                    if not found:
                      shelter[4].append(adjacency[1])
                  found = True
                  break
              if found:
                break
            if not found:
              for test in newboundary: #don't put it in the search list twice.
                if test == connection:
                  found = True
                  break
              if not found:
                newboundary.append(connection)
          break
    shelter[2] = newboundary
    numsearching += len(newboundary) #keeping track of how many rooms are in the next iteration so we don't have to go through any empty ones.
  return(numsearching != 0)

def worldfix(world): #stitches together the regions by connecting the shelters that share a gate.
  for shelter in world:
    index = -1
    for connection in shelter[4]:
      index += 1
      if connection[:5] == "GATE_": #gates are always of the format 'GATE_[region]_[region]', so we can save time by not having to look for the gate flag in the room list.
        found = False
        for pair in world:
          pairindex = -1
          if pair == shelter:
            continue
          for match in pair[4]:
            pairindex += 1
            if match == connection:
              found = True
              pair[4][pairindex] = shelter[1] #have to do this this way because just doing match = shelter[1] doesn't actually modify it properly
              shelter[4][index] = pair[1]
              break
          if found:
            break
  return world      

def applyweights(world, weights): #replaces region names in the shelter list with the weight applied to that region.
  for shelter in world:
    for region in weights:
      if region[0] == shelter[0]:
        shelter[0] = region[1]
        break

def makeweb(world, size): #prepares the web of connected shelters for use with Dijkstra's algorithm, including setting estimated distance to 999999 (roughly infinity)
  web = []
  if size:
    for shelter in world:
      node = [shelter[1],[],999999]
      for connection in shelter[4]:
        for search in world:
          if search[1]==connection:
            weight = (shelter[0] * len(shelter[3])) + (search[0]*len(search[3])) #uses number of rooms in a shelter zone as a rough estimate of how long it'll take to travel through it.
        node[1].append([connection, weight])
      web.append(node)
  else:
    for shelter in world:
      node = [shelter[1],[],999999]
      for connection in shelter[4]:
        for search in world:
          if search[1]==connection:
            weight = (shelter[0]) + (search[0]) #uses raw weights instead of modifying them by estimated length.
        node[1].append([connection, weight])
      web.append(node)
  return web

def dijkstra(web, start, target): #runs Dijstra's algorithm to connect a given start shelter to a given end shelter.
  Q = web[:]
  R = []
  for node in Q:
    node.append("")
    if node[0] == start:
      node[2] = 0
  while len(Q) > 0:
    min = 999999 #starts at the same 'roughly infinite' that we used earlier.
    current = []
    for node in Q:
      if node[2] < min:
        min = node[2]
        current = node
    if current == []:
      print("Sorry, that route doesn't seem to be possible!")
      return []
    R.append(current) #removes it from the list of unsearched and saves it in our searched list so we can use it for traceback later.
    Q.remove(current) 
    
    if current[0] == target:
      traceback = current
      route = []
      while True:
        route.append(traceback[0])
        if traceback[3] == "":
          return route[::-1] #if we didn't do this little trick it would print a route from destination to origin instead of origin to destination.
        for node in R:
          if node[0] == traceback[3]:
            traceback = node
    
    for neighbor in current[1]:
      for node in Q:
        if neighbor[0] == node[0]:
          alt = current[2] + neighbor[1]
          if node[2] > alt:
            node[2] = alt
            node[3] = current[0]
          break
        
weights = [["SU", .1], ["HI", .1], ["CC", .25], ["GW", .4], ["SH", 1], ["SL", .4], ["UW", .3], ["DS", .25], ["SS", .6], ["LF", .7], ["SB", .7], ["SI", .7], ["OE", .6], ["RM", .9], ["DM", .5], ["MS", 1], ["CL", .5], ["HR", .3], ["LC", .5], ["LM", .4], ["UG", .5], ["VS", .6]] #weights in here are 'defaults' although that's not actually implemented
conditional = ""
aliases = loadaliases()
while True:
  world = []
  while True:
    slugcat = input("Which slugcat are you playing as?")
    temp = slugcatpicker(slugcat)
    weights = temp[0]
    conditional = temp[1]
    if conditional == "UNRECOGNIZED":
      print("Sorry, I don't recognize that slugcat.")
    else:
      break
  for region in weights:
    world += loadregion(region[0])
    if conditional=="Saint":
      for name in aliases[1]:
        if region[0]==name[0]:
          regionname = name[1]
          break
    elif conditional=="Inv":
      for name in aliases[2]:
        if region[0]==name[0]:
          regionname = name[1]
          break
    else:
      for name in aliases[0]:
        if region[0]==name[0]:
          regionname = name[1]
          break
    while True:
      temp = input("Please input a difficulty value for "+regionname+": ")
      if temp.isnumeric():
        region.append(float(temp))
        break
      else:
        print("That's not a number!")
  world = worldfix(world)
  applyweights(world, weights)
  web = makeweb(world, size)
  while True:
    found = False
    start = input("Input origin room name: ")
    start = parseroom(start, world, aliases)
    if not start=="NOT FOUND":
      break
    print("Could not resolve room name. Please try again.\n")
  while True:
    found = False
    end = input("Input destination room name: ")
    end = parseroom(end, world, aliases)
    if not end=="NOT FOUND":
      break
    print("Could not resolve room name. Please try again.\n")
  print(dijkstra(web, start, end))
  if input("type QUIT to exit: ") == "QUIT":
    break
