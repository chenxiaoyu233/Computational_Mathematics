#!/bin/bash

for name in ./pic/*
do
	for pic in $name/*
	do
		mv $pic ./
		expect=`basename $name`
		filename=`basename $pic`
		ans=`python3 face_ver2.py ./pic ./$filename fresh`
		echo $expect $ans
		mv ./$filename $pic
	done
done
