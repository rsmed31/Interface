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

* You have installed the latest version of Python
* You are using a Linux Machine. 

## Installation

To install the project on your machine, follow the steps : 

### 1. Clone the project

Open a terminal and use the following command : **_git clone https://devops.telecomste.fr/printerfaceadmin/2024-25/group1/printerface.git_** 

### 2. Install virtual environment and dependencies

To be able to run the project, you will need a python virtual environment and some libraries used in the project. 

#### a) Virtual Environment 



#### b) Dependencies

All of the dependencies used in the project have been written in a file name 'requirements.txt'. To install them, choose the directory \printerface and use the command : **_pip install -r requirements.txt_**

## Run project


