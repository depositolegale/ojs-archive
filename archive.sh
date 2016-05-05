#!/bin/bash

if [ -z "$1" ]
then
    echo "USAGE: archive.sh {seed_file}"
    exit
fi

jobname=$(basename "$1" .seeds)

wget-lua --user-agent='Wget/1.14.lua.20130523-9a5c - http://www.depositolegale.it' \
	--lua-script=ojs.lua \
	--input-file=$1 \
	--warc-file=data/warc/$jobname \
	--page-requisites \
	--output-file=logs/$jobname.log