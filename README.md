# Basic API Gateway Demo

This project deploys a lambda to AWS and sets up a get endpoint to access it.  It also deploys a DynamoDB table to use as a data source.

## Dependencies
1. Deployment bucket
This is where zipped lambdas are sent.  Create it in advance.

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
```bash
curl ${ENDPOINT_URL}/ping
{"message":"Unauthorized"}
```

## Authenticated access

To access this method, the `IdToken` from an Authenticated Cognito client is required.

### Create a user
Go to the UserPool's hosted login page and create and verify a new user.  If in doubt see [Using the Hosted UI](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-app-integration.html) or [my cognito walkthrough](http://timelson.com/posts/apig/api-gateway3/)

### Get and Use the Auth Token

*I use an ipython shell here to simplify JSON parsing*

```ipython
In [5]: !curl $ENDPOINT_URL/ping
{"message":"Unauthorized"}

In [6]: cognito_idp = session.client('cognito-idp')         # or use boto3.client

In [7]: idToken = cognito_idp.initiate_auth(
    ...:     AuthFlow='USER_PASSWORD_AUTH',
    ...:     AuthParameters={
    ...:         'USERNAME': 'testuser0@gmail.com',
    ...:         'PASSWORD': 'Password12',
    ...:     },
    ...:     ClientId='3vnkpvi180nrmd44h4gnoj8cs4',  # App client WITHOUT 'App client secret'
    ...: )['AuthenticationResult']['IdToken']

In [8]: !curl $ENDPOINT_URL/ping -H "Authorization:$idToken"
{"message": "pong", "response": {}}
```

