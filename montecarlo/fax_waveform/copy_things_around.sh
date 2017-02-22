#!/bin/bash
file_header=/project/lgrandi/feigao/fax_data/ac_background/
datetime=$1
truth_dir=$file_header"$datetime/truth_minitrees_"$datetime
processed_dir=$file_header"$datetime/processed_minitrees_"$datetime
merged_dir=$file_header"$datetime/merged_minitrees_"$datetime
pax_dir=$file_header"$datetime/pax_"$datetime
peaks_dir=$file_header"$datetime/peak_minitrees_"$datetime
basics_dir=$file_header"$datetime/basics_minitrees_"$datetime

if [ -d "$truth_dir" ] || [ -d "$processed_dir" ]; then
    echo "minitree dirs already exist for $datetime; exiting..."
    exit
fi
mkdir $truth_dir
mkdir $processed_dir
mkdir $merged_dir
mkdir $pax_dir
mkdir $peaks_dir
mkdir $basics_dir
for dirname in $file_header$datetime"/0*"; do
    for filename in $dirname/*; do
        if [[ $filename =~ .*truth\.root$ ]]; then
            echo "moving $filename to truth minitree dir"
            mv $filename $truth_dir/
        elif [[ $filename =~ .*pax_Basics\.root$ ]]; then
            echo "moving $filename to basics minitree dir"
            mv $filename $basics_dir/
        elif [[ $filename =~ .*pax_.*\.root$ ]]; then
            echo "moving $filename to processed minitree dir"
            mv $filename $processed_dir/
        elif [[ $filename =~ .*pax\.root$ ]]; then
            echo "moving $filename to pax tree dir"
            mv $filename $pax_dir/
        fi
    done
done
if [[ $2 =~ kill ]]; then
    for dirname in $file_header$datetime"/0*"; do
        rm -rf $dirname
    done
fi
