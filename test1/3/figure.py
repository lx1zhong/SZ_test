# 压缩率随压缩粒度的变化曲线图，每个数据集一个图

from cProfile import label
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import glob2


input_files = glob2.glob("/home/zhongyu/test/paper_test/test1/1/output/2*.txt")

ID = ['SIZE_HUF_PART','TIME_HUF_PART','SIZE_ZSTD_PART','TIME_ZSTD_PART','SIZE_HUF_ALL','TIME_HUF_ALL','SIZE_ZSTD_ALL','TIME_ZSTD_ALL']
SIZE_HUF_PART = 0       #compressed size (huffman / fse) (encoder)
TIME_HUF_PART = 1       #compression time (huffman / fse) (encoder)
SIZE_ZSTD_PART = 2      #compressed size (zstd / fse) (encoder)
TIME_ZSTD_PART = 3      #compression time (zstd / fse) (encoder)
SIZE_HUF_ALL = 4        #compressed size (huffman / fse) (sz)
TIME_HUF_ALL = 5        #compression time (huffman / fse) (sz)
SIZE_ZSTD_ALL = 6       #compressed size (zstd / fse) (sz)
TIME_ZSTD_ALL = 7       #compression time (zstd / fse) (sz)
DTIME_HUF_ALL = 8       #decompression time (huffman / fse) (sz)
DTIME_ZSTD_ALL = 9      #decompression time (zstd / fse) (sz)
TOTAL_NUM = 10

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
    else:
        return str(x/1024)+'M'

