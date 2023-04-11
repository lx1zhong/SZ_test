# [Curve chart] Compression ratio ~ Granularity

from cProfile import label
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import glob2


input_files = glob2.glob("/home/zhongyu/test/paper_test/test1/1/output/*_1E-4.txt")
filter = ['EXAALT_HELIUM', 'Hurricane', 'Miranda', 'EXASKY_NYX']

HUFFMAN = 0
ZSTD = 1
FSE = 2

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

for input_file in input_files:
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
            stats[dir_name] = [{},{},{}]
            
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

            if 'origin data' in lines[i+7]:
                i += 1

            
            i += 7
            # zstd
            assert('===zstd===' in lines[i])
            assert('[zstd]' in lines[i+2])
            temp = lines[i+2].split()
            zstd_ratio += 1/get_f(temp[1])
            i += 6

            # fse
            # print(str(i) + ':' + lines[i])
            assert('===fse===' in lines[i])
            assert('[fse]' in lines[i+3])
            temp = lines[i+3].split()
            fse_ratio += 1/get_f(temp[1])

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
fig = plt.figure(figsize=[6,5], dpi=100)

# filter = ['CESM_ATM', 'EXAALT', 'EXAALT_HELIUM', 'EXASKY_NYX', 'Hurricane', 'Miranda', 'QMCPack',  'SCALE']
# ylims=[0,11,6,6,12,9,13,7,12]
# filter = ['bump_dense', 'eddy_velx_f4', 'EXAALT', 'CESM_ATM', 'Hurricane', 'Miranda', 'EXASKY_NYX', 'QMCPack']

ylims=[0,7.5,12,16,13]

i = 1
r=2
l=2
for dataset in filter:
    # print(dataset)
    print(Res[1][dataset][HUFFMAN])
    # print(Res[1][dataset][ZSTD])
    print(Res[1][dataset][FSE])
    ax = fig.add_subplot(r,l,i)
    ax.set_title('('+ chr(ord('a')+i-1) +') '+ dataset , y=-0.5, fontsize=14)
    
    # if (i-1)%l==0:
    ax.set_ylabel('Compression Ratio')
    ax.set_xlabel('Compression Granularity (Bytes)')
    a0,=plt.plot(Res[1][dataset][0].keys(),Res[1][dataset][HUFFMAN].values(),'*-.',markersize=6,label='Huffman(ABS)',color='#1f77b4')
    a1,=plt.plot(Res[1][dataset][0].keys(),Res[1][dataset][ZSTD].values(),'x:',markersize=5,label='Zstd(ABS)',color='#1f77b4')#ff7f0e
    a2,=plt.plot(Res[1][dataset][0].keys(),Res[1][dataset][FSE].values(),'o-',markersize=3,label='ADT-FSE(ABS)',color='#1f77b4')#2ca02c
    b0,=plt.plot(Res[0][dataset][0].keys(),Res[0][dataset][HUFFMAN].values(),'*-.',markersize=6,label='Huffman(PWR)',color='#ff7f0e')#1f77b4
    b1,=plt.plot(Res[0][dataset][0].keys(),Res[0][dataset][ZSTD].values(),'x:',markersize=5,label='Zstd(PWR)',color='#ff7f0e')#ff7f0e
    b2,=plt.plot(Res[0][dataset][0].keys(),Res[0][dataset][FSE].values(),'o-',markersize=3,label='ADT-FSE(PWR)',color='#ff7f0e')#2ca02c
    plt.xticks(size=9)
    plt.ylim([0,ylims[i]])

    # l1=plt.legend(frameon=False,fontsize=7,loc='lower left',ncol=1,columnspacing=1) #去掉图例边框
    if i == 2:
        l1=plt.legend((a0,a1,a2),['Huffman(ABS)','Zstd(ABS)','ADT-FSE(ABS)'],frameon=True,fontsize=7,loc = 'upper left',ncol=1,columnspacing=1) #去掉图例边框
        # ax.set_yticklabels([0,2,4,6,8,10])
        plt.yticks(np.linspace(0,12,6,endpoint=False))
    else:
        l1=plt.legend((a0,a1,a2),['Huffman(ABS)','Zstd(ABS)','ADT-FSE(ABS)'],frameon=True,fontsize=7,loc = 'upper left',ncol=1,columnspacing=1) #去掉图例边框
    plt.legend((b0,b1,b2),['Huffman(PWR)','Zstd(PWR)','ADT-FSE(PWR)'],frameon=True,fontsize=7,loc = 'upper right',ncol=1,columnspacing=1) #去掉图例边框
    plt.gca().add_artist(l1)
    i += 1

# matplotlib.rcParams['font.family']='SimHei'
# matplotlib.rcParams['figure.figsize']=[12,8]

plt.subplots_adjust(left=0.1,right=0.96,bottom=0.17,top=0.96,wspace=0.32,hspace=0.6) 
# plt.tight_layout()
# plt.subplots_adjust(wspace=0.3,hspace=0.4) #left=1,right=1,bottom=1,top=1,
# plt.legend(loc = 'upper right')
picpath = './fig/ratio_part.png'
plt.savefig(picpath)
picpath_pdf = './fig/ratio_part.pdf'
plt.savefig(picpath_pdf)
print(picpath_pdf)
# plt.show()
