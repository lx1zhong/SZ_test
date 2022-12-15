# 压缩率随EB的变化曲线图，每个数据集一个图

# DIR--EB--FILE

from cProfile import label
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
import glob2
import os
import math

SZ=0
SZ_ADT=1 #27.88 17.5375 8.74 4.5275
sz2num = {'SZ':0, 'SZ_ADT':1}

PRED=0
REAL=1
PRED_TIME=2
ERROR_FABS=3
ERROR=4

# os.system("/home/zhongyu/test/paper_test/test3/run.sh")

input_files = glob2.glob("/home/zhongyu/test/paper_test/test3/SZ*.txt")


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


# # 总体压缩时间
# i = 1
# ylims=[0,12,55,160,240,880,1400,6500,7000]
# ylabels=[
#     [],
#     [0,1,4,16],
#     [0,1,4,16,64,256],
#     [0,1,4,16],
#     [0,1,4,16]
# ]
# print('HHHHHHHHHHHHHHHHHH')
# fig3 = plt.figure(figsize=size, dpi=100)
# print('HHHHHHHHHHHHHHHHHH')
# for ebMode in ebModes:
#     # print(dataset)
#     # print(stat[CTIME_ALL][dataset][HUFFMAN])
#     # print(stat[CTIME_ALL][dataset][ZFP])
#     # print(stat[CTIME_ALL][dataset][FSE])
#     ax = fig3.add_subplot(r,l,i)
#     ax.set_title('('+ chr(ord('a')+i-1) +') '+ ebMode , y=-0.5, fontsize=14)
#     # if (i-1)%l==0:
#     ax.set_ylabel('Compression Ratio')
#     ax.set_xlabel('Error Bounds')
#     # plt.ylim(0,2500)
    
#     x = np.arange(len(stats[sche][percentage][dataset_names[0]][ebMode][PRED].keys())) #总共有几组，就设置成几，我们这里有三组，所以设置为3
#     total_width, n = 0.6, 3    # 有多少个类型，只需更改n即可，比如这里我们对比了四个，那么就把n设成4
#     width = total_width / n
#     x = x - (total_width - width) / 2
#     width += 0.02
#     plt.grid(linestyle=':', color="gray",axis='y',zorder=1)

#     c0=plt.bar(x-1.5*width,stats[sche][percentage][dataset_names[0]][ebMode][REAL].values(),width=width-0.06,label=dataset_names[0],lw=0.02,edgecolor='Black',color='w',zorder=100)
#     c2=plt.bar(x-0.5*width,stats[sche][percentage][dataset_names[0]][ebMode][PRED].values(),width=width-0.06,label=dataset_names[0]+'-pred',lw=0.01,edgecolor='black',color='#87CEFA',zorder=100)
#     plt.xticks(x,stats[sche][percentage][dataset_names[0]][ebMode][PRED].keys())
#     # plt.ylim([0,ylims[i]])
    
#     c10=plt.bar(x+0.5*width,stats[sche][percentage][dataset_names[2]][ebMode][REAL].values(),width=width-0.06,label=dataset_names[2],lw=0.02,edgecolor='Black',color='#DCDCDC',zorder=100)
#     c12=plt.bar(x+1.5*width,stats[sche][percentage][dataset_names[2]][ebMode][PRED].values(),width=width-0.06,label=dataset_names[2]+'-pred',lw=0.01,edgecolor='black',color='#ff9912',zorder=100)
    
#     # c20=plt.bar(x+2*width,stats[sche][percentage][dataset_names[2]][ebMode][REAL].values(),width=width-0.06,label=dataset_names[2],lw=0.02,edgecolor='Black',color='#DCDCDC',zorder=100)
#     # c22=plt.bar(x+3*width,stats[sche][percentage][dataset_names[2]][ebMode][PRED].values(),width=width-0.06,label=dataset_names[2]+'-pred',lw=0.01,edgecolor='black',color='#ff9912',zorder=100)
    
#     plt.legend(frameon=True,fontsize=8,loc='upper right',ncol=1,columnspacing=1) #去掉图例边框
    
#     # l1=plt.legend([c0,c2],['comp-SZ','comp-SZ_ADT'],frameon=True,fontsize=7,loc='upper left',ncol=1,columnspacing=1) #去掉图例边框
    
#     # plt.legend([c10,c12],['decomp-SZ','decomp-SZ_ADT'],frameon=True,fontsize=7,loc=[0.02,0.51],ncol=1,columnspacing=1) #去掉图例边框
#     # plt.gca().add_artist(l1)
#     ax.set_yscale('log',base=2)
#     ax.set_ylim(bottom=1)
#     # ax.set_yticklabels(ylabels[i])
#     i += 1

# plt.subplots_adjust(left=0.1,right=0.96,bottom=0.17,top=0.96,wspace=0.32,hspace=0.6) 
# # plt.tight_layout()
# picpath = '/home/zhongyu/test/paper_test/test3/predicion.png'
# plt.savefig(picpath)
# picpath_pdf = '/home/zhongyu/test/paper_test/test3/predicion.pdf'
# plt.savefig(picpath_pdf)
# print(picpath_pdf)


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
x = np.arange(len(means[SZ]['1'].keys())) #总共有几组，就设置成几，我们这里有三组，所以设置为3
total_width, n = 0.6, 3    # 有多少个类型，只需更改n即可，比如这里我们对比了四个，那么就把n设成4
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
# c10=plt.bar(x+0.5*width,stat[DTIME_ALL][dataset][HUFFMAN].values(),width=width-0.06,label='decomp-SZ',lw=0.02,edgecolor='Black',color='#DCDCDC',zorder=100)
# # matplotlib.rcParams['hatch.color']=colors[0]
# c12=plt.bar(x+1.5*width,stat[DTIME_ALL][dataset][FSE].values(),width=width-0.06,label='decomp-SZ_ADT',lw=0.01,edgecolor='black',color='#ff9912',zorder=100)
plt.legend(frameon=True,fontsize=8,loc='upper left',ncol=1,columnspacing=1) #去掉图例边框
    

ax.set_ylim(bottom=0)
picpath = '/home/zhongyu/test/paper_test/test3/avg_pred.png'
plt.savefig(picpath)
picpath_pdf = '/home/zhongyu/test/paper_test/test3/avg_pred.pdf'
plt.savefig(picpath_pdf)
print(picpath_pdf)