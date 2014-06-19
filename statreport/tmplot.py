#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg',warn=False)
from mpl_toolkits.axes_grid1 import make_axes_locatable

def tmplot(time0,data,cfg):
	print "Plotting into " + cfg['TMplot']['img_dir'] + "tm-"+time0.strftime("%Y_%m_%d_%H_%M")+".png ... ",

	T = [[] for i in range(0,int(cfg['Physics']['layers']))]
	#Temperature[Layer # -1][Shelf # -1]

	i = 0
	n = 0
	T_sum = 0
	T_err = []
	for miner_stat in data:
		for dev_stat in miner_stat[4]:
			for T_single in dev_stat[4]:
				T_single = int(T_single)
				if T_single > 0 and T_single<255 :
					T_sum += T_single
					n += 1
		if n != 0 :
			T_avg = float(T_sum) / n
		else:
			T_avg = 256
			T_err.append([int(cfg['Physics']['layers']) - 1 - i % int(cfg['Physics']['layers']), i / int(cfg['Physics']['layers'])])
		T_sum = 0
		n = 0

		T[int(cfg['Physics']['layers']) - 1 - i % int(cfg['Physics']['layers'])].append(T_avg)
		i += 1
	T = np.ma.masked_greater(T, 255.5)
	cmap = matplotlib.cm.jet
	norm = matplotlib.colors.Normalize(vmin=50, vmax=80)

	fig = plt.figure(figsize=(float(cfg['TMplot']['width'])/float(cfg['TMplot']['dpi']),float(cfg['TMplot']['height'])/float(cfg['TMplot']['dpi'])), dpi=int(cfg['TMplot']['dpi']), facecolor="white")
	titlefont = {'family' : cfg['TMplot']['font_family1'],
		'weight' : 'normal',
		'size'   : int(cfg['TMplot']['font_size1']),
		}
	labelfont = {'family' : cfg['TMplot']['font_family2'],
		'weight' : 'normal',
		'size'   : int(cfg['TMplot']['font_size2']),
		}
	ticks_font = matplotlib.font_manager.FontProperties(family=cfg['TMplot']['font_family3'], style='normal', size=int(cfg['TMplot']['font_size3']), weight='normal', stretch='normal')

	for j in range(0,(int(cfg['Physics']['shelves'])+int(cfg['TMplot']['x_split'])-1)/int(cfg['TMplot']['x_split'])):
		ax=plt.subplot((int(cfg['Physics']['shelves'])+int(cfg['TMplot']['x_split'])-1)/int(cfg['TMplot']['x_split']), 1 , j+1)
		if j==0:
			ax.set_title(cfg['TMplot']['title'],fontdict=titlefont)
		gci = ax.pcolormesh(T, cmap=cmap, norm = norm, edgecolors='white', linewidths=0)
		for p in T_err:
			ax.add_patch(matplotlib.patches.Rectangle((p[1],p[0]),1,1,facecolor='none',edgecolor='r',hatch = '/'))

		for i in range(j*int(cfg['TMplot']['x_split'])*int(cfg['Physics']['layers']),(j+1)*int(cfg['TMplot']['x_split'])*int(cfg['Physics']['layers'])):
			try:
				miner = data[i]
			except IndexError:
				break
			sum_mod_num = 0
			for dev_stat in miner[4]:
				sum_mod_num += int(dev_stat[3])
			ax.text(i/int(cfg['Physics']['layers']) + .5 , int(cfg['Physics']['layers']) - .5 - i % int(cfg['Physics']['layers']),str(sum_mod_num)+'/'+cfg['Miner']['module_number'],ha='center',va='center',fontproperties=ticks_font,color='k')

		ax.set_xticks(np.linspace(0.5, int(cfg['Physics']['shelves']) - 0.5, int(cfg['Physics']['shelves'])))
		xl=[]
		for i in range(1, int(cfg['Physics']['shelves'])+1): xl.append(str(i))
		yl=[]
		for i in range(1, int(cfg['Physics']['layers'])+1): yl.append(str(i))
		ax.set_xticklabels(tuple(xl))
		ax.set_yticks(np.linspace(0.5,int(cfg['Physics']['layers'])-0.5,int(cfg['Physics']['layers'])))
		ax.set_yticklabels(tuple(yl))
		for label in ax.get_xticklabels() :
			label.set_fontproperties(ticks_font)
		for label in ax.get_yticklabels() :
			label.set_fontproperties(ticks_font)
		ax.set_ylabel("Layers",fontdict=labelfont)
		ax.tick_params(tick1On = False, tick2On = False)
		ax.set_xlim(j * int(cfg['TMplot']['x_split']), (j + 1) * int(cfg['TMplot']['x_split']))
		ax.set_ylim(0,5)

		divider = make_axes_locatable(ax)
		cax = divider.append_axes("right", size="5%", pad=0.05)
		cbar = plt.colorbar(gci,cax=cax)
		cbar.set_label('Temperature ($^{\circ}C$)',fontdict=labelfont)
		cbar.set_ticks(np.linspace(50,80,4))
		cbar.set_ticklabels( ('50', '60', '70', '80'))
		for tick in cbar.ax.yaxis.majorTicks:
			tick.label2.set_fontproperties(ticks_font)

	ax.set_xlabel("Shelves",fontdict=labelfont)
	plt.tight_layout()

	plt.savefig(cfg['TMplot']['img_dir'] + "tm-"+time0.strftime("%Y_%m_%d_%H_%M")+".png")
	plt.clf()
	print "Done."
	return "tm-"+time0.strftime("%Y_%m_%d_%H_%M")+".png"

