#!/bin/bash

# 压缩率随EB变化

# DIR--EB--FILE

SZ_PATH=/home/zhongyu/sz/sz1/bin
ZFP_PATH=/home/zhongyu/zfp/build/bin
TEST_DIR=/home/zhongyu/test
ERROR_BOUND_MODE=ABS
ERROR_BOUND_Fs="1E-1 1E-2 1E-3 1E-4 1E-5 1E-6 1E-7 1E-8 1E-9" # "1E-2 5E-3 1E-3 5E-4 1E-4 5E-5 1E-5 5E-6 1E-6 5E-7 1E-7" 
ERROR_BOUND_Ds="1E-1 1E-2 1E-3 1E-4 1E-5 1E-6 1E-7 1E-8 1E-9"
DIM=1
TYPE=f


output=./output/${ERROR_BOUND_MODE}.txt

dims=(1 1 1 1)

echo "START" > $output

float=0
num_of_pieces=0

for dir in `ls $TEST_DIR`
do
if [[ -d $TEST_DIR"/"$dir ]] && [[ $dir == "SMALL"* || $dir == "SDRBENCH"* ]]
then
# A dir
    array=(${dir//-/ }) 

    # Dimension
    dims=(${array[2]//x/ })
    # for var in ${dims[@]}
    # do
    #     echo $var
    # done
    DIM=${#dims[@]}

    # float or double
    TYPE=f
    type_len=4
    ERROR_BOUNDs=$ERROR_BOUND_Fs
    if [[ $dir == *"-d" ]]
    then
        TYPE=d
        type_len=8
        ERROR_BOUNDs=$ERROR_BOUND_Ds
    fi

    # file size
    i=0
    max=type_len
    while [ $i -lt $DIM ]
    do
        max=$(($max*${dims[$i]}))
        i=$(($i+1))
    done
    echo $max
    # if [ $max -lt 25600000 ]
    # then
    #     echo skip dir:$dir
    #     continue
    # fi

    echo " DIR: $dir"
    echo "DIR: $dir" >> $output

    test_name=${array[1]}

    # Dimension
    dims=(${array[2]//x/ })
    # for var in ${dims[@]}
    # do
    #     echo $var
    # done
    DIM=${#dims[@]}
    
    # reverse dims
    if [ $DIM == 2 ]
    then
        temp=${dims[0]}
        dims[0]=${dims[1]}
        dims[1]=$temp
    elif [ $DIM == 3 ]
    then
        temp=${dims[0]}
        dims[0]=${dims[2]}
        dims[2]=$temp
    elif [ $DIM == 4 ]
    then
        temp0=${dims[0]}
        temp1=${dims[1]}
        dims[0]=${dims[3]}
        dims[1]=${dims[2]}
        dims[2]=$temp1
        dims[3]=$temp0
    fi

    for ERROR_BOUND in $ERROR_BOUNDs
    do  
        echo "  EB: $ERROR_BOUND"
        echo "EB: $ERROR_BOUND" >> $output
        # file count
        cnt=0

        for file in `ls $TEST_DIR"/"$dir`
        do
            # A file    
            # echo ${dims[@]}

            if [[ $file == *".f32" ]] || [[ $file == *".dat" ]] || [[ $file == *".dat2" ]] || [[ $file == *".d64" ]] || [[ $file == *".bin" ]]
            then
                # filesize_origin=`ls -l $TEST_DIR"/"$dir"/"$file | awk '{print $5}'`
                echo "   FILE: $file"
                echo "FILE: $file" >> $output
                # # echo "float"
                # if [[ $filesize_origin -gt $filesize_set ]] || [[ $filesize_origin == $filesize_set ]] 
                # then
                #     filesize_origin=$filesize_set
                # else 
                #     continue
                # fi
                cnt=$[$cnt + 1]
                float=1

        # huffman
                echo "===huffman===" >> $output
            ## comp
                echo "$SZ_PATH"/"sz -z -$TYPE -g 0 -i $TEST_DIR"/"$dir"/"$file -M $ERROR_BOUND_MODE -A $ERROR_BOUND -$DIM ${dims[@]}"
                $SZ_PATH"/"sz -z -$TYPE -g 0 -i $TEST_DIR"/"$dir"/"$file -M $ERROR_BOUND_MODE -A $ERROR_BOUND -$DIM ${dims[@]} >> $output
                $SZ_PATH"/"sz -z -$TYPE -g 0 -i $TEST_DIR"/"$dir"/"$file -M $ERROR_BOUND_MODE -A $ERROR_BOUND -$DIM ${dims[@]} >> $output
                $SZ_PATH"/"sz -z -$TYPE -g 0 -i $TEST_DIR"/"$dir"/"$file -M $ERROR_BOUND_MODE -A $ERROR_BOUND -$DIM ${dims[@]} >> $output
                filesize_compressed=`ls -l $TEST_DIR"/"$dir"/"$file".sz" | awk '{print $5}'`
                echo "$filesize_compressed/$max" >> $output 
            ## decomp
                # echo "$SZ_PATH"/"sz -x -$TYPE -s $TEST_DIR"/"$dir"/"$file.sz -$DIM ${dims[@]}"
                $SZ_PATH"/"sz -x -$TYPE -s $TEST_DIR"/"$dir"/"$file.sz -$DIM ${dims[@]} >> $output
                $SZ_PATH"/"sz -x -$TYPE -s $TEST_DIR"/"$dir"/"$file.sz -$DIM ${dims[@]} >> $output
                $SZ_PATH"/"sz -x -$TYPE -s $TEST_DIR"/"$dir"/"$file.sz -$DIM ${dims[@]} >> $output

        # zfp
                echo "===zfp===" >> $output
            ## comp
                echo "$ZFP_PATH"/"zfp -$TYPE -i $TEST_DIR"/"$dir"/"$file -z $TEST_DIR"/"$dir"/"$file.zfp -a $ERROR_BOUND -$DIM ${dims[@]}"
                $ZFP_PATH"/"zfp -$TYPE -i $TEST_DIR"/"$dir"/"$file -z $TEST_DIR"/"$dir"/"$file.zfp -a $ERROR_BOUND -$DIM ${dims[@]} >> $output
                $ZFP_PATH"/"zfp -$TYPE -i $TEST_DIR"/"$dir"/"$file -z $TEST_DIR"/"$dir"/"$file.zfp -a $ERROR_BOUND -$DIM ${dims[@]} >> $output
                $ZFP_PATH"/"zfp -$TYPE -i $TEST_DIR"/"$dir"/"$file -z $TEST_DIR"/"$dir"/"$file.zfp -a $ERROR_BOUND -$DIM ${dims[@]} >> $output
                filesize_compressed=`ls -l $TEST_DIR"/"$dir"/"$file.zfp | awk '{print $5}'`
                echo "$filesize_compressed/$max" >> $output 
            ## decomp
                # echo "$ZFP_PATH"/"zfp -$TYPE -z $TEST_DIR"/"$dir"/"$file.zfp -o $TEST_DIR"/"$dir"/"$file.zfp.out -a $ERROR_BOUND -$DIM ${dims[@]}"
                $ZFP_PATH"/"zfp -$TYPE -z $TEST_DIR"/"$dir"/"$file.zfp -o $TEST_DIR"/"$dir"/"$file.zfp.out -a $ERROR_BOUND -$DIM ${dims[@]} >> $output
                $ZFP_PATH"/"zfp -$TYPE -z $TEST_DIR"/"$dir"/"$file.zfp -o $TEST_DIR"/"$dir"/"$file.zfp.out -a $ERROR_BOUND -$DIM ${dims[@]} >> $output
                $ZFP_PATH"/"zfp -$TYPE -z $TEST_DIR"/"$dir"/"$file.zfp -o $TEST_DIR"/"$dir"/"$file.zfp.out -a $ERROR_BOUND -$DIM ${dims[@]} >> $output
                
                rm -rf  $TEST_DIR"/"$dir"/"$file.zfp  $TEST_DIR"/"$dir"/"$file.zfp.out
        # fse
                echo "===fse===" >> $output
            ## comp
                # echo "$SZ_PATH"/"sz -z -$TYPE -g 2 -i $TEST_DIR"/"$dir"/"$file -M $ERROR_BOUND_MODE -A $ERROR_BOUND -$DIM ${dims[@]}"
                $SZ_PATH"/"sz -z -$TYPE -g 2 -i $TEST_DIR"/"$dir"/"$file -M $ERROR_BOUND_MODE -A $ERROR_BOUND -$DIM ${dims[@]} >> $output
                $SZ_PATH"/"sz -z -$TYPE -g 2 -i $TEST_DIR"/"$dir"/"$file -M $ERROR_BOUND_MODE -A $ERROR_BOUND -$DIM ${dims[@]} >> $output
                $SZ_PATH"/"sz -z -$TYPE -g 2 -i $TEST_DIR"/"$dir"/"$file -M $ERROR_BOUND_MODE -A $ERROR_BOUND -$DIM ${dims[@]} >> $output
                filesize_compressed=`ls -l $TEST_DIR"/"$dir"/"$file".sz" | awk '{print $5}'`
                echo "$filesize_compressed/$max" >> $output 
            ## decomp
                # echo "$SZ_PATH"/"sz -x -$TYPE -s $TEST_DIR"/"$dir"/"$file.sz -$DIM ${dims[@]}"
                $SZ_PATH"/"sz -x -$TYPE -s $TEST_DIR"/"$dir"/"$file.sz -$DIM ${dims[@]} >> $output
                $SZ_PATH"/"sz -x -$TYPE -s $TEST_DIR"/"$dir"/"$file.sz -$DIM ${dims[@]} >> $output
                $SZ_PATH"/"sz -x -$TYPE -s $TEST_DIR"/"$dir"/"$file.sz -$DIM ${dims[@]} >> $output
                
                rm -rf  $TEST_DIR"/"$dir"/"$file.sz  $TEST_DIR"/"$dir"/"$file.sz.out

            fi
            # A file
        done
        echo "CNT: $cnt" >> $output
        # one size
    done 
    echo " END DIR" #>> $output
fi
done

echo "FINISHED." >> $output
