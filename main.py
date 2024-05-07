from pydantic import __version__
import os

print(os.environ['APIKEY'])
print(os.environ['SECRETAPIKEY'])
print(f"pydantic version: {__version__}")
