#################################################################
#
# Looper for multiple dataset processing
#
# First Input Argument:
#    0 - Dry run, producing directory structure and submit files
#    1 - Real submission, same as above except with submission
#    2 - Pull back results
#    3 - Concatenate ROOT files with 'hadd'
#
#################################################################

WORKDIR=${PWD}

PAX_VERSION=4.4.0

RUNS=(14 10)
LISTS=(3H_run14.txt 160202-Run10_datasets.txt)

SUBMITLOG=${PWD}/submit.log
rm -rf ${SUBMITLOG}

DATADIR=/stash2/project/@xenon1t/xenon100/archive/data

# Flag to submit jobs (1) or dry run (0)
PROCESS_FLAG=0

if [ "$1" != "" ]; then
    PROCESS_FLAG=$1
fi

if [ $PROCESS_FLAG -eq 3 ]; then
    module load ROOT
fi

irun=0
for run in ${RUNS[@]}
do

DIRS=(`cat ${LISTS[$irun]}`)

for dir in ${DIRS[@]}
do
    OUTDIR=output/run_${run}/${dir}

    mkdir -p ${OUTDIR}
    
    cd ${OUTDIR}

    if [ $PROCESS_FLAG -le 1 ]; then

	#ln -sf ${WORKDIR}/run_pax.sh .
	ln -sf ../../../run_pax.sh .  # Necessary if creating submit files on stash then submitting from Midway

	${WORKDIR}/./pax_process.py --pax-tarball pax-${PAX_VERSION}.tar.bz2  --run-directory ${DATADIR}/run_${run}/${dir} --outputfile_append _pax${PAX_VERSION} --batch-size 5 2>&1 | tee -a ${SUBMITLOG}
	
	if [ $PROCESS_FLAG -eq 1 ]; then
	    pwd
	    connect submit process_run.submit
	else
	    echo Fake connect submit ${OUTDIR}/process_run.submit
	fi

    elif [ $PROCESS_FLAG -eq 2 ]; then

	pwd
	connect pull

	
    elif [ $PROCESS_FLAG -eq 3 ]; then

	hadd -f ${dir}_pax${PAX_VERSION}.root ${dir}_*.root &
    fi
    
    cd -
    echo
done

irun=$(( $irun + 1 ))

done
