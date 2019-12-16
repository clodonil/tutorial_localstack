# Desenvolvendo para Cloud AWS localmente com LocalStack

[LocalStack](https://github.com/localstack/localstack) é uma ferramenta que fornece toda estrutura necessário para o desenvolvimento local de aplicações para a Cloud. 
Ele gera um ambiente local que fornece a mesma funcionalidade e APIs que o ambiente real da Cloud AWS.   

Dessa forma podemos executar funções em Lambda, armazenar dados em tabelas do DynamoDB, enviar eventos da fila SQS, alocar aplicações atrás de API Gateway e muito mais.

E tudo isso acontece na sua máquina local, sem nunca falar com a Cloud, economizando com o ambiente de teste. 

O cliclo de desenvolvimento de uma aplicação para a Cloud utilizando o LocalStack é a seguinte:

1. O desenvolvimento é realizado inteiramente na máquina local do desenvolveder, utilizando as APIs do LocalStack;
2. O código é frequentemente enviado para um repositório de SCM como o `Git` para integração  contínua que executa os testes automatizados
O LocalStack provisiona todos os recursos "da Cloud" necessários no ambiente do servidor de integração contínua.
3. Após todos os testes estarem finalizados com sucesso, o próximo passo é realizar o deploy no ambiente real na Cloud AWS.

Uma das vantagens de usar o LocalStack tanto no desenvolvimento como nos testes integrados é a possibilidade de simular erros que acontecem frequentemente no ambiente real da Cloud.
Por exemplo, podemos aumentar taxa de transferência de leitura/gravação do DynamoDB ou Kinesis até a geração da 
exceção `ProvisionedThroughputExceededException` pelo Kinesis ou DynamoDB 

Os resources atualmente disponibilizados na versão gratuita do LocalStack são:

|  Resources   | EndPoint             |
|-------------|--------------|
| API Gateway | http://localhost:4567|
| Kinesis | http://localhost:4568|
| DynamoDB | http://localhost:4569|
| DynamoDB Streams | http://localhost:4570|
| Elasticsearch | http://localhost:4571|
| S3 | http://localhost:4572|
| Firehose | http://localhost:4573|
| Lambda | http://localhost:4574|
| SNS | http://localhost:4575|
| SQS | http://localhost:4576|
| Redshift | http://localhost:4577|
| Elasticsearch | http://localhost:4578|
| SES | http://localhost:4579|
| Route53 | http://localhost:4580|
| CloudFormation | http://localhost:4581|
| CloudWatch | http://localhost:4582|
| SSM | http://localhost:4583|
| SecretsManager | http://localhost:4584|
| StepFunctions | http://localhost:4585|
| CloudWatch Logs | http://localhost:4586|
| CloudWatch Events | http://localhost:4587|
| STS | http://localhost:4592|
| IAM | http://localhost:4593|
| EC2 | http://localhost:4597|


# Instalação

Podemos realizar a instalação do  [LocalStack](https://github.com/localstack/localstack) de duas formas.

A primeira é utilizando o `pip` do Python. Não recomendo essa opção devido as necessidade de atender multiplas dependências. 
  
```
$ pip install localstack
```
O recomendado é utilizar container por ser muito mais simples e ser facil integração. Nesse laboratório estou utilizando o `podman` para executar o container. 

```
$ podman run -it  -p 4567-4599:4567-4599 -p 8080:8080 localstack/localstack
```

Se você tiver `docker`, pode usar o `docker-composer`.

```
ersion: '2.1'
services:
...
  localstack:
    image: localstack/localstack
    ports:
      - "4567-4584:4567-4584"
      - "${PORT_WEB_UI-8080}:${PORT_WEB_UI-8080}"
    environment:
      - SERVICES=${SERVICES- }
      - DEBUG=${DEBUG- }
      - DATA_DIR=${DATA_DIR- }
      - PORT_WEB_UI=${PORT_WEB_UI- }
      - LAMBDA_EXECUTOR=${LAMBDA_EXECUTOR- }
      - KINESIS_ERROR_PROBABILITY=${KINESIS_ERROR_PROBABILITY- }
      - DOCKER_HOST=unix:///var/run/docker.sock
    volumes:
      - "${TMPDIR:-/tmp/localstack}:/tmp/localstack"
```

Uma interface do `Admin Web Ui` é acessivel através do `http://localhost:8080`.

# Tutorial de Uso

Nesse tutorial vamos ver como utilizar o LocalStack. Vamos analisar os principais resources disponiveis, entrentado a utilização nao é diferente do uso do 'AWS CLI'. 

## Recurso: S3
http://localhost:4572

Criar um novo Bucket com o nome `Bucket-localstack`
```
$ aws --endpoint-url=http://localhost:4572 s3 mb s3://bucket-localstack
```

Listando todos os bucket.

```
$ aws  --endpoint-url=http://localhost:4572 s3 ls
```

Copiando o arquivo para o bucket

```
$ aws  --endpoint-url=http://localhost:4572 s3 cp index.html s3://bucket-localstack
```

Removendo o bucket

```
$ aws  --endpoint-url=http://localhost:4572 s3 rb s3://bucket-localstack --force
```

## Recurso: SQS
http://localhost:4576

Criando uma fila SQS

```
$ aws --endpoint-url=http://localhost:4576 sqs create-queue --queue-name fila-localstack 
```

```
$ aws --endpoint-url=http://localhost:4576 sqs get-queue-attributes --queue-url http://localhost:4576/queue/fila-localstack --attribute-names All
```

Enviando mensagem para a fila

```
$ aws --endpoint-url=http://localhost:4576 sqs send-message --queue-url  http://localhost:4576/queue/fila-localstack --message-body "Validando o localstack"
```
Lendo a mensagem da fila

```
$ aws --endpoint-url=http://localhost:4576 sqs receive-message --queue-url http://localhost:4576/queue/fila-localstack
```

## Recurso: SNS

http://localhost:4575

Criando um novo tópico.

```
$ aws --endpoint-url=http://localhost:4575  sns create-topic --name topic-localstack
```

Para assinar um tópico

```
aws --endpoint-url=http://localhost:4575 sns subscribe --topic-arn arn:aws:sns:us-east-1:000000000000:topic-localstack --protocol email --notification-endpoint clodonil@nisled.org
```

```
aws --endpoint-url=http://localhost:4575 sns subscribe --topic-arn arn:aws:sns:us-east-1:000000000000:topic-localstack --protocol sqs --notification-endpoint arn:aws:sqs:us-east-1:000000000000:fila-localstack
```

Publicar em um tópico

```
$ aws --endpoint-url=http://localhost:4575 sns publish --topic-arn arn:aws:sns:us-east-1:000000000000:topic-localstack --message "Hello World!"
```

Lista as subscrição

```
$ aws --endpoint-url=http://localhost:4575 sns list-subscriptions
```

Listando os tópicos:

```
$ aws --endpoint-url=http://localhost:4575 sns list-topics
```


## Recurso: IAM
http://localhost:4593


```
$ aws --endpoint-url=http://localhost:4593 iam list-roles
```
```
$ aws --endpoint-url=http://localhost:4593 iam list-policie
```

```
$ aws --endpoint-url=http://localhost:4593 iam create-group --group-name localstackgroup
```

```
$ aws --endpoint-url=http://localhost:4593 iam create-user --user-name localstack-user
```

```
$ aws --endpoint-url=http://localhost:4593 iam add-user-to-group --user-name localstack-user --group-name localstackgroup
```

```
$ aws --endpoint-url=http://localhost:4593 iam get-group --group-name localstackgroup
```
 
``` 
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "SpecificTable",
            "Effect": "Allow",
            "Action": [
                "dynamodb:BatchGet*",
                "dynamodb:DescribeStream",
                "dynamodb:DescribeTable",
                "dynamodb:Get*",
                "dynamodb:Query",
                "dynamodb:Scan",
                "dynamodb:BatchWrite*",
                "dynamodb:CreateTable",
                "dynamodb:Delete*",
                "dynamodb:Update*",
                "dynamodb:PutItem"
            ],
            "Resource": "arn:aws:dynamodb:*:*:table/MyTable"
        }
    ]
}
```

```
$ aws --endpoint-url=http://localhost:4593 iam create-policy --policy-name my-policy --policy-document file://policy_dynamodb.json
```

    
## Recurso: Route53
http://localhost:4580

```
$ aws --endpoint-url=http://localhost:4580 route53 create-hosted-zone --name localstack.corp --caller-reference 2014-04-01-18:47 --hosted-zone-config Comment="command-line version"
```

```
$ aws --endpoint-url=http://localhost:4580 route53 change-resource-record-sets --hosted-zone-id /hostedzone/Z3TUCH569WK9YCQ --change-batch file://sample.json
```

```
$ aws --endpoint-url=http://localhost:4580 route53  get-change --id //change/C2682N5HXP0BZ4
```

## Recurso: CloudFormation

O EndPoint do CloudFormation é `http://localhost:4581`. 

Como exemplo vamos utilizar o seguinte template de CloudFormation que instância uma lista SQS, cria role e armazena dados no SSM.

```
```

Vamos utilizar o `aws cli` para criar uma nova stack de CloudFormation. 

```
aws --endpoint-url=http://localhost:4581 cloudformation create-stack --stack-name infra \
    --template-body file://cf/template.yml
```

Podemos utilizar o `wait` para aguardar a stack ser criada.

```
aws --endpoint-url=http://localhost:4581 cloudformation wait stack-create-complete --stack-name infra
```

Podemos listar todas as stack criadas.

```
aws --endpoint-url=http://localhost:4581 cloudformation describe-stack-events
```


## Recurso: CloudWatch

http://localhost:4582

aws --endpoint-url=http://localhost:4582 cloudwatch set-alarm-state --alarm-name "myalarm" --state-value ALARM --state-reason "testing purposes"

aws --endpoint-url=http://localhost:4587 events put-rule --name my-scheduled-rule --schedule-expression 'rate(1 minutes)'

## Recurso: SSM

http://localhost:4583

```
$ aws --endpoint-url=http://localhost:4583 ssm put-parameter --name "nome" --type "String" --value "clodonil" --overwrite
```

```
$ aws --endpoint-url=http://localhost:4583 ssm get-parameters --names "nome"
```



## Recurso: DynamoDB
http://localhost:4569

Criando a tabela no Dynamdb.

```
$ aws --endpoint-url=http://localhost:4569 dynamodb create-table --table-name table1  \
      --attribute-definitions AttributeName=Nome,AttributeType=S AttributeName=Idade,AttributeType=N \
      --key-schema AttributeName=Nome,KeyType=HASH AttributeName=Idade,KeyType=RANGE \
      --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5

```
Lista as tabelas criadas do Dynamodb.

```
$ aws --endpoint-url=http://localhost:4569 dynamodb list-tables
```

Populando a tabela do Dynamodb.

```
$ aws --endpoint-url=http://localhost:4569 dynamodb put-item --table-name table1 --item '{ "Nome":{"S":"Clodonil"},"Idade":{"N":"10"}}' --return-consumed-capacity TOTAL
```

Realizando um scan na tabela para retornar todos os items.

```
$ aws --endpoint-url=http://localhost:4569 dynamodb scan --table-name table1  --return-consumed-capacity TOTAL
```

Obtendo um item especifico.

```
$ aws --endpoint-url=http://localhost:4569 dynamodb get-item --table-name table1 --key '{"Nome": {"S": "Clodonil"}, "Idade":{"N":"10"}}'
```


## Recurso: Lambda
http://localhost:4574

```
$ cd tutorial/lambda
```

```
$ zip  lambda_v1.zip index.py
```

```
$ aws --endpoint-url=http://localhost:4574 lambda create-function --function-name my-function --zip-file fileb://./lambda_v1.zip --handler index.handler --runtime python3.7 --role arn:aws:iam::000000000000:role/roles2-CopyLambdaDeploymentRole-UTTWQYRJH2VQ
{
    "FunctionName": "my-function",
    "FunctionArn": "arn:aws:lambda:us-east-1:000000000000:function:my-function",
    "Runtime": "python3.7",
    "Role": "arn:aws:iam::000000000000:role/roles2-CopyLambdaDeploymentRole-UTTWQYRJH2VQ",
    "Handler": "index.handler",
    "CodeSize": 287,
    "Description": "",
    "Timeout": 3,
    "LastModified": "2019-12-03T03:41:49.290+0000",
    "CodeSha256": "+tIqyD399zm0ArPmCapjD14klK5pML/v9UQZcQQW4eM=",
    "Version": "$LATEST",
    "TracingConfig": {
        "Mode": "PassThrough"
    },
    "RevisionId": "796080cb-a3f0-48e9-8e9c-11607254fc8d"
}
```
Listando as lambdas:

```
$ aws --endpoint-url=http://localhost:4574 lambda list-functions
```

Envocando a lambda e passando um payload.

```
$ aws --endpoint-url=http://localhost:4574 lambda invoke --function-name my-function --payload '{}' saida.txt
```

No arquivo `saida.txt` está a retorno da lambda.

```
$ cat saida.txt
```


## Recurso: Api Gateway
http://localhost:4567


```
$ aws --endpoint-url=http://localhost:4567 apigateway create-rest-api --name 'HelloWorld (AWS CLI)'
```

```
$ aws --endpoint-url=http://localhost:4567 apigateway apigateway get-resources --rest-api-id 36twoi21n1
```

```
$ aws --endpoint-url=http://localhost:4567 apigateway create-resource --rest-api-id 36twoi21n1 --parent-id kr9zrfk6bq --path-part greeting
```

```
$ aws --endpoint-url=http://localhost:4567 apigateway put-method --rest-api-id 36twoi21n1 --resource-id nxoi851xk0 --http-method GET --authorization-type "NONE" --request-parameters method.request.querystring.greeter=false
```