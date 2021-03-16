#  SPDX-License-Identifier: GPL-3.0+
#
# Copyright © 2020 T. Beck.
#
# This file is part of CBSplot.
#
# CBSplot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CBSplot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CBSplot.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
import matplotlib.pyplot as plt

from uncertainties import ufloat

#---------------------------------------------------------------------------------------#
#		General
#---------------------------------------------------------------------------------------#

#Colors

COLOR_LEVEL 		= 'black'
COLOR_E2 		= 'royalblue'
COLOR_RHO2E0 		= 'firebrick'

#Offsets

EN_X_OFF		= 0.3
EN_Y_OFF		= 150

STATE_X_OFF		= 0.05
STATE_Y_OFF		= 150

#Arrows

WIDTH	 		= 5
FONTSIZE 		= 14
OFFSET 			= 0.003

#---------------------------------------------------------------------------------------#
#		Classes
#---------------------------------------------------------------------------------------#

class Level():
	def __init__(self,ax,band,energy,name):
		
		self.ax 	= ax
		self.band 	= band
		#if energy > 25:
		self.energy 	= energy/10**3
		self.offset 	= 10/10**3
		#else:
		#	self.energy 	= energy
		#	self.offset 	= 10
		self.name 	= name
		self.color 	= COLOR_LEVEL

	def plot(self):
		self.ax.set_xlim(0,self.band*5+6)
		self.ax.axis('off')
		self.ax.plot([WIDTH*self.band,WIDTH*self.band+(WIDTH-1)],[self.energy,self.energy],
			linewidth=2,color=self.color,zorder=25)
		self.ax.text(WIDTH*self.band+0.025,self.energy+self.offset,r'%s'% self.name,
			color=self.color,horizontalalignment='left',zorder=25,fontsize=FONTSIZE)
		self.ax.text(WIDTH*self.band+(WIDTH-1.15),self.energy+self.offset,'%.3f'% self.energy,
			color=self.color,horizontalalignment='right',zorder=25,fontsize=FONTSIZE)
		return

class Transition():
	def __init__(self,ax,bands,energies,value,print_val,color):
		self.ax 	= ax
		self.bands 	= bands
		self.energies	= np.array(energies)/10**3
		self.value 	= value
		self.print_val 	= print_val
		self.color 	= color

	def create_string(self):

		if len(self.value)==1:
			out_string = r'$%s$'% (str(self.value[0]))
		elif len(self.value)==2:
			unc_value  = ufloat(self.value[0],self.value[1])
			if self.value[1] > 2 and self.value[1] < 10:
				out_string = '{:.1uS}'.format(unc_value)
			else:
				out_string = '{:.2uS}'.format(unc_value)
			#out_string = r'$%s(%s)$'% (str(self.value[0]),str(self.value[1]))
		elif len(self.value)==3:
			out_string = r'$%s^{%s}_{%s}$'% (str(self.value[0]),str(self.value[1]),str(self.value[2]))

		return out_string

	def plot(self):

		if self.value:
			arrow_width 	= np.max((self.value[0]/20,0.5))
			head_width 	= np.max((1.5*arrow_width,2))
		else:
			arrow_width 	= 0.5
			head_width 	= 2

		if self.bands[0] == self.bands[1]:
			self.ax.annotate('',xy=(WIDTH*self.bands[1]+1.5,self.energies[1]+OFFSET),
				xytext=(WIDTH*self.bands[0]+1.5,self.energies[0]),
				arrowprops=dict(color=self.color,width=arrow_width,headwidth=head_width),fontsize=FONTSIZE)
			if self.value and self.print_val:
				string = self.create_string()
				self.ax.text(WIDTH*self.bands[1]+1.5,(1-0.55)*min(self.energies[0],self.energies[1])+0.55*max(self.energies[0],self.energies[1]),
					string,ha='center',va='center',bbox=dict(color='white',alpha=0.85,pad=0.5),zorder=10,fontsize=0.75*FONTSIZE)
		
		elif self.bands[0]+1 == self.bands[1]:
			self.ax.annotate('',xy=(WIDTH*self.bands[1],self.energies[1]),
				xytext=(WIDTH*self.bands[0]+(WIDTH-1),self.energies[0]),
				arrowprops=dict(color=self.color,width=arrow_width,headwidth=head_width))
			if self.value and self.print_val:
				string = self.create_string()
				self.ax.text(0.5*(WIDTH*self.bands[0]+(WIDTH-1)+WIDTH*self.bands[1]),0.5*(self.energies[0]+self.energies[1]),
					string,ha='center',va='center',bbox=dict(color='white',alpha=0.85,pad=0.5),zorder=10,fontsize=0.75*FONTSIZE)
		
		elif self.bands[0] == self.bands[1]+1:
			self.ax.annotate('',xy=(WIDTH*self.bands[1]+(WIDTH-1),self.energies[1]),
				xytext=(WIDTH*self.bands[0],self.energies[0]),
				arrowprops=dict(color=self.color,width=arrow_width,headwidth=head_width))
			if self.value and self.print_val:
				string = self.create_string()
				self.ax.text(0.5*(WIDTH*self.bands[0]+WIDTH*self.bands[1]+(WIDTH-1)),0.5*(self.energies[0]+self.energies[1]),
					string,ha='center',va='center',bbox=dict(color='white',alpha=0.85,pad=0.5),zorder=10,fontsize=0.75*FONTSIZE)

		elif self.bands[0]+1 < self.bands[1]:
			print('Not included yet.')

		elif self.bands[0] > self.bands[1]+1:
			#extend level first
			plt.plot([WIDTH*self.bands[1]+(WIDTH-1),WIDTH*(self.bands[0]-1)+2.5],[self.energies[1],self.energies[1]],
				linestyle='--',color='grey')
			self.ax.annotate('',xy=(WIDTH*(self.bands[0]-1)+2.5,self.energies[1]),
				xytext=(WIDTH*self.bands[0],self.energies[0]),
				arrowprops=dict(color=self.color,width=arrow_width,headwidth=head_width))
			if self.value and self.print_val:
				string = self.create_string()
				self.ax.text(0.5*(WIDTH*self.bands[0]+WIDTH*(self.bands[0]-1)+2.5),0.5*(self.energies[0]+self.energies[1]),
					string,ha='center',va='center',bbox=dict(color='white',alpha=0.85,pad=0.5),zorder=10,fontsize=0.75*FONTSIZE)

