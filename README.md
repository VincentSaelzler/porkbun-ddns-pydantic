# Porkbun Dynamic DNS with Pydantic
*Use pydantic to make handling the api calls and responses smooth as butter*

## Secrets
Use linux environment variables for development, and systemd credentials for production.
```
echo export PORKBUN_API_KEY=pk1_redacted >> ~/.bashrc
echo export PORKBUN_SECRET_API_KEY=sk1_redacted >> ~/.bashrc
source ~/.bashrc
```

## Virtual Environments
To create/update/change the virtual environment
```
rm -rf .venv
rm requirements.txt

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install --upgrade pip-tools shiv

pip-compile
pip-sync

python -m ddns.main
```

## Limitations
The desired URL must be either the root domain, or a subdomain.

## Credits
Inspired by [abstractionmage/unofficial-porkbun-ddns-python](https://github.com/abstractionmage/unofficial-porkbun-ddns-python)
