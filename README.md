# Porkbun Dynamic DNS with Pydantic
*Use pydantic to make handling the api calls and responses smooth as butter*

## Secrets

The `loadcredential` library loads

1. systemd credentials
1. environment variables (fallback)

Typically the systemd credentials are in production servers and the environment variables are used for development.

## Local Development

Securely prompt and export the Porkbun API credentials in your current terminal session (this hides keystrokes and avoids writing secrets to shell history):
```bash
read -rsp "Enter Porkbun API Key: " PORKBUN_API_KEY && echo
export PORKBUN_API_KEY

read -rsp "Enter Porkbun Secret API Key: " PORKBUN_SECRET_API_KEY && echo
export PORKBUN_SECRET_API_KEY
```

Configure your domain and DNS records in `ddns/conf.json`.

Create and set up the virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip pip-tools

pip-compile pyproject.toml
pip-sync

# Install package in editable mode so console script and imports work
pip install -e .
```

Run the sync script:
```bash
python -m ddns.main
# or via the entrypoint script
syncrecords
```
## Release & Publishing

### 1. Bump the Version
Update the version number in `pyproject.toml` (e.g., `version = "4.21"`).

### 2. Build Release Binary
Ensure `shiv` is installed, then build the standalone executable zipapp (which bundles `ddns/conf.json`):
```bash
pip install --upgrade shiv
shiv -c syncrecords -o syncrecords.pyz .
```

### 3. Commit and Push Changes
Commit and push the updated changes to the `main` branch via IDE integration. 

### 4. Tag the Version and Push Tag
```bash
git tag v4.21
git push origin v4.21
```

### 5. Create GitHub Release
1. Navigate to the [Releases page](https://github.com/VincentSaelzler/porkbun-ddns-pydantic/releases/new).
2. Choose tag: **`v4.21`** (or your bumped version).
3. Set Release title: **`v4.21`**.
4. Drag and drop the generated **`syncrecords.pyz`** file into the *"Attach binaries by dropping them here or selecting them"* section.
5. Click **Publish release**.

## Limitations
The desired URL must be either the root domain, or a subdomain.

## Credits
Inspired by [abstractionmage/unofficial-porkbun-ddns-python](https://github.com/abstractionmage/unofficial-porkbun-ddns-python)
