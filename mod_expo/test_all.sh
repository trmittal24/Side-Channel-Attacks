#!/bin/bash

chmod 775 processing.py
for file in [1-9]*.mat;
do
	./processing.py $file
	echo
done
