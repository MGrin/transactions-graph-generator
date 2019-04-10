from .Transaction import Transaction
from random import randint, random
from datetime import timedelta

transactionsHeader = ['id', 'source', 'target', 'date', 'time', 'amount', 'currency']

def int2str(val):
  if val < 10: return '0' + str(val)
  return str(val)

def __updateCurrentDate(date, delays):
  return date + timedelta(days=delays['days'])

def __updateCurrentTime(time, delays):
  hval = int(time.hour) + delays['hours']
  mval = int(time.minute) + delays['minutes']
  sval = int(time.second) + delays['seconds']

  if hval < 24:
    time.replace(hour=hval)
  if mval < 60:
    time.replace(minute=mval)
  if sval < 60:
    time.replace(second=sval)

  return time

def __generateDelays():
  return {
    'days': randint(0, 4),
    'hours': randint(0, 12),
    'minutes': randint(0, 59),
    'seconds': randint(0, 59)
  }

def __generateRandomIndex(nodes, participatingIndexes):
  idx = randint(0, len(nodes) - 1)
  while idx in participatingIndexes:
    idx = randint(0, len(nodes) - 1)
  participatingIndexes.add(idx)
  return idx

def generateFlowPattern(nodes):
  delays = __generateDelays()
  transactions = []
  participatingIndexes = set()
  patternStructure = []

  currentDate = None
  currentTime = None
  
  startIdx = __generateRandomIndex(nodes, participatingIndexes)
  endIdx = __generateRandomIndex(nodes, participatingIndexes)

  totalSum = 50000 * random() + 50000 * random() # Total sum of starting transaction
  totalPayback = 0.1 * random() * totalSum # Total sum of payments to all of intermediat players

  numberOfLayers = randint(2, 6) # Magic limits, number of intermediat levels

  initialTotalPaybackPerLayer = totalPayback / numberOfLayers
  totalPaybackPerLayer = 0
  executedPayback = 0
  remainingSum = totalSum

  for layer in range(numberOfLayers):
    nodesPerLayer = randint(1, 8) # Magic limits, number of nodes per layer
    patternStructure.append([])

    if layer != numberOfLayers - 1:
      totalPaybackPerLayer -= 0.1 * random() * initialTotalPaybackPerLayer
      totalPaybackPerLayer += 0.1 * random() * totalPaybackPerLayer

      executedPayback += totalPaybackPerLayer
    else:
      totalPaybackPerLayer = totalPayback - executedPayback
    
    layerNodeFee = totalPaybackPerLayer / nodesPerLayer

    for layerNode in range(nodesPerLayer):
      rndMiddlewareIdx = __generateRandomIndex(nodes, participatingIndexes)
      patternStructure[layer].append(nodes[rndMiddlewareIdx])

    if layer == 0:
      amount = remainingSum / len(patternStructure[0])
      i = 0

      for node in patternStructure[layer]:
        t = Transaction(nodes[startIdx], node)
        t.amount = amount

        if i == 0:
          currentDate = t.date
          currentTime = t.time
        else:
          currentDate = __updateCurrentDate(currentDate, delays)
          currentTime = __updateCurrentTime(currentTime, delays)

        t.date = currentDate
        t.time = currentTime

        transactions.append(t.toRow(transactionsHeader))
        i += 1

    else:
      prevLayerLength = len(patternStructure[layer-1])
      currentLayerLength = len(patternStructure[layer])

      for sourceNode in patternStructure[layer-1]:
        for targetNode in patternStructure[layer]:
          amount = (remainingSum - totalPaybackPerLayer) / (prevLayerLength * currentLayerLength)
          t = Transaction(sourceNode, targetNode)
          t.amount = amount

          currentDate = __updateCurrentDate(currentDate, delays)
          currentTime = __updateCurrentTime(currentTime, delays)

          t.date = currentDate
          t.time = currentTime

          transactions.append(t.toRow(transactionsHeader))

      remainingSum -= totalPaybackPerLayer
  
  lastLayerLength = len(patternStructure[numberOfLayers - 1])
  for node in patternStructure[numberOfLayers - 1]:
    amount = remainingSum / lastLayerLength
    t = Transaction(node, nodes[endIdx])
    t.amount = amount
    
    currentDate = __updateCurrentDate(currentDate, delays)
    currentTime = __updateCurrentTime(currentTime, delays)

    t.date = currentDate
    t.currentTime = currentTime

    transactions.append(t.toRow(transactionsHeader))  

  return transactions
      
def generateCircularPattern(nodes):
  delays = __generateDelays()
  transactions = []
  participatingIndexes = set()

  currentDate = None
  currentTime = None
  
  startIdx = randint(0, len(nodes) - 1)
  participatingIndexes.add(startIdx)

  totalSum = 50000 * random() + 50000 * random() # Total sum of starting transaction
  totalPayback = 0.1 * random() * totalSum # Total sum of payments to all of intermediat players
  remainingSum = totalSum

  order = randint(1, 8) # Magic limits, number of intermediat levels
  prevIdx = startIdx
  initialPaybackPerStep = totalPayback / order
  stepPayback = 0

  for step in range(order):
    rndMiddlewareIdx = __generateRandomIndex(nodes, participatingIndexes)
    stepPayback += 0.1 * random() * initialPaybackPerStep
    stepPayback -= 0.1 * random() * stepPayback

    amount = remainingSum - stepPayback
    t = Transaction(nodes[prevIdx], nodes[rndMiddlewareIdx])
    t.amount = amount
    if step == 0:
      currentDate = t.date
      currentTime = t.time
    else:
      currentDate = __updateCurrentDate(currentDate, delays)
      currentTime = __updateCurrentTime(currentTime, delays)

    t.date = currentDate
    t.time = currentTime

    transactions.append(t.toRow(transactionsHeader))

    prevIdx = rndMiddlewareIdx
    remainingSum -= stepPayback

  stepPayback += 0.1 * random() * initialPaybackPerStep
  stepPayback -= 0.1 * random() * stepPayback

  amount = remainingSum - stepPayback
  t = Transaction(nodes[prevIdx], nodes[startIdx])
  t.amount = amount
  if step == 0:
    currentDate = t.date
    currentTime = t.time
  else:
    currentDate = __updateCurrentDate(currentDate, delays)
    currentTime = __updateCurrentTime(currentTime, delays)

  t.date = currentDate
  t.time = currentTime

  transactions.append(t.toRow(transactionsHeader))
  return transactions

def generateTimePattern(nodes):
  delays = __generateDelays()
  transactions = []
  participatingIndexes = set()

  currentDate = None
  currentTime = None

  startIdx = __generateRandomIndex(nodes, participatingIndexes)
  endIdx = __generateRandomIndex(nodes, participatingIndexes)

  order = randint(5, 50)
  amount = 50000 * random()

  for i in range(order):
    t = Transaction(nodes[startIdx], nodes[endIdx])
    t.amount = amount

    if i == 0:
      currentDate = t.date
      currentTime = t.time
    else:
      currentDate = __updateCurrentDate(currentDate, delays)
      currentTime = __updateCurrentTime(currentTime, delays)

    t.date = currentDate
    t.time = currentTime

    transactions.append(t.toRow(transactionsHeader))


  return transactions
