function update_secret() {
    vault_name="$1"
    secret_name="$2"
    secret_value="$3"

    echo
    echo "Checking secret $secret_name in Key Vault $vault_name.."

    # Check if the secret exists
    secretExists=$(az keyvault secret list --vault-name "$vault_name" --query "[?name=='$secret_name'].name" -o tsv)

    if [ -n "$secretExists" ]; then
        # Secret exists, retrieve its value
        kv_secret_value=$(az keyvault secret show --vault-name "$vault_name" --name "$secret_name" --query value -o tsv)

        # Encode both values to avoid direct string comparison issues
        encoded_kv_secret_value=$(echo -n "$kv_secret_value" | base64)
        encoded_secret_value=$(echo -n "$secret_value" | base64)

        if [ "$encoded_kv_secret_value" = "$encoded_secret_value" ]; then
            echo "KV value is the same as the provided secret value. Skipping update."
            return
        fi
        echo "KV value is different from the provided secret value. Updating..."
    else
        echo "Secret $secret_name does not exist in Key Vault. Creating it now..."
    fi

    # Create or update the secret
    echo "Uploading secret $secret_name to Key Vault $vault_name..."
    az keyvault secret set --name "$secret_name" --vault-name "$vault_name" --value "$secret_value" -o none
    echo "Secret $secret_name successfully uploaded!"
}
