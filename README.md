# sam-python

SAM application test (python). This readme is essentially just a summary of what is already [covered by AWS](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-quick-start.html). The notes are just a summary for my own reference.

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

Run this from the root of the directory, where the CFN template is defined. This will start an HTTP server which will listen on port 3000 to mimic an API gateway.

```bash
sam local start-api
```

## Package the Application

This will zip the application and save it to s3. This needs to be in the same region as where the SAM resources will be deployed. In my example, this will be eu-west-1, to one of my own personal buckets:

```bash
# If you need to, create a new bucket
aws s3 mb s3://snowco-sam-eu-west-1

# Package the application to the bucket
sam package --output-template-file packaged.yaml --s3-bucket snowco-sam-eu-west-1
```

This will create a new file, `packaged.yaml` in the root of your project directory and will package the application as a zip and store in s3 with a hash(?) of the application, eg `6dc94d8800f18ccee45fac149e07fbbb`. 

The `packaged.yaml` file is used to deploy the application to the cloud. It's almost identical to the `template.yaml` file that was created with the `sam init` command, except it contains the location of the s3 + file when the `sam package` command was run.

The package is all the contents of your application, along with any dependencies. 

## Deploy the Application

Run the following command to deploy the application, using the template defined in `packaged.yaml`.

```bash
sam deploy \
    --template-file packaged.yaml \
    --stack-name sam-python \
    --capabilities CAPABILITY_IAM \
    --region eu-west-1
```

The URL for the API gateway is returned as an output to the CFN stack which we can retrieve using the following command:

```bash
aws cloudformation describe-stacks \
    --stack-name sam-python \
    --query 'Stacks[].Outputs[?OutputKey == `ReturnCertExpiry`].OutputValue[]' --output=text 
```

To test the actual endpoint in a single command:

```bash
curl $(aws cloudformation describe-stacks --stack-name sam-python --query 'Stacks[].Outputs[?OutputKey == `ReturnCertExpiry`].OutputValue[]' --output=text )/certchecker
```
