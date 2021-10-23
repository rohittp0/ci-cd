#!/bin/bash

pull_and_build()
{
  if [ -d ~/hopital-availabilty-frontend-${1} ]; then
    cd ~/hopital-availabilty-frontend-$1
    echo "Switched to ~/hopital-availabilty-frontend-${1}"
  else
    git clone https://github.com/Trebuchet-ltd/hopital-availabilty-frontend ~/hopital-availabilty-frontend-${1}
    cd ~/hopital-availabilty-frontend-$1
    git switch -c $1 || git switch $1
  fi
  
   [ ! $(git status -b --porcelain=v2 | grep -m 1 "^# branch.upstream
 " | cut -d " " -f 3-) ] && git branch --set-upstream-to origin/$1
  
  UPSTREAM=${1:-'@{u}'}
  DIFFCOMM=$(git fetch origin --quiet; git rev-list HEAD..."$UPSTREAM" --count)
  
  echo "Found ${DIFFCOMM} changes"
  
  if [ "$DIFFCOMM" -gt 0 ]; then
    echo "<-- Pulling ${1}" >> /home/user/update_log
    git pull
    yarn ci
    yarn stage &
  fi
}

pull_and_build master
pull_and_build sanu
pull_and_build nidhin

echo "Everything upto date @ $(date)" >> /home/user/update_log
