# 压缩/解压时延随EB的变化柱状图，每个EBMODE一个图

# DIR--EB--FILE

from cProfile import label
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import glob2
import os
import brewer2mpl

input_file = "/home/zhongyu/test/paper_test/test2/3/output/result.txt"

ID = ['RATIO_ALL','CTIME_ALL','DTIME_ALL']
RATIO_ALL = 0
CTIME_ALL = 1
DTIME_ALL = 2
TOTAL_NUM = 3


HUFFMAN = 0
FSE = 1
PLAN_NUM = 2

No = {'bump_dense':0, 'eddy_velx_f4':1, 'EXAALT':2, 'CESM_ATM':3, 'Hurricane':4, 'Miranda':5, 'EXASKY_NYX':6, 'QMCPack':7}
# filter = dataset_names

# eb range to show
bottom = [3,1,1,2,4,3,1,1]
top    = [8,6,6,7,8,8,6,6]

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

def num2tag(x):
    if x < 1024:
        return str(x)+'K'
    elif x < 1024*1024:
        return str(int(x/1024))+'M'
    else:
        return str(int(x/1024/1024))+'G'

def cal_size(stringa, stringb):
    temp = stringa.split('x')
    n = 1
    for t in temp:
        n = n * int(t)
    n *= 4
    if 'd' in stringb:
        n = n * 2
    return int(n/1024)


f = open(input_file, 'r')


# # 最后打印数据
stat = [ {} for i in range(TOTAL_NUM)]
# stats_com = {}
# stats_decom = {}
dataset_names = []

file_count = 0
error_bound = ""
dir_flag = 0

