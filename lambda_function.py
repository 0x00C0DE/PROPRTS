import sys
from os import environ

sys.path.insert(0, './src')

def is_local():
    return not environ.get('AWS_LAMBDA_RUNTIME_API')

# DO NOT IMPORT THIRD-PARTY LIBRARIES BEFORE THIS LINE.
if is_local():
    sys.path.insert(0, './python-local/lib/python3.9/site-packages')
else:
    sys.path.insert(0, './python-aws/lib/python3.9/site-packages')


from proprts.main_proto_v2 import CryptoBot
from json import dumps  # noqa: E402
from dotenv import load_dotenv  # noqa: E402
from proprts.main_proto_v1 import runBot  # noqa: E402
from scheduler import Scheduler  # noqa: E402

def lambda_handler(event, context):
    print('Lambda handler')

    scheduler = Scheduler()
    cryptobot = CryptoBot()
    if scheduler.should_run:
        scheduler.start(cryptobot.)
    else:
        return runBot()

def run():
    body = None
    status = 200

    try:
        print('Running')

        body = run()
        
        print('Run successful')
    except Exception as e:
        print('Failed to run')
        print(e)
        
        status = 500
        body = e.__str__()

    if is_local():
        print(body)
    else:
        return {
            'statusCode': status,
            'body': dumps(body)
        }

if is_local():
    load_dotenv()
    lambda_handler(None, None)
