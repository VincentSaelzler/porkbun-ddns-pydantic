# Porkbun Dynamic DNS with Pydantic
*Use pydantic to make handling the api calls and responses smooth as butter*

## Secrets

The `loadcredential` library loads

1. systemd credentials
1. environment variables (fallback)

Typically the systemd credentials are in production servers and the environment variables are used for development.

## Configuration

Configure your domain and DNS records in `ddns/conf.json`.

> **Note:** The desired URL must be either the root domain or a subdomain.

## Local Development

Securely prompt and export the Porkbun API credentials in your current terminal session (this hides keystrokes and avoids writing secrets to shell history):
```bash
read -rsp "Enter Porkbun API Key: " PORKBUN_API_KEY && echo
export PORKBUN_API_KEY

read -rsp "Enter Porkbun Secret API Key: " PORKBUN_SECRET_API_KEY && echo
export PORKBUN_SECRET_API_KEY
```

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
Commit and push the updated changes to the `main` branch.

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

## Production Deployment

On your target production server, download the standalone release binary directly from GitHub Releases:

```bash
# Download the specific release binary (replace v4.21 with desired version)
curl -LO https://github.com/VincentSaelzler/porkbun-ddns-pydantic/releases/download/v4.21/syncrecords.pyz

# Make it executable
chmod +x syncrecords.pyz
```

The executable can be placed in a system path (such as `/usr/local/bin/syncrecords`) and invoked on a timer (e.g., via a systemd service and timer). 

> **Note on Credentials:** In production, credentials should be supplied via systemd credentials (`PORKBUN_API_KEY` and `PORKBUN_SECRET_API_KEY`), which `loadcredential` automatically loads before falling back to environment variables. Setting up and provisioning systemd credentials or unit files is outside the scope of this repository.

## Architecture Compatibility

The generated `.pyz` executable is not cross-architecture portable. For the binary to run successfully, the target machine's CPU architecture (e.g., x86_64 vs. ARM64) and Python version must match the machine where it was built with Shiv.

**For example, a release binary built on an x86_64 machine will not run on an ARM-based device like a Raspberry Pi.**

If you are running this on a Raspberry Pi (or any different architecture), the recommended approach is to build the project using Shiv directly on the target device itself, rather than trying to adapt or tailor a `.pyz` built on a mismatched machine.

## Credits
Inspired by [abstractionmage/unofficial-porkbun-ddns-python](https://github.com/abstractionmage/unofficial-porkbun-ddns-python)
