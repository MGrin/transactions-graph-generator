import os
import multiprocessing as mp
from models.Client import Client
from models.Company import Company
from models.ATM import ATM
from .utils import writeBatch, log

clientHeaders = ['id']
companyHeaders = ['id']
#atmHeaders = ['id', 'latitude', 'longitude']

def __generateModel(count, file, header, Model, modelname, batchSize, verbose=True):
	try:
		os.remove(file)
	except OSError:
		pass

	with open(file, 'a') as file:
		batch = []

		file.write('|'.join(header) + '\n')
		for i in range(0, count):
			c = Model(i)
			batch.append(c.toRow(header))

			if verbose and i % batchSize == 0:
				log(str(i) + ' ' + modelname + ' of ' + str(count) + ' are generated')

			if len(batch) > batchSize:
				writeBatch(file, batch)
				batch = []

		writeBatch(file, batch)
		log('TOTAL ' + modelname + ' of ' + str(count) + ' are generated')

def generateNodes(files, counts, batchSize):
	clientsProcess = mp.Process(target=__generateModel, args=(
		counts["client"],
		files["client"],
		clientHeaders,
		Client,
		'Client',
		batchSize,
		True
	))
	companiesProcess = mp.Process(target=__generateModel, args=(
		counts["company"],
		files["company"],
		companyHeaders,
		Company,
		'Company',
		batchSize,
		True
	))

	clientsProcess.start()
	companiesProcess.start()

	clientsProcess.join()
	companiesProcess.join()
