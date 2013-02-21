#! /bin/bash
#echo $@

for i in $@
do
   dname=`dirname $i`
   bname=`basename $i`
   mv -v $dname/$bname $dname/.$bname
done
