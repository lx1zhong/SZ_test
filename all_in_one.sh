#!/bin/bash

# Complete everything from SZ_ADT installation, dataset download, to test and drawing.
# Corresponding to Figure.6 and Figure.8 in paper.




path=`pwd`
echo "=== download SZ_ADT==="
git clone https://github.com/lx1zhong/SZ_ADT.git
cd SZ_ADT
git fetch
git checkout develop

echo "=== install SZ_ADT==="
mkdir ../sz_install
./configure --prefix=$path/sz_install
make -j8
sudo make install 
cd ../

echo "=== download dataset ==="
# ./download_dataset.sh

echo "=== run Figure.6 test ==="
cd test1/3
./script/run_abs.sh

echo "=== draw Figure.6 ==="
python3 ./script/figure.py
cd ../../

echo "=== install ZFP ==="
git clone https://github.com/LLNL/zfp.git
cd zfp
mkdir build
cd build
cmake ..
cmake --build . --config Release
ctest

echo "=== run Figure.8 test ==="
cd $path/test2/1
./script/run.sh

echo "=== draw Figure.8 ==="
python3 ./script/figure.py
cd ../../