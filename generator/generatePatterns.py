import csv
import threading
import os
from math import ceil
from random import random
from .utils import writeBatch, log
from models.Patterns import generateFlowPattern, generateCircularPattern, generateTimePattern

transactionHeaders = ['id', 'source', 'target', 'date', 'time', 'amount', 'currency']

def __generatePatterns(nodes, counts, transactionsFile, batchSize, patternsGenerator, label):
	try:
		os.remove(transactionsFile)
	except OSError:
		pass

	totalNumberOfPatterns = 0
	totalNumberOfTransactions = 0

	numberOfPatterns = ceil(0.1 * random() * counts['client'])
	# numberOfPatterns = 1

	log(label + ': Number of patterns to be generated: ' + str(numberOfPatterns))

	with open(transactionsFile, 'a') as transactions:
		batch = []

		# transactions.write('|'.join(transactionHeaders) + '\n')
		for i in range(numberOfPatterns):
			batch += patternsGenerator(nodes)

			totalNumberOfPatterns += 3
			totalNumberOfTransactions += len(batch)

			if len(batch) > batchSize:
				writeBatch(transactions, batch)
				batch = []
				log(label + ': Generated ' + str(totalNumberOfPatterns) + ' patterns with ' + str(totalNumberOfTransactions) + ' transactions in total')

		if len(batch) != 0:
			writeBatch(transactions, batch)

		log(label + ': TOTAL Generated ' + str(totalNumberOfPatterns) + ' patterns with ' + str(totalNumberOfTransactions) + ' transactions in total')


def generatePatterns(files, counts, batchSize):
	print("Reading nodes in memory")
	nodes = []

	with open(files['client'], 'r') as f:
		reader = csv.reader(f, delimiter="|")
		next(reader)
		log("Loading clients...")
		for row in reader:
			nodes.append(row[0])

	with open(files['company'], 'r') as f:
		reader = csv.reader(f, delimiter="|")
		next(reader)
		log("Loading companies...")
		for row in reader:
			nodes.append(row[0])

	# with open(files['atm'], 'r') as f:
	# 	reader = csv.reader(f)
	# 	next(reader)
	# 	log("Loading atms...")
	# 	for row in reader:
	# 		atms.add(row[0])
	flow = threading.Thread(target = lambda: __generatePatterns(
		nodes,
		counts,
		files['flow-pattern-transactions'],
		batchSize,
		generateFlowPattern,
		label='Flow patterns'
	))

	circular = threading.Thread(target = lambda: __generatePatterns(
		nodes,
		counts,
		files['circular-pattern-transactions'],
		batchSize,
		generateCircularPattern,
		label='Circular patterns'
	))

	time = threading.Thread(target = lambda: __generatePatterns(
		nodes,
		counts,
		files['time-pattern-transactions'],
		batchSize,
		generateTimePattern,
		label='Time patterns'
	))

	flow.start()
	circular.start()
	time.start()

	flow.join()
	circular.join()
	time.join()