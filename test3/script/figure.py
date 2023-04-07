
# DIR--EB--FILE

from cProfile import label
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
import glob2
import os
import math

SZ=0
SZ_ADT=1 
sz2num = {'SZ':0, 'SZ_ADT':1}

PRED=0
REAL=1
PRED_TIME=2
ERROR_FABS=3
ERROR=4

# os.system("/home/zhongyu/test/paper_test/test3/run.sh")

input_files = glob2.glob("./output/SZ*.txt")


def get_num(string):
    temp = string.split('=')
    temp = temp[1]
    if temp[-1] == ',':
        temp =  temp[:-1]
    return int(temp)
def get_f(string):
    temp = string.split('=')
    temp = temp[1]
    if temp[-1] == ',' or temp[-1] == '.':
        temp =  temp[:-1]
    return float(temp)

def num2tag(string):
    x = int(string)
    if x < 1024:
        return str(x)+'K'
    elif x < 1024*1024:
        return str(int(x/1024))+'M'
    else:
        return str(int(x/1024/1024))+'G'
Res = [{},{}]
k = 0

dataset_names = []
ebModes = ['ABS', 'REL', 'PW_REL', 'PSNR']
stats = [{},{}]


for input_file in input_files:
    print(input_file)
    temp = input_file.split('/')
    temp = temp[-1]
    temp = temp.split('-')
    sche = sz2num[temp[0]]
    temp = temp[-1].split('.')
    percentage = temp[0]

    stats[sche][percentage] = {}

    dataset_names = []
    f = open(input_file, 'r')


    error_bound = ""

    lines = f.readlines()
    i = 0
    while i <= len(lines):
        line = lines[i]
        # print(str(i) + ':' + line[:-1])
        if "DAT" in line:
            temp = line.split()
            dataset = temp[-1]

            stats[sche][percentage][dataset] = {}
            dataset_names.append(dataset)

        elif "EBMODE" in line:
            temp = line.split()
            ebMode = temp[-1]
            stats[sche][percentage][dataset][ebMode]=[{},{},{},{},{}]

        elif "EB" in line:
            temp = line.split()
            error_bound = temp[-1]
            
            while "[prediction]" not in lines[i]:
                i += 1
            line = lines[i]
            temp = line.split()
            pre = get_f(temp[3])

            temp = lines[i+1].split()
            pred_time = float(temp[-1])

            while "[ratio]" not in lines[i]:
                i += 1
            temp = lines[i-1].split()
            real_time = float(temp[-1])

            temp = lines[i].split()
            real = float(temp[-1])

            stats[sche][percentage][dataset][ebMode][PRED][error_bound]=pre
            stats[sche][percentage][dataset][ebMode][REAL][error_bound]=real
            stats[sche][percentage][dataset][ebMode][PRED_TIME][error_bound]=(pred_time)/(real_time-pred_time)
            stats[sche][percentage][dataset][ebMode][ERROR_FABS][error_bound]=math.fabs((pre-real)/real)
            stats[sche][percentage][dataset][ebMode][ERROR][error_bound]=(pre-real)/real

        elif "FINISHED" in line:
            break 
            
        i += 1

    f.close()
    for dataset in dataset_names:
        print(dataset+':')
        for ebMode in ebModes:
            print('\t'+ebMode)
            for error_bound in stats[sche][percentage][dataset][ebMode][PRED].keys():
                print('\t\t['+error_bound+']\tpred: {:.2f} \treal: {:.2f} \terror {:.1%} \ttime_ratio: {:.1%}'.format(stats[sche][percentage][dataset][ebMode][PRED][error_bound],stats[sche][percentage][dataset][ebMode][REAL][error_bound],stats[sche][percentage][dataset][ebMode][ERROR][error_bound],stats[sche][percentage][dataset][ebMode][PRED_TIME][error_bound]))


print(dataset_names)
# filter = ['CESM_ATM', 'EXAALT', 'EXAALT_HELIUM', 'EXASKY_NYX', 'Hurricane', 'Miranda', 'QMCPack',  'SCALE']
filter = ['EXAALT_HELIUM', 'Hurricane', 'Miranda', 'EXASKY_NYX']

i = 1
r=2
l=2
size = [6,3]

errors = [{},{}]
means = [{},{}]
stds = [{},{}]
for sche in range(2):
    for percentage in stats[sche].keys():
        errors[sche][percentage] = {}
        means[sche][percentage] = {}
        stds[sche][percentage] = {}
        for dataset in dataset_names:
            errors[sche][percentage][dataset]=[]
            for ebMode in ebModes:
                for error_bound in stats[sche][percentage][dataset][ebMode][ERROR_FABS].keys():
                    errors[sche][percentage][dataset].append(stats[sche][percentage][dataset][ebMode][ERROR_FABS][error_bound])
            means[sche][percentage][dataset] = np.mean(errors[sche][percentage][dataset])
            stds[sche][percentage][dataset] = np.std(errors[sche][percentage][dataset])


fig3 = plt.figure(figsize=size, dpi=100)
ax = fig3.add_subplot(1,1,1)
# ax.set_title('('+ chr(ord('a')+i-1) +') '+ ebMode , y=-0.5, fontsize=14)
# if (i-1)%l==0:
# ax.set_ylabel('Compression Ratio')
ax.set_ylabel('Prediction Error')
plt.grid(linestyle=':', color="gray",axis='y',zorder=1)
x = np.arange(len(means[SZ]['1'].keys())) 
total_width, n = 0.6, 3   
width = total_width / n
x = x - (total_width - width) / 2
width += 0.02

# plt.xticks(means.keys())
# plt.bar(means.keys(), means.values(),yerr=stds.values(),ecolor='black',capsize=4,zorder=100)
print(means)
c0=plt.bar(x-1.5*width,means[SZ]['1'].values(),yerr=stds[SZ]['1'].values(),width=width-0.06,label='1% SZ',lw=0.02,edgecolor='Black',color='w',ecolor='black',capsize=4,zorder=100)

c2=plt.bar(x-0.5*width,means[SZ_ADT]['1'].values(),yerr=stds[SZ_ADT]['1'].values(),width=width-0.06,label='1% SZ_ADT',lw=0.01,edgecolor='black',color='#87CEFA',ecolor='black',capsize=4,zorder=100)
# print(means[SZ]['1'].keys())
plt.xticks(x,means[SZ]['1'].keys(), rotation=0)
# plt.ylim([0,ylims[i]])
c10=plt.bar(x+0.5*width,means[SZ]['5'].values(),yerr=stds[SZ]['5'].values(),width=width-0.06,label='5% SZ',lw=0.02,edgecolor='Black',color='#DCDCDC',ecolor='black',capsize=4,zorder=100)

c12=plt.bar(x+1.5*width,means[SZ_ADT]['5'].values(),yerr=stds[SZ_ADT]['5'].values(),width=width-0.06,label='5% SZ_ADT',lw=0.01,edgecolor='black',color='#ff9912',ecolor='black',capsize=4,zorder=100)

def to_percent(temp, position):
  return '%1.0f'%(100*temp) + '%'
plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))
plt.legend(frameon=True,fontsize=8,loc='upper left',ncol=1,columnspacing=1) 
    

ax.set_ylim(bottom=0)
picpath = './output/avg_pred.png'
plt.savefig(picpath)
picpath_pdf = './output/avg_pred.pdf'
plt.savefig(picpath_pdf)
print(picpath_pdf)