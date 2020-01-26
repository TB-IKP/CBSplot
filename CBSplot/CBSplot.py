import warnings

import numpy as np

from .CBS_commands import *
from .plots import *

#---------------------------------------------------------------------------------------#
#		Class
#---------------------------------------------------------------------------------------#

class CBSplot:

	def __init__(self,nucleus=None,input_file=None,exp_data_file=None,out_path='',write_output=False):

		if nucleus == None or len(nucleus) != 3:
			raise ValueError('no nucleus is given. Must be list [name,Z,N], e.g. [`Sm`,62,92] for 154Sm.')
		else:
			if not isinstance(nucleus[0],str):
				raise ValueError('name of nucleus must be given as string, e.g. Sm!')
			else:
				self.nucl_name 	= nucleus[0]

				if not isinstance(nucleus[1],int) or not isinstance(nucleus[2],int):
					raise ValueError('Z and N must be integers!')
				else:
					self.A 	= nucleus[1]+nucleus[2]
					self.Z 	= nucleus[1]

		if not isinstance(input_file,str):
			raise ValueError('input_file contains all CBS commands.\n \
						It must be string pointing to the CBS input file.\n \
						Name must be e.g. input_154Sm.cbs!')
		else:
			self.input_file = input_file.split('/')[-1]
			self.input_path = '/'.join(input_file.split('/')[:-1])

		#if not isinstance(cbs_data_file,str):
		#	raise ValueError('cbs_data_file contains all energies and transition strengths the CBS is adapted to.\n \
		#				It must be string pointing to the CBS input file.\n \
		#				Name must be e.g. cbs_data_154Sm.ET!')
		#else:
		#	self.cbs_file 	= cbs_data_file.split('/')[-1]
		#	self.cbs_path 	= '/'.join(cbs_data_file.split('/')[:-1])

		if not isinstance(exp_data_file,str):
			raise ValueError('exp_data_file contains all energies and transition strengths\n \
						to be plotted in the experimental spectrum.\n \
						It must be string pointing to the CBS input file.\n \
						Name must be e.g. exp_data_154Sm.ET!')
		else:
			self.exp_file 	= exp_data_file.split('/')[-1]
			self.exp_path 	= '/'.join(exp_data_file.split('/')[:-1])

		if not isinstance(out_path,str):
			raise ValueError('out_path must be string')
		else:
			self.out_path	= out_path

		if not isinstance(write_output,bool):
			raise ValueError('write_output must be bool!')
		else:
			self.write_output = write_output

		self.cbs_energies	= None
		self.cbs_BE2		= None
		self.cbs_ME2		= None

	def run(self):
		main_cbs_calculations(self)
		#print(self.cbs_energies)
		#print(self.cbs_BE2)
		#print(self.cbs_ME2)

	def plot(self):
		plot_comparison(self)