for input_file in input_files:
    print(input_file)
    temp = input_file.split('/')
    temp = temp[-1]
    temp = temp.split('.')
    eb = temp[0]

    f = open(input_file, 'r')
    
    # # 最后打印数据
    # stat = [ {} for i in range(TOTAL_NUM)]
    # # 一个DIR内的所有ratios数值
    # ratios = [ [] for i in range(TOTAL_NUM)]
    # # 一个ratio数值
    # ratio = [ 0.0 for i in range (TOTAL_NUM)]

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
            # 一个ratio数值
            ratio = [ 0.0 for i in range (TOTAL_NUM)]

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
            # huffman_outsize_part = get_num(temp[1])
            # huffman_time_part = get_f(temp[2])
            
            # temp = lines[i+5].split()
            # huffman_time_all = float(temp[-1])
            # huffman_outsize_all = float(lines[i+6].split('/')[0])

            if 'origin data' in lines[i+7]:
                i += 1

            # temp = lines[i+7].split()
            # # print(str(i) + str(temp))
            # huffman_dtime_all = float(temp[3])
            
            i += 7
            # zstd
            assert('===zstd===' in lines[i])
            assert('[zstd]' in lines[i+2])
            temp = lines[i+2].split()
            zstd_ratio += 1/get_f(temp[1])
            # zstd_outsize_part = get_num(temp[1])
            # zstd_time_part = get_f(temp[2])
            
            # temp = lines[i+4].split()
            # zstd_time_all = float(temp[-1])
            # zstd_outsize_all = float(lines[i+5].split('/')[0])

            # if 'decompress' in lines[i+6]:
            
            #     temp = lines[i+6].split()
            #     zstd_dtime_all = float(temp[3])
            #     i += 7
            # else:
            #     zstd_dtime_all = 0
            i += 6

            # fse
            # print(str(i) + ':' + lines[i])
            assert('===fse===' in lines[i])
            assert('[fse]' in lines[i+3])
            temp = lines[i+3].split()
            fse_ratio += 1/get_f(temp[1])
            # fse_outsize_part = get_num(temp[1])
            # fse_time_part = get_f(temp[2])
            
            # temp = lines[i+5].split()
            # fse_time_all = float(temp[-1])
            # fse_outsize_all = float(lines[i+6].split('/')[0])

            
            # temp = lines[i+7].split()
            # print(str(i) + str(temp))
            # fse_dtime_all = float(temp[3])

            # 计算
            file_count += 1
            # print(ratio)
            # ratio[SIZE_HUF_PART] = huffman_outsize_part / fse_outsize_part
            # ratio[TIME_HUF_PART] = huffman_time_part / fse_time_part

            # ratio[SIZE_ZSTD_PART] = zstd_outsize_part / fse_outsize_part
            # ratio[TIME_ZSTD_PART] = zstd_time_part /fse_time_part

            # ratio[SIZE_HUF_ALL] = huffman_outsize_all / fse_outsize_all
            # ratio[TIME_HUF_ALL] = huffman_time_all / fse_time_all

            # ratio[SIZE_ZSTD_ALL] = zstd_outsize_all / fse_outsize_all
            # ratio[TIME_ZSTD_ALL] = zstd_time_all / fse_time_all

            # ratio[DTIME_HUF_ALL] = huffman_dtime_all / fse_dtime_all
            # ratio[DTIME_ZSTD_ALL] = zstd_dtime_all / fse_dtime_all

            # for j in range(TOTAL_NUM):
            #     ratios[j].append(ratio[j])

        elif "CNT" in line:
            # end of one size
            if file_count == 0:
                i += 1
                continue
            
            # calculate ave ratio
            stats[dir_name][HUFFMAN][num2tag(size)] = 1 / (huffman_ratio/file_count)
            stats[dir_name][ZSTD][num2tag(size)] = 1 / (zstd_ratio/file_count)
            stats[dir_name][FSE][num2tag(size)] = 1 / (fse_ratio/file_count)
            
            # for j in range(TOTAL_NUM):
            #     sum = 0.0
            #     for r in ratios[j]:
            #         sum += r
            #     ave_ratio = sum / file_count

            #     stat[j][dir_name] = ave_ratio

            # print(dir_name + ' ' + error_bound + ':')
            # for j in range(TOTAL_NUM):
            #     print('\t' + ID[j] + '=' + str(stat[j][dir_name]))

            # for j in range(TOTAL_NUM):
            #     ratios.clear()
        elif "FINISHED" in line:
            break 
            
        i += 1

    f.close()

    print(dataset_names)
    # matplotlib.rcParams['font.family']='SimHei'
    fig = plt.figure()

    filter = ['CESM_ATM', 'EXAALT ', 'exaalt_helium', 'EXASKY_NYX', 'Hurricane', 'Miranda', 'QMCPack',  'SCALE']

    i = 1
    for dataset in dataset_names:
        print(dataset)
        print(stats[dataset][HUFFMAN])
        print(stats[dataset][ZSTD])
        print(stats[dataset][FSE])
        ax = fig.add_subplot(3,4,i)
        ax.set_title(dataset)
        ax.set_ylabel('compression ratio')
        plt.plot(stats[dataset][0].keys(),stats[dataset][HUFFMAN].values(),label='huffman')
        plt.plot(stats[dataset][0].keys(),stats[dataset][ZSTD].values(),label='zstd')
        plt.plot(stats[dataset][0].keys(),stats[dataset][FSE].values(),label='fse')

        i += 1
    plt.legend()

    # # 1
    # ax1 = fig.add_subplot(2,2,1)
    # ax1.set_title('huf  /  fse '  + eb)
    # # ax1.set_xlabel('size ratio')
    # ax1.set_ylabel('time ratio')
    # # plt.xlim(-1,1)
    # # plt.ylim(-1,1)
    # plt.vlines(x=1, ymin=0.5, ymax=1.5, 
    #         colors='black', linewidth=1)
    # plt.hlines(y=1, xmin=0.5, xmax=1.5,
    #         colors='black', linewidth=1)

    # for dataset in dataset_names:
    #     if dataset in stat[0].keys() :
    #         ax1.scatter(stat[SIZE_HUF_PART][dataset], stat[TIME_HUF_PART][dataset], label=dataset)
    #         # ax1.plot(stat_size[dataset], stat_time[dataset], label = dataset)
    #         # print(stat_size[dataset] + stat_time[dataset])
    
    # # 2
    # ax2 = fig.add_subplot(2,2,2)
    # ax2.set_title('huf  /  fse  all '  + eb)
    # # ax2.set_xlabel('size ratio')
    # # ax2.set_ylabel('time ratio')
    # # plt.xlim(-1,1)
    # # plt.ylim(-1,1)
    # plt.vlines(x=1, ymin=0.75, ymax=1.25, 
    #         colors='black', linewidth=1)
    # plt.hlines(y=1, xmin=0.75, xmax=1.25,
    #         colors='black', linewidth=1)

    # for dataset in dataset_names:
    #     if dataset in stat[0].keys() :
    #         ax2.scatter(stat[SIZE_HUF_ALL][dataset], stat[TIME_HUF_ALL][dataset], label=dataset)
    #         # ax2.plot(stat_size[dataset], stat_time[dataset], label = dataset)
    #         # print(stat_size[dataset] + stat_time[dataset])

    # # 3
    # ax3 = fig.add_subplot(2,2,3)
    # ax3.set_title('zstd  /  fse '  + eb)
    # ax3.set_xlabel('size ratio')
    # ax3.set_ylabel('time ratio')
    # # plt.xlim(-1,1)
    # # plt.ylim(-1,1)
    # plt.vlines(x=1, ymin=0.5, ymax=1.5, 
    #         colors='black', linewidth=1)
    # plt.hlines(y=1, xmin=0.5, xmax=1.5,
    #         colors='black', linewidth=1)

    # for dataset in dataset_names:
    #     if dataset in stat[0].keys() :
    #         ax3.scatter(stat[SIZE_ZSTD_PART][dataset], stat[TIME_ZSTD_PART][dataset], label=dataset)
    #         # ax3.plot(stat_size[dataset], stat_time[dataset], label = dataset)
    #         # print(stat_size[dataset] + stat_time[dataset])

    # # 4
    # ax4 = fig.add_subplot(2,2,4)
    # ax4.set_title('zstd  /  fse  all '  + eb)
    # ax4.set_xlabel('size ratio')
    # # ax1.set_ylabel('time ratio')
    # # plt.xlim(-1,1)
    # # plt.ylim(-1,1)
    # plt.vlines(x=1, ymin=0.5, ymax=1.5, 
    #         colors='black', linewidth=1)
    # plt.hlines(y=1, xmin=0.5, xmax=1.5,
    #         colors='black', linewidth=1)

    # for dataset in dataset_names:
    #     if dataset in stat[0].keys() :
    #         ax4.scatter(stat[SIZE_ZSTD_ALL][dataset], stat[TIME_ZSTD_ALL][dataset], label=dataset)
    #         # ax1.plot(stat_size[dataset], stat_time[dataset], label = dataset)
    #         # print(stat_size[dataset] + stat_time[dataset])

    plt.tight_layout()
    # plt.legend(loc = 'upper left')
    picpath = '/home/zhongyu/test/paper_test/test1/1/fig/3' + eb + '.png'
    plt.savefig(picpath)
    print(picpath)
    # plt.show()
