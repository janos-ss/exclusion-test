#!/bin/bash
root=$(git rev-parse --show-toplevel)
cd $root
python3.7 -m pytest -x $root
