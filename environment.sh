#general purpose aliases
alias la='ls -lah --color'
alias lt='ls -lrth --color'
alias lc='ls -h --color'
alias ll='ls -lh --color'

#.bin specific aliases
alias web='~/.bin/web.py'
alias hide='~/.bin/hide.sh'
alias show='~/.bin/reveal.sh'
alias term='kill -s SIGINT'
alias pyRoot="python -i -c 'execfile(\"/afs/hep.wisc.edu/home/mverzett/.bin/pyroot.py\")'"
alias pydbg="python -i -c 'execfile(\"/afs/cern.ch/user/m/mverzett/.bin/pyDebug.py\")'"
alias sc='scram b -j 4' 
alias startCrab='source /afs/cern.ch/cms/ccs/wm/scripts/Crab/crab.sh'
alias serialHadd='~/.bin/serialHadd.sh'
alias extDiff='~/.bin/extended_diff.sh'
alias rightLumi='lumiCalc2.py -norm pp7TeV overview -i'
