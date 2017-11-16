# TRANSACTIONS-GRAPH-GENERATOR

A big graph generator for transactions graph. As output you'll get:
* a csv with transactions
* 3 csv, one for clients, one for companies, one for ATMs, containing information about nodes of the graph

Also generates some patterns inside the graph (FLow, Circle, Time patterns)

Theoretically supports generation of any sized graph (kind of optimized, but not tested n graph more than 100000 nodes and > 10^9 transactions)

# Resulting files structure
The generator outputs its result to the data folder (can be changed using parameters). These are different files with data from different steps.
To merge these files into 4 well defined csv, you have to run the transformation script from `scripts` folder:
```
./scripts/transform.sh
```

# How to use
## Config-less
```
./generateGraph 100

./sctipts/transform.sh
```
Will generate a graph with 100 clients, 1 ATM and 2 companies.  Number of transactions is following a given distribution (look code to know more)

## Config-full
All configurations are described in `generateGraph.py` file
```
./generateGraph --data=./myOwnFolder --props=0.01,0.001,0.03,0.005 --steps=nodes,edges,transactions,patterns --batch-size=5000 10000

./scripts/transform.sh
```
* `--data` : folder to store generated data
* `--props` : list of connection creation probabilities. Format: client-client,client-company,client-atm,company-client
* `--steps` : Steps to do. possible values (comma - separated): nodes, edges, transactions, patterns. Should be ordered (transaction swill not be generated before edges, for example)
* `--batch-size` : While generating, data is written to disk by batches of given size. An element in a batch is a line in CSV file. Also, batch size controls frequency of logs. More batch size is more memory you need (will be used to store generated data) but should work faster (in theory, not in practice :))