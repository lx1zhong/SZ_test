#!/bin/bash

# 压缩率随压缩粒度的变化

# DIR--SIZE--FILE

SZ_PATH=/home/zhongyu/sz/sz1/bin
TEST_DIR=/home/zhongyu/test
ERROR_BOUND_MODE=PW_REL
ERROR_BOUND_Fs="1E-2 1E-3 1E-4" # "1E-2 5E-3 1E-3 5E-4 1E-4 5E-5 1E-5 5E-6 1E-6 5E-7 1E-7" 
filesize_set_KBs="1048576 262144 65536 16384 4096 1024 256 64 16"

run(){

    thread_dir=/home/zhongyu/p${ERROR_BOUND_F}
    mkdir $thread_dir
    rm -rf $thread_dir/*

    DIM=1
    TYPE=f
    output=/home/zhongyu/test/paper_test/test1/1/output/${ERROR_BOUND_MODE}_${ERROR_BOUND_F}.txt
    echo $ERROR_BOUND_F

    dims=(1 1 1 1)

    echo "START" > $output

    float=0
    num_of_pieces=0

    for dir in `ls $TEST_DIR`
    do
    if [[ -d $TEST_DIR"/"$dir ]] && [[ $dir == "SDRBENCH"* ]] # || $dir == "SMALL"* 
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
        ERROR_BOUND=$ERROR_BOUND_F
        if [[ $dir == *"-d" ]]
        then
            TYPE=d
            type_len=8
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

        num_of_pieces=0

        for filesize_set_KB in $filesize_set_KBs
        do
            # one size
            echo "  SIZE: $filesize_set_KB"
            echo SIZE: $filesize_set_KB >> $output
            filesize_set=$((filesize_set_KB*1024))
            filesize_real=0

            # Dimension
            dims=(${array[2]//x/ })
            # for var in ${dims[@]}
            # do
            #     echo $var
            # done
            DIM=${#dims[@]}
            
            # reverse and calculate dims
            if [ $DIM == 1 ]
            then
                if [[ $filesize_set -gt $((${dims[0]}*type_len)) ]]
                then
                    echo "  skip size:$filesize_set dir:$dir"
                    continue
                fi
                if [[ $filesize_set != 0 ]]
                then
                    dims[0]=$((filesize_set/type_len))
                fi
                filesize_real=$((${dims[0]}*type_len))
            elif [ $DIM == 2 ]
            then
                if [[ $filesize_set -gt $((${dims[0]}*${dims[1]}*type_len)) ]]
                then
                # too small
                    echo "  skip size:$filesize_set dir:$dir"
                    continue
                fi
                if [[ $((${dims[1]}*type_len)) -gt $filesize_set ]] && [[ $filesize_set != 0 ]]
                then
                # 1D
                    dims[1]=1
                    dims[0]=$((filesize_set/type_len))
                else
                # 2D
                    temp=${dims[0]}
                    dims[0]=${dims[1]}
                    if [[ $filesize_set != 0 ]]
                    then
                        dims[1]=$((filesize_set/${dims[1]}/type_len))
                    else
                        dims[1]=$temp
                    fi
                fi
                filesize_real=$((${dims[0]}*${dims[1]}*type_len))
            elif [ $DIM == 3 ]
            then
                if [[ $filesize_set -gt $((${dims[0]}*${dims[1]}*${dims[2]}*type_len)) ]]
                then
                    echo "  skip size:$filesize_set dir:$dir"
                    continue
                fi
                if [[ $((${dims[2]}*type_len)) -gt $filesize_set ]] && [[ $filesize_set != 0 ]]
                then
                # 1D
                    dims[0]=$((filesize_set/type_len))
                    dims[1]=1
                    dims[2]=1
                elif [[ $((${dims[1]}*${dims[2]}*type_len)) -gt $filesize_set ]] && [[ $filesize_set != 0 ]]
                then
                # 2D
                    dims[0]=${dims[2]}
                    dims[1]=$((filesize_set/${dims[2]}/type_len))
                    dims[2]=1
                else
                # 3D
                    temp=${dims[0]}
                    dims[0]=${dims[2]}
                    if [[ $filesize_set != 0 ]]
                    then
                        dims[2]=$((filesize_set/${dims[1]}/${dims[2]}/type_len))
                    else
                        dims[2]=$temp
                    fi
                fi
                filesize_real=$((${dims[0]}*${dims[1]}*${dims[2]}*type_len))
            elif [ $DIM == 4 ]
            then
                if [[ $filesize_set -gt $((${dims[0]}*${dims[1]}*${dims[2]}*${dims[3]}*type_len)) ]]
                then
                    echo "  skip size:$filesize_set dir:$dir"
                    continue
                fi
                if [[ $((${dims[3]}*type_len)) -gt $filesize_set ]] && [[ $filesize_set != 0 ]]
                then
                # 1D
                    dims[0]=$((filesize_set/type_len))
                    dims[1]=1
                    dims[2]=1
                    dims[3]=1
                elif [[ $((${dims[2]}*${dims[3]}*type_len)) -gt $filesize_set ]] && [[ $filesize_set != 0 ]]
                then
                # 2D
                    dims[0]=${dims[3]}
                    dims[1]=$((filesize_set/${dims[3]}/type_len))
                    dims[2]=1
                    dims[3]=1
                elif [[ $((${dims[1]}*${dims[2]}*${dims[3]}*type_len)) -gt $filesize_set ]] && [[ $filesize_set != 0 ]]
                then
                # 3D
                    dims[0]=${dims[3]}
                    dims[1]=${dims[2]}
                    dims[2]=$((filesize_set/${dims[3]}/${dims[2]}/type_len))
                    dims[3]=1
                else
                # 4D
                    temp0=${dims[0]}
                    temp1=${dims[1]}
                    dims[0]=${dims[3]}
                    dims[1]=${dims[2]}
                    dims[2]=$temp1
                    dims[3]=$temp0
                    if [[ $filesize_set != 0 ]]
                    then
                        dims[3]=$((filesize_set/${dims[3]}/${dims[2]}/${dims[1]}/type_len))
                    fi
                fi
                filesize_real=$((${dims[0]}*${dims[1]}*${dims[2]}*${dims[3]}*type_len))
            fi

            # file count
            cnt=0
            
            # cut one file into pieces
            # calculate cut size to maintain dimensions of file
            if [[ $num_of_pieces -lt 10 ]] # when too many pieces, use previos result
            then
                i=0
                bytes=type_len
                while [ $i -lt $DIM ]
                do
                    bytes=$(($bytes*${dims[$i]}))
                    i=$(($i+1))
                done
                # echo bytes=$bytes

                # num of pieces
                num_of_pieces=$(($max/$bytes))
                # echo "   num_of_pieces: $num_of_pieces"
            fi

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

                    
                    echo "   num_of_pieces: $num_of_pieces"
                    # echo "num_of_pieces: $num_of_pieces" >> $output
                    split $TEST_DIR"/"$dir"/"$file -b $bytes $thread_dir"/"piece
                    

                    i=0
                    for piecex in `ls $thread_dir`
                    do
                    if [ $i -lt $num_of_pieces ] && [[ $piecex == "piece"* ]] && [[ $piecex != *".sz" ]]
                    then
                        # compress each piece
                        # echo $piecex
                        echo "piece: $piecex" >> $output
                        i=$(($i+1))

                # huffman
                        echo "===huffman===" >> $output
                    ## comp
                        # echo "$SZ_PATH"/"sz -z -$TYPE -g 0 -i $thread_dir"/"$piecex -M $ERROR_BOUND_MODE -P $ERROR_BOUND -$DIM ${dims[@]}"
                        $SZ_PATH"/"sz -z -$TYPE -g 0 -i $thread_dir"/"$piecex -M $ERROR_BOUND_MODE -P $ERROR_BOUND -$DIM ${dims[@]} >> $output
                        filesize_compressed=`ls -l $thread_dir"/"$piecex".sz" | awk '{print $5}'`
                        echo "$filesize_compressed/$filesize_real" >> $output 
                    ## decomp
                        # echo "$SZ_PATH"/"sz -x -$TYPE -s $thread_dir"/"$piecex.sz -$DIM ${dims[@]}"
                        # $SZ_PATH"/"sz -x -$TYPE -s $thread_dir"/"$piecex.sz -$DIM ${dims[@]} >> $output

                # zstd
                        echo "===zstd===" >> $output
                    ## comp
                        # echo "$SZ_PATH"/"sz -z -$TYPE -g 1 -i $thread_dir"/"$piecex -M $ERROR_BOUND_MODE -P $ERROR_BOUND -$DIM ${dims[@]}"
                        $SZ_PATH"/"sz -z -$TYPE -g 1 -i $thread_dir"/"$piecex -M $ERROR_BOUND_MODE -P $ERROR_BOUND -$DIM ${dims[@]} >> $output
                        filesize_compressed=`ls -l $thread_dir"/"$piecex".sz" | awk '{print $5}'`
                        echo "$filesize_compressed/$filesize_real" >> $output 
                    ## decomp
                        # echo "$SZ_PATH"/"sz -x -$TYPE -s $thread_dir"/"$piecex.sz -$DIM ${dims[@]}"
                        # $SZ_PATH"/"sz -x -$TYPE -s $thread_dir"/"$piecex.sz -$DIM ${dims[@]} >> $output

                # fse
                        echo "===fse===" >> $output
                    ## comp
                        # echo "$SZ_PATH"/"sz -z -$TYPE -g 2 -i $thread_dir"/"$piecex -M $ERROR_BOUND_MODE -P $ERROR_BOUND -$DIM ${dims[@]}"
                        $SZ_PATH"/"sz -z -$TYPE -g 2 -i $thread_dir"/"$piecex -M $ERROR_BOUND_MODE -P $ERROR_BOUND -$DIM ${dims[@]} >> $output
                        filesize_compressed=`ls -l $thread_dir"/"$piecex".sz" | awk '{print $5}'`
                        echo "$filesize_compressed/$filesize_real" >> $output 
                    ## decomp
                        # echo "$SZ_PATH"/"sz -x -$TYPE -s $thread_dir"/"$piecex.sz -$DIM ${dims[@]}"
                        # $SZ_PATH"/"sz -x -$TYPE -s $thread_dir"/"$piecex.sz -$DIM ${dims[@]} >> $output
                        
                        rm -rf  $thread_dir"/"$piecex.sz  $thread_dir"/"$piecex.sz.out

                        # 验证压缩解压正确性
                        # /bin/python3 /home/zhongyu/tmp/check.py $((filesize_origin/type_len))
                        
                    fi
                    done
                    echo rm -f $thread_dir"/piece*"
                    # delete all pieces
                    rm -f $thread_dir"/piece"*
                    
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
    rm -rf $thread_dir
}

for ERROR_BOUND_F in $ERROR_BOUND_Fs
do
    run ERROR_BOUND_F &
done

# done
