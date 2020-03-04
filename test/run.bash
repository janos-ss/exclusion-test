#!/bin/bash
cd "${0%/*}/codecov" # This put all the codecov mess in test and not in root project
root=$(git rev-parse --show-toplevel)
PYTHONPATH=$root python3.7 -m pytest $root --cov-report xml:cov.xml --cov=$root --cov-config=.coveragerc
