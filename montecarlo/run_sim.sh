#!/usr/bin/env bash
echo  "Start time: " `/bin/date`
echo "Job is running on node: " `/bin/hostname`
echo "Job running as user: " `/usr/bin/id`
echo "Job is running in directory: $PWD"

module load gcc/4.9.2
module load clhep/2.1.0.1
module load geant4/9.4p02
module load root/5.34-32
module load zlib/1.2.8
start_dir=$PWD
mkdir $start_dir/output
if [ "$OSG_WN_TMP" == "" ];
then
    OSG_WN_TMP=$PWD
fi
cd $OSG_WN_TMP
work_dir=`mktemp -d --tmpdir=$OSG_WN_TMP`
cp $start_dir/xenon1t.tar.gz $work_dir
cd $work_dir
mkdir work
cd work
tar xzf ../xenon1t.tar.gz
export G4WORKDIR="$PWD/xenon-work"
mkdir -p xenon-work/tmp/Linux-g++/xenon1t_v3.7A/exe/
cd xenon1t
make
if [ $? -ne 0 ];
then
  echo "Error compiling xenon1t code: " `/bin/date`
  echo "Job failed"
  exit 1
fi
cd  macros
/bin/cp -f $start_dir/*.mac .
$G4WORKDIR/bin/Linux-g++/xenon1t_v3.7A -p preinit.mac -f $2 -o $start_dir/output/output.$1.root -n 100
cd $start_dir
rm -fr $work_dir