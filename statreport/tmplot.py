#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from mpl_toolkits.axes_grid1 import make_axes_locatable

def griddata(x,y,T):
	z=[]
	for j in range(0,len(y)):
		z.append([])
		for i in range(0, len(x)):
			z[j].append(T[int(x[i])][int(y[j])])

	return np.array(z)

def tmplot(time0,data,cfg):
	print "Plotting into " + cfg['TMplot']['img_dir'] + "tm-"+time0.strftime("%Y_%m_%d_%H_%M")+".png ... ",
	T = []
	#Temperature[Shelf #][Layer #]
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
		T_avg = float(T_sum) / n
		T_sum = 0
		n = 0
		i += 1
		if ( i - 1 ) % int(cfg['Physics']['layers']) == 0:
			T.append([])
		T[(i-1)/int(cfg['Physics']['layers'])].append(T_avg)



	grid_x = np.arange(0,int(cfg['Physics']['shelves']),int(cfg['Physics']['shelves'])/100.0)
	grid_y = np.arange(0,int(cfg['Physics']['layers']),int(cfg['Physics']['layers'])/100.0)
	grid_z = griddata(grid_x,grid_y,T)
	extent = (0 , int(cfg['Physics']['shelves']) , 0 , int(cfg['Physics']['layers']))
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


	gci=plt.imshow(grid_z, extent=extent, origin='lower',cmap=cmap, norm=norm)
	ax=plt.gca()
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

