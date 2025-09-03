#!/bin/bash
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# Activate the virtual environment
source myenv/bin/activate

python3 new.py 2>/dev/null

