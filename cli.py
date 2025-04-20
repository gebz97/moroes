import os
import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config
from vault_client import init_vault_client, get_db_credentials
from models import Base

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from handlers import (
  system as system_h,
  service as service_h,
  server as server_h,
  database as db_h,
  credential as cred_h
)

def create_db_session(creds: dict):
  #print(creds['password'])
  url = (
    f"postgresql://{creds['username']}:{creds['password']}"
    f"@{creds['host']}:{creds['port']}/{creds['dbname']}"
  )
  engine = create_engine(url)
  Base.metadata.create_all(engine)
  return sessionmaker(bind=engine)()

def build_parser():
  parser = argparse.ArgumentParser(
    description='Manage system lifecycle resources'
  )
  subs = parser.add_subparsers(dest='resource', required=True)

  def add_res(name):
    p = subs.add_parser(name)
    sp = p.add_subparsers(dest='action', required=True)
    for act in ('create','list','update','delete'):
      ap = sp.add_parser(act)
      ap.add_argument('--id', type=int, help='Resource ID')
      ap.add_argument('--name', help='Resource name')
      ap.add_argument('--system-id', type=int, help='For services')
      ap.add_argument('--service-id', type=int, help='For servers')
      ap.add_argument('--server-id', type=int, help='For databases')
      ap.add_argument('--vault-path', help='For credentials')
      # further flags as needed per-resource
    return p

  for r in ('system','service','server','database','credential'):
    add_res(r)

  return parser

def dispatch(args, session, vault_client):
  r, a = args.resource, args.action
  mapping = {
    'system':   system_h,
    'service':  service_h,
    'server':   server_h,
    'database': db_h,
    'credential': cred_h
  }
  module = mapping[r]
  func = getattr(module, f"{a}_handler")
  func(args, session, vault_client)

def main():
  vault = init_vault_client()
  db_creds = get_db_credentials(vault)
  session = create_db_session(db_creds)

  parser = build_parser()
  args   = parser.parse_args()
  dispatch(args, session, vault)

if __name__ == '__main__':
  main()
