export DOTBIN="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

#general purpose aliases
alias la='ls -lah --color'
alias lt='ls -lrth --color'
alias lc='ls -h --color'
alias ll='ls -lh --color'

#.bin specific aliases
alias web='$DOTBIN/web.py'
alias hide='$DOTBIN/hide.sh'
alias show='$DOTBIN/reveal.sh'
alias hist2txt='$DOTBIN/hist2txt.py'
alias term='kill -s SIGINT'
alias pyRoot="python -i -c 'execfile(\"$DOTBIN/pyroot.py\")'"
alias pydbg="python -i -c 'execfile(\"/afs/cern.ch/user/m/mverzett/.bin/pyDebug.py\")'"
alias sc='scram b -j 4' 
alias serialHadd='$DOTBIN/hierarchicalHadd.py'
alias rootfind='$DOTBIN/rootfind.py'
alias calc='$DOTBIN/pycalc.sh'
alias shroot='$DOTBIN/shroot.py'
alias dump_branch_names='$DOTBIN/dump_branch_names.py'
alias hcompare='$DOTBIN/hcompare.py'
alias rootfs='$DOTBIN/rootfs.py'

#git aliases
alias git_ci='git commit -m'

#CMS aliases
alias proxy_init='voms-proxy-init -voms cms --valid 200:00'
