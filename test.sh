cd ~ || exit 1

git clone "$1" || echo "Working with pre-cloned repo."
cd "$2" || exit 2

git fetch -p
git switch "$3"
git pull

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
