#!/bin/bash
if [ -z "$1" ]; then
    echo usage: $0 file id
    exit
fi
LOC="/media/sda3/data/source/bmlsp/1400OS_"$1"_Codes.zip"
EXT="${LOC#*.}"

if [ "$EXT" = "zip" ]; then
    unzip $LOC -d .
    echo "finish extracting zip "$LOC
    exit
fi

if [ "$EXT" = "tar" ]; then
    tar xzf $LOC
    echo "finish extracting tar "$LOC
    exit
fi

