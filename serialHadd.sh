#! /bin/bash

# $1 -> TargetFile Name
# $2 -> castor dir where to find the files

targetBase=$1
castorDir=$2
nRootFiles=`nsls $castorDir | wc -l`
leftOver=$((`nsls $castorDir | wc -l` % 10))
#nsls $2 | awk '{print "rfio:/castor/cern.ch/user/m/mverzett/store/tauPUDzStudies/dzCut0_2/"$1}'

for nLines in $(seq 10 10 $nRootFiles); do

    printList=`nsls $castorDir | awk '{print "rfio:/castor/cern.ch/user/m/mverzett/"v1$1}' v1=$castorDir | head -n $nLines | tail -n 10`
    target=`echo -n $targetBase'_'$nLines'.root'`
    hadd $target $printList &
done
lastTarget=`echo -n $targetBase'_last.root'`
hadd $lastTarget `nsls $2 | awk '{print "rfio:/castor/cern.ch/user/m/mverzett/store/tauPUDzStudies/dzCut0_2/"v1$1}' v1=$castorDir | tail -n $leftOver` &