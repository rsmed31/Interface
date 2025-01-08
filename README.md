# Monitoring Agent

# Project Status


[![Pipeline Status](https://devops.telecomste.fr/printerfaceadmin/2024-25/group1/printerface/badges/main/pipeline.svg)](https://devops.telecomste.fr/printerfaceadmin/2024-25/group1/printerface/-/pipelines)
[![Coverage](https://devops.telecomste.fr/printerfaceadmin/2024-25/group1/printerface/badges/main/coverage.svg?min_good=80&min_acceptable=75)](https://devops.telecomste.fr/printerfaceadmin/2024-25/group1/printerface/-/graphs/main)



A Server Monitoring tool :
* Connecting to all the machines "to be monitored",through SSH.
* Get CPU & RAM & DISK info from these distant machines.
* Extract info from LOGs on the machines.
* Continuous delivery of the project in a Docker image.

## Usage

Run project with `make debug` and consult url in log for api doc at `/docs` or `/redoc`.

Application is running 2 threads, one for the API to expose metrics and one for collecting metrics.

## Prerequisites 

Before you continue, ensure you have met the following requirements:

* You have installed the latest version of Python, Docker
* You are using a Linux Machine. Windows is not currently supported.

## Installation

To install the project on your machine, follow the steps : 

### 1. Clone the project

Open a terminal and use the following command : 
```sh
git clone https://devops.telecomste.fr/printerfaceadmin/2024-25/group1/printerface.git 
```

### 2. Install virtual environment and dependencies

To be able to run the project, you will need a python virtual environment and some libraries used in the project. 

#### a) Virtual Environment 



#### b) Dependencies

All of the dependencies used in the project have been written in a file name `requirements.txt`. To install them, choose the directory `\printerface` in your terminal and use the command : 
```sh
pip install -r requirements.txt 
```

## Run project

### Locally 

To run the project on your machine, you first need to activate your virtual environment. Access `/printerface` and use the command : 
```sh
source env/bin/activate
```
Once you've done that, run the command : 
```sh
python3 src/main.python
```

### Using Docker

You can run the project only using Docker. Open a terminal and run the command : 

```sh
docker run -d --name printerface-container -p 80:8000 /var/logs:/app/log
```
Explanation on the command : 

* `printerface` : That's the name of the docker container
* `80` : server port
* `8000` : docker container port
* `/var/logs` : path to logs on the server
* `/app/logs` : path to logs on the docker container


