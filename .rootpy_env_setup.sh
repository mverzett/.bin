export VIRTUAL_ENV_DISABLE_PROMPT=1
vpython=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd -P)/vpython
pushd $vpython
# See https://github.com/pypa/virtualenv/issues/150
source bin/activate
popd

export PYTHONPATH=$vpython/lib/python2.7/site-packages/:$PYTHONPATH
