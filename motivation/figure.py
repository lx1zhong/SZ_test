# motivation : huffman时间占比和树占比

from cProfile import label
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
import os
import palettable
from palettable.cartocolors.qualitative import Bold_9

labels= ['Compresion', 'Decompression']

ctime = {
    'Predict & Quantize': 3.179,
    'Huffman': 4.433,
    'Zstd': 2.335,
    'Other': 0.525
}

dtime = {
    'Zstd': 0.620,
    'Huffman': 5.705,
    'P': 1.44,
    'Other':0.144
}

length = {
    'Huffman tree': 1703482,
    'Huffman encode': 5576703,
    'Unpredictable': 169202,
    'Other':    105
}

ctime_all=113.256
ctime_huffman=57.932
ctime_point=32.197
ctime_zstd=16.57
ctime_other=ctime_all-ctime_huffman-ctime_point-ctime_zstd

dtime_all=251.564
dtime_huffman=233.015
dtime_point=11.228
dtime_zstd=6.061
dtime_other=dtime_all-dtime_huffman-dtime_point-dtime_zstd


stats = {
    'Predict & Quantize': [ctime_point, dtime_point],
    'Huffman': [ctime_huffman,dtime_huffman],
    'Zstd':[ctime_zstd,dtime_zstd],
    'Other': [ctime_other,dtime_other],
}

fig3 = plt.figure(figsize=[6,4], dpi=100)
ax = fig3.add_subplot(1,2,1)
ax.set_title('(a) Time cost breakdown' , y=-0.25, fontsize=14)
# if (i-1)%l==0:
ax.set_ylabel('Time cost (ms)', fontsize=12)
plt.grid(linestyle=':', color="gray",axis='y',zorder=1)
x = np.arange(2) #总共有几组，就设置成几，我们这里有三组，所以设置为3
total_width, n = 0.6, 1    # 有多少个类型，只需更改n即可，比如这里我们对比了四个，那么就把n设成4
width = total_width / n
x = x - (total_width - width) / 2

# plt.xticks(means.keys())
# plt.bar(means.keys(), means.values(),yerr=stds.values(),ecolor='black',capsize=4,zorder=100)

plt.ylim([0,300])

plt.xticks(x,labels, fontsize=12)
# plt.bar(x,stats['Predict & Quantize'],label='Predict & Quantize',width=width-0.05,zorder=100)
# plt.bar(x,stats['Huffman'],label='Huffman',width=width-0.05,zorder=100)
# plt.bar(x,stats['Zstd'],label='Zstd',width=width-0.05,zorder=100)
bottom=[0,0]


colors = ['mediumturquoise','lightskyblue','steelblue','orange']
j=0
for label in stats.keys():
    print(label)
    if j == 1:
        plt.bar(x,stats[label],label=label,width=width-0.05,edgecolor='black',hatch='///',lw=0.01,zorder=100,bottom=bottom,color=colors[j])
        matplotlib.rcParams['hatch.linewidth']=0.1
    else:
        plt.bar(x,stats[label],label=label,width=width-0.05,edgecolor='black',lw=0.01,zorder=100,bottom=bottom,color=colors[j])
    for i in range(len(bottom)):
        bottom[i] = bottom[i] + stats[label][i]
    j = j+1

# c0=plt.bar(x-1.5*width,means[SZ]['1'].values(),yerr=stds[SZ]['1'].values(),width=width-0.06,label='1% SZ',lw=0.02,edgecolor='Black',color='w',ecolor='black',capsize=4,zorder=100)

# c2=plt.bar(x-0.5*width,means[SZ_ADT]['1'].values(),yerr=stds[SZ_ADT]['1'].values(),width=width-0.06,label='1% SZ_ADT',lw=0.01,edgecolor='black',color='#87CEFA',ecolor='black',capsize=4,zorder=100)
# # print(means[SZ]['1'].keys())
# plt.xticks(x,means[SZ]['1'].keys(), rotation=0)
# # plt.ylim([0,ylims[i]])
# c10=plt.bar(x+0.5*width,means[SZ]['5'].values(),yerr=stds[SZ]['5'].values(),width=width-0.06,label='5% SZ',lw=0.02,edgecolor='Black',color='#DCDCDC',ecolor='black',capsize=4,zorder=100)

# c12=plt.bar(x+1.5*width,means[SZ_ADT]['5'].values(),yerr=stds[SZ_ADT]['5'].values(),width=width-0.06,label='5% SZ_ADT',lw=0.01,edgecolor='black',color='#ff9912',ecolor='black',capsize=4,zorder=100)

