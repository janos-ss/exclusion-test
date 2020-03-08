#!/bin/bash
codecovDir="codecov" 
root=$(git rev-parse --show-toplevel)
PYTHONPATH=$root COVERAGE_FILE="$codecovDir/.coverage" python3.7 -m pytest $root --cov-report xml:"$codecovDir/cov.xml" --cov=$root --cov-config="$codecovDir/.coveragerc"
