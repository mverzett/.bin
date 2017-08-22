export DOTBIN="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

#general purpose aliases
alias la='ls -lah --color'
alias lt='ls -lrth --color'
alias lc='ls -h --color'
alias ll='ls -lh --color'

#.bin specific aliases
export PATH=$DOTBIN:$PATH

alias term='kill -s SIGINT'
alias pyRoot="python -i -c 'execfile(\"$DOTBIN/pyroot.py\")'"
alias sc='scram b -j 4' 

#git aliases
alias git_ci='git commit -m'

#CMS aliases
alias proxy_init='voms-proxy-init -voms cms --valid 200:00'
