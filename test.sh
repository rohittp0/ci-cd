cd ~ || exit 1

if [ ! -d "$2" ]; then
  git clone "$1"
fi

cd "$2" || exit 2

git fetch -p
git switch "$3"
git fetch origin "$3"
git reset --hard FETCH_HEAD
git clean -df

if [ -f "package.json" ]; then
  echo "Running tests using yarn"

  yarn ci || yarn install
  echo "Installed Dependencies"

  yarn test || exit 3
  yarn lint || exit 3
  yarn build || exit 3

else
  echo "Unrecognised project type passing blindly"
fi

exit 0
