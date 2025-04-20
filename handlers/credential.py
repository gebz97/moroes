from models import Credential
from vault_client import get_secret

def create_handler(args, session, vault):
  # write secret into Vault first
  data = {
    'username': args.db_username,
    'password': args.db_password
  }
  vault.secrets.kv.v2.create_or_update_secret(
    path=args.vault_path,
    secret=data
  )
  cred = Credential(
    vault_path=args.vault_path,
    resource_type=args.resource,
    resource_id=args.id
  )
  session.add(cred)
  session.commit()
  print(f"Stored credential id={cred.id} for {args.resource} {args.id}")

def list_handler(args, session, vault):
  for c in session.query(Credential).all():
    print(f"{c.id}\t{c.resource_type}\t{c.resource_id}\t{c.vault_path}")

def update_handler(args, session, vault):
  c = session.query(Credential).get(args.id)
  if args.vault_path:
    c.vault_path = args.vault_path
  session.commit()
  print(f"Updated Credential id={c.id}")

def delete_handler(args, session, vault):
  c = session.query(Credential).get(args.id)
  session.delete(c)
  session.commit()
  print(f"Deleted Credential id={args.id}")
