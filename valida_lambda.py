import boto3  
import json    
import logging  
import sys  
  
boto_sts = boto3.client('sts')  
logging.getLogger().setLevel(logging.INFO) 
 
def create_client_with_auth(name_client, account_id):  
    sts_response = boto_sts.assume_role(  
        RoleArn="arn:aws:iam::" + account_id +":role/DevOpsRole",  
        RoleSessionName='newsession'  
    )  
    client = boto3.client(  
        name_client,  
        aws_access_key_id = sts_response["Credentials"]["AccessKeyId"],  
        aws_secret_access_key = sts_response["Credentials"]["SecretAccessKey"],  
        aws_session_token = sts_response["Credentials"]["SessionToken"]  
    )  
    return client  
  
def execution_test(path_payload=None, account_id=None):      
      
    try:  
        client = create_client_with_auth("lambda", account_id)  
        #client = boto3.client('lambda')  
          
        with open(path_payload) as myfile:  
            config = json.loads(myfile.read())  
            json_payloads = config.get('payload')
            name_lambda = config.get('nameFunction')            
            update_config_lambda(client, name_lambda, config.get('handler'), config.get('timeout'))
            inputs = json_payloads.get('input')
            outputs = json_payloads.get('output')  
            results = dict()  
            is_error = False  
            for ct_input in inputs:  
                ct_key = next(iter(ct_input))  
                response = client.invoke(  
                    FunctionName=name_lambda,  
                    InvocationType='RequestResponse',  
                    Payload=bytes(str(ct_input.get(ct_key)), 'utf-8').decode().replace("'", '"')  
                )  
                res_payload = json.loads(response.get('Payload').read())   
                is_valid = verify_output(outputs, ct_key, res_payload)  
                if is_valid:  
                    results[ct_key] = "Lambda successfully executed!"  
                else:  
                    error_message = res_payload.get('errorMessage')  
                    is_error = True 
                    if error_message is None:  
                        results[ct_key] = "Payload returned does not match expected: " + str(res_payload)  
                    else:  
                        results[ct_key] = res_payload.get('errorMessage')
            if is_error:       
                return on_failure("Lambda failure, description error: " + str(results))  
            else:  
                logging.info("Test successfully executed!" + str(results))  
                exit(0)  
  
    except Exception as e:  
        logging.error(e)  
        return on_failure("Test execution failed!")  
  
def verify_output(outputs, ct_key, output_resul):  
    for ct_output in outputs:  
        if next(iter(ct_output)) == ct_key and output_resul == ct_output.get(ct_key):  
            return True  
    return False  

def update_config_lambda(client, name_lambda, handler=None, timeout=None):
    handler = "index.handler" if handler is None else handler #set value default
    timeout = 3 if timeout is None else timeout #set value default
    client.update_function_configuration(
        FunctionName=name_lambda,
        Handler = handler,
        Timeout=timeout
    )
  
def on_failure(print_message=None):  
    if print_message:  
        logging.critical(print_message)  
    exit(1)  
  
if __name__ == '__main__':  
    execution_test(*sys.argv[1:])  