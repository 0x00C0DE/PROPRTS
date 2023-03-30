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
`cp .env.example .env`

- Install python with
`pip install --target ./python-local/lib/python3.9/site-packages -r requirements.txt --upgrade`

- Run the script
`python3 lambda_function.py`

## Running on AWS Lambda

- Set up environment variables and secrets.

- Update python-aws. You MUST do this every time you add a package. You also need to do this inside an amazonlinux docker container.
`pip install --target ./python-aws/lib/python3.9/site-packages -r requirements.txt --upgrade`

## Tools

- Install "ruff" extension in IDE.

- Use this to get a list of lint errors (will fail the pipeline in the future):
`ruff check --format=github --target-version=py39 ./src`

Instructions are located within the scripts source code via comments in PROPRTS-main-protoV1.py
