import subprocess
import warnings
import sys

import numpy as np

from datetime import datetime

#---------------------------------------------------------------------------------------#
#		Dics and Colors
#---------------------------------------------------------------------------------------#

Dic_Keys 	= {0:'energy',1:'BE2',2:'ME2',3:'rho2E0'}

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#---------------------------------------------------------------------------------------#
#		Read input file
#---------------------------------------------------------------------------------------#

def read_input(self):
	'''Read and parse cbsmodel input file'''

	out_cbs_energies 	= []
	out_cbs_BE2 		= []
	out_cbs_ME2 		= []
	out_cbs_rho2E0 		= []

	cbs_data_file 		= open('%s%s'% (self.input_path,self.input_file))
	lines_cbs_data_file 	= list(cbs_data_file.readlines())

	for num_line,line in enumerate(lines_cbs_data_file):
		
		if len(line) > 1:
			elements_line = line.split()
		
			if elements_line[0] == 'A':
				if self.A != int(elements_line[1]):
					warnings.warn('Mass numbers do not coincide! Using A = %i'% self.A,UserWarning)

			elif elements_line[0] == 'Z':
				if self.Z != int(elements_line[1]):
					warnings.warn('Charge numbers do not coincide! Using Z = %i'% self.Z,UserWarning)

			elif elements_line[0] == 'fit':
				if len(elements_line) < 3:
					raise ValueError('cbsmodel fit command should specify the data file\n \
						and at least one fit parameter!')

				self.name_fit_params 	= elements_line[2:]

				splitted_cbs_file 	= elements_line[1].split('/')
				self.cbs_file 		= splitted_cbs_file[-1]

				if len(splitted_cbs_file) == 1:
					self.cbs_path  	= ''
				else:
					self.cbs_path  	= '/'.join(elements_line[1].split('/')[:-1])+'/'

			elif elements_line[0] == 'energy':
				if len(elements_line) != 3:
					raise ValueError('cbsmodel input for energy not correct in %s!\n \
						Must be `energy L s` not `%s`!'% (self.cbs_file,' '.join(elements_line)))

				out_cbs_energies.append([int(elements_line[1]),int(elements_line[2])])

			elif elements_line[0] == 'BE2':
				if int(elements_line[1]) == 0 and int(elements_line[3]) == 0:
					warnings.warn('No E2 gamma transition between two states with J=0 possible.\n \
						Ignoring the transition %s.'% ' '.join(elements_line),UserWarning)
				else:
					out_cbs_BE2.append([int(elements_line[1]),int(elements_line[2]),
							int(elements_line[3]),int(elements_line[4])])

			elif elements_line[0] == 'ME2':
				if int(elements_line[1]) == 0 and int(elements_line[3]) == 0:
					warnings.warn('No E2 gamma transition between two states with J=0 possible.\n \
						Ignoring the transition %s.'% ' '.join(elements_line),UserWarning)
				else:
					out_cbs_ME2.append([int(elements_line[1]),int(elements_line[2]),
							int(elements_line[3]),int(elements_line[4])])

			elif elements_line[0] == 'rho2E0':
				out_cbs_rho2E0.append([int(elements_line[1]),int(elements_line[2]),
							int(elements_line[3]),int(elements_line[4])])

	return np.array(out_cbs_energies),np.array(out_cbs_BE2),np.array(out_cbs_ME2),np.array(out_cbs_rho2E0)

#---------------------------------------------------------------------------------------#
#		Fit CBS to input data
#---------------------------------------------------------------------------------------#

def cbs_fit_data(self,*args):
	'''Fit CBS to data as indicated in cbsmodel input file'''

	run_string  = 'A %i Z %i '% (self.A,self.Z)
	run_string += 'Wu '
	
	for arg in args:
		run_string += '%s '% arg
	
	run_string += 'fit %s%s %s '% (self.cbs_path,self.cbs_file,' '.join(self.name_fit_params))	
	run_string += 'exit'  

	output_cbs = subprocess.run('cbsmodel %s'% run_string,shell=True,capture_output=True).stdout

	return output_cbs

#---------------------------------------------------------------------------------------#
#		Extract CBS parameters
#---------------------------------------------------------------------------------------#

def extract_params(self):
	'''Extract structural parameters (r_beta etc.) from cbsmodel output'''

	#Perform fits to data with different r_beta until solution is found
	for r_beta in np.arange(0.1,1,0.2):

		output_cbs = cbs_fit_data(self,'rb %s'% r_beta)
		
		if b'Fit successful' in output_cbs:
			self.cbs_fit_success = True
			if self.verbose:
				print('Fit successful!')
			break

		if self.verbose:
			print('Fit with starting value r_beta = %.2f not successful. Continuing...'% r_beta)
	
	else:	
		sys.exit(f'{bcolors.FAIL}Error: Fits in cbsmodel did not converge.{bcolors.ENDC}')

	#Split output by linebreaks
	output_cbs 	= output_cbs.split(b'\n')

	#extract reduced chisquare and fit parameters
	self.red_chi 	= float(output_cbs[16].split(b':')[1])
	self.fit_params = np.zeros((2*len(self.name_fit_params)))

	for i in range(len(self.name_fit_params)):

		string_param = output_cbs[7+i].split(b':')[1].split(b'+-')

		self.fit_params[2*i] 	= float(string_param[0])
		self.fit_params[2*i+1] 	= float(string_param[1])

	return

