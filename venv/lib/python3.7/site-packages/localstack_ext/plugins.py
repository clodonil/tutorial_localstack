import os
vdOPF=Exception
vdOPB=str
vdOPM=any
vdOPl=True
import logging
from localstack.utils import common
from localstack.constants import(LOCALSTACK_WEB_PROCESS,LOCALSTACK_INFRA_PROCESS,TRUE_STRINGS,FALSE_STRINGS)
from localstack.utils.bootstrap import is_api_enabled
from localstack_ext import config as config_ext
from localstack_ext.bootstrap import licensing,cli,install
def register_localstack_plugins():
 _setup_logging()
 if os.environ.get(LOCALSTACK_INFRA_PROCESS)in TRUE_STRINGS:
  install.install_libs()
 if os.environ.get(LOCALSTACK_WEB_PROCESS):
  from localstack_ext.bootstrap.dashboard import dashboard_extended
  dashboard_extended.patch_dashboard()
  return{}
 with licensing.prepare_environment():
  try:
   from localstack_ext.services import dns_server
   dns_server.setup_network_configuration()
  except vdOPF:
   return
  try:
   from localstack.services.infra import register_plugin,Plugin,start_ec2
   from localstack.services.apigateway import apigateway_listener
   from localstack_ext.services.cognito import cognito_starter,cognito_idp_api,cognito_listener
   from localstack_ext.services.sts import sts_starter
   from localstack_ext.services.elasticache import elasticache_starter
   from localstack_ext.services.rds import rds_starter,rds_listener
   from localstack_ext.services.awslambda import lambda_extended
   from localstack_ext.services.sqs import sqs_extended
   from localstack_ext.services.apigateway import apigateway_extended
   from localstack_ext.services.cloudformation import cloudformation_extended
   from localstack_ext.services.ec2 import ec2_listener
   from localstack_ext.services.ecs import ecs_starter,ecs_listener
   from localstack_ext.services.iot import iot_starter,iot_listener
   from localstack_ext.services.eks import eks_starter
   from localstack_ext.services.kms import kms_starter,kms_listener
   from localstack_ext.services.xray import xray_starter,xray_listener
   from localstack_ext.services.cloudfront import cloudfront_starter
   from localstack_ext.services.athena import athena_starter
   from localstack_ext.services.glue import glue_starter,glue_listener
   from localstack_ext.services.appsync import appsync_starter
   from localstack_ext.services import edge
   from localstack_ext.utils.aws import aws_utils
   apigateway_listener.UPDATE_APIGATEWAY.forward_request=cognito_idp_api.wrap_api_method('apigateway',apigateway_listener.UPDATE_APIGATEWAY.forward_request)
   register_plugin(Plugin('rds',start=rds_starter.start_rds,listener=rds_listener.UPDATE_RDS))
   register_plugin(Plugin('sts',start=sts_starter.start_sts))
   register_plugin(Plugin('cognito-idp',start=cognito_starter.start_cognito_idp,listener=cognito_listener.UPDATE_COGNITO))
   register_plugin(Plugin('cognito-identity',start=cognito_starter.start_cognito_identity,listener=cognito_listener.UPDATE_COGNITO_IDENTITY))
   register_plugin(Plugin('elasticache',start=elasticache_starter.start_elasticache))
   register_plugin(Plugin('edge',start=edge.start_edge))
   register_plugin(Plugin('ec2',start=start_ec2,listener=ec2_listener.UPDATE_EC2))
   register_plugin(Plugin('ecs',start=ecs_starter.start_ecs,listener=ecs_listener.UPDATE_ECS))
   register_plugin(Plugin('iot',start=iot_starter.start_iot,listener=iot_listener.UPDATE_IOT))
   register_plugin(Plugin('eks',start=eks_starter.start_eks))
   register_plugin(Plugin('kms',start=kms_starter.start_kms,listener=kms_listener.UPDATE_KMS))
   register_plugin(Plugin('xray',start=xray_starter.start_xray,listener=xray_listener.UPDATE_XRAY))
   register_plugin(Plugin('cloudfront',start=cloudfront_starter.start_cloudfront))
   register_plugin(Plugin('athena',start=athena_starter.start_athena))
   register_plugin(Plugin('glue',start=glue_starter.start_glue,listener=glue_listener.UPDATE_GLUE))
   register_plugin(Plugin('appsync',start=appsync_starter.start_appsync))
   lambda_extended.patch_lambda()
   sqs_extended.patch_sqs()
   apigateway_extended.patch_apigateway()
   cloudformation_extended.patch_cloudformation()
   aws_utils.patch_aws_stack()
  except vdOPF as e:
   if 'No module named' not in vdOPB(e):
    print(e)
   pass
 docker_flags=[]
 if is_api_enabled('edge')and config_ext.DNS_ADDRESS not in FALSE_STRINGS:
  if not common.is_port_open(dns_server.DNS_PORT,protocols='tcp'):
   docker_flags+=['-p {a}:{p}:{p}'.format(a=config_ext.DNS_ADDRESS,p=dns_server.DNS_PORT)]
  if not common.is_port_open(dns_server.DNS_PORT,protocols='udp'):
   docker_flags+=['-p {a}:{p}:{p}/udp'.format(a=config_ext.DNS_ADDRESS,p=dns_server.DNS_PORT)]
 if vdOPM([is_api_enabled(api)for api in('rds','elasticache','ecs','athena')]):
  docker_flags+=['-p {start}-{end}:{start}-{end}'.format(start=config_ext.SERVICE_INSTANCES_PORTS_START,end=config_ext.SERVICE_INSTANCES_PORTS_END)]
 if is_api_enabled('eks'):
  kube_config=os.path.expanduser('~/.kube/config')
  if os.path.exists(kube_config):
   docker_flags+=['-v %s:/root/.kube/config'%kube_config]
 result={'docker':{'run_flags':' '.join(docker_flags)}}
 return result
def _setup_logging():
 logging.getLogger('kubernetes').setLevel(logging.INFO)
def register_localstack_commands():
 if os.environ.get('LOCALSTACK_API_KEY'):
  cli.register_commands()
 return vdOPl
# Created by pyminifier (https://github.com/liftoff/pyminifier)
