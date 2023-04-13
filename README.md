# SZ_test

SZ_test includes evaluation scripts for **ADT-FSE**([lx1zhong/SZ_ADT at develop (github.com)](https://github.com/lx1zhong/SZ_ADT/tree/develop)).



All evaluations are divided into 3 parts:

- test1 for performance only of encoders.
- test2 for overall performance.
- test3 for compression ratio prediction.



Please run on linux and make sure you have 2GB of free space.

## Guide

For short, you can do the main evaluation by simply running one script:

```
git clone https://github.com/lx1zhong/SZ_test.git
cd SZ_test
sudo ./all_in_one.sh
```

This will give Figure 6, 7 and 8 in the paper. （cost 3~4 compute-hours）



---

If you want to do the full evaluation, follow these steps: 

- overview:
  1. Dependencies (5 human-minutes + 10 compute-minutes)
  2. Installation  (10 human-minutes)
  3. Dataset download  (0.5~2 compute-hours, depends on network)
  4. Edit script  (2 human-minutes each test)
  5. Run  (1 compute-hour each test)
  6. Draw  (1 human-minutes each test)





1. **Dependencies**: if you have installed, ignore it.

   ```
   sudo apt install python3 python3-pip 
   pip install matplotlib numpy glob2 brewer2mpl
   ```

2. **Installation**: if you have installed, ignore it.

   1. Before evaluation, you should install SZ_ADT(ADT-FSE-enhanced SZ) here: ([lx1zhong/SZ_ADT at develop (github.com)](https://github.com/lx1zhong/SZ_ADT/tree/develop)). The "./easytest.sh" script there may help you have a quick look of our work. Please remember your install path.

   2. Then install another tool ZFP here: ([lx1zhong/zfp: Add performance statistic output (github.com)](https://github.com/lx1zhong/zfp)). This is for comparison with SZ_ADT.

3. **Dataset**: then download datasets from [here](https://sdrbench.github.io/) (SDRBENCH) and [here](https://github.com/taovcu/LossyCompressStudy/tree/master/inputdata) (small data). Make sure the directory will be in this format: [SDRBENCH/SMALL]-name-d1xd2xd3-[f/d], for example:

   ```
   test/
   -SDRBENCH-CESM_ATM-1800x3600-f/
   -SDRBENCH-EXAALT_HELIUM-7852x1037-f/
   -SDRBENCH-Miranda-256x384x384-d/
   -SMALL-dump_dense-55692-d/
   ......
   ```

   

4. **Edit script**: For each test, go to the specified directory, such as `SZ_test/test1/1/`, then scripts can be found in `script` directory. Before execute any script, **be sure SZ/ZFP install paths and datasets path are right**! 

   The corresponding directory for the figures in the paper are as follows

   | Figure.   | Dir     | Description                   |
   | --------- | ------- | ----------------------------- |
   | Figure 5  | test1/1 |                               |
   | Figure 6  | test1/3 |                               |
   | Figure 7  | test2/2 | generated along with Figure 8 |
   | Figure 8  | test2/1 |                               |
   | Figure 9  | test2/3 |                               |
   | Figure 10 | test3   |                               |

   

5. **Run**: First, execute shell script. 

   ```
   ./script/run_multithread_abs.sh
   ```

   then results will be written into `output` directory.  

6. **Draw**: After done, you can execute python scripts to draw the figure.

   ```
   python3 ./script/figure.py
   ```



## Further more

We have integrated ADT-FSE into TDengine, a time-series database. You can get the full implementation here: [TDengine (github.com)](https://github.com/zbsun-code/TDengine-SZ_ADT).

The UK-DALE dataset in paper can be found here: [The UK-DALE dataset, domestic appliance-level electricity demand and whole-house demand from five UK homes | Scientific Data (nature.com)](https://www.nature.com/articles/sdata20157)