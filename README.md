# PROPRTS

[![Deploy](https://github.com/0x00C0DE/PROPRTS/actions/workflows/main.yml/badge.svg)](https://github.com/0x00C0DE/PROPRTS/actions/workflows/main.yml)

A robinhood high frequency Predictive Reactive Observational Pattern Recognition Trading System

Latest files:

- PROPRTS-main-protoV1.py
- proprtsImageViewer-1-protoV1.py
- PROPRTS-1-protoV1.py
- Robinhood cryptocurrency high frequency PROPRTS.pdf ( information and instructions how to run latest files together )

## Running Locally

- Copy .env.example to .env and edit the values accordignly.
- Install python with `pip install --target ./python-local/lib/python3.9/site-packages -r requirements.txt --upgrade`
- Run python3 ./src/aws_lambda_function.py in the main folder.

Instructions are located within the scripts source code via comments in PROPRTS-main-protoV1.py
