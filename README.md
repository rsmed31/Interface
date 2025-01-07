# Monitor Them
[![Coverage Status](https://devops.telecomste.fr:5050/printerfaceadmin/2024-25/group1/printerface/badges/main/coverage.svg)](https://devops.telecomste.fr:5050/printerfaceadmin/2024-25/group1/printerface/-/jobs?scope=success&name=coverage)

[![Pipeline Status](https://gitlab.com/%{project_path}/badges/%{default_branch}/pipeline.svg)]https://gitlab.com/%{project_path}/-/commits/%{default_branch})

[![pipeline status](https://devops.telecomste.fr/printerfaceadmin/2024-25/group1/printerface/badges/main/pipeline.svg)](https://devops.telecomste.fr/printerfaceadmin/2024-25/group1/printerface/-/commits/main)
[![coverage report](https://devops.telecomste.fr/printerfaceadmin/2024-25/group1/printerface/badges/main/coverage.svg)](https://devops.telecomste.fr/printerfaceadmin/2024-25/group1/printerface/-/commits/main)

[![lint status](https://devops.telecomste.fr/printerfaceadmin/2024-25/group1/printerface/badges/main/lint.svg)](https://devops.telecomste.fr/printerfaceadmin/2024-25/group1/printerface/-/pipelines?page=1&scope=all&ref=main)

A Server Monitoring tool :
* Connecting to all the machines "to be monitored",through SSH.
* Get CPU & RAM & DISK info from these distant machines.
* Extract info from LOGs on the machines.
* Continuous delivery of the project in a Docker image.

## Usage

Run project with `make debug` and consult url in log for api doc at `/docs` or `/redoc`.

Application is running 2 threads, one for the API to expose metrics and one for collecting metrics.
