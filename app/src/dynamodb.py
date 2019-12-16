import boto3
import logging

def conn_dynamodb(table):
    try:
        dydb = boto3.resource('dynamodb',endpoint_url="http://localhost:4570")
        table = dydb.Table(table)
        return table
    except:
        print("Problema na conexao com DynamoDB")
        return False

def dynamodb_save(table,dados,new):
    retorno= {'ResponseMetadata': {'HTTPStatusCode' : 300 }}
    try:
        retorno=table.put_item(Item=dados)
    except botocore.exceptions.ClientError as e:
        print(e)

    if retorno['ResponseMetadata']['HTTPStatusCode'] == 200:
        logging.info(f"Dados Salvo: {dados}")
        return True
    else:
        return False

table = conn_dynamodb('teste3')
dados = {'id':'user1','detail':{'end':'sdfsdfsd'}}
retorno = dynamodb_save(table,dados, True)
dyretorno  = table.scan()
print(dyretorno)