#!/bin/bash
for((i = 1; i <= 40; i = i + 1))
do
	for((j = 1; j <= 5; j = j + 1))
	do
		mv testCase/s$i/$j.pgm att_faces/s$i
	done
done
