import os
import socket
from botocore.exceptions import EndpointConnectionError
from localstack.utils.common import short_uid
from localstack.utils.aws import aws_stack
from localstack.dashboard import infra as dashboard_infra
from localstack_ext.utils.aws.aws_models import RDSDatabase
get_graph_orig=dashboard_infra.get_graph
def get_rds_databases(name_filter,pool,env):
 result=[]
 try:
  client=aws_stack.connect_to_service('rds')
  dbs=client.describe_db_instances()
  for inst in dbs['DBInstances']:
   db=RDSDatabase(id=inst['DBInstanceArn'])
   result.append(db)
 except(socket.error,EndpointConnectionError):
  pass
 return result
def get_graph(*args,**kwargs):
 os.environ['AWS_ACCESS_KEY_ID']=os.environ.get('AWS_ACCESS_KEY_ID')or 'foobar'
 os.environ['AWS_SECRET_ACCESS_KEY']=os.environ.get('AWS_SECRET_ACCESS_KEY')or 'foobar'
 result=get_graph_orig(*args,**kwargs)
 env=kwargs.get('env')
 name_filter=kwargs.get('name_filter')
 pool={}
 node_ids={}
 databases=get_rds_databases(name_filter,pool=pool,env=env)
 for db in databases:
  uid=short_uid()
  node_ids[db.id]=uid
  result['nodes'].append({'id':uid,'arn':db.id,'name':db.name(),'type':'rds'})
 return result
def patch_dashboard():
 dashboard_infra.get_graph=get_graph
# Created by pyminifier (https://github.com/liftoff/pyminifier)
