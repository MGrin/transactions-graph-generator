import os
import threading
from models.Client import Client
from models.Company import Company
from models.ATM import ATM
from .utils import writeBatch, log

clientHeaders = ['id', 'first_name', 'last_name', 'age', 'email', 'occupation', 'political_views', 'nationality', 'university', 'academic_degree', 'address', 'postal_code', 'country', 'city']
companyHeaders = ['id', 'type', 'name', 'country']
atmHeaders = ['id', 'latitude', 'longitude']

def __generateModel(count, file, header, Model, modelname, batchSize, verbose=True):
	try:
		os.remove(file)
	except OSError:
		pass

	with open(file, 'a') as file:
		batch = []

		file.write('|'.join(header) + '\n')
		for i in range(0, count):
			c = Model()
			batch.append(c.toRow(header))

			if verbose and i % batchSize == 0:
				log(str(i) + ' ' + modelname + ' of ' + str(count) + ' are generated')

			if len(batch) > batchSize:
				writeBatch(file, batch)
				batch = []

		writeBatch(file, batch)
		log('TOTAL ' + modelname + ' of ' + str(count) + ' are generated')

def generateNodes(files, counts, batchSize):
	clientsProcess = threading.Thread(target=lambda : __generateModel(
		counts["client"],
		files["client"],
		header=clientHeaders,
		Model=Client,
		modelname='Client',
		batchSize=batchSize
	))
	companiesProcess = threading.Thread(target=lambda : __generateModel(
		counts["company"],
		files["company"],
		header=companyHeaders,
		Model=Company,
		modelname='Company',
		batchSize=batchSize
	))
	atmsProcess = threading.Thread(target=lambda : __generateModel(
		counts["atm"],
		files["atm"],
		header=atmHeaders,
		Model=ATM,
		modelname='ATM',
		batchSize=batchSize
	))

	clientsProcess.start()
	companiesProcess.start()
	atmsProcess.start()

	clientsProcess.join()
	companiesProcess.join()
	atmsProcess.join()
