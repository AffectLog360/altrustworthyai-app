#!/bin/bash
# Clear stale bytecode caches.
find . -name "*.pyc" -delete
find . -name "__pycache__" -delete

# Run the unit tests.
python -m unittest discover -s . -p "test_app.py"