#---------------------------------------------------------------------------------------#
#		Load data experiment
#---------------------------------------------------------------------------------------#

def load_experiment(self):
	'''Load experimental values as specified in exp_data_file'''

	out_exp_energies 	= []
	out_exp_BE2 		= []
	out_exp_rho2E0 		= []

	exp_data_file 		= open('%s%s'% (self.exp_path,self.exp_file))
	lines_exp_data_file 	= list(exp_data_file.readlines())
	exp_data_file.close()

	for num_line,line in enumerate(lines_exp_data_file):
		if len(line) > 1:
			elements_line = line.split()

			if elements_line[0] == 'E':
				#if len(elements_line) != 5:
				#	raise ValueError('experimental input for energy not correct in %s!\n \
				#		Must be `E L s val delta_val` not `%s`!'% (self.exp_file,' '.join(elements_line)))
				
				out_exp_energies.append([int(elements_line[1]),int(elements_line[2]),
							float(elements_line[3]),float(elements_line[4])])

			elif elements_line[0] == 'T':
				#if len(elements_line) != 7:
				#	raise ValueError('experimental input for energy not correct in %s!\n \
				#		Must be `T L1 s1 L2 s2 val delta_val` not `%s`!'% (self.exp_file,' '.join(elements_line)))

				if int(elements_line[1]) == 0 and int(elements_line[3]) == 0:
					out_exp_rho2E0.append([int(elements_line[1]),int(elements_line[2]),
							int(elements_line[3]),int(elements_line[4]),
							float(elements_line[5]),float(elements_line[6])])
				else:
					out_exp_BE2.append([int(elements_line[1]),int(elements_line[2]),
							int(elements_line[3]),int(elements_line[4]),
							float(elements_line[5]),float(elements_line[6])])

	return np.array(out_exp_energies),np.array(out_exp_BE2),np.array(out_exp_rho2E0)

#---------------------------------------------------------------------------------------#
#		Plot comparison
#---------------------------------------------------------------------------------------#