lines = f.readlines()
i = 1
while i <= len(lines):
    line = lines[i]
    # print(str(i) + ':' + line[:-1])
    # if 'EXAALT-2' in line or 'EXASKY_NYX' in line or 'coordinates' in line or 'bump_dense' in line or 'dpot' in line or 'eddy_velx_f4' in line :
    #     i += 1
    #     while 'DIR' not in lines[i] and 'FINISHED' not in lines[i]:
    #         i += 1
    #     continue
    if "EBMODE" in line:
        dir_flag = 1
        temp = line.split()
        # dataset name
        dir_name = temp[1]
        # print("dir:"+dir_name)
        dataset_names.append(dir_name)

        for j in range(TOTAL_NUM):
            stat[j][dir_name] = [{},{},{}]

    elif "EB" in line:
        file_count = 0
        temp = line.split()
        error_bound = temp[-1]
        
        # stats[dir_name][size] = [0,0,0]
        t_eb = [ [0,0] for i in range(TOTAL_NUM)]
        huffman_ctime = 0
        fse_ctime = 0
        huffman_dtime = 0
        fse_dtime = 0

    elif "FILE" in line:
        t = [ [0,0] for i in range(TOTAL_NUM)]
        temp = line.split()
        file_name = temp[1]

        wrong = 0

        if i+2 < len(lines) and 'all same data!' in lines[i+2]:
            i += 2
            while 'FILE' not in lines[i] and 'EB' not in lines[i] and 'DIR' not in lines[i] and 'CNT' not in lines[i] and 'FINISHED' not in lines[i]:
                i += 1
            continue
        
        i += 1
        # huffman
        # print(str(i) + ':' + lines[i])
        # if '===huffman===' not in lines[i]:
        #     i += 1
        #     continue
        assert('===huffman===' in lines[i])
        assert('[huffman]' in lines[i+3])
        assert('[huffman]' in lines[i+8])
        assert('[huffman]' in lines[i+13])

        temp = lines[i+3+2].split()
        t[CTIME_ALL][HUFFMAN] += float(temp[-1])
        temp = lines[i+8+2].split()
        t[CTIME_ALL][HUFFMAN] += float(temp[-1])
        temp = lines[i+13+2].split()
        t[CTIME_ALL][HUFFMAN] += float(temp[-1])

        temp = lines[i+16].split('/')
        t[RATIO_ALL][HUFFMAN] += float(temp[1]) / float(temp[0])

        
        if '[decoder]' not in lines[i+17]:
            i += 17
            while 'FILE' not in lines[i] and 'EB' not in lines[i] and 'DIR' not in lines[i] and 'CNT' not in lines[i] and 'FINISHED' not in lines[i]:
                i += 1
            continue
        assert('[decoder]' in lines[i+17])
        assert('[decoder]' in lines[i+19])
        assert('[decoder]' in lines[i+21])
        
        temp = lines[i+17+1].split()
        t[DTIME_ALL][HUFFMAN] += float(temp[-2])
        temp = lines[i+19+1].split()
        t[DTIME_ALL][HUFFMAN] += float(temp[-2])
        temp = lines[i+21+1].split()
        t[DTIME_ALL][HUFFMAN] += float(temp[-2])

        if 'origin data' in lines[i+7]:
            i += 1

        i += 23
        
        # fse
        # print(str(i) + ':' + lines[i])
        assert('===fse===' in lines[i])
        assert('[fse]' in lines[i+3])
        assert('[fse]' in lines[i+8])
        assert('[fse]' in lines[i+13])

        temp = lines[i+3+2].split()
        t[CTIME_ALL][FSE] += float(temp[-1])
        temp = lines[i+8+2].split()
        t[CTIME_ALL][FSE] += float(temp[-1])
        temp = lines[i+13+2].split()
        t[CTIME_ALL][FSE] += float(temp[-1])
        
        temp = lines[i+16].split('/')
        t[RATIO_ALL][FSE] += float(temp[1]) / float(temp[0])
        
        if '[decoder]' not in lines[i+17]:
            i += 17
            while 'FILE' not in lines[i] and 'EB' not in lines[i] and 'EBMODE' not in lines[i] and 'CNT' not in lines[i] and 'FINISHED' not in lines[i]:
                i += 1
            continue
        assert('[decoder]' in lines[i+17])
        assert('[decoder]' in lines[i+19])
        assert('[decoder]' in lines[i+21])
        
        temp = lines[i+17+1].split()
        t[DTIME_ALL][FSE] += float(temp[-2])
        temp = lines[i+19+1].split()
        t[DTIME_ALL][FSE] += float(temp[-2])
        temp = lines[i+21+1].split()
        t[DTIME_ALL][FSE] += float(temp[-2])

        i += 22
        
        for j in range(TOTAL_NUM):
            for k in range(PLAN_NUM):
                t_eb[j][k] += t[j][k]

        # print('end:'+str(i) + ':' + lines[i])
        file_count += 1

    elif "CNT" in line:
        # print("dir:"+dir_name+",eb:"+error_bound+",cnt:"+str(file_count))
        # end of one eb
        if file_count == 0:
            i += 1
            continue
        
        # calculate ave time
        e = int(error_bound[-1])
        for j in range(TOTAL_NUM):
            for k in range(PLAN_NUM):
                if j == RATIO_ALL:
                    stat[j][dir_name][k][error_bound] = (t_eb[j][k]/file_count)
                else:
                    stat[j][dir_name][k][error_bound] = ((t_eb[j][k]/file_count/3) * 1000)
        
    elif "FINISHED" in line:
        break 
        
    i += 1

f.close()

print(dataset_names)
# matplotlib.rcParams['font.family']='Times New Roman'

bmap = brewer2mpl.get_map('set1', 'qualitative', 9)
colors = bmap.mpl_colors

filter = ['bump_dense', 'eddy_velx_f4', 'EXAALT', 'CESM_ATM', 'Hurricane', 'Miranda', 'EXASKY_NYX', 'QMCPack']
filter = dataset_names

# bottom = [3,2,1,3,4,3,1,1]
# top    = [8,7,6,8,8,8,6,6]

i = 1
r=2
l=2
size = [6,5*r/2]


