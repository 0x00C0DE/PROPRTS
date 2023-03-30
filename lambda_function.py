import json
import sys
from os import environ

sys.path.insert(0, "./src")

print(environ.get('AWS_LAMBDA_RUNTIME_API'))
print(not environ.get('AWS_LAMBDA_RUNTIME_API'))

def is_local():
    return not environ.get('AWS_LAMBDA_RUNTIME_API')


if is_local():
    sys.path.insert(0, "./python-local/lib/python3.9/site-packages")
else:
    sys.path.insert(0, "./python-local/lib/python3.9/site-packages")

from aws.mainFunction import run
from dotenv import load_dotenv

def lambda_handler(event, context):
    print('Lambda handler')

    run()

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from IRV LOCAL')
    }

if is_local():
    load_dotenv()
    lambda_handler(None, None)
