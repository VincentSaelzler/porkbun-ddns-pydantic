# Porkbun Dynamic DNS with Pydantic
*Use pydantic to make handling the api calls and responses smooth as butter*

## Credits
Inspired by [abstractionmage/unofficial-porkbun-ddns-python](https://github.com/abstractionmage/unofficial-porkbun-ddns-python)

## Dev Env (via Ansible)
The Ansible playbook that sets up the container this script runs in uses apt to install `python3-ansible`.

As of 2024-05-05 that installs the outdated pydantic version `1.10.4`.

For now, that's fine, because no advanced pydantic features are being used.

## Dev Env (Manual Steps)
Manually install extensions within the ssh remote session of vscode.
```sh
code --install-extension ms-python.python
code --install-extension ms-python.black-formatter
```


## Virtual Environments
To update/change the virtual environment
```
rm -rf .devenv
rm requirements.txt

python3 -m venv .devenv
source .devenv/bin/activate

pip install --upgrade pip
pip install --upgrade pip-tools

pip-compile
pip-sync
```
