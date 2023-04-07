SZ_test includes evaluation scripts for [ADT-FSE]([lx1zhong/SZ_ADT at develop (github.com)](https://github.com/lx1zhong/SZ_ADT/tree/develop)).



All evaluations are divided into 4 parts:

- test1 for performance only of encoders.
- test2 for overall performance.
- test3 for compression ratio prediction.



### Guide

- Before evaluation, you should install SZ_ADT(ADT-FSE-enhanced SZ) [here]([lx1zhong/SZ_ADT at develop (github.com)](https://github.com/lx1zhong/SZ_ADT/tree/develop)). The "./easytest.sh" script there may help you have a quick look of our work. Please remember your install path.

- then download datasets from [here]([https://sdrbench.github.io](https://sdrbench.github.io/)). Make sure the directory will be in this format:

  ```
  test/
  -SDRBENCH-CESM_ATM-1800x3600-f/
  -SDRBENCH-EXAALT_HELIUM-7852x1037-f
  -SDRBENCH-Miranda-256x384x384-d
  ......
  ```

  

- For each test, go to the specified directory, such as `SZ_test/test1/1/`, then scripts can be found in `script` directory. Before execute any script, **edit SZ install path and datasets path** firtst!

- First, execute shell script. 

  ```
  ./script/run_multithread_abs.sh
  ```

  then results will be written into `output` directory.  

- After done, you can execute python scripts to draw the figure.

  ```
  python3 ./script/figure.py
  ```

  

