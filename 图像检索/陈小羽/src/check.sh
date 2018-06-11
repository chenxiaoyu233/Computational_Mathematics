#!/bin/bash

for((i = 1; i; i = i + 1))
do
	python3 make_data.py > main.in
	python3 kd-tree.py
	if [ $? -ne 1 ]; then
		echo Wa
		exit
	else 
		echo Ac
	fi
done
