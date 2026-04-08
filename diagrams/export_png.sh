#!/bin/bash

file=$1

if [ -z "$file" ]; then
    echo "Nope... not gonna work."
    echo "-> Usage: $0 <file>"
    exit 1
fi

qlmanage -t -s 2000 -o ./ ./$file.svg
