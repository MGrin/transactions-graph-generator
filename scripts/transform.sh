#!/bin/bash

rm output/{atms,clients,companies,transactions}.csv

echo "id,source,target,date,time,amount,currency" >> output/transactions.csv

perl -MList::Util=shuffle -e 'print shuffle(<STDIN>);' < data/nodes.transactions.patterns.circular.csv >> output/transactions.csv
perl -MList::Util=shuffle -e 'print shuffle(<STDIN>);' < data/nodes.transactions.patterns.flow.csv >> output/transactions.csv
cat data/nodes.transactions.client-sourcing.csv >> output/transactions.csv
perl -MList::Util=shuffle -e 'print shuffle(<STDIN>);' < data/nodes.transactions.company-sourcing.csv >> output/transactions.csv
perl -MList::Util=shuffle -e 'print shuffle(<STDIN>);' < data/nodes.transactions.patterns.time.csv >> output/transactions.csv

cp data/nodes.atms.csv output/atms.csv
cp data/nodes.clients.csv output/clients.csv
cp data/nodes.companies.csv output/companies.csv
