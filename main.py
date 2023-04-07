import re
world = []
size = True #Should the program take number of rooms into account when pathing?
def loadregion(abbr): #loads the rooms in a region, and then compacts them into shelter zones. Returns a list of shelters.
  worldfile = open('world_'+abbr.lower()+".txt",'r')
  region = []
  shelters = []
  while True:
    line = worldfile.readline()
    line = re.split('\n',line)[0]
    if(line == "END ROOMS"): #'END ROOMS' is, as expected, the end of the list of rooms. We don't want to read more data after this point in the file.
      break
    linesplit = re.split(' : ',line)
    if(len(linesplit)>=2):
      linesplit[1] = list(filter(None,re.split(', |DISCONNECTED',linesplit[1])))
      if(len(linesplit)==2):
        linesplit.append("NORMAL")
      elif(linesplit[2]=="ANCIENTSHELTER" or linesplit[2]=="SHELTER"):
        linesplit[2] = "SHELTER"
        shelter = [abbr,linesplit[0],linesplit[1],[linesplit[0]],[]]
        shelters.append(shelter)
      elif(linesplit[2]=="GATE"):
        linesplit[2] = "GATE" #This is a specific case in case I need to do something with these later.
      else:
        linesplit[2] = "NORMAL"
      region.append(linesplit)
  while expand(shelters,region): 
    pass
  worldfile.close() #Don't need this still in memory!
  return(shelters)

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
        node[1].append([connection,weight])
      web.append(node)
  else:
    for shelter in world:
      node = [shelter[1],[],999999]
      for connection in shelter[4]:
        for search in world:
          if search[1]==connection:
            weight = (shelter[0]) + (search[0]) #uses raw weights instead of modifying them by estimated length.
        node[1].append([connection,weight])
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
    
# Hardcoded weights! Change this to a user query of some kind later.
weights = [["SU",.1],["HI",.1],["CC",.25],["GW",.4],["SH",1],["SL",.4],["UW",.3],["DS",.25],["SS",.6],["LF",.7],["SB",.7],["SI",.7]]
for region in weights:
  world += loadregion(region[0])
world = worldfix(world)
applyweights(world, weights)
web = makeweb(world, size)
while True:
  found = False
  start = input("Input origin shelter name: ")
  for shelter in world:
    if start == shelter[1]:
      found = True
      break
  if found:
    break
  print("Shelter name not recognized. Please try again.\n")
while True:
  found = False
  end = input("Input destination shelter name: ")
  for shelter in world:
    if end == shelter[1]:
      found = True
      break
  if found:
    break
  print("Shelter name not recognized. Please try again.\n")
print(dijkstra(web, start,end))
