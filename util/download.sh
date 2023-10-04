#!/bin/bash

if [ $# -lt 1 ];
then
	echo "Please input the captcha generator's api as an argument"; echo;
	exit 1;
else
	url="$1"
fi

doit() {
  i="$1"
  curl "$url" --silent | jq '.["image"]'| sed 's/^.\(.*\).$/\1/' | base64 -d > test/data/$i.png
}
export -f doit

seq 1 10 | parallel -j12 --results . doit
