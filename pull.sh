#!/bin/bash

cd /home/user/hopital-availabilty-frontend

UPSTREAM=${1:-'@{u}'}
DIFFCOMM=$(git fetch origin --quiet; git rev-list HEAD..."$UPSTREAM" --count)
if [ "$DIFFCOMM" -gt 0 ]; then
  echo "Pulling $UPSTREAM" >> /home/user/update_log
  git pull
  yarn build
else
  echo "master Upto date" >> /home/user/update_log
fi

cd /home/user/hopital-availabilty-frontend-nidhin

UPSTREAM=${1:-'@{u}'}
DIFFCOMM=$(git fetch origin --quiet; git rev-list HEAD..."$UPSTREAM" --count)
if [ "$DIFFCOMM" -gt 0 ]; then
  echo "Pulling $UPSTREAM" >> /home/user/update_log
  git pull
  yarn build
else
  echo "nidhin Upto date" >> /home/user/update_log
fi

cd /home/user/hopital-availabilty-frontend-sanu

UPSTREAM=${1:-'@{u}'}
DIFFCOMM=$(git fetch origin --quiet; git rev-list HEAD..."$UPSTREAM" --count)
if [ "$DIFFCOMM" -gt 0 ]; then
  echo "Pulling $UPSTREAM" >> /home/user/update_log
  git pull
  yarn build
else
  echo "sanu Upto date" >> /home/user/update_log
fi
