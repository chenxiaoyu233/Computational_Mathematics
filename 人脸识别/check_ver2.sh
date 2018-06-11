#!/bin/bash

dataDir=./att_faces
testDir=./testCase

for name in $testDir/*
do
	for pic in $name/*
	do
		expect=`basename $name`
		ans=`python3 face_ver2.py $dataDir $pic`
		echo $expect $ans
	done
done
