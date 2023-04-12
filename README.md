# SZ_test

SZ_test includes evaluation scripts for **ADT-FSE**([lx1zhong/SZ_ADT at develop (github.com)](https://github.com/lx1zhong/SZ_ADT/tree/develop)).



All evaluations are divided into 3 parts:

- test1 for performance only of encoders.
- test2 for overall performance.
- test3 for compression ratio prediction.



## Guide

For short, you can do the main evaluation by simply running one script:

```
git clone https://github.com/lx1zhong/SZ_test.git
cd SZ_test
sudo ./all_in_one.sh
```

This will give Figure 6 and Figure 8 in the paper.



---

If you want to do the full evaluation, follow these steps: 

1. **Installation**: if you have installed, ignore it.

   1. Before evaluation, you should install SZ_ADT(ADT-FSE-enhanced SZ) here: ([lx1zhong/SZ_ADT at develop (github.com)](https://github.com/lx1zhong/SZ_ADT/tree/develop)). The "./easytest.sh" script there may help you have a quick look of our work. Please remember your install path.

   2. Then install another tool ZFP here: ([lx1zhong/zfp: Add performance statistic output (github.com)](https://github.com/lx1zhong/zfp)). This is for comparison with SZ_ADT.

2. **Dataset**: then download datasets from [here](https://sdrbench.github.io/) (SDRBENCH) and [here](https://github.com/taovcu/LossyCompressStudy/tree/master/inputdata) (small data). Make sure the directory will be in this format: [SDRBENCH/SMALL]-name-d1xd2xd3-[f/d], for example:

   ```
   test/
   -SDRBENCH-CESM_ATM-1800x3600-f/
   -SDRBENCH-EXAALT_HELIUM-7852x1037-f/
   -SDRBENCH-Miranda-256x384x384-d/
   -SMALL-dump_dense-55692-d/
   ......
   ```

   

3. **Edit script**: For each test, go to the specified directory, such as `SZ_test/test1/1/`, then scripts can be found in `script` directory. Before execute any script, **be sure SZ/ZFP install paths and datasets path are right**!

4. **Run**: First, execute shell script. 

   ```
   ./script/run_multithread_abs.sh
   ```

   then results will be written into `output` directory.  

5. **Draw**: After done, you can execute python scripts to draw the figure.

   ```
   python3 ./script/figure.py
   ```


## Further more

We have integrated ADT-FSE into TDengine, a time-series database. You can get the full implementation here: [lx1zhong/TDengine (github.com)](https://github.com/lx1zhong/TDengine).

The UK-DALE dataset in paper can be found here: [The UK-DALE dataset, domestic appliance-level electricity demand and whole-house demand from five UK homes | Scientific Data (nature.com)](https://www.nature.com/articles/sdata20157)

