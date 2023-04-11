#!/bin/bash

SZ_PATH=../../sz_install/bin
TEST_FILE=../../data/SDRBENCH-EXAALT-2869440-f/vx.dat2
TEST_DIR=../../data/SDRBENCH-EXAALT-2869440-f
DIM=1
filesize_set_rows="2869440"


output=./output/result.txt
echo "START" > $output
run() {
    echo "EBMODE: $ERROR_BOUND_MODE" >> $output
    for ERROR_BOUND in $ERROR_BOUNDs
    do
        echo "EB: $ERROR_BOUND" >> $output
        for file in `ls $TEST_DIR`
        do
            # A file    
            # echo ${dims[@]}

            if [[ $file == *".f32" ]] || [[ $file == *".dat" ]] || [[ $file == *".dat2" ]] || [[ $file == *".d64" ]] || [[ $file == *".bin" ]]
            then
                filesize_origin=`ls -l $TEST_DIR"/"$file | awk '{print $5}'`
                # filesize_origin=`ls -l $TEST_DIR"/"$dir"/"$file | awk '{print $5}'`
                echo "FILE: $file" >> $output
                echo "===huffman===" >> $output
                # echo "---compress---"
                echo "sz -z -f -g 0 -i $TEST_DIR"/"$file -M $ERROR_BOUND_MODE -$PPP $ERROR_BOUND -$DIM $filesize_set_rows"
                $SZ_PATH"/bin/"sz -z -f -g 0 -i $TEST_DIR"/"$file -M $ERROR_BOUND_MODE -$PPP $ERROR_BOUND -$DIM $filesize_set_rows >> $output
                $SZ_PATH"/bin/"sz -z -f -g 0 -i $TEST_DIR"/"$file -M $ERROR_BOUND_MODE -$PPP $ERROR_BOUND -$DIM $filesize_set_rows >> $output
                $SZ_PATH"/bin/"sz -z -f -g 0 -i $TEST_DIR"/"$file -M $ERROR_BOUND_MODE -$PPP $ERROR_BOUND -$DIM $filesize_set_rows >> $output
                filesize_compressed=`ls -l $TEST_DIR"/"$file".sz" | awk '{print $5}'`
                echo "$filesize_compressed/$filesize_origin" >> $output

                # echo "---decompress---"
                # # echo "$SZ_PATH"/bin/"sz -x -f -s $TEST_DIR"/"$file.sz -1 $filesize_set_rows"
                $SZ_PATH"/bin/"sz -x -f -s $TEST_DIR"/"$file.sz -$DIM $filesize_set_rows >> $output
                $SZ_PATH"/bin/"sz -x -f -s $TEST_DIR"/"$file.sz -$DIM $filesize_set_rows >> $output
                $SZ_PATH"/bin/"sz -x -f -s $TEST_DIR"/"$file.sz -$DIM $filesize_set_rows >> $output


                echo "===fse===" >> $output
                # echo "---compress---"
                # echo "$SZ_PATH"/bin/"sz -z -f -g 2 -i $TEST_DIR"/"$file -M $ERROR_BOUND_MODE -$PPP $ERROR_BOUND -$DIM $filesize_set_rows"
                $SZ_PATH"/bin/"sz -z -f -g 2 -i $TEST_DIR"/"$file -M $ERROR_BOUND_MODE -$PPP $ERROR_BOUND -$DIM $filesize_set_rows >> $output
                $SZ_PATH"/bin/"sz -z -f -g 2 -i $TEST_DIR"/"$file -M $ERROR_BOUND_MODE -$PPP $ERROR_BOUND -$DIM $filesize_set_rows >> $output
                $SZ_PATH"/bin/"sz -z -f -g 2 -i $TEST_DIR"/"$file -M $ERROR_BOUND_MODE -$PPP $ERROR_BOUND -$DIM $filesize_set_rows >> $output
                filesize_compressed=`ls -l $TEST_DIR"/"$file".sz" | awk '{print $5}'`
                echo "$filesize_compressed/$filesize_origin" >> $output
                # echo `echo "scale=6;$filesize_origin/$filesize_compressed" | bc` >> $output

                # echo "--decompress---"
                # echo "$SZ_PATH"/bin/"sz -x -f -s $TEST_DIR"/"$file.sz -$DIM $filesize_set_rows"
                $SZ_PATH"/bin/"sz -x -f -s $TEST_DIR"/"$file.sz -$DIM $filesize_set_rows  >> $output
                $SZ_PATH"/bin/"sz -x -f -s $TEST_DIR"/"$file.sz -$DIM $filesize_set_rows  >> $output
                $SZ_PATH"/bin/"sz -x -f -s $TEST_DIR"/"$file.sz -$DIM $filesize_set_rows  >> $output

                rm -rf $TEST_DIR"/"$file.sz $TEST_DIR"/"$file.sz.out
            fi
        done
        echo "CNT:" >> $output
    done
}

ERROR_BOUND_MODE=REL
PPP=R
ERROR_BOUNDs="1E-1 1E-2 1E-3 1E-4 1E-5"
run

ERROR_BOUND_MODE=PW_REL
PPP=P
ERROR_BOUNDs="1E-1 1E-2 1E-3 1E-4 1E-5"
run

ERROR_BOUND_MODE=PSNR
PPP=S
ERROR_BOUNDs="40 60 80 100 120"
run 

ERROR_BOUND_MODE=NORM
PPP=N
ERROR_BOUNDs="1E5 1E4 1E3 1E2 1E1"
run

echo "FINISHED." >> $output