def plot_comparison(self):
	'''Plot experimental data alongside CBS predictions for comparison'''

	fig,ax = plt.subplots(1,2,figsize=(12,10))

	#----- Experiment -----#

	self.exp_energies,self.exp_BE2,self.exp_rho2E0 = load_experiment(self)

	if self.exp_energies != []:
		for state in self.exp_energies:
			Level(ax[0],int(state[1]),state[2],'$%i^+$'% state[0]).plot()

	#dummy state to ensure correct width of plot
	#Level(ax[0],1,-1e5,'').plot()

	if self.exp_BE2 != []:
		for transition in self.exp_BE2:

			energy_start = self.exp_energies[(self.exp_energies[:,0:2]==(transition[0],transition[1])).all(axis=1).nonzero()][0,2]
			energy_stop  = self.exp_energies[(self.exp_energies[:,0:2]==(transition[2],transition[3])).all(axis=1).nonzero()][0,2]

			Transition(ax[0],[transition[1],transition[3]],[energy_start,energy_stop],[transition[4],transition[5]],True,COLOR_E2).plot()

	if self.exp_rho2E0 != []:
		for transition in self.exp_rho2E0:

			energy_start = self.exp_energies[(self.exp_energies[:,0:2]==(transition[0],transition[1])).all(axis=1).nonzero()][0,2]
			energy_stop  = self.exp_energies[(self.exp_energies[:,0:2]==(transition[2],transition[3])).all(axis=1).nonzero()][0,2]

			Transition(ax[0],[transition[1],transition[3]],[energy_start,energy_stop],[transition[4],transition[5]],True,COLOR_RHO2E0).plot()

	#----- CBS -----#

	if self.cbs_energies != []:
		for state in self.cbs_energies:

			Level(ax[1],int(state[1]),state[2],'$%i^+$'% state[0]).plot()

	if self.cbs_BE2 != []:
		for transition in self.cbs_BE2:

			energy_start = self.cbs_energies[(self.cbs_energies[:,0:2]==(transition[0],transition[1])).all(axis=1).nonzero()][0,2]
			energy_stop  = self.cbs_energies[(self.cbs_energies[:,0:2]==(transition[2],transition[3])).all(axis=1).nonzero()][0,2]

			Transition(ax[1],[transition[1],transition[3]],[energy_start,energy_stop],[int(transition[4])],True,COLOR_E2).plot()

	if self.cbs_rho2E0 != []:
		for transition in self.cbs_rho2E0:

			energy_start = self.cbs_energies[(self.cbs_energies[:,0:2]==(transition[0],transition[1])).all(axis=1).nonzero()][0,2]
			energy_stop  = self.cbs_energies[(self.cbs_energies[:,0:2]==(transition[2],transition[3])).all(axis=1).nonzero()][0,2]

			Transition(ax[1],[transition[1],transition[3]],[energy_start,energy_stop],[int(transition[4])],True,COLOR_RHO2E0).plot()

	#----- labels -----#

	#labels grund-state band
	ax[0].text(0.5*(WIDTH-1),-0.075,r'$K^{\pi}=0^+$',ha='center',va='center',fontsize=FONTSIZE)
	ax[1].text(0.5*(WIDTH-1),-0.075,r'$K^{\pi}=0^+$',ha='center',va='center',fontsize=FONTSIZE)

	#label beta band only if its states are plotted
	if np.sum(self.exp_energies[:,1]) > 0:
		ax[0].text(0.5*(3*WIDTH-1),np.min(self.exp_energies[:,2][self.exp_energies[:,1]==1])/10**3-0.075,
			r'$K^{\pi}=0^+$',ha='center',va='center',fontsize=FONTSIZE)

	if np.sum(self.cbs_energies[:,1]) > 0:
		ax[1].text(0.5*(3*WIDTH-1),np.min(self.cbs_energies[:,2][self.cbs_energies[:,1]==1])/10**3-0.075,
			r'$K^{\pi}=0^+$',ha='center',va='center',fontsize=FONTSIZE)

	#find value of r_beta
	val_rb 			= self.fit_params[2*self.name_fit_params.index('rb')]
	title_string_cbs 	= 'CBS '+r'($r_{\beta}=%.2f$)'% val_rb +'\n'

	#figure title
	fig.suptitle(r'$^{%i}$%s'% (self.A,self.nucl_name),fontsize=2*FONTSIZE)
	ax[0].set_title('Experiment\n',fontsize=1.5*FONTSIZE)
	ax[1].set_title(title_string_cbs,fontsize=1.5*FONTSIZE)

	#----- limits -----#

	#ax[0].set_xlim(0,1*5+6)
	#ax[1].set_xlim(0,1*5+6)

	max_energy = np.max(np.concatenate((self.exp_energies[:,2],self.cbs_energies[:,2])))/10**3

	ax[0].set_ylim(-0.1,max_energy+0.1)
	ax[1].set_ylim(-0.1,max_energy+0.1)

	#----- other stuff -----#

	plt.savefig('%slevelscheme_%i%s.pdf'% (self.out_path,self.A,self.nucl_name))

	return





