from json import dumps
from rh_crypto.bot_2022_v4 import Bot

def run():
    body = None
    status = 200

    try:
        print("Running")

        body = Bot().run()
        
        print("Run successful")
    except Exception as e:
        print("Failed to run")
        print(e)
        
        body = e.__str__()

    return {
        'statusCode': status,
        'body': dumps(body)
    }