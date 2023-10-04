#!/bin/bash

doit() {
  i="$1"
  touch test/label/$i.txt
}
export -f doit

seq 1 10 | parallel -j12 --results . doit
