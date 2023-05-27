#!/bin/env bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=src uvicorn src.app:app --reload
