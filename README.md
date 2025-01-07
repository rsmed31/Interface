# Monitoring Agent

# Project Status


[![Pipeline Status](https://devops.telecomste.fr/printerfaceadmin/2024-25/group1/printerface/badges/main/pipeline.svg)](https://devops.telecomste.fr/printerfaceadmin/2024-25/group1/printerface/-/pipelines)
[![Coverage](https://devops.telecomste.fr/printerfaceadmin/2024-25/group1/printerface/badges/main/coverage.svg)](https://devops.telecomste.fr/printerfaceadmin/2024-25/group1/printerface/-/graphs/main)
[![Lint Status](https://devops.telecomste.fr/printerfaceadmin/2024-25/group1/printerface/badges/main/job.svg?job=lint)](https://devops.telecomste.fr/printerfaceadmin/2024-25/group1/printerface/-/jobs)
[![Static Analysis Status](https://devops.telecomste.fr/printerfaceadmin/2024-25/group1/printerface/badges/main/job.svg?job=static-analysis)](https://devops.telecomste.fr/printerfaceadmin/2024-25/group1/printerface/-/jobs)



A Server Monitoring tool :
* Connecting to all the machines "to be monitored",through SSH.
* Get CPU & RAM & DISK info from these distant machines.
* Extract info from LOGs on the machines.
* Continuous delivery of the project in a Docker image.

## Usage

Run project with `make debug` and consult url in log for api doc at `/docs` or `/redoc`.

Application is running 2 threads, one for the API to expose metrics and one for collecting metrics.

Prerequisites 

Before you continue, ensure you have met the following requirements:

* You have installed the latest version of Python* 