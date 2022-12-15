#!/bin/bash

# 压缩率随EB变化

# DIR--EB--FILE

SZ_PATH=/home/zhongyu/sz/sz1/bin
TEST_DIR=/home/zhongyu/test
ERROR_BOUND_MODE=ABS
ERROR_BOUND_Fs="1 2 3 4 5 1E-2 1E-3 1E-4 1E-5" # "1E-2 5E-3 1E-3 5E-4 1E-4 5E-5 1E-5 5E-6 1E-6 5E-7 1E-7" 
ERROR_BOUND_D="1E-7"
DIM=1
TYPE=f

filesize_set_KBs="1048576 262144 65536 16384 4096 1024 256 64 16"

test() {
    echo $1 start
    for ERROR_BOUND_F in $ERROR_BOUND_Fs
    do
        output=$ERROR_BOUND_F
        echo $1:$output
    done
    echo $1 end
}

for filesize in $filesize_set_KBs
do
    test $filesize &
done

