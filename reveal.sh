#! /bin/bash

for i in $@
do
   dname=`dirname $i`
   bname=`basename $i`
   newbname=`echo $bname | sed 's/\.//'`
   mv -v $dname/$bname $dname/$newbname
done
