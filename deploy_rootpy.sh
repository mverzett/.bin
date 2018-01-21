#! /bin/bash

mkdir rootpy_deployment
pushd rootpy_deployment

git clone https://github.com/pypa/virtualenv.git 
git clone https://github.com/rootpy/rootpy.git

pushd virtualenv
./virtualenv.py --distribute ../vpython
popd

pushd vpython
source bin/activate
popd

pip install -e rootpy

cp $DOTBIN/.rootpy_env_setup.sh env.sh

popd