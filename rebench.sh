#!/usr/bin/env bash
BRANCH=`git rev-parse --abbrev-ref HEAD`

if [ "$(hostname)" == "beast" ]; then
    ENV="Ubuntu_13.10"
else
    ENV="Travis_Builder"
fi

if [ "$BRANCH" == "master" ]; then
    BRANCH="default"
fi
uname -a
sudo ./ReBench/rebench/rebench.py ./rebench.conf --commit-id=`git log -n 1 | grep commit | awk '{print $2}'` --environment="$ENV" --project=wlvlang -v --branch=$BRANCH $@
