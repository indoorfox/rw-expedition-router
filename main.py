import re
world = []
size = True
def loadregion(abbr):
  worldfile = open('world_'+abbr.lower()+".txt",'r')
  region = []
  shelters = []
  while True:
    
    line = worldfile.readline()
    line = re.split('\n',line)[0]
    if(line == "END ROOMS"):
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
        linesplit[2] = "GATE"
      else:
        linesplit[2] = "NORMAL"
  #    print(linesplit)
      region.append(linesplit)
  while expand(shelters,region):
    pass
  return(shelters)

def expand(shelters, region):
  numsearching = 0
  for shelter in shelters:
    shelter[3] += shelter[2]
    newboundary = []
    for room in shelter[2]:
      for x in region:
        if x[0] == room:
          if x[2] == "GATE":
            gatefound = False
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
                  if adjacency != shelter:
                    for test in shelter[4]:
                      if test == adjacency[1]:
                        found = True
                        break
                    if not found:
                      shelter[4].append(adjacency[1])
                  found = True
                  break
              if found:
                break
            if not found:
              for test in newboundary:
                if test == connection:
                  found = True
                  break
              if not found:
                newboundary.append(connection)
          break
    shelter[2] = newboundary
    numsearching += len(newboundary)
  return(numsearching != 0)


#fix up all the gated connections
def worldfix(world):
  for shelter in world:
    index = -1
    for connection in shelter[4]:
      index += 1
      if connection[:5] == "GATE_":
        found = False
        for pair in world:
          pairindex = -1
          if pair == shelter:
            continue
          for match in pair[4]:
            pairindex += 1
            if match == connection:
              found = True
              pair[4][pairindex] = shelter[1]
              shelter[4][index] = pair[1]
              break
          if found:
            break
  return world      
#print world



#construct the weighted connections web
def applyweights(world, weights):
  for shelter in world:
    for region in weights:
      if region[0] == shelter[0]:
        shelter[0] = region[1]
        break
def makeweb(world, size):
  web = []
  if size:
    for shelter in world:
      node = [shelter[1],[],999999]
      for connection in shelter[4]:
        for search in world:
          if search[1]==connection:
            weight = (shelter[0] * len(shelter[3])) + (search[0]*len(search[3]))
        node[1].append([connection,weight])
      web.append(node)
  else:
    for shelter in world:
      node = [shelter[1],[],999999]
      for connection in shelter[4]:
        for search in world:
          if search[1]==connection:
            weight = (shelter[0]) + (search[0])
        node[1].append([connection,weight])
      web.append(node)
  return web


#print web
def dijkstra(web, start, target):
  Q = web[:]
  R = []
  for node in Q:
    node.append("")
    if node[0] == start:
      node[2] = 0
  while len(Q) > 0:
    min = 999999
    current = []
    for node in Q:
      if node[2] < min:
        min = node[2]
        current = node
    R.append(current)
    Q.remove(current)
    
    
    if current[0] == target:
      traceback = current
      route = []
      while True:
        route.append(traceback[0])
        if traceback[3] == "":
          return route[::-1]
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
