# Porkbun Dynamic DNS
*Use pydantic to make handling the api calls and responses smooth as butter*

# Dev Env (via Ansible)
The Ansible playbook that sets up the container this script runs in uses apt to install `python3-ansible`.

As of 2024-05-05 that installs the outdated pydantic version `1.10.4`.

For now, that's fine, because no advanced pydantic features are being used.

# Dev Env (Manual Steps)
Manually install extensions within the ssh remote session of vscode.
```sh
code --install-extension ms-python.python
code --install-extension ms-python.black-formatter
```
