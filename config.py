import os
from dotenv import load_dotenv

# Load environment variables from conf.env in CWD
load_dotenv(dotenv_path=os.path.join(os.getcwd(), 'conf.env'))

def get_env(key: str, default: str = None) -> str:
  value = os.getenv(key, default)
  if value is None:
    raise RuntimeError(f'Missing required env var: {key}')
  return value

def get_bool_env(key: str, default: bool = False) -> bool:
  val = os.getenv(key)
  if val is None:
    return default
  return val.strip().lower() in ['1', 'true', 'yes']

class Config:
  VAULT_ADDR        = get_env('VAULT_ADDR')
  VAULT_ROLE_ID     = get_env('VAULT_ROLE_ID')
  VAULT_SECRET_ID   = get_env('VAULT_SECRET_ID')
  DB_VAULT_PATH     = get_env('DB_VAULT_PATH', 'secret/data/db/crm')
  VAULT_SKIP_VERIFY = get_bool_env('VAULT_SKIP_VERIFY', False)
