#!/bin/bash

output=/home/zhongyu/test/paper_test/test3/output/SZ-5.txt
output2=/home/zhongyu/test/paper_test/test3/output/SZ_ADT-5.txt


SZ_PATH=/home/zhongyu/sz/sz2
TEST_FILE=/home/zhongyu/test/SDRBENCH-EXAALT-2869440-f/vx.dat2
DIM=1
filesize_set_rows="2869440"

echo $TEST_FILE
echo "DAT: EXAALT" > $output
run() {
    echo "EBMODE: $ERROR_BOUND_MODE" >> $output
    for ERROR_BOUND in $ERROR_BOUNDs
    do
        echo "EB: $ERROR_BOUND" >> $output
        filesize_origin=`ls -l $TEST_FILE | awk '{print $5}'`
        # filesize_origin=`ls -l $TEST_FILE | awk '{print $5}'`
        # echo "$SZ_PATH"/bin/"sz -z -f -g 0 -i $TEST_FILE -M $ERROR_BOUND_MODE -$PPP $ERROR_BOUND -$DIM $filesize_set_rows"
        $SZ_PATH"/bin/"sz -z -f -e -g 0 -i $TEST_FILE -M $ERROR_BOUND_MODE -$PPP $ERROR_BOUND -$DIM $filesize_set_rows >> $output
        $SZ_PATH"/bin/"sz -z -f -g 0 -i $TEST_FILE -M $ERROR_BOUND_MODE -$PPP $ERROR_BOUND -$DIM $filesize_set_rows >> $output
        filesize_compressed=`ls -l $TEST_FILE".sz" | awk '{print $5}'`
        # echo "$filesize_compressed/$filesize_origin" >> $output
        echo "[ratio]:  "`echo "scale=6;$filesize_origin/$filesize_compressed" | bc` >> $output

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


echo "CNT." >> $output

SZ_PATH=/home/zhongyu/sz/sz2
TEST_FILE=/home/zhongyu/test/SDRBENCH-EXAALT_HELIUM-7852x1037-f/dataset1-7852x1037.x.f32.dat
DIM=2
filesize_set_rows="1037 7852"

echo $TEST_FILE
echo "DAT: EXAALT_HELIUM" >> $output
run() {
    echo "EBMODE: $ERROR_BOUND_MODE" >> $output
    for ERROR_BOUND in $ERROR_BOUNDs
    do
        echo "EB: $ERROR_BOUND" >> $output
        filesize_origin=`ls -l $TEST_FILE | awk '{print $5}'`
        # filesize_origin=`ls -l $TEST_FILE | awk '{print $5}'`
        # echo "$SZ_PATH"/bin/"sz -z -f -g 0 -i $TEST_FILE -M $ERROR_BOUND_MODE -$PPP $ERROR_BOUND -$DIM $filesize_set_rows"
        $SZ_PATH"/bin/"sz -z -f -e -g 0 -i $TEST_FILE -M $ERROR_BOUND_MODE -$PPP $ERROR_BOUND -$DIM $filesize_set_rows >> $output
        $SZ_PATH"/bin/"sz -z -f -g 0 -i $TEST_FILE -M $ERROR_BOUND_MODE -$PPP $ERROR_BOUND -$DIM $filesize_set_rows >> $output
        filesize_compressed=`ls -l $TEST_FILE".sz" | awk '{print $5}'`
        # echo "$filesize_compressed/$filesize_origin" >> $output
        echo "[ratio]:  "`echo "scale=6;$filesize_origin/$filesize_compressed" | bc` >> $output

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


echo "CNT." >> $output

SZ_PATH=/home/zhongyu/sz/sz2
TEST_FILE=/home/zhongyu/test/SDRBENCH-CESM_ATM-1800x3600-f/FSNSC_1_1800_3600.f32
DIM=2
filesize_set_rows="3600 1800"


echo $TEST_FILE
echo "DAT: CESM_ATM" >> $output
run() {
    echo "EBMODE: $ERROR_BOUND_MODE" >> $output
    for ERROR_BOUND in $ERROR_BOUNDs
    do
        echo "EB: $ERROR_BOUND" >> $output
        filesize_origin=`ls -l $TEST_FILE | awk '{print $5}'`
        # filesize_origin=`ls -l $TEST_FILE | awk '{print $5}'`
        # echo "$SZ_PATH"/bin/"sz -z -f -g 0 -i $TEST_FILE -M $ERROR_BOUND_MODE -$PPP $ERROR_BOUND -$DIM $filesize_set_rows"
        $SZ_PATH"/bin/"sz -z -f -e -g 0 -i $TEST_FILE -M $ERROR_BOUND_MODE -$PPP $ERROR_BOUND -$DIM $filesize_set_rows >> $output
        $SZ_PATH"/bin/"sz -z -f -g 0 -i $TEST_FILE -M $ERROR_BOUND_MODE -$PPP $ERROR_BOUND -$DIM $filesize_set_rows >> $output
        filesize_compressed=`ls -l $TEST_FILE".sz" | awk '{print $5}'`
        # echo "$filesize_compressed/$filesize_origin" >> $output
        echo "[ratio]:  "`echo "scale=6;$filesize_origin/$filesize_compressed" | bc` >> $output

        rm -rf $TEST_FILE.sz
    done
}


ERROR_BOUND_MODE=ABS
PPP=A
ERROR_BOUNDs="1E-1 1E-2 1E-3 1E-4 1E-5"
run

ERROR_BOUND_MODE=REL
PPP=R
ERROR_BOUNDs="1E-3 1E-4 1E-5 1E-6"
run

ERROR_BOUND_MODE=PW_REL
PPP=P
ERROR_BOUNDs="1E-3 1E-4 1E-5"
run

ERROR_BOUND_MODE=PSNR
PPP=S
ERROR_BOUNDs="60 80 100 120"
run 

echo "CNT." >> $output

SZ_PATH=/home/zhongyu/sz/sz2
TEST_FILE=/home/zhongyu/test/SMALL-eddy_velx_f4-282616-d/eddy_velx_f4.dat
DIM=1
filesize_set_rows="282616"

echo $TEST_FILE
echo "DAT: eddy_velx_f4" >> $output
run() {
    echo "EBMODE: $ERROR_BOUND_MODE" >> $output
    for ERROR_BOUND in $ERROR_BOUNDs
    do
        echo "EB: $ERROR_BOUND" >> $output
        filesize_origin=`ls -l $TEST_FILE | awk '{print $5}'`
        # filesize_origin=`ls -l $TEST_FILE | awk '{print $5}'`
        # echo "$SZ_PATH"/bin/"sz -z -d -g 0 -i $TEST_FILE -M $ERROR_BOUND_MODE -$PPP $ERROR_BOUND -$DIM $filesize_set_rows"
        $SZ_PATH"/bin/"sz -z -d -e -g 0 -i $TEST_FILE -M $ERROR_BOUND_MODE -$PPP $ERROR_BOUND -$DIM $filesize_set_rows >> $output
        $SZ_PATH"/bin/"sz -z -d -g 0 -i $TEST_FILE -M $ERROR_BOUND_MODE -$PPP $ERROR_BOUND -$DIM $filesize_set_rows >> $output
        filesize_compressed=`ls -l $TEST_FILE".sz" | awk '{print $5}'`
        # echo "$filesize_compressed/$filesize_origin" >> $output
        echo "[ratio]:  "`echo "scale=6;$filesize_origin/$filesize_compressed" | bc` >> $output

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
ERROR_BOUNDs="60 80 100 120"
run 


echo "FINISHED." >> $output

# FSE

SZ_PATH=/home/zhongyu/sz/sz2
TEST_FILE=/home/zhongyu/test/SDRBENCH-EXAALT-2869440-f/vx.dat2
DIM=1
filesize_set_rows="2869440"

echo $TEST_FILE
echo "DAT: EXAALT" > $output2
run() {
    echo "EBMODE: $ERROR_BOUND_MODE" >> $output2
    for ERROR_BOUND in $ERROR_BOUNDs
    do
        echo "EB: $ERROR_BOUND" >> $output2
        filesize_origin=`ls -l $TEST_FILE | awk '{print $5}'`
        # filesize_origin=`ls -l $TEST_FILE | awk '{print $5}'`
        # echo "$SZ_PATH"/bin/"sz -z -f -g 2 -i $TEST_FILE -M $ERROR_BOUND_MODE -$PPP $ERROR_BOUND -$DIM $filesize_set_rows"
        $SZ_PATH"/bin/"sz -z -f -e -g 2 -i $TEST_FILE -M $ERROR_BOUND_MODE -$PPP $ERROR_BOUND -$DIM $filesize_set_rows >> $output2
        $SZ_PATH"/bin/"sz -z -f -g 2 -i $TEST_FILE -M $ERROR_BOUND_MODE -$PPP $ERROR_BOUND -$DIM $filesize_set_rows >> $output2
        filesize_compressed=`ls -l $TEST_FILE".sz" | awk '{print $5}'`
        # echo "$filesize_compressed/$filesize_origin" >> $output2
        echo "[ratio]:  "`echo "scale=6;$filesize_origin/$filesize_compressed" | bc` >> $output2

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


echo "CNT." >> $output2

SZ_PATH=/home/zhongyu/sz/sz2
TEST_FILE=/home/zhongyu/test/SDRBENCH-EXAALT_HELIUM-7852x1037-f/dataset1-7852x1037.x.f32.dat
DIM=2
filesize_set_rows="1037 7852"

echo $TEST_FILE
echo "DAT: EXAALT_HELIUM" >> $output2
run() {
    echo "EBMODE: $ERROR_BOUND_MODE" >> $output2
    for ERROR_BOUND in $ERROR_BOUNDs
    do
        echo "EB: $ERROR_BOUND" >> $output2
        filesize_origin=`ls -l $TEST_FILE | awk '{print $5}'`
        # filesize_origin=`ls -l $TEST_FILE | awk '{print $5}'`
        # echo "$SZ_PATH"/bin/"sz -z -f -g 2 -i $TEST_FILE -M $ERROR_BOUND_MODE -$PPP $ERROR_BOUND -$DIM $filesize_set_rows"
        $SZ_PATH"/bin/"sz -z -f -e -g 2 -i $TEST_FILE -M $ERROR_BOUND_MODE -$PPP $ERROR_BOUND -$DIM $filesize_set_rows >> $output2
        $SZ_PATH"/bin/"sz -z -f -g 2 -i $TEST_FILE -M $ERROR_BOUND_MODE -$PPP $ERROR_BOUND -$DIM $filesize_set_rows >> $output2
        filesize_compressed=`ls -l $TEST_FILE".sz" | awk '{print $5}'`
        # echo "$filesize_compressed/$filesize_origin" >> $output2
        echo "[ratio]:  "`echo "scale=6;$filesize_origin/$filesize_compressed" | bc` >> $output2

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

echo "CNT." >> $output2

SZ_PATH=/home/zhongyu/sz/sz2
TEST_FILE=/home/zhongyu/test/SDRBENCH-CESM_ATM-1800x3600-f/FSNSC_1_1800_3600.f32
DIM=2
filesize_set_rows="3600 1800"


echo $TEST_FILE
echo "DAT: CESM_ATM" >> $output2
run() {
    echo "EBMODE: $ERROR_BOUND_MODE" >> $output2
    for ERROR_BOUND in $ERROR_BOUNDs
    do
        echo "EB: $ERROR_BOUND" >> $output2
        filesize_origin=`ls -l $TEST_FILE | awk '{print $5}'`
        # filesize_origin=`ls -l $TEST_FILE | awk '{print $5}'`
        # echo "$SZ_PATH"/bin/"sz -z -f -g 2 -i $TEST_FILE -M $ERROR_BOUND_MODE -$PPP $ERROR_BOUND -$DIM $filesize_set_rows"
        $SZ_PATH"/bin/"sz -z -f -e -g 2 -i $TEST_FILE -M $ERROR_BOUND_MODE -$PPP $ERROR_BOUND -$DIM $filesize_set_rows >> $output2
        $SZ_PATH"/bin/"sz -z -f -g 2 -i $TEST_FILE -M $ERROR_BOUND_MODE -$PPP $ERROR_BOUND -$DIM $filesize_set_rows >> $output2
        filesize_compressed=`ls -l $TEST_FILE".sz" | awk '{print $5}'`
        # echo "$filesize_compressed/$filesize_origin" >> $output2
        echo "[ratio]:  "`echo "scale=6;$filesize_origin/$filesize_compressed" | bc` >> $output2

        rm -rf $TEST_FILE.sz
    done
}


ERROR_BOUND_MODE=ABS
PPP=A
ERROR_BOUNDs="1E-1 1E-2 1E-3 1E-4 1E-5"
run

ERROR_BOUND_MODE=REL
PPP=R
ERROR_BOUNDs="1E-3 1E-4 1E-5 1E-6"
run

ERROR_BOUND_MODE=PW_REL
PPP=P
ERROR_BOUNDs="1E-3 1E-4 1E-5"
run

ERROR_BOUND_MODE=PSNR
PPP=S
ERROR_BOUNDs="60 80 100 120"
run 


echo "CNT." >> $output2

SZ_PATH=/home/zhongyu/sz/sz2
TEST_FILE=/home/zhongyu/test/SMALL-eddy_velx_f4-282616-d/eddy_velx_f4.dat
DIM=1
filesize_set_rows="282616"

echo $TEST_FILE
echo "DAT: eddy_velx_f4" >> $output2
run() {
    echo "EBMODE: $ERROR_BOUND_MODE" >> $output2
    for ERROR_BOUND in $ERROR_BOUNDs
    do
        echo "EB: $ERROR_BOUND" >> $output2
        filesize_origin=`ls -l $TEST_FILE | awk '{print $5}'`
        # filesize_origin=`ls -l $TEST_FILE | awk '{print $5}'`
        # echo "$SZ_PATH"/bin/"sz -z -d -g 2 -i $TEST_FILE -M $ERROR_BOUND_MODE -$PPP $ERROR_BOUND -$DIM $filesize_set_rows"
        $SZ_PATH"/bin/"sz -z -d -e -g 2 -i $TEST_FILE -M $ERROR_BOUND_MODE -$PPP $ERROR_BOUND -$DIM $filesize_set_rows >> $output2
        $SZ_PATH"/bin/"sz -z -d -g 2 -i $TEST_FILE -M $ERROR_BOUND_MODE -$PPP $ERROR_BOUND -$DIM $filesize_set_rows >> $output2
        filesize_compressed=`ls -l $TEST_FILE".sz" | awk '{print $5}'`
        # echo "$filesize_compressed/$filesize_origin" >> $output2
        echo "[ratio]:  "`echo "scale=6;$filesize_origin/$filesize_compressed" | bc` >> $output2

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
ERROR_BOUNDs="60 80 100 120"
run 


echo "FINISHED." >> $output2
