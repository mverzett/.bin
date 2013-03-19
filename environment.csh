set SCRIPT=`readlink -f $0`
setenv DOTBIN `dirname $SCRIPT`
echo "Do you know that bash is much better?"

#general purpose aliases
alias la 'ls -lah --color'
alias lt 'ls -lrth --color'
alias lc 'ls -h --color'
alias ll 'ls -lh --color'

#.bin specific aliases
alias web '$DOTBIN/web.py'
alias hide '$DOTBIN/hide.sh'
alias show '$DOTBIN/reveal.sh'
alias term 'kill -s SIGINT'
alias pyRoot "python -i -c 'execfile(\"$DOTBIN/pyroot.py\")'"
alias pydbg "python -i -c 'execfile(\"/afs/cern.ch/user/m/mverzett/.bin/pyDebug.py\")'"
alias sc 'scram b -j 4' 
alias serialHadd '$DOTBIN/serialHadd.sh'
alias rootfind '$DOTBIN/rootfind.py'
alias calc '$DOTBIN/pycalc.py'
alias shroot '$DOTBIN/shroot.py'
