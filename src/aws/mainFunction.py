from json import dumps
from dotenv import load_dotenv
from os import environ
from rh_crypto.bot_2022_v4 import run

def lambda_handler():
    body = None
    status = 200

    try:
        print("Running")

        body = run()
        
        print("Run successful")
    except Exception as e:
        print("Failed to run")
        print(e)
        
        body = e.__str__()

    return {
        'statusCode': status,
        'body': dumps(body)
    }

if not environ.get('AWS_LAMBDA_RUNTIME_API'):
    load_dotenv()
    lambda_handler()
