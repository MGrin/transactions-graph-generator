import csv
import os
import threading
import math
from random import random
from .utils import writeBatch, log

def __transactionCount():
	y = random()
	return math.ceil((-10/4) * math.log(y))
	
def __generateEdges(sourceNodes, targetNodes, outputFile, connectionProbability, batchSize, label=''):
	try:
		os.remove(outputFile)
	except OSError:
		pass

	totalNumberOfEdges = 0
	with open(outputFile, 'a') as file:
		batch = []
		sourceNodesCount = 0

		for sourceNode in sourceNodes:
			sourceNodesCount += 1
			edgesOutOfSourceNode = [sourceNode, {}]

			if sourceNodesCount % batchSize == 1:
				log(label + ': Source node number ' + str(sourceNodesCount) + ', number of edges: ' + str(totalNumberOfEdges))

			for targetNode in targetNodes:
				if sourceNode == targetNode: continue
				
				if random() < connectionProbability:
					connectionsNumber = __transactionCount()
					edgesOutOfSourceNode[1][targetNode] = connectionsNumber
					totalNumberOfEdges += 1

			edgesOutOfSourceNode[1] = '"' + str(edgesOutOfSourceNode[1]) + '"'
			batch.append('|'.join(edgesOutOfSourceNode))

			if (len(batch) > batchSize):
				writeBatch(file, batch)
				batch = []

		writeBatch(file, batch)
		log(label + ' ### TOTAL number of edges ' + str(totalNumberOfEdges))

def generateEdges(files, probs, batchSize):
	print("Reading nodes in memory")
	clients = set()
	companies = set()
	atms = set()

	with open(files['client'], 'r') as f:
		reader = csv.reader(f, delimiter="|")
		next(reader)
		log("Loading clients...")
		for row in reader:
			clients.add(row[0])

	with open(files['company'], 'r') as f:
		reader = csv.reader(f, delimiter="|")
		next(reader)
		log("Loading companies...")
		for row in reader:
			companies.add(row[0])

	with open(files['atm'], 'r') as f:
		reader = csv.reader(f, delimiter="|")
		next(reader)
		log("Loading atms...")
		for row in reader:
			atms.add(row[0])

	clientClientEdgesProcess = threading.Thread(target=lambda: __generateEdges(
		clients,
		clients,
		files['clients-clients-edges'],
		probs[0],
		batchSize,
		label='client->client'
	))
	clientCompanyEdgesProcess = threading.Thread(target=lambda: __generateEdges(
		clients,
		companies,
		files['clients-companies-edges'],
		probs[1],
		batchSize,
		label='client->company'
	))
	clientAtmEdgesProcess = threading.Thread(target=lambda: __generateEdges(
		clients,
		atms,
		files['clients-atms-edges'],
		probs[2],
		batchSize,
		label='client->atm'
	))
	comapnyClientEdgesProcess = threading.Thread(target=lambda: __generateEdges(
		companies,
		clients,
		files['companies-clients-edges'],
		probs[3],
		batchSize,
		label='company->client'
	))

	clientClientEdgesProcess.start()
	clientCompanyEdgesProcess.start()
	clientAtmEdgesProcess.start()
	comapnyClientEdgesProcess.start()

	clientClientEdgesProcess.join()
	clientCompanyEdgesProcess.join()
	clientAtmEdgesProcess.join()
	comapnyClientEdgesProcess.join()
