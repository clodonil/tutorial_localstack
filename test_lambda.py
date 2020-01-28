import lambda_function
import json


def test_validate_message():
    event = '10'
    retorno = json.loads(lambda_function.my_lambda(event))
    assert retorno['message'] == 'Hello, World!!!'
    assert retorno['result'] == True
