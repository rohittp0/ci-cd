#!/bin/bash

cd /home/user/hopital-availabilty-frontend

UPSTREAM=${1:-'@{u}'}
DIFFCOMM=$(git fetch origin --quiet; git rev-list HEAD..."$UPSTREAM" --count)
if [ "$DIFFCOMM" -gt 0 ]; then
  echo "<-- Pulling master" >> /home/user/update_log
  git pull
  yarn ci
  yarn build
fi

cd /home/user/hopital-availabilty-frontend-nidhin

UPSTREAM=${1:-'@{u}'}
DIFFCOMM=$(git fetch origin --quiet; git rev-list HEAD..."$UPSTREAM" --count)
if [ "$DIFFCOMM" -gt 0 ]; then
  echo "<-- Pulling nidhin" >> /home/user/update_log
  git pull
  yarn ci
  yarn build
fi

cd /home/user/hopital-availabilty-frontend-sanu

UPSTREAM=${1:-'@{u}'}
DIFFCOMM=$(git fetch origin --quiet; git rev-list HEAD..."$UPSTREAM" --count)
if [ "$DIFFCOMM" -gt 0 ]; then
  echo "<-- Pulling sanu" >> /home/user/update_log
  git pull
  yarn ci
  yarn build
fi

echo "Everything upto date" >> /home/user/update_log
