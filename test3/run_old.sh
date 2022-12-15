#!/bin/bash

SZ_PATH=/home/zhongyu/sz/sz2
TEST_FILE=/home/zhongyu/test/SDRBENCH-EXAALT_HELIUM-7852x1037-f/dataset1-7852x1037.x.f32.dat
DIM=2
filesize_set_rows="1037 7852"

echo $TEST_FILE
output=/home/zhongyu/test/paper_test/test3/EXAALT_HELIUM.txt
echo "START" > $output
run() {
    echo "EBMODE: $ERROR_BOUND_MODE" >> $output
    for ERROR_BOUND in $ERROR_BOUNDs
    do
        echo "EB: $ERROR_BOUND" >> $output
        filesize_origin=`ls -l $TEST_FILE | awk '{print $5}'`
        # filesize_origin=`ls -l $TEST_FILE | awk '{print $5}'`
        # echo "$SZ_PATH"/bin/"sz -z -f -g 2 -i $TEST_FILE -M $ERROR_BOUND_MODE -$PPP $ERROR_BOUND -$DIM $filesize_set_rows"
        $SZ_PATH"/bin/"sz -z -f -e -g 2 -i $TEST_FILE -M $ERROR_BOUND_MODE -$PPP $ERROR_BOUND -$DIM $filesize_set_rows >> $output
        filesize_compressed=`ls -l $TEST_FILE".sz" | awk '{print $5}'`
        # echo "$filesize_compressed/$filesize_origin" >> $output
        echo `echo "scale=6;$filesize_origin/$filesize_compressed" | bc` >> $output

        rm -rf $TEST_FILE.sz
    done
}

ERROR_BOUND_MODE=ABS
PPP=A
ERROR_BOUNDs="1E-1 1E-2 1E-3 1E-4 1E-5"
run

ERROR_BOUND_MODE=REL
PPP=R
ERROR_BOUNDs="1E-2 1E-3 1E-4 1E-5 1E-6"
run

ERROR_BOUND_MODE=PW_REL
PPP=P
ERROR_BOUNDs="1E-2 1E-3 1E-4 1E-5"
run

ERROR_BOUND_MODE=PSNR
PPP=S
ERROR_BOUNDs="40 60 80 100 120"
run 

echo "FINISHED." >> $output

SZ_PATH=/home/zhongyu/sz/sz2
TEST_FILE=/home/zhongyu/test/SDRBENCH-CESM_ATM-1800x3600-f/FSNSC_1_1800_3600.f32
DIM=2
filesize_set_rows="3600 1800"


echo $TEST_FILE
output=/home/zhongyu/test/paper_test/test3/CESM_ATM.txt
echo "START" > $output
run() {
    echo "EBMODE: $ERROR_BOUND_MODE" >> $output
    for ERROR_BOUND in $ERROR_BOUNDs
    do
        echo "EB: $ERROR_BOUND" >> $output
        filesize_origin=`ls -l $TEST_FILE | awk '{print $5}'`
        # filesize_origin=`ls -l $TEST_FILE | awk '{print $5}'`
        # echo "$SZ_PATH"/bin/"sz -z -f -g 2 -i $TEST_FILE -M $ERROR_BOUND_MODE -$PPP $ERROR_BOUND -$DIM $filesize_set_rows"
        $SZ_PATH"/bin/"sz -z -f -e -g 2 -i $TEST_FILE -M $ERROR_BOUND_MODE -$PPP $ERROR_BOUND -$DIM $filesize_set_rows >> $output
        filesize_compressed=`ls -l $TEST_FILE".sz" | awk '{print $5}'`
        # echo "$filesize_compressed/$filesize_origin" >> $output
        echo `echo "scale=6;$filesize_origin/$filesize_compressed" | bc` >> $output

        rm -rf $TEST_FILE.sz
    done
}

ERROR_BOUND_MODE=ABS
PPP=A
ERROR_BOUNDs="1E-1 1E-2 1E-3 1E-4 1E-5"
run

ERROR_BOUND_MODE=REL
PPP=R
ERROR_BOUNDs="1E-2 1E-3 1E-4 1E-5 1E-6"
run

ERROR_BOUND_MODE=PW_REL
PPP=P
ERROR_BOUNDs="1E-2 1E-3 1E-4 1E-5"
run

ERROR_BOUND_MODE=PSNR
PPP=S
ERROR_BOUNDs="40 60 80 100 120"
run 

echo "FINISHED." >> $output

SZ_PATH=/home/zhongyu/sz/sz2
TEST_FILE=/home/zhongyu/test/SDRBENCH-EXAALT-2869440-f/vx.dat2
TEST_DIR=/home/zhongyu/test/SDRBENCH-EXAALT-2869440-f
DIM=1
filesize_set_rows="2869440"


echo $TEST_FILE
output=/home/zhongyu/test/paper_test/test3/EXAALT.txt
echo "START" > $output
run() {
    echo "EBMODE: $ERROR_BOUND_MODE" >> $output
    for ERROR_BOUND in $ERROR_BOUNDs
    do
        echo "EB: $ERROR_BOUND" >> $output
        filesize_origin=`ls -l $TEST_FILE | awk '{print $5}'`
        # filesize_origin=`ls -l $TEST_FILE | awk '{print $5}'`
        # echo "$SZ_PATH"/bin/"sz -z -f -g 2 -i $TEST_FILE -M $ERROR_BOUND_MODE -$PPP $ERROR_BOUND -$DIM $filesize_set_rows"
        $SZ_PATH"/bin/"sz -z -f -e -g 2 -i $TEST_FILE -M $ERROR_BOUND_MODE -$PPP $ERROR_BOUND -$DIM $filesize_set_rows >> $output
        filesize_compressed=`ls -l $TEST_FILE".sz" | awk '{print $5}'`
        # echo "$filesize_compressed/$filesize_origin" >> $output
        echo `echo "scale=6;$filesize_origin/$filesize_compressed" | bc` >> $output

        rm -rf $TEST_FILE.sz
    done
}

ERROR_BOUND_MODE=ABS
PPP=A
ERROR_BOUNDs="1E-1 1E-2 1E-3 1E-4 1E-5"
run

ERROR_BOUND_MODE=REL
PPP=R
ERROR_BOUNDs="1E-2 1E-3 1E-4 1E-5 1E-6"
run

ERROR_BOUND_MODE=PW_REL
PPP=P
ERROR_BOUNDs="1E-2 1E-3 1E-4 1E-5"
run

ERROR_BOUND_MODE=PSNR
PPP=S
ERROR_BOUNDs="40 60 80 100 120"
run 

echo "FINISHED." >> $output