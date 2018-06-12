# Basic API Gateway Demo Project

This branch only deploys a lambda

## Deployment
```
ARTIFACT_BUCKET=<your_existing_bucket>
aws cloudformation package --template-file template.yaml --s3-bucket $ARTIFACT_BUCKET --s3-prefix <subfolderpath>  --output-template /tmp/packaged.yaml
aws cloudformation deploy --template-file /tmp/packaged.yaml --capabilities CAPABILITY_IAM --stack-name my-lambda-stack
```
