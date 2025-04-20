#!/usr/bin/env bash
set -euo pipefail

APP_NAME="moroes-v0-1-0"

# 1. Ensure KV v2 is enabled at secret/
vault secrets enable -path=secret kv-v2 \
  || echo "kv-v2 already enabled at secret/"

# 2. Populate initial DB credentials for this app
vault kv put secret/apps/${APP_NAME}/db \
  username="${APP_NAME}_user" \
  password="$(openssl rand -base64 16)" \
  host="db-${APP_NAME}.internal" \
  port="5432" \
  dbname="${APP_NAME}"

# 3. Create a policy granting read/list on this app’s path
cat <<EOF | vault policy write ${APP_NAME}-db-policy -
path "secret/data/apps/${APP_NAME}/db" {
  capabilities = ["read","list"]
}
EOF

# 4. Enable AppRole if not already enabled
vault auth enable approle \
  || echo "approle auth already enabled"

# 5. Create (or update) an AppRole for this app
vault write auth/approle/role/${APP_NAME}-app \
  token_ttl="1h" \
  token_max_ttl="4h" \
  secret_id_ttl="24h" \
  secret_id_num_uses=10 \
  policies="${APP_NAME}-db-policy"

# 6. Fetch RoleID & SecretID for runtime use
ROLE_ID=$(vault read -field=role_id auth/approle/role/${APP_NAME}-app/role-id)
SECRET_ID=$(vault write -f -field=secret_id auth/approle/role/${APP_NAME}-app/secret-id)

# 7. Print exports for your environment
cat <<EOL
# For application "${APP_NAME}", set:
export VAULT_ROLE_ID="${ROLE_ID}"
export VAULT_SECRET_ID="${SECRET_ID}"
export DB_VAULT_PATH="secret/data/apps/${APP_NAME}/db"
EOL

echo "✅ Vault bootstrapped for application: ${APP_NAME}"
