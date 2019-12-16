import json

def handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps('Lambda executada com Sucesso!!!')
    }
