# Porkbun Dynamic DNS with Pydantic
*Use pydantic to make handling the api calls and responses smooth as butter*

## Credits
Inspired by [abstractionmage/unofficial-porkbun-ddns-python](https://github.com/abstractionmage/unofficial-porkbun-ddns-python)


## Dev Env (Manual Steps)
Manually install extensions within the ssh remote session of vscode.
```sh
code --install-extension ms-python.python
code --install-extension ms-python.black-formatter
code --install-extension ms-python.isort
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