# c10=plt.bar(x+0.5*width,stat[DTIME_ALL][dataset][HUFFMAN].values(),width=width-0.06,label='decomp-SZ',lw=0.02,edgecolor='Black',color='#DCDCDC',zorder=100)
# # matplotlib.rcParams['hatch.color']=colors[0]
# c12=plt.bar(x+1.5*width,stat[DTIME_ALL][dataset][FSE].values(),width=width-0.06,label='decomp-SZ_ADT',lw=0.01,edgecolor='black',color='#ff9912',zorder=100)
plt.legend(frameon=True,fontsize=9,loc='upper left',ncol=1,columnspacing=1) #去掉图例边框
    

ax.set_ylim(bottom=0)



ax2 = fig3.add_subplot(1,2,2)
ax2.set_title('(b) Size breakdown\nof compressed data' , y=-0.3, fontsize=14)
# if (i-1)%l==0:
ax2.set_ylabel('Data Size (MB)', fontsize=12)
plt.grid(linestyle=':', color="gray",axis='y',zorder=1)
x = np.arange(1) #总共有几组，就设置成几，我们这里有三组，所以设置为3
total_width, n = 0.6, 1    # 有多少个类型，只需更改n即可，比如这里我们对比了四个，那么就把n设成4
width2 = total_width / n
x = x - (total_width - width2) / 2

# plt.xticks(means.keys())
# plt.bar(means.keys(), means.values(),yerr=stds.values(),ecolor='black',capsize=4,zorder=100)

plt.ylim([0,10])

plt.xticks(x,['Compressed data'], fontsize=12)
# plt.bar(x,stats['Predict & Quantize'],label='Predict & Quantize',width=width-0.05,zorder=100)
# plt.bar(x,stats['Huffman'],label='Huffman',width=width-0.05,zorder=100)
# plt.bar(x,stats['Zstd'],label='Zstd',width=width-0.05,zorder=100)
bottom=0


colors = ['mediumturquoise','lightskyblue','steelblue','orange']
j=0
        
for label in length.keys():
    print(label)
    if j == 0:
        plt.bar(x,length[label]/1024/1024,label=label,width=width+0.1,edgecolor='black',hatch='///',lw=0.01,zorder=100,bottom=bottom,color=colors[j])
        matplotlib.rcParams['hatch.linewidth']=0.1
    else:
        plt.bar(x,length[label]/1024/1024,label=label,width=width+0.1,edgecolor='black',lw=0.01,zorder=100,bottom=bottom,color=colors[j])
    bottom = bottom + length[label]/1024/1024
    j = j+1

# c0=plt.bar(x-1.5*width,means[SZ]['1'].values(),yerr=stds[SZ]['1'].values(),width=width-0.06,label='1% SZ',lw=0.02,edgecolor='Black',color='w',ecolor='black',capsize=4,zorder=100)

# c2=plt.bar(x-0.5*width,means[SZ_ADT]['1'].values(),yerr=stds[SZ_ADT]['1'].values(),width=width-0.06,label='1% SZ_ADT',lw=0.01,edgecolor='black',color='#87CEFA',ecolor='black',capsize=4,zorder=100)
# # print(means[SZ]['1'].keys())
# plt.xticks(x,means[SZ]['1'].keys(), rotation=0)
# # plt.ylim([0,ylims[i]])
# c10=plt.bar(x+0.5*width,means[SZ]['5'].values(),yerr=stds[SZ]['5'].values(),width=width-0.06,label='5% SZ',lw=0.02,edgecolor='Black',color='#DCDCDC',ecolor='black',capsize=4,zorder=100)

# c12=plt.bar(x+1.5*width,means[SZ_ADT]['5'].values(),yerr=stds[SZ_ADT]['5'].values(),width=width-0.06,label='5% SZ_ADT',lw=0.01,edgecolor='black',color='#ff9912',ecolor='black',capsize=4,zorder=100)

# c10=plt.bar(x+0.5*width,stat[DTIME_ALL][dataset][HUFFMAN].values(),width=width-0.06,label='decomp-SZ',lw=0.02,edgecolor='Black',color='#DCDCDC',zorder=100)
# # matplotlib.rcParams['hatch.color']=colors[0]
# c12=plt.bar(x+1.5*width,stat[DTIME_ALL][dataset][FSE].values(),width=width-0.06,label='decomp-SZ_ADT',lw=0.01,edgecolor='black',color='#ff9912',zorder=100)
plt.tight_layout()
plt.legend(frameon=True,fontsize=9,loc='upper left',ncol=1,columnspacing=1) #去掉图例边框
plt.bar(x,0,label=label,width=width*3)
picpath = '/home/zhongyu/test/paper_test/motivation/time.png'
plt.savefig(picpath)
picpath_pdf = '/home/zhongyu/test/paper_test/motivation/time.pdf'
plt.savefig(picpath_pdf)
print(picpath_pdf)