# cmpe273-spring18

## Dev guide
* `docker-compose build app`
* `docker-compose up -d app`
* run test.py on local, it will hit the endpoint inside the docker container
* go to `localhost:9002` to stop/start/restart processes with code changes

## Design

* here we enforce the policy where each block will host exactly one transaction
* no rewards for mining, this blockchian is only used for evidence storage instead of a currency for investment
* blocks are daisy-chained

* endpoint to add/get a transaction to/from the blockchain
* endpoint to verify that a transaction is valid
* endpoint to verify that the chain is valid
* endpoint to sync with all nodes to get the longest chain
* endpoint to add/update/delete/get a manufacturer
* endpoint to add/update/delete/get a product

## Design choices by Haoji

* using mongodb to store transactions, each current transaction list will be one collection, currently using list, but list lives on memory and is prone to data loss
* using a linked list instead of list, we shouldn't allow moving backwards, a node should only contain information about it's next node

# References

https://hackernoon.com/blockchain-101-only-if-you-know-nothing-b883902c59f7

https://en.bitcoin.it/wiki/Help:Introduction
