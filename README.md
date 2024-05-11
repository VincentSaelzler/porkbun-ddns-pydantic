# Porkbun Dynamic DNS with Pydantic
*Use pydantic to make handling the api calls and responses smooth as butter*

## Credits
Inspired by [abstractionmage/unofficial-porkbun-ddns-python](https://github.com/abstractionmage/unofficial-porkbun-ddns-python)

## Secrets
Use linux environment variables.
```
echo export APIKEY=pk1_redacted >> ~/.bashrc
echo export SECRETAPIKEY=sk1_redacted >> ~/.bashrc
```

## Dev Environment
Use VS Code devcontainers extension. Environment is defined in .devcontainer folder.


## Virtual Environments
To create/update/change the virtual environment
```
rm -rf .venv
rm requirements.txt

python3 -m venv .venv
source .devenv/bin/activate

pip install --upgrade pip
pip install --upgrade pip-tools

pip-compile
pip-sync
```
