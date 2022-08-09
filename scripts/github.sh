#!/bin/bash

set -e

git config --global user.email "travis@travis-ci.org"
git config --global user.name "Travis CI"
# git remote set-url --push origin "https://${GH_TOKEN}@github.com/${TRAVIS_REPO_SLUG}.git"
# git remote -v
git checkout -f -b version-branch

pip install --upgrade bump2version wheel
bump2version build

git commit -am "$(git log -1 --pretty=%B) .... bump version [skip ci]"
git push origin version-branch:master --follow-tags

rm -rf ./dist
python setup.py sdist bdist_wheel

