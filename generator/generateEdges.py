import csv
import os
import multiprocessing as mp
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

	clientClientEdgesProcess = mp.Process(target=__generateEdges, args=(
		clients,
		clients,
		files['clients-clients-edges'],
		probs[0],
		batchSize,
		"client->client"))

	clientCompanyEdgesProcess = mp.Process(target=__generateEdges, args=(
		clients,
		companies,
		files['clients-companies-edges'],
		probs[1],
		batchSize,
		"client->company"))

	companyClientEdgesProcess = mp.Process(target=__generateEdges, args=(
		companies,
		clients,
		files['companies-clients-edges'],
		probs[2],
		batchSize,
		'company->client'
	))

	clientClientEdgesProcess.start()
	clientCompanyEdgesProcess.start()
	companyClientEdgesProcess.start()

	clientClientEdgesProcess.join()
	clientCompanyEdgesProcess.join()
	companyClientEdgesProcess.join()
