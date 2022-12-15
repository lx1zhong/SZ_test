from cProfile import label
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
import glob2
import os
import math

labels=['Write h5 file','Read h5 file','File Size']
COMPRESS=0
DECOMPRESS=1
SIZE=2

ORIGIN=0
HUFFMAN=1
FSE=2

# [1.033906,0.224876,536875448]
# stats_time=[EB0][HUFFMAN][DECOMPRESS]
# stats_time=[
#     [[4.464538,3.880342,132641664],[4.352146,2.208056,132611613]],
#     [[4.641400,5.885011,188971696],[4.553757,2.093539,188970005]]
# ]


# [6.985760,3.043829,536875448]
# stats_time=[EB0][HUFFMAN][DECOMPRESS]
stats_time=[
    [[6.985760,3.043829,536875448],[8.268137,4.680105,132641664],[7.685800,3.000042,132611613]],
    [[6.985760,3.043829,536875448],[8.650103,7.020755,188971696],[8.434660,3.196634,188970005]]
]


fig = plt.figure(figsize=[6,2.7], dpi=100)
ax = fig.add_subplot(1,2,1)
ax.set_title('(a) EB=1E0' , y=-0.35, fontsize=14)
# if (i-1)%l==0:
# ax.set_ylabel('Compression Ratio')
ax.set_ylabel('Time Cost (s)')
plt.grid(linestyle=':', color="gray",axis='y',zorder=1)
x = np.arange(2) #总共有几组，就设置成几，我们这里有三组，所以设置为3
total_width, n = 0.6, 3    # 有多少个类型，只需更改n即可，比如这里我们对比了四个，那么就把n设成4
width = total_width / n
x = x - (total_width - width) / 2

# plt.xticks(means.keys())
# plt.bar(means.keys(), means.values(),yerr=stds.values(),ecolor='black',capsize=4,zorder=100)
c0=plt.bar(x-1*width,stats_time[0][ORIGIN][:-1],width=width-0.06,label='HDF5',lw=0.02,edgecolor='Black',color='w',zorder=100)

c1=plt.bar(x-0*width,stats_time[0][HUFFMAN][:-1],width=width-0.06,label='HDF5-SZ',lw=0.02,edgecolor='Black',color='#DCDCDC',zorder=100)

c2=plt.bar(x+1*width,stats_time[0][FSE][:-1],width=width-0.06,label='HDF5-SZ_ADT',lw=0.01,edgecolor='black',color='#ff9912',zorder=100)
# print(means[SZ]['1'].keys())
plt.xticks(x,labels[:-1])
plt.ylim([0,10])
# c10=plt.bar(x+0.5*width,stats_time[1][HUFFMAN][:-1],width=width-0.06,label='HDF5-SZ',lw=0.02,edgecolor='Black',color='#DCDCDC',zorder=100)

# c12=plt.bar(x+1.5*width,stats_time[1][FSE][:-1],width=width-0.06,label='HDF5-SZ_ADT',lw=0.01,edgecolor='black',color='#ff9912',zorder=100)

# def to_percent(temp, position):
#   return '%1.0f'%(100*temp) + '%'
# plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))
plt.legend(frameon=True,fontsize=8,loc='upper right',ncol=1,columnspacing=1) #去掉图例边框
    

ax2 = fig.add_subplot(1,2,2)
ax2.set_title('(b) EB=1E-1' , y=-0.35, fontsize=14)
# if (i-1)%l==0:
# ax.set_ylabel('Compression Ratio')
ax2.set_ylabel('Time Cost (s)')
plt.grid(linestyle=':', color="gray",axis='y',zorder=1)
x = np.arange(2) #总共有几组，就设置成几，我们这里有三组，所以设置为3
total_width, n = 0.6, 3    # 有多少个类型，只需更改n即可，比如这里我们对比了四个，那么就把n设成4
width = total_width / n
x = x - (total_width - width) / 2

plt.ylim([0,10])
# plt.xticks(means.keys())
# plt.bar(means.keys(), means.values(),yerr=stds.values(),ecolor='black',capsize=4,zorder=100)
# c0=plt.bar(x-0.5*width,stats_time[0][HUFFMAN][:-1],width=width-0.06,label='HDF5-SZ',lw=0.02,edgecolor='Black',color='#DCDCDC',zorder=100)

# c2=plt.bar(x+0.5*width,stats_time[0][FSE][:-1],width=width-0.06,label='HDF5-SZ_ADT',lw=0.01,edgecolor='black',color='#ff9912',zorder=100)
# print(means[SZ]['1'].keys())
plt.xticks(x,labels[:-1])
# plt.ylim([0,ylims[i]])
c10=plt.bar(x-1*width,stats_time[1][ORIGIN][:-1],width=width-0.06,label='HDF5',lw=0.02,edgecolor='Black',color='w',zorder=100)

c10=plt.bar(x-0*width,stats_time[1][HUFFMAN][:-1],width=width-0.06,label='HDF5-SZ',lw=0.02,edgecolor='Black',color='#DCDCDC',zorder=100)

c12=plt.bar(x+1*width,stats_time[1][FSE][:-1],width=width-0.06,label='HDF5-SZ_ADT',lw=0.01,edgecolor='black',color='#ff9912',zorder=100)

# def to_percent(temp, position):
#   return '%1.0f'%(100*temp) + '%'
# plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))
plt.legend(frameon=True,fontsize=8,loc='upper right',ncol=1,columnspacing=1) #去掉图例边框
ax2.set_ylim(bottom=0)
# plt.tight_layout()
plt.subplots_adjust(left=0.1,right=0.97,bottom=0.3,top=0.96,wspace=0.32,hspace=0.6) 
picpath = '/home/zhongyu/test/paper_test/test4/hdf5.png'
plt.savefig(picpath)
picpath_pdf = '/home/zhongyu/test/paper_test/test4/hdf5.pdf'
plt.savefig(picpath_pdf)
print(picpath_pdf)