# motivation : huffman树比例

from cProfile import label
from turtle import color
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from matplotlib.ticker import FuncFormatter
import glob2


# input_files = glob2.glob("/home/zhongyu/test/paper_test/test1/1/output/ABS_1E-4.txt")

input_file = '/home/zhongyu/test/paper_test/motivation/ABS_1E-4_fse.txt'

HUFFMAN = 0
ZSTD = 1
FSE = 2
TREE_PERC = 3
CTIME_PERC = 4
DTIME_PERC = 5
FSE_TB_PERC = 6

def get_num(string):
    temp = string.split('=')
    temp = temp[1]
    if temp[-1] == ',':
        temp =  temp[:-1]
    return int(temp)
def get_f(string):
    temp = string.split('=')
    temp = temp[1]
    if temp[-1] == ',':
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


print(input_file)
temp = input_file.split('/')
temp = temp[-1]
temp = temp.split('.')
eb = temp[0]

f = open(input_file, 'r')

stats = {}
dataset_names = []

file_count = 0
error_bound = ""
dir_flag = 0

lines = f.readlines()
i = 1
while i <= len(lines):
    line = lines[i]
    # print(str(i) + ':' + line[:-1])
    if "DIR" in line:
        dir_flag = 1
        temp = line.split()
        temp = temp[1].split('-')
        # dataset name
        dir_name = temp[1]
        dataset_names.append(dir_name)
        stats[dir_name] = [{},{},{},{},{},{},{}]
        
        # 一个DIR内的所有ratios数值
        # ratios = [ [] for i in range(TOTAL_NUM)]

    elif "SIZE" in line:
        file_count = 0
        temp = line.split()
        size = temp[-1]
        
        # stats[dir_name][size] = [0,0,0]
        huffman_ratio = 0
        zstd_ratio = 0
        fse_ratio = 0
        tree_ratio = 0
        ctime_ratio = 0
        dtime_ratio = 0
        fse_tb_ratio = 0

    elif "FILE" in line:
        temp = line.split()
        file_name = temp[1]

    elif "piece" in line:
        wrong = 0
        temp = line.split()
        piece_name = temp[1]

        if i+2 < len(lines) and 'all same data!' in lines[i+2]:
            i += 4*3
            continue
        
        i += 1
        # huffman
        # print(str(i) + ':' + lines[i])
        # if '===huffman===' not in lines[i]:
        #     i += 1
        #     continue
        assert('===huffman===' in lines[i])
        assert('[huffman]' in lines[i+3])
        temp = lines[i+3].split()
        huffman_ratio += 1/get_f(temp[1])

        temp = lines[i+2].split()
        tree_ratio += get_f(temp[0])/get_f(lines[i+4])
        
        temp = lines[i+3].split()
        temp2 = lines[i+5].split()
        temp2 = temp2[-1][:-1]
        ctime_ratio += get_f(temp[-1])/float(temp2)

        if '[decoder]' not in lines[i+7]:
            while '===zstd===' not in lines[i]:
                i += 1
        else:
            temp = lines[i+7].split()
            temp2 = lines[i+8].split()
            dtime_ratio += get_f(temp[-1])/float(temp2[-2])
            i += 9

        # zstd
        assert('===zstd===' in lines[i])
        assert('[zstd]' in lines[i+2])
        temp = lines[i+2].split()
        zstd_ratio += 1/get_f(temp[-3])
        i += 6

        # fse
        # print(str(i) + ':' + lines[i])
        assert('===fse===' in lines[i])
        assert('[fse]' in lines[i+3])
        temp = lines[i+3].split()
        fse_ratio += 1/get_f(temp[1])

        temp = lines[i+2].split()
        fse_tb_ratio = get_f(temp[0])/get_f(lines[i+4])
        # 计算
        file_count += 1
        

    elif "CNT" in line:
        # end of one size
        if file_count == 0:
            i += 1
            continue
        
        # calculate ave ratio
        stats[dir_name][HUFFMAN][num2tag(size)] = 1 / (huffman_ratio/file_count)
        stats[dir_name][ZSTD][num2tag(size)] = 1 / (zstd_ratio/file_count)
        stats[dir_name][FSE][num2tag(size)] = 1 / (fse_ratio/file_count)
        stats[dir_name][TREE_PERC][num2tag(size)] = tree_ratio/file_count
        stats[dir_name][CTIME_PERC][num2tag(size)] = ctime_ratio/file_count
        stats[dir_name][DTIME_PERC][num2tag(size)] = dtime_ratio/file_count
        stats[dir_name][FSE_TB_PERC][num2tag(size)] = fse_tb_ratio/file_count
        
    elif "FINISHED" in line:
        break 
        
    i += 1

