#!/bin/bash

for name in ./att_faces/*
do
	for pic in $name/*
	do
		mv $pic ./
		expect=`basename $name`
		filename=`basename $pic`
		rm $name/.info
		ans=`python3 face_ver2.py ./att_faces ./$filename fresh`
		echo $expect $ans
		mv ./$filename $pic
	done
done
