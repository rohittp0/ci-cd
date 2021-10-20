#!/bin/bash

cd /home/user/hopital-availabilty-frontend

UPSTREAM=${1:-'@{u}'}
DIFFCOMM=$(git fetch origin --quiet; git rev-list HEAD..."$UPSTREAM" --count)
if [ "$DIFFCOMM" -gt 0 ]; then
  echo "Pulling $UPSTREAM" >> /home/user/update_log
  git pull
  yarn build
else
  echo "Upto date" >> /home/user/update_log
fi
