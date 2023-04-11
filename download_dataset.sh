#!/bin/bash

mkdir data

wget https://g-8d6b0.fd635.8443.data.globus.org/ds131.2/Data-Reduction-Repo/raw-data/EXAALT/SDRBENCH-EXAALT-2869440.tar.gz
wget https://g-8d6b0.fd635.8443.data.globus.org/ds131.2/Data-Reduction-Repo/raw-data/Hurricane-ISABEL/SDRBENCH-Hurricane-ISABEL-100x500x500.tar.gz
wget https://g-8d6b0.fd635.8443.data.globus.org/ds131.2/Data-Reduction-Repo/raw-data/Miranda/SDRBENCH-Miranda-256x384x384.tar.gz
wget https://github.com/taovcu/LossyCompressStudy/raw/master/inputdata/bump_dense.dat

tar -xvzf SDRBENCH-EXAALT-2869440.tar.gz -C data
mv data/2869440 data/SDRBENCH-EXAALT-2869440-f

tar -xvzf SDRBENCH-Hurricane-ISABEL-100x500x500.tar.gz -C data
mv data/100x500x500 data/SDRBENCH-Hurricane-100x500x500-f

tar -xvzf SDRBENCH-Miranda-256x384x384.tar.gz -C data
mv data/SDRBENCH-Miranda-256x384x384 data/SDRBENCH-Miranda-256x384x384-d

mkdir data/SMALL-bump_dense-55692-d
mv bump_dense.dat data/SMALL-bump_dense-55692-d

rm -rf ./SDRBENCH*
