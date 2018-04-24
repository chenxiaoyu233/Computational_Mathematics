#!/bin/bash
for((i = 1; i <= 40; i = i + 1))
do
	mkdir testCase/s$i
	for((j = 1; j <= 5; j = j + 1))
	do
		mv att_faces/s$i/$j.pgm testCase/s$i
	done
done
