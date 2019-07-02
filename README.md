# sam-python

SAM application test (python). 

When called, the application will return a certificate from a website

## Create template

This will create a hello world app template (python 3.7)

```bash
sam init --runtime python3.7
```

## Build

Build the application (this will package it in .<app>/build/<function_name>) along with dependancies defined in requirements.txt

Run this from the root of the directory, where the CFN template is defined

```bash
sam build
```

## Run locally

Run this from the root of the directory, where the CFN template is defined

```bash
sam local start-api
```