from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# The Vault URL comes from your Azure Portal Overview page
KEY_VAULT_URL = "https://team3-tm-key-vault.vault.azure.net/"

def get_database_credentials():
    try:
        # 1. Authenticate using your Azure CLI login
        credential = DefaultAzureCredential()
        
        # 2. Create the client to talk to your specific vault
        secret_client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)

        # 3. Pull each secret by the Name you gave it in the Portal
        # These names must match EXACTLY what is in your 'Secrets' list
        host = secret_client.get_secret("psql-host").value
        database = secret_client.get_secret("psql-database").value
        user = secret_client.get_secret("psql-user").value
        password = secret_client.get_secret("psql-password").value
        # blob_url = secret_client.get_secret("azure-storage-blob-url").value
        container_name = secret_client.get_secret("container-name").value
        # resource_group_name = secret_client.get_secret("resource-group-name").value
        # storage_account_name = secret_client.get_secret("storage-account-name").value
        storage_connection = secret_client.get_secret("storage-connection").value
        # subscription_id = secret_client.get_secret("subscription-id").value
        port = secret_client.get_secret("psql-port").value

        return {
            "host": host,
            "database": database,
            "user": user,
            "password": password,
            "port": port,
            "container_name": container_name,
            "storage_connection": storage_connection
        }

    except Exception as e:
        print(f"Error retrieving secrets: {e}")
        return None