# 总体压缩时间
i = 1
ylims=[0,12,55,160,240,880,1400,6500,7000]
fig3 = plt.figure(figsize=size, dpi=500)
for dataset in filter:
    # print(dataset)
    # print(stat[CTIME_ALL][dataset][HUFFMAN])
    # print(stat[CTIME_ALL][dataset][ZFP])
    # print(stat[CTIME_ALL][dataset][FSE])
    ax = fig3.add_subplot(r,l,i)
    ax.set_title('('+ chr(ord('a')+i-1) +') '+ dataset , y=-0.5, fontsize=14)
    # if (i-1)%l==0:
    ax.set_ylabel('Time Cost (ms)')
    ax.set_xlabel('Error Bounds')
    # plt.ylim(0,2500)
    
    x = np.arange(len(stat[CTIME_ALL][dataset][0].keys())) #总共有几组，就设置成几，我们这里有三组，所以设置为3
    total_width, n = 0.6, 3    # 有多少个类型，只需更改n即可，比如这里我们对比了四个，那么就把n设成4
    width = total_width / n
    x = x - (total_width - width) / 2
    # width += 0.01
    plt.grid(linestyle=':', color="gray",axis='y',zorder=1)
    c0=plt.bar(x-1.5*width,stat[CTIME_ALL][dataset][HUFFMAN].values(),width=width-0.01,label='comp-SZ',lw=0.02,edgecolor='Black',color='w',zorder=100)
    # matplotlib.rcParams['hatch.color']=colors[0]
    matplotlib.rcParams['hatch.linewidth']=0.04
    c2=plt.bar(x-0.5*width,stat[CTIME_ALL][dataset][FSE].values(),width=width-0.01,label='comp-SZ_ADT',lw=0.01,edgecolor='black',color='#87CEFA',zorder=100)
    plt.xticks(x,stat[CTIME_ALL][dataset][0].keys())
    # plt.ylim([0,ylims[i]])
    c10=plt.bar(x+0.5*width,stat[DTIME_ALL][dataset][HUFFMAN].values(),width=width-0.01,label='decomp-SZ',lw=0.02,edgecolor='Black',color='#DCDCDC',zorder=100)
    # matplotlib.rcParams['hatch.color']=colors[0]
    c12=plt.bar(x+1.5*width,stat[DTIME_ALL][dataset][FSE].values(),width=width-0.01,label='decomp-SZ_ADT',lw=0.01,edgecolor='black',color='#ff9912',zorder=100)
    plt.legend(frameon=True,fontsize=8,loc='upper left',ncol=1,columnspacing=1) #去掉图例边框
    
    # l1=plt.legend([c0,c2],['comp-SZ','comp-SZ_ADT'],frameon=True,fontsize=7,loc='upper left',ncol=1,columnspacing=1) #去掉图例边框
    
    # plt.legend([c10,c12],['decomp-SZ','decomp-SZ_ADT'],frameon=True,fontsize=7,loc=[0.02,0.51],ncol=1,columnspacing=1) #去掉图例边框
    # plt.gca().add_artist(l1)
    
    i += 1

plt.subplots_adjust(left=0.1,right=0.96,bottom=0.17,top=0.96,wspace=0.32,hspace=0.6) 
# plt.tight_layout()
picpath = '/home/zhongyu/test/paper_test/test2/3/fig/ebmodes.png'
plt.savefig(picpath)
picpath_pdf = '/home/zhongyu/test/paper_test/test2/3/fig/ebmodes.pdf'
plt.savefig(picpath_pdf)
print(picpath_pdf)


# 总体解压时间
i = 1
fig4 = plt.figure(figsize=size, dpi=100)
for dataset in filter:
    # print(dataset)
    # print(stat[DTIME_ALL][dataset][HUFFMAN])
    # print(stat[DTIME_ALL][dataset][ZFP])
    # print(stat[DTIME_ALL][dataset][FSE])
    ax = fig4.add_subplot(r,l,i)
    ax.set_title('('+ chr(ord('a')+i-1) +') '+ dataset , y=-0.5, fontsize=14)
    # if (i-1)%l==0:
    ax.set_ylabel('Decompression Time (ms)')
    ax.set_xlabel('Error Bounds')
    
    x = np.arange(len(stat[DTIME_ALL][dataset][0].keys())) #总共有几组，就设置成几，我们这里有三组，所以设置为3
    total_width, n = 0.6, 2    # 有多少个类型，只需更改n即可，比如这里我们对比了四个，那么就把n设成4
    width = total_width / n
    x = x - (total_width - width) / 2

    plt.grid(linestyle=':', color="gray",axis='y',zorder=1)
    c0=plt.bar(x-width,stat[DTIME_ALL][dataset][HUFFMAN].values(),width=width,label='SZ',lw=0.02,edgecolor='Black',color='w',zorder=2)
    # matplotlib.rcParams['hatch.color']=colors[0]
    matplotlib.rcParams['hatch.linewidth']=0.04
    c2=plt.bar(x+width,stat[DTIME_ALL][dataset][FSE].values(),width=width,label='SZ_ADT',lw=0.01,edgecolor='black',color='#ff9912',zorder=2)
    plt.xticks(x,stat[DTIME_ALL][dataset][0].keys())
    # plt.ylim([0,ylims[i]])

    plt.legend([c0,c2],['SZ','SZ_ADT'],frameon=False,fontsize=7,loc='upper center',ncol=1,columnspacing=1) #去掉图例边框
    # plt.legend(loc='best',frameon=False) #去掉图例边框
    i += 1


