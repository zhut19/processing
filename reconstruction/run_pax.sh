#!/usr/bin/env bash

# takes 4 arguments:
# arg1 -- pax version number (must be pre-installed on OASIS/OSG)
# arg2 -- name of input files separated by commas
# arg3 -- name of output files separated by commas
# arg4 -- pax configuration to use (allowed values given by 'paxer --help', or pass a .ini for custom config file)

which gfal-copy > /dev/null 2>&1
if [[ $? -eq 1 ]];
then
    source /cvmfs/oasis.opensciencegrid.org/osg-software/osg-wn-client/3.3/current/el6-x86_64/setup.sh
    export GFAL_CONFIG_DIR=$OSG_LOCATION/etc/gfal2.d
    export GFAL_PLUGIN_DIR=$OSG_LOCATION/usr/lib64/gfal2-plugins/
else
    # Not ideal but some sites don't have the gfal config and plug directories =(
    if [[ ! -d /etc//etc/gfal2.d ]];
    then
        OSG_LOCATION=`source /cvmfs/oasis.opensciencegrid.org/osg-software/osg-wn-client/3.3/current/el6-x86_64/setup.sh; env | grep OSG_LOCATION | cut -f 2 -d=`
        export GFAL_CONFIG_DIR=$OSG_LOCATION/etc/gfal2.d
    fi
    if [[ ! -d /usr/lib64/gfal2-plugins/ ]];
    then
        OSG_LOCATION=`source /cvmfs/oasis.opensciencegrid.org/osg-software/osg-wn-client/3.3/current/el6-x86_64/setup.sh; env | grep OSG_LOCATION | cut -f 2 -d=`
        export GFAL_PLUGIN_DIR=$OSG_LOCATION/usr/lib64/gfal2-plugins/
    fi
fi


start_dir=$PWD
if [ "${OSG_WN_TMP}" == "" ];
then
    OSG_WN_TMP=$PWD
fi

cd ${OSG_WN_TMP}
work_dir=`mktemp -d --tmpdir=${OSG_WN_TMP}`
cd ${work_dir}
IFS=',' read -r -a input_files <<< "$2"
IFS=',' read -r -a output_files <<< "$3"
IFS=',' read -r -a configs <<< "$4"

mkdir ${start_dir}/results
# loop and use gfal-copy before pax gets loaded to avoid
# gfal using wrong python version/libraries
for index in "${!input_files[@]}";
do
    input_filename=`echo ${input_files[index]} | rev | cut -f 1 -d/ | rev`
    gfal-copy -n2 --cert ${start_dir}/user_cert ${input_files[index]} file://${work_dir}/$input_filename
done

# load python modules for paxer
module load pax/$1
source activate pax-$1

for index in "${!input_files[@]}";
do
    input_filename=`echo ${input_files[index]} | rev | cut -f 1 -d/ | rev`

    if [[ ${configs[index]} == *".ini"* ]]; then
        pax_config="--config_path ${start_dir}/${configs[index]}"
    else
        pax_config="--config ${configs[index]}"
    fi

    echo paxer --input $input_filename --output ${output_files[index]} --output_type root ${pax_config}
    paxer --input $input_filename --output ${output_files[index]} --output_type root ${pax_config} --stop_after 2

done
cp *.root ${start_dir}/results
cd ${start_dir}

rm -fr ${work_dir}
