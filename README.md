# Basic API Gateway Demo

This project deploys a lambda to AWS and sets up a get endpoint to access it.  It also deploys a DynamoDB table to use as a data source.

## Dependencies
1. Deployment bucket
This is where zipped lambdas are sent.  Create it in advance.
2. Lambda execution role.
Create this separate so that an agent can be used to deploy the project without having IAM permissions.  The role should allow your lambda to access any resources it needs.  At this basic stage just give it log and DynamoDB access.

## Deployment
```bash
ARTIFACT_BUCKET=<your_existing_bucket>
aws cloudformation package \
    --template-file template.yaml \
    --s3-bucket ${ARTIFACT_BUCKET} \
    --s3-prefix <subfolderpath>  \
    --output-template /tmp/packaged.yaml
aws cloudformation deploy \
    --capabilities CAPABILITY_IAM \
    --template-file /tmp/packaged.yaml \
    --stack-name my-API-dev
```

Check the stack exports for the API URL
```
curl ${ENDPOINT_URL}/ping
{"message": "pong", "response": {}}
```

