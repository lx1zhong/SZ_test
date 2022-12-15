#!/bin/bash

# 清除piece文件

TEST_DIR=/home/zhongyu/test

for dir in `ls $TEST_DIR`
do
    if [[ -d $TEST_DIR"/"$dir ]] && [[ $dir == "1SDRBENCH"* ]] # || $dir == "SMALL"* 
    then
    # A dir

        for file in `ls $TEST_DIR"/"$dir`
        do
            
            if [[ $file == "piece"* ]]
            then
               
                echo rm -f $TEST_DIR"/"$dir"/"$file
                # delete all pieces
                rm -f $TEST_DIR"/"$dir"/"$file
                
            fi
            # A file
        done
        # one size
    fi
    echo " END DIR"

echo "FINISHED."
done
