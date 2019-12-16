import re
WtUdw=Exception
WtUds=True
WtUdk=False
WtUdJ=None
WtUdC=len
import json
from docopt import docopt
from localstack import config
from localstack_ext.bootstrap import licensing
def cmd_login(argv,args):
 args.update(docopt(cmd_login.__doc__.strip(),argv=argv))
 auth=import_auth()
 try:
  provider=args['--provider']or 'github'
  auth.login(provider,args['--username'])
  print('Successfully logged in via provider: %s'%provider)
 except WtUdw as e:
  print('Authentication error: %s'%e)
def cmd_ci(argv,args):
 args.update(docopt(cmd_ci.__doc__.strip(),argv=argv))
 auth=import_auth()
 if args['<subcommand>']=='repos':
  provider=args['--provider']or 'travis'
  result=auth.get_ci_repos(provider)
  print(result)
 elif args['<subcommand>']=='init':
  provider=opt_params(args,['--provider'])or 'travis'
  repo,token=mand_params(args,['--repo','--token'])
  auth.init_ci_repo(repo,token,provider=provider)
  print(repo,token)
def cmd_logout(argv,args):
 args.update(docopt(cmd_logout.__doc__.strip(),argv=argv))
 auth=import_auth()
 auth.logout()
def cmd_config(argv,args):
 args.update(docopt(cmd_config.__doc__.strip(),argv=argv))
 auth=import_auth()
 if args['<value>']:
  auth.set_user_config(args['<key>'],args['<value>'])
  print('Successfully updated configuration value')
 else:
  result=auth.retrieve_user_config()
  if args['<key>']:
   all_values=result
   result={}
   for key,value in all_values.items():
    if re.match(args['<key>'],key):
     result[key]=value
  print(json.dumps(result,indent=4))
def register_commands():
 config.CLI_COMMANDS['config']={'command':'  localstack config','description':'Manage configuration values','parameters':[],'function':cmd_config}
 config.CLI_COMMANDS['login']={'description':'Log in using an external OAuth provider (e.g., Github)','function':cmd_login}
 config.CLI_COMMANDS['logout']={'description':'Log out and delete any session tokens','function':cmd_logout}
 config.CLI_COMMANDS['ci']={'description':'Manage continuous integration repositories and settings','function':cmd_ci}
def import_auth():
 try:
  with licensing.prepare_environment():
   from localstack_ext.utils import auth
   return auth
 except WtUdw:
  raise WtUdw('Command not available in this version')
def mand_params(args,names=[]):
 return get_params(args,names,mandatory=WtUds)
def opt_params(args,names=[]):
 return get_params(args,names,mandatory=WtUdk)
def get_params(args,names=[],mandatory=WtUds):
 result=()
 for name in names:
  value=WtUdJ
  if name in args:
   value=args[name]
  if not value and mandatory:
   raise WtUdw('Please provide %s=... parameter'%name)
  result+=(value)
 if WtUdC(result)==1:
  return result[0]
 return result
# Created by pyminifier (https://github.com/liftoff/pyminifier)
