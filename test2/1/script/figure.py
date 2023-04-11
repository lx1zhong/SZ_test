# 压缩/解压时延随EB的变化柱状图，每个数据集一个图

# DIR--EB--FILE

from cProfile import label
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import glob2
import os
import brewer2mpl

input_files = glob2.glob("./output/ABS.txt")

ID = ['RATIO_ALL','CTIME_ALL','DTIME_ALL']
RATIO_ALL = 0
CTIME_ALL = 1
DTIME_ALL = 2
TOTAL_NUM = 3


HUFFMAN = 0
ZFP = 1
FSE = 2
PLAN_NUM = 3

No = {'bump_dense':0, 'eddy_velx_f4':1, 'EXAALT':2, 'CESM_ATM':3, 'Hurricane':4, 'Miranda':5, 'EXASKY_NYX':6, 'QMCPack':7}
# filter = dataset_names

# eb range to show
bottom = [3,1,1,2,1,3,1,1]
top    = [8,6,6,7,6,8,6,6]

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

for input_file in input_files:
    print(input_file)
    temp = input_file.split('/')
    temp = temp[-1]
    temp = temp.split('.')
    ebMode = temp[0]
    if ebMode[0] == '2':
        ebMode = ebMode[1:]

    f = open(input_file, 'r')


    # # 最后打印数据
    stat = [ {} for i in range(TOTAL_NUM)]
    # stats_com = {}
    # stats_decom = {}
    dataset_names = []

    file_count = 0
    error_bound = ""
    dir_flag = 0
    dirs_size = {}

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
        if "DIR" in line:
            dir_flag = 1
            temp = line.split()
            temp = temp[1].split('-')
            # dataset name
            dir_name = temp[1]
            dir_size = cal_size(temp[2], temp[3])
            # print(dir_name + ':' + str(dir_size))
            dirs_size[dir_name] = dir_size
            # print("dir:"+dir_name)
            dataset_names.append(dir_name)

            for j in range(TOTAL_NUM):
                stat[j][dir_name] = [{},{},{}]

        elif "EB" in line:
            file_count = 0
            temp = line.split()
            error_bound = temp[-1]
            
            # stats[dir_name][size] = [0,0,0]
            t_eb = [ [0,0,0] for i in range(TOTAL_NUM)]
            huffman_ctime = 0
            zfp_ctime = 0
            fse_ctime = 0
            huffman_dtime = 0
            zfp_dtime = 0
            fse_dtime = 0

        elif "FILE" in line:
            t = [ [0,0,0] for i in range(TOTAL_NUM)]
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
            # zfp
            assert('===zfp===' in lines[i])
            assert('compress' in lines[i+1])
            assert('compress' in lines[i+3])
            assert('compress' in lines[i+5])
            temp = lines[i+1].split()
            t[CTIME_ALL][ZFP] += float(temp[2])
            temp = lines[i+3].split()
            t[CTIME_ALL][ZFP] += float(temp[2])
            temp = lines[i+5].split()
            t[CTIME_ALL][ZFP] += float(temp[2])

            temp = lines[i+2].split()
            t[RATIO_ALL][ZFP] += get_f(temp[-2])

            assert('decompress' in lines[i+8])
            assert('decompress' in lines[i+10])
            assert('decompress' in lines[i+12])
            temp = lines[i+8].split()
            t[DTIME_ALL][ZFP] += float(temp[2])
            temp = lines[i+10].split()
            t[DTIME_ALL][ZFP] += float(temp[2])
            temp = lines[i+12].split()
            t[DTIME_ALL][ZFP] += float(temp[2])

            i += 14

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
                while 'FILE' not in lines[i] and 'EB' not in lines[i] and 'DIR' not in lines[i] and 'CNT' not in lines[i] and 'FINISHED' not in lines[i]:
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
            if ebMode == 'ABS' and dir_name in No.keys() and e >= bottom[No[dir_name]] and e <= top[No[dir_name]] or ebMode == 'PW_REL':
                for j in range(TOTAL_NUM):
                    for k in range(PLAN_NUM):
                        if j == RATIO_ALL:
                            stat[j][dir_name][k][error_bound] = (t_eb[j][k]/file_count)
                        else:
                            stat[j][dir_name][k][error_bound] = dirs_size[dir_name]  / ((t_eb[j][k]/file_count/3) * 1000) if t_eb[j][k] != 0 else 0 
                        
        elif "FINISHED" in line:
            break 
            
        i += 1

    f.close()

    print(dataset_names)
    # matplotlib.rcParams['font.family']='Times New Roman'

    bmap = brewer2mpl.get_map('set1', 'qualitative', 9)
    colors = bmap.mpl_colors

    i = 1
    r=2
    l=4

    filter = ['bump_dense', 'EXAALT', 'Hurricane', 'Miranda']
    
    # overall compression throughput
    for dataset in filter:
        print(dataset)
        print(stat[CTIME_ALL][dataset][HUFFMAN])
        # print(stat[CTIME_ALL][dataset][ZFP])
        print(stat[CTIME_ALL][dataset][FSE])

    i = 1
    ylims=[0,12.6,55,160,240,880,1400,6500,7000]
    fig3 = plt.figure(figsize=[6,5], dpi=100)
    for dataset in filter:
        # print(dataset)
        # print(stat[CTIME_ALL][dataset][HUFFMAN])
        # print(stat[CTIME_ALL][dataset][ZFP])
        # print(stat[CTIME_ALL][dataset][FSE])
        ax = fig3.add_subplot(2,2,i)
        ax.set_title('('+ chr(ord('a')+i-1) +') '+ dataset + ' (' + num2tag(dirs_size[dataset]) + 'B)', y=-0.5, fontsize=14)
        # if (i-1)%l==0:
        ax.set_ylabel('Compression Time (ms)')
        if 'ABS' in ebMode:  
            ax.set_xlabel('Absolute Error Bounds')
        elif 'PW_REL' in ebMode:  
            ax.set_xlabel('Point-wise Relative Error Bounds')
        
        x = np.arange(len(stat[CTIME_ALL][dataset][0].keys())) #总共有几组，就设置成几，我们这里有三组，所以设置为3
        total_width, n = 0.6, 2    # 有多少个类型，只需更改n即可，比如这里我们对比了四个，那么就把n设成4
        width = total_width / n
        x = x - (total_width - width) / 2
        width -= 0.05

        plt.grid(linestyle=':', color="gray",axis='y',zorder=1)
        c0=plt.bar(x-width,stat[CTIME_ALL][dataset][HUFFMAN].values(),width=width-0.01,label='SZ',lw=0.01,edgecolor='black',color='#DCDCDC',zorder=2)
        # matplotlib.rcParams['hatch.color']=colors[0]
        c1=plt.bar(x,stat[CTIME_ALL][dataset][ZFP].values(),width=width-0.01,label='ZFP',lw=0.01,edgecolor='black',color='#87CEFA',zorder=2)
        c2=plt.bar(x+width,stat[CTIME_ALL][dataset][FSE].values(),width=width-0.01,label='SZ_ADT',lw=0.01,edgecolor='black',color='#ff9912',zorder=2)
        plt.xticks(x,stat[CTIME_ALL][dataset][0].keys())
        # plt.ylim([0,ylims[i]])

        plt.legend([c0,c1,c2],['SZ','ZFP','SZ_ADT'],frameon=False,fontsize=7,loc='upper center',ncol=3,columnspacing=1) #去掉图例边框
        # plt.legend(loc='best',frameon=False) #去掉图例边框
        i += 1
    
    plt.subplots_adjust(left=0.1,right=0.96,bottom=0.17,top=0.96,wspace=0.32,hspace=0.6) 

    # plt.subplots_adjust(left=0.06,right=0.96,bottom=0.33,top=0.93,wspace=0.4,hspace=0.6) 
    # plt.tight_layout()
    picpath = './fig/com_' + ebMode + '_overall.png'
    plt.savefig(picpath)
    picpath_pdf = './fig/com_' + ebMode + '_overall.pdf'
    plt.savefig(picpath_pdf)
    print(picpath_pdf)

    # overall decompression throughput
    i = 1
    fig4 = plt.figure(figsize=[12,2.8], dpi=100)
    for dataset in filter:
        # print(dataset)
        # print(stat[DTIME_ALL][dataset][HUFFMAN])
        # print(stat[DTIME_ALL][dataset][ZFP])
        # print(stat[DTIME_ALL][dataset][FSE])
        ax = fig4.add_subplot(1,l,i)
        ax.set_title('('+ chr(ord('a')+i-1) +') '+ dataset + ' (' + num2tag(dirs_size[dataset]) + 'B)', y=-0.5, fontsize=14)
        # if (i-1)%l==0:
        ax.set_ylabel('Decomp. Throughput (MB/s)')
        if 'ABS' in ebMode:  
            ax.set_xlabel('Absolute Error Bounds')
        elif 'PW_REL' in ebMode:  
            ax.set_xlabel('Point-wise Relative Error Bounds')
        
        x = np.arange(len(stat[DTIME_ALL][dataset][0].keys())) #总共有几组，就设置成几，我们这里有三组，所以设置为3
        total_width, n = 0.6, 2    # 有多少个类型，只需更改n即可，比如这里我们对比了四个，那么就把n设成4
        width = total_width / n
        x = x - (total_width - width) / 2
        width -= 0.05

        plt.grid(linestyle=':', color="gray",axis='y',zorder=1)
        c0=plt.bar(x-width,stat[DTIME_ALL][dataset][HUFFMAN].values(),width=width-0.01,label='SZ',lw=0.01,edgecolor='Black',color='#DCDCDC',zorder=2)
        # matplotlib.rcParams['hatch.color']=colors[0]
        c1=plt.bar(x,stat[DTIME_ALL][dataset][ZFP].values(),width=width-0.01,label='ZFP',lw=0.01,edgecolor='black',color='#87CEFA',zorder=2)
        c2=plt.bar(x+width,stat[DTIME_ALL][dataset][FSE].values(),width=width-0.01,label='SZ_ADT',lw=0.01,edgecolor='black',color='#ff9912',zorder=2)
        plt.xticks(x,stat[DTIME_ALL][dataset][0].keys())
        # plt.ylim([0,ylims[i]])
        if i==1:
            plt.legend([c0,c1,c2],['SZ','ZFP','SZ_ADT'],fontsize=11,loc=[1.5,1.05],ncol=3,columnspacing=4) #去掉图例边框
        # plt.legend(loc='best',frameon=False) #去掉图例边框
        i += 1


    plt.subplots_adjust(left=0.06,right=0.96,bottom=0.30,top=0.84,wspace=0.4,hspace=0.7) 
    # plt.tight_layout()
    # plt.legend(loc = 'upper right')
    picpath = './fig/decom_' + ebMode + '_overall.png'
    plt.savefig(picpath)
    picpath_pdf = './fig/decom_' + ebMode + '_overall.pdf'
    plt.savefig(picpath_pdf)
    picpath_pdf = '../../Figure8-overall_decomp_throughput.pdf'
    plt.savefig(picpath_pdf)
    print(picpath_pdf)

    # overall compression ratio
    i = 1
    fig5 = plt.figure(figsize=[6,5], dpi=100)
    ylabels=[ 
        [],
        [0,1,4,16],
        [0,1,2],
        [0,1,2],
        [0,1,4,16,64],
        [0,1,4,16,64,256],
        [0,1,4,16,64],
        [0,1,2,4,8],
        [0,1,4,16]
    ]
    for dataset in filter:
        # print(dataset)
        # print(stat[RATIO_ALL][dataset][HUFFMAN])
        # print(stat[RATIO_ALL][dataset][ZFP])
        # print(stat[RATIO_ALL][dataset][FSE])
        ax = fig5.add_subplot(2,2,i)
        ax.set_title('('+ chr(ord('a')+i-1) +') '+ dataset + ' (' + num2tag(dirs_size[dataset]) + 'B)', y=-0.5, fontsize=14)
        # if (i-1)%l==0:
        ax.set_ylabel('Compression Ratio')
        if 'ABS' in ebMode:  
            ax.set_xlabel('Absolute Error Bounds')
        elif 'PW_REL' in ebMode:  
            ax.set_xlabel('Point-wise Relative Error Bounds')
        
        x = np.arange(len(stat[RATIO_ALL][dataset][0].keys())) #总共有几组，就设置成几，我们这里有三组，所以设置为3
        total_width, n = 0.6, 2    # 有多少个类型，只需更改n即可，比如这里我们对比了四个，那么就把n设成4
        width = total_width / n
        x = x - (total_width - width) / 2
        width -= 0.05

        plt.grid(linestyle=':', color="gray",axis='y',zorder=1)
        c0=plt.bar(x-width,stat[RATIO_ALL][dataset][HUFFMAN].values(),width=width-0.01,label='SZ',lw=0.01,edgecolor='Black',color='#DCDCDC',zorder=2)
        c1=plt.bar(x,stat[RATIO_ALL][dataset][ZFP].values(),width=width-0.01,label='ZFP',lw=0.01,edgecolor='black',color='#87CEFA',zorder=2)
        c2=plt.bar(x+width,stat[RATIO_ALL][dataset][FSE].values(),width=width-0.01,label='SZ_ADT',lw=0.01,edgecolor='black',color='#ff9912',zorder=2)
        plt.xticks(x,stat[RATIO_ALL][dataset][0].keys())

        if i==1:
            plt.legend([c0,c1,c2],['SZ','ZFP','SZ_ADT'],frameon=True,fontsize=11,loc=[0.45,1.05],ncol=3,columnspacing=1) #去掉图例边框
        

        ax.set_yscale('log',base=2)
        ax.set_ylim(bottom=1)
        ax.set_yticklabels(ylabels[i])
        i += 1
    
    plt.subplots_adjust(left=0.1,right=0.96,bottom=0.17,top=0.92,wspace=0.32,hspace=0.6) 

    # plt.subplots_adjust(left=0.06,right=0.96,bottom=0.33,top=0.93,wspace=0.4,hspace=0.6) 
    # plt.tight_layout()
    picpath = '../2/fig/' + ebMode + '_overall.png'
    plt.savefig(picpath)
    picpath_pdf = '../2/fig/' + ebMode + '_overall.pdf'
    plt.savefig(picpath_pdf)
    print(picpath_pdf)
    # os.system('rm -f {} {}' .format(picpath,picpath_pdf))