plt.subplots_adjust(left=0.1,right=0.96,bottom=0.17,top=0.96,wspace=0.32,hspace=0.6) 
# plt.tight_layout()
# plt.legend(loc = 'upper right')
picpath = '/home/zhongyu/test/paper_test/test2/3/fig/decom_overall.png'
# plt.savefig(picpath)
picpath_pdf = '/home/zhongyu/test/paper_test/test2/3/fig/decom_overall.pdf'
plt.savefig(picpath_pdf)
print(picpath)

# 总体压缩率
i = 1
fig5 = plt.figure(figsize=size, dpi=100)
ylabels=[ 
    [],
    [0,1,4,16],
    [0,1,2],
    [0,1,2],
    [0,1,4,16,64],
]
for dataset in filter:
    # print(dataset)
    # print(stat[RATIO_ALL][dataset][HUFFMAN])
    # print(stat[RATIO_ALL][dataset][ZFP])
    # print(stat[RATIO_ALL][dataset][FSE])
    ax = fig5.add_subplot(r,l,i)
    ax.set_title('('+ chr(ord('a')+i-1) +') '+ dataset , y=-0.5, fontsize=14)
    # if (i-1)%l==0:
    ax.set_ylabel('Compression Ratio')
    ax.set_xlabel('Error Bounds')
    
    x = np.arange(len(stat[RATIO_ALL][dataset][0].keys())) #总共有几组，就设置成几，我们这里有三组，所以设置为3
    total_width, n = 0.6, 2    # 有多少个类型，只需更改n即可，比如这里我们对比了四个，那么就把n设成4
    width = total_width / n
    x = x - (total_width - width) / 2

    plt.grid(linestyle=':', color="gray",axis='y',zorder=1)
    c0=plt.bar(x-width,stat[RATIO_ALL][dataset][HUFFMAN].values(),width=width-0.01,label='SZ',lw=0.02,edgecolor='Black',color='w',zorder=2)
    matplotlib.rcParams['hatch.linewidth']=0.04
    c2=plt.bar(x+width,stat[RATIO_ALL][dataset][FSE].values(),width=width-0.01,label='SZ_ADT',lw=0.01,edgecolor='black',color='#ff9912',zorder=2)
    plt.xticks(x,stat[RATIO_ALL][dataset][0].keys())
    # plt.ylim(bottom=0)

    plt.legend([c0,c2],['SZ','ZFP','SZ_ADT'],frameon=True,fontsize=7,loc='upper right',ncol=1,columnspacing=1) #去掉图例边框
    

    ax.set_yscale('log',base=2)
    ax.set_ylim(bottom=1)
    # ax.set_yticklabels(ylabels[i])
    i += 1

plt.subplots_adjust(left=0.1,right=0.96,bottom=0.17,top=0.96,wspace=0.32,hspace=0.6) 
# plt.tight_layout()
picpath = '/home/zhongyu/test/paper_test/test2/3/fig/overall.png'
# plt.savefig(picpath)
picpath_pdf = '/home/zhongyu/test/paper_test/test2/3/fig/overall.pdf'
plt.savefig(picpath_pdf)
print(picpath)
# os.system('rm -f {} {}' .format(picpath,picpath_pdf))


# from matplotlib import font_manager
 
# for font in font_manager.fontManager.ttflist:
#     # 查看字体名以及对应的字体文件名
#     print(font.name, '-', font.fname)