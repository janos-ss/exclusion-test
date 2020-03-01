#!/bin/bash
#This script is gonna be lanched on all modifed file by git, file path as command argument. If this script return a non zero status code, commit dont pass


listDeco='  *'

if [[ $1 == *.py ]] 
then
	echo "$listDeco" linting $1 
	./lint/autopep8.py $1 --in-place
fi

