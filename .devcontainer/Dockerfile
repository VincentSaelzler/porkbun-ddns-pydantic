FROM debian:latest

# apt dependencies
RUN apt-get update && apt-get full-upgrade -y

# WARN: what happens if the default version of python changes?
RUN apt install -y git python3 python3.11-venv
