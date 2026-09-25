# Porkbun Dynamic DNS with Pydantic
*Use pydantic to make handling the api calls and responses smooth as butter*

## Secrets

The `loadcredential` library loads

1. systemd credentials
1. environment variables (fallback)

Typically the systemd credentials are in production servers and the environment variables are used for development.

## Local Development
To create/update/change the virtual environment
```
echo export PORKBUN_API_KEY=pk1_redacted >> ~/.bashrc
echo export PORKBUN_SECRET_API_KEY=sk1_redacted >> ~/.bashrc
source ~/.bashrc

rm -rf .venv
rm requirements.txt

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install --upgrade pip-tools

pip-compile
pip-sync

python -m ddns.main
```
## Create Release Binary

```
pip install --upgrade shiv
shiv -c syncrecords -o syncrecords.pyz .
```

## Limitations
The desired URL must be either the root domain, or a subdomain.

## Credits
Inspired by [abstractionmage/unofficial-porkbun-ddns-python](https://github.com/abstractionmage/unofficial-porkbun-ddns-python)