f.close()

print(str(k) + ':' + eb)
if k <= 1:
    Res[k]=stats
    k += 1

print(dataset_names)
# matplotlib.rcParams['font.family']='SimHei'
fig = plt.figure(figsize=[6,2.75], dpi=100)

# filter = ['CESM_ATM', 'EXAALT', 'EXAALT_HELIUM', 'EXASKY_NYX', 'Hurricane', 'Miranda', 'QMCPack',  'SCALE']
# ylims=[0,11,6,6,12,9,13,7,12]
# filter = ['bump_dense', 'eddy_velx_f4', 'EXAALT', 'CESM_ATM', 'Hurricane', 'Miranda', 'EXASKY_NYX', 'QMCPack']
    
filter = ['EXAALT_HELIUM', 'Hurricane', 'Miranda', 'EXASKY_NYX']
ylims=[0,7.5,12,16,13]

i = 1
r=2
l=2
# print(dataset)
# print(stats[dataset][HUFFMAN])
# print(stats[dataset][ZSTD])
# print(stats[dataset][FSE])
ax = fig.add_subplot(1,1,1)
# ax.set_title('('+ chr(ord('a')+i-1) +') '+ dataset , y=-0.5, fontsize=14)

plt.grid(linestyle=':', color="gray",axis='y',zorder=1)
# if (i-1)%l==0:
ax.set_ylabel('Decoding Table Overhead')
ax.set_xlabel('Compression Granularity (Bytes)')

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#9467bd', '#8c564b',  # 使用颜色编码定义颜色
          '#d62728', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
i=0

filter = ['Miranda', 'CESM_ATM', 'EXAALT', 'Hurricane', 'QMCPack']
for dataset in filter:
    plt.plot(stats[dataset][0].keys(),stats[dataset][TREE_PERC].values(),'o-',markersize=3,label='Huff_tree-'+dataset,color=colors[i])#2ca02c
    i += 1
l1=plt.legend(frameon=True,fontsize=8,loc = 'upper left',ncol=1,columnspacing=1) #去掉图例边框

filter = ['Miranda']
for dataset in filter:
    p1=plt.plot(stats[dataset][0].keys(),stats[dataset][FSE_TB_PERC].values(),'x-.',markersize=5,label='FSE_tbl-'+dataset,color=colors[i])#2ca02c
l2=plt.legend((p1),['FSE_nCount-Miranda'],frameon=True,fontsize=8,loc = 'upper center',ncol=1,columnspacing=1) #去掉图例边框
plt.gca().add_artist(l1)
plt.ylim(top=1)


def to_percent(temp, position):
    return '%1.0f'%(100*temp) + '%'
plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))
# l1=plt.legend(frameon=False,fontsize=7,loc='lower left',ncol=1,columnspacing=1) #去掉图例边框




# plt.subplots_adjust(left=0.1,right=0.96,bottom=0.17,top=0.96,wspace=0.32,hspace=0.6) 
plt.tight_layout()
# plt.subplots_adjust(wspace=0.3,hspace=0.4) #left=1,right=1,bottom=1,top=1,
# plt.legend(loc = 'upper right')
picpath = '/home/zhongyu/test/paper_test/motivation/huff_tree_percent.png'
plt.savefig(picpath)
picpath_pdf = '/home/zhongyu/test/paper_test/motivation/huff_tree_percent.pdf'
plt.savefig(picpath_pdf)
print(picpath_pdf)
# plt.show()
