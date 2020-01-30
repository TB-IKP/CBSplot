'''Plotting routine for the program cbsmodel'''

import warnings

import numpy as np

from .CBS_commands import *
from .plots import *

#---------------------------------------------------------------------------------------#
#		Class
#---------------------------------------------------------------------------------------#

class CBSplot:
	'''Class for CBS calculations and subsequent plotting. 
	
	Arguments:
	----------
	nucleus: list
		information on nucleus to be calculated; [abbreviated name,Z,N]
	input_file: string
		CBS input file containing all CBS commands
	exp_data_file: string
		experimental data solely for plotting, not for CBS fit
	out_path: string
		location where output is stored
	write_output: bool
		True if summary of CBS output shall be written to file
	verbose: bool
		Status output is plotted if True. 
		If set to False a successful run will not produce any output.

	Note:
	-----
	CBSplot entirely uses the cbsmodel syntax. 
	cbsmodel is a program by Michael Reese and is available at https://sourceforge.net/projects/cbsmodel/
	See the included documentation for more information.
	'''

	def __init__(self,nucleus=None,input_file=None,exp_data_file=None,out_path='',write_output=False,verbose=True):

		if nucleus == None or len(nucleus) != 3:
			raise ValueError('no nucleus is given. Must be list [abbreviated name,Z,N], e.g. [`Sm`,62,92] for 154Sm.')
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
			raise ValueError('input_file must be string pointing to the CBS input file.\n \
						This file must contain all CBS commands.')
		else:
			splitted_input_file 	= input_file.split('/')
			self.input_file 	= splitted_input_file[-1]

			if len(splitted_input_file) == 1:
				self.input_path = ''
			else:
				self.input_path = '/'.join(splitted_input_file[:-1])+'/'

		if not isinstance(out_path,str):
			raise ValueError('out_path must be string.\n \
						It defines the location where the final levelscheme and (if requested) output file are stored.')
		else:
			self.out_path	= out_path

		if not isinstance(write_output,bool):
			raise ValueError('write_output must be bool!')
		else:
			self.write_output = write_output

		#already set exp_data_file which will be checked later on in self.run()
		self.exp_data_file 	= exp_data_file

		self.cbs_energies	= []
		self.cbs_BE2		= []
		self.cbs_ME2		= []
		self.cbs_rho2E0		= []

		#Check whether CBS calculation has been performed. Substitute with success message at later stage. 
		self.cbs_fit_success 	= False

		self.verbose 		= verbose

	def run(self):
		'''Run the requested calculations in cbsmodel'''
		main_cbs_calculations(self)

	def plot(self):
		'''Plot experimental values alongside results of the CBS calculation'''

		if not isinstance(self.exp_data_file,str):
			raise ValueError('exp_data_file must be string pointing to a data file.\n \
			 			This file contains all energies and transition strengths\n \
						to be plotted in the experimental spectrum.')
		else:
			splitted_exp_data_file 	= self.exp_data_file.split('/')
			self.exp_file 		= splitted_exp_data_file[-1]

			if len(splitted_exp_data_file) == 1:
				self.exp_path 	= ''
			else:
				self.exp_path 	= '/'.join(splitted_exp_data_file[:-1])+'/'

		if not self.cbs_fit_success:
			raise ValueError('No CBS calculation available.\n \
				Either .run() was not invoked before .plot()\n \
				or the fit of cbsmodel was not successful!')

		plot_comparison(self)






