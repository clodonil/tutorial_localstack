import json


def my_lambda(event, context):
   valor = event['numero']
   result = int(valor) % 2 == 0
   msg = {"message" : "Hello, World!!!", "result" : result}
   return json.dumps(msg)
