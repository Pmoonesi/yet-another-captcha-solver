#!/bin/bash

for i in {5001..5500}
do
	cp preprocessed/processed_captcha/$i.png dataset/test_captchas/$i.png
	cp new_label_ns/$i.txt dataset/test_labels/$i.txt
done
