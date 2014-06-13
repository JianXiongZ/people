#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg',warn=False)
from mpl_toolkits.axes_grid1 import make_axes_locatable

def tmplot(time0,data,cfg):
	print "Plotting into " + cfg['TMplot']['img_dir'] + "tm-"+time0.strftime("%Y_%m_%d_%H_%M")+".png ... ",
	T = []
	#Temperature[Layer #][Shelf #]

	i = 0
	n = 0
	T_sum = 0
	for miner_stat in data:
		for dev_stat in miner_stat[4]:
			for T_single in dev_stat[4]:
				T_single = int(T_single)
				if T_single > 0 and T_single<255 :
					T_sum += T_single
					n += 1
		T_avg = float(T_sum) / n if len(miner_stat[4]) != 0 else 256
		T_sum = 0
		n = 0
		if i < int(cfg['Physics']['layers']):
			T.append([])
		T[i % int(cfg['Physics']['layers'])].append(T_avg)
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

	ax=plt.gca()
	gci = ax.pcolormesh(T, cmap=cmap, norm = norm, edgecolors='white', linewidths=0)
	ax.patch.set_hatch('/')

	ax.set_xticks(np.linspace(0.5,int(cfg['Physics']['shelves'])-0.5,int(cfg['Physics']['shelves'])))
	xl=[]
	for i in range(1,int(cfg['Physics']['shelves'])+1): xl.append(str(i))
	yl=[]
	for i in range(1,int(cfg['Physics']['layers'])+1): yl.append(str(i))
	ax.set_xticklabels(tuple(xl))
	ax.set_yticks(np.linspace(0.5,int(cfg['Physics']['layers'])-0.5,int(cfg['Physics']['layers'])))
	ax.set_yticklabels(tuple(yl))
	ax.set_title(cfg['TMplot']['title'],fontdict=titlefont)
	for label in ax.get_xticklabels() :
		label.set_fontproperties(ticks_font)
	for label in ax.get_yticklabels() :
		label.set_fontproperties(ticks_font)
	ax.set_xlabel("Shelves",fontdict=labelfont)
	ax.set_ylabel("Layers",fontdict=labelfont)
	ax.tick_params(tick1On = False, tick2On = False)

	divider = make_axes_locatable(ax)
	cax = divider.append_axes("right", size="5%", pad=0.05)
	cbar = plt.colorbar(gci,cax=cax)
	cbar.set_label('Temperature ($^{\circ}C$)',fontdict=labelfont)
	cbar.set_ticks(np.linspace(50,80,4))
	cbar.set_ticklabels( ('50', '60', '70', '80'))
	for tick in cbar.ax.yaxis.majorTicks:
		    tick.label2.set_fontproperties(ticks_font)
	plt.tight_layout()

	plt.savefig(cfg['TMplot']['img_dir'] + "tm-"+time0.strftime("%Y_%m_%d_%H_%M")+".png")
	plt.clf()
	print "Done."
	return "tm-"+time0.strftime("%Y_%m_%d_%H_%M")+".png"

