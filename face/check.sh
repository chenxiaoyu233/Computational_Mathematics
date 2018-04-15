for (( people = 1; people <= 40; people += 1 ))
do
	for (( which = 1; which <= 10; which += 1 ))
	do
		echo people : s$people, picture $which.pgm
		mv ./att_faces/s$people/$which.pgm ./$which.pgm
		python3 face_ver2.py ./att_faces ./$which.pgm
		mv ./$which.pgm ./att_faces/s$people/$which.pgm
	done
done
