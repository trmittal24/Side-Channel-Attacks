#!/bin/bash

chmod 775 decrypt.py
for file in [1-9]*.mat;
do
	./decrypt.py $file
	echo
done
