# TRANSACTIONS-GRAPH-GENERATOR
`Before starting, please manually create folders data, output and logs in the root of the repo`

[Medium](https://medium.com/@mgrin/how-to-generate-a-huge-financial-graph-with-money-laundering-patterns-5c3e490dd683) article.

A big graph generator for transactions graph. As output you'll get:
* a csv with transactions
* 3 csv, one for clients, one for companies, one for ATMs, containing information about nodes of the graph

Also generates some patterns inside the graph (FLow, Circle, Time patterns)

Theoretically supports generation of any sized graph (kind of optimized, but not tested on graph more than 100000 nodes and > 10^9 transactions)

# How to use
## Installation
* You'll need `pipenv` installed
* `pipenv install`
* `mkdir -p data output logs`

## Config-less
```
pipenv run python generateGraph.py 100
```
Will generate a graph with 100 clients, 1 ATM and 2 companies.  Number of transactions is following a given distribution (look code to know more)

## Config-full
All configurations are described in `generateGraph.py` file
```
pipenv run python generateGraph.py --data=./myOwnFolder --probs=0.01,0.001,0.03,0.005 --steps=nodes,edges,transactions,patterns --batch-size=5000 10000
```
* `--data` : folder to store generated data
* `--probs` : list of connection creation probabilities. Format: client-client,client-company,client-atm,company-client
* `--steps` : Steps to do. possible values (comma - separated): nodes, edges, transactions, patterns. Should be ordered (transaction swill not be generated before edges, for example)
* `--batch-size` : While generating, data is written to disk by batches of given size. An element in a batch is a line in CSV file. Also, batch size controls frequency of logs. More batch size is more memory you need (will be used to store generated data) but should work faster (in theory, not in practice :))

# Transformation scripts
There is a number of transformation scripts that transform generated data into something more usefull:

* `./scripts/output2csv.sh` - shuffles all transactions and concats them into one file. As a result you'll get 4 csv files with atms, clients, companies and transactions
* `./scripts/output2neo4j.sh` - generates folders and files needed for neo4j to import data. Also can start a neo4j docker image with already imported graph
* `./scripts/output2postgres.sh` - generates csv files using `output2csv.sh` script. Also can start a postgres docker image with imported data
* `./scripts/output2orientdb.sh` - generates folders and files needed for orientdb to import data. Also can start an orientdb docker image with already imported data

# Data and Patterns
## Client
* id
* first_name
* last_name
* age
* email
* occupation
* political_views
* nationality
* university
* academic_degree
* address
* postal_code
* country
* city

## Company
* id
* type
* name
* country

## ATM
* id
* latitude
* longitude

## Transaction
* id
* source (points by ID to other node types)
* target (points by ID to other node types)
* date
* time
* amount
* currency

## Patterns
There are 3 types of pattern generated:
### Flow
Money starts from node A, goes through K levels, with K_N nodes on each level, and comes to a node B without a small sum payed to all network participants for their "work". Parameners:
* K (number of layers): randint(2, 6)
* K_N (number of nodes on layer K): randint(1, 8)
* Total payback (payed to intermediate nodes): 0.1 * random() * totalSum

So `TOTAL_SUM` exits from NodeA and `TOTAL_SUM * (1 - 0.1 * random())` comes to NodeB.

All transactions between layers are delayed by a random time (not that random, like between couple of seconds and couple of days)
### Circular
Money starts from node A, goes through N nodes one by one and comes back to node A without a small sum payed to all network participants for their "work". Parameters:
* N (number of nodes in the circle): randint(1, 8)
* Total payback (payed to intermediate nodes): 0.1 * random() * totalSum

Again, transactions are delayed

### Time
Exactly same amount goes from node A to node B multiple times separated by T equal time intervals. Parameters:
* T (number of time intervals): randint(5, 50)
