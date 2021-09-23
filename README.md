# Basic API Gateway Demo

This project deploys a lambda to AWS and sets up a get endpoint to access it.  It also deploys a DynamoDB table to use as a data source.

## Dependencies
1. Deployment bucket
This is where zipped lambdas are sent.  Create it in advance.
2. Lambda execution role.
Create this separate so that an agent can be used to deploy the project without having IAM permissions.  The role should allow your lambda to access any resources it needs.  At this basic stage just give it log and DynamoDB access.

## Deployment
```bash
aws --profile personal s3 ls
ARTIFACT_BUCKET=telson-lambda-bucket2
STACKNAME='apidemo'
aws --profile personal cloudformation package \
    --template-file template.yaml \
    --s3-bucket ${ARTIFACT_BUCKET} \
    --s3-prefix ${STACKNAME}  \
    --output-template /tmp/packaged.yaml
aws --profile personal cloudformation deploy \
    --capabilities CAPABILITY_IAM \
    --template-file /tmp/packaged.yaml \
    --stack-name ${STACKNAME}
    
aws --profile personal --output text cloudformation describe-stack-events \
     --stack-name ${STACKNAME} --max-items 50 | grep FAILED

```


Check the stack exports for the API URL and see the template output in action.
```
ENDPOINT_URL=$(aws --profile personal cloudformation list-exports --output text \
    --query 'Exports[?Name==`apidemo-Endpoint`].Value') 
echo $ENDPOINT_URL
curl ${ENDPOINT_URL}/ping/toto -sSL -D - 
curl ${ENDPOINT_URL}/ping/200 -sSL -D - 
curl ${ENDPOINT_URL}/ping/201 -sSL -D - 
curl ${ENDPOINT_URL}/ping/404 -sSL -D - 
```

Delete the stack
```
aws --profile personal cloudformation delete-stack --stack-name $STACKNAME
```
