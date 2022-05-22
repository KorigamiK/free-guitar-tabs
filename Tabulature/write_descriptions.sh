#!/bin/bash

if [ -z "$1" ]; then
        echo "No argument supplied"

else
        yt-dlp --skip-download --write-description "$1"
fi
