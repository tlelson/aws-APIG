# Lambda Layers

In the past, we used to install pip packages locally and bomb the dynamically linked libs into `/opt`.  Now we can better organise packages by using layers and ensure all compiled resources are present.  It also gets around the lambda package size limit of 50MB.

## Building Specialty Layer

```
docker run -it -v $(pwd -P):/opt --workdir="/opt"  --entrypoint=/bin/bash amazonlinux:2017.03
```

First install python3 and pip then install layer packages with:
```
pip install --no-deps -r requirements.txt -t python/
```


## Deployment
Set environment variables
```python
os.environ['ARTIFACT_BUCKET']='<you_bucket>'
```
OR:
```bash
ARTIFACT_BUCKET=<you_bucket>
```

Then deploy the whole lot
```bash
aws cloudformation package \
    --template-file template.yaml \
    --s3-bucket ${ARTIFACT_BUCKET} \
    --s3-prefix LambdaLayersDemo \
    --output-template /tmp/packaged.yaml
aws cloudformation deploy \
    --capabilities CAPABILITY_IAM \
    --template-file /tmp/packaged.yaml \
    --stack-name LambdaLayersDemoStack
```


## Invocation

```python
FunctionARN = '<get_lambda_arn_from_exports>'

import boto3
import json
lam = boto3.Session().client('lambda')

lam.invoke(
    FunctionName=FunctionARN,
    InvocationType='RequestResponse',
    LogType='Tail',
    Payload=json.dumps({'transactions': [2,4,6,8]}),
)['Payload'].read()


# prints: b'[1, 3, 5, 7]'

```
