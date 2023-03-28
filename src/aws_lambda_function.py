from json import dumps;
from rh_crypto_bot_2022_v4 import run;

def lambda_handler():
    print("Running")

    run()
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': dumps('Hello from Lambdasz!')
    }

def main():
    lambda_handler()
