#!/bin/bash
cd "$(dirname "$0")"
if [ ! -f ./id_rsa ]; then
    echo "key not found, creating key!"
    yes | ssh-keygen -f id_rsa -t rsa -N ''
else
    echo "keys already exist, moving on..."
fi

