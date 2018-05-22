# Basic API Gateway Demo Project

This project deploys a lambda to AWS and sets up a get endpoint to access it.  It also deploys a dynamodb table to use as a datasource.

## Dependecies
1. Deployment bucket
This is where zipped lambdas are sent.  Create it in advance.
2. Lambda execution role.
Create this seperate so that an agent can be used to deploy the project without having IAM permissions.  The role should allow your lambda to access any resources it needs.  At this basic stage just give it log and dynamodb access.

## Deployment
```
ARTIFACT_BUCKET=<your_existing_bucket>
aws cloudformation package --template-file template.yaml --s3-bucket $ARTIFACT_BUCKET --s3-prefix <subfolderpath>  --output-template /tmp/led-packaged.yaml
aws cloudformation deploy --template-file /tmp/led-packaged.yaml --stack-name my-API-dev
```

Check the stack exports for the API URL
```
curl ${ENDPOINT_URL}/bet/ping
{"message": "pong", "response": {}}
```
