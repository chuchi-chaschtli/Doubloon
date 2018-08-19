## Doubloon
Open-source blockchain protocol written using Python3, wrapped by Flask, a robust web-app framework.

### About
Doubloon is a fairly standard proof-of-work blockchain protocol. It is not built to be a production cryptocurrency, but more of a self-educational and fun personal project. As such, it has been built to maximize efficiency and maintainability, not scalability.

Doubloon implements several deterrals to deny various service abuses. It features proof-of-work as its underlying protocol for mining, with RSA key validation to verify block transactions. Block transactions are authorized using a consensus algorithm. Again, this project is simple - consensus is determined by chain length.

### Usage
Usage is fairly straightforward.
* Clone the project
* From the project dir, simply run\
`python3 src/app.py`
    * You can specify the host and port with which to run the app on using `-H [url]` and `-p [port]`, respectively.
* To run the unit tests, simply run\
`python3 tests/tester.py`

### Read more
[What is Blockchain Technology?](https://blockgeeks.com/guides/what-is-blockchain-technology/)\
[What is Flask?](https://github.com/pallets/flask)

### To-Do
- [x] Proof of Work implementation
- [x] Consensus Algorithm
- [x] Transaction Validation
- [ ] More robust Wallet support
- [ ] Client

### Contributing
This is a personal project. As such, I'm not looking for contributions at this time. Feel more than welcome to fork the repo though :)