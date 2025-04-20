import hvac
from config import Config
import os

def init_vault_client():
    client = hvac.Client(
        url=Config.VAULT_ADDR,
        token=Config.VAULT_TOKEN,
        verify=not Config.VAULT_SKIP_VERIFY
    )

    if not client.is_authenticated():
        raise RuntimeError("Vault token authentication failed.")
    return client


def get_secret(
      client: hvac.Client,
      path: str
    ) -> dict:
    """
    Reads a KV v2 secret at the given path and returns its data dict.
    """
    resp = client.secrets.kv.v2.read_secret_version(path=path)
    return resp['data']['data']

def get_db_credentials(client: hvac.Client) -> dict:
    data = get_secret(client, Config.DB_VAULT_PATH)
    return {
      'username': data['username'],
      'password': data['password'],
      'host':     data.get('host', 'localhost'),
      'port':     data.get('port', 5432),
      'dbname':   data.get('dbname', 'postgres')
    }
    
def login_userpass(username: str, password: str) -> str:
    client = hvac.Client(url=os.getenv("VAULT_ADDR"))
    response = client.auth_userpass(username, password)
    return response["auth"]["client_token"]