#---------------------------------------------------------------------------------------#
#		Calculate quantities of interest
#---------------------------------------------------------------------------------------#

def calculate_cbs_quantities(self,in_list,in_keyword):
	'''Use obtained structural parameters to calculate CBS predictions for quantities specified in input file'''

	run_string  = 'A %i Z %i '% (self.A,self.Z)
	run_string += 'Wu simpleoutput '
	
	for num_param,param in enumerate(self.name_fit_params):
		run_string += '%s %.5f '% (param,self.fit_params[2*num_param])

	for num_quantity,quantity in enumerate(in_list):
		if in_keyword == 'energy':
			run_string += '%s %i %i '% (in_keyword,in_list[num_quantity,0],in_list[num_quantity,1])
		elif in_keyword in ['BE2','ME2','rho2E0']:
			run_string += '%s %i %i %i %i '% (in_keyword,in_list[num_quantity,0],in_list[num_quantity,1],
								in_list[num_quantity,2],in_list[num_quantity,3])
		else:
			warning.warn('keyword %s not known in cbsmodel!'% in_keyword,UserWarning)

	run_string += 'exit'

	output_cbs = subprocess.run('cbsmodel %s'% run_string,shell=True,capture_output=True).stdout

	return output_cbs

#---------------------------------------------------------------------------------------#
#		Extract calculated CBS quantities
#---------------------------------------------------------------------------------------#

def extract_cbs_quantities(self,in_output_cbs):
	'''Extract specified qauntities from cbsmodel output'''

	in_output_cbs 	= in_output_cbs.split()

	out_quantities 	= np.array([float(i) for i in in_output_cbs[2:]])

	return out_quantities

#---------------------------------------------------------------------------------------#
#		Write results to output file
#---------------------------------------------------------------------------------------#

def write_output(self):
	'''Write essential output of cbsmodel to file'''

	out_string  = '#############################\n'
	out_string += '#      Results CBSplot      #\n'
	out_string += '#           %i%s           #\n'% (self.A,self.nucl_name)
	out_string += '#    %s    #\n'% datetime.now().strftime('%d-%m-%Y %H:%M:%S')
	out_string += '#############################\n'
	out_string += '\n'

	#CBS parameters
	for num_param,param in enumerate(self.name_fit_params):
		out_string += '%s\t%.5f +/- %.5f\n'% (param,self.fit_params[2*num_param],self.fit_params[2*num_param+1])

	out_string += '\n'

	#extracted quantities
	for num_quantity,quantity in enumerate([self.cbs_energies,self.cbs_BE2,self.cbs_ME2,self.cbs_rho2E0]):
		if isinstance(quantity,np.ndarray):
			for element in quantity:
				#print(element)
				if num_quantity == 0:
					out_string += '%s %i %i %.2f\n'% (Dic_Keys[num_quantity],element[0],
										element[1],element[2])
				else:
					out_string += '%s %i %i %i %i %.2f\n'% (Dic_Keys[num_quantity],element[0],
										element[1],element[2],element[3],element[4])
			out_string += '\n'

	return out_string

#---------------------------------------------------------------------------------------#
#		Main CBS calculations
#---------------------------------------------------------------------------------------#

def main_cbs_calculations(self):
	'''Perform complete CBS calculation as specified in cbsmodel input file'''

	#extract quantities to be calculated
	cbs_energies,cbs_BE2,cbs_ME2,cbs_rho2E0 	= read_input(self)
	
	#perform CBS fit to data and extract parameters (r_beta, etc.)
	extract_params(self)

	for num_quantity,quantity in enumerate([cbs_energies,cbs_BE2,cbs_ME2,cbs_rho2E0]):
		if quantity != []:
			output_cbs_quantities = calculate_cbs_quantities(self,quantity,Dic_Keys[num_quantity])
			
			if num_quantity == 0:
				self.cbs_energies 	= np.zeros((len(cbs_energies),3))
				self.cbs_energies[:,:2]	= cbs_energies
				self.cbs_energies[:,2]	= extract_cbs_quantities(self,output_cbs_quantities)
			elif num_quantity == 1:
				self.cbs_BE2 		= np.zeros((len(cbs_BE2),5))
				self.cbs_BE2[:,:4]	= cbs_BE2
				self.cbs_BE2[:,4]	= extract_cbs_quantities(self,output_cbs_quantities)
			elif num_quantity == 2:
				self.cbs_ME2 		= np.zeros((len(cbs_ME2),5))
				self.cbs_ME2[:,:4]	= cbs_ME2
				self.cbs_ME2[:,4]	= extract_cbs_quantities(self,output_cbs_quantities)
			elif num_quantity == 3:
				self.cbs_rho2E0 	= np.zeros((len(cbs_rho2E0),5))
				self.cbs_rho2E0[:,:4]	= cbs_rho2E0
				self.cbs_rho2E0[:,4]	= extract_cbs_quantities(self,output_cbs_quantities)

	#create output and save/print it if requested
	output = write_output(self)

	if self.write_output:
		out_file = open('%sresults_%i%s.txt'% (self.out_path,self.A,self.nucl_name),'w')
		out_file.write(output)
		out_file.close()
	
	if self.verbose:
		print(output)

	return


