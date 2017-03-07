#!/bin/sh

#number of Components
ncomp="15"

icomp="3"
while [ $icomp -le $ncomp ]
do

#number of Isotopes
niso="7"

iiso="0"

while [ $iiso -le $niso ]
do

./test $icomp $iiso

iiso=`expr $iiso + 1`
done

icomp=`expr $icomp + 1`
done

