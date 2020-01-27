import subprocess
import warnings

import numpy as np

from datetime import datetime

#---------------------------------------------------------------------------------------#
#		Dic Keys
#---------------------------------------------------------------------------------------#

Dic_Keys = {0:'energy',1:'BE2',2:'ME2',3:'rho2E0'}

#---------------------------------------------------------------------------------------#
#		Read input file
#---------------------------------------------------------------------------------------#

def read_input(self):

	out_cbs_energies 	= []
	out_cbs_BE2 		= []
	out_cbs_ME2 		= []
	out_cbs_rho2E0 		= []

	cbs_data_file 		= open('%s/%s'% (self.input_path,self.input_file))
	lines_cbs_data_file 	= list(cbs_data_file.readlines())
	cbs_data_file.close()

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
				self.name_fit_params 	= elements_line[2:]
				self.cbs_file 		= elements_line[1].split('/')[-1]
				self.cbs_path  		= '/'.join(elements_line[1].split('/')[:-1])

			elif elements_line[0] == 'energy':
				out_cbs_energies.append([int(elements_line[1]),int(elements_line[2])])

			elif elements_line[0] == 'BE2':
				out_cbs_BE2.append([int(elements_line[1]),int(elements_line[2]),
							int(elements_line[3]),int(elements_line[4])])

			elif elements_line[0] == 'ME2':
				out_cbs_ME2.append([int(elements_line[1]),int(elements_line[2]),
							int(elements_line[3]),int(elements_line[4])])

			elif elements_line[0] == 'rho2E0':
				out_cbs_rho2E0.append([int(elements_line[1]),int(elements_line[2]),
							int(elements_line[3]),int(elements_line[4])])

	return np.array(out_cbs_energies),np.array(out_cbs_BE2),np.array(out_cbs_ME2),np.array(out_cbs_rho2E0)

#---------------------------------------------------------------------------------------#
#		Fit CBS to input data
#---------------------------------------------------------------------------------------#

def cbs_fit_data(self):

	run_string  = 'A %i Z %i '% (self.A,self.Z)
	run_string += 'Wu simpleoutput '
	run_string += 'fit %s/%s %s '% (self.cbs_path,self.cbs_file,' '.join(self.name_fit_params))
	run_string += 'exit'  

	output_cbs = subprocess.run('cbsmodel %s'% run_string,shell=True,capture_output=True).stdout

	return output_cbs

#---------------------------------------------------------------------------------------#
#		Extract CBS parameters
#---------------------------------------------------------------------------------------#

def extract_params(self,in_output_cbs):

	in_output_cbs 	= in_output_cbs.split()

	self.red_chi 	= float(in_output_cbs[3])
	self.fit_params = np.zeros((2*len(self.name_fit_params)))

	for i in range(len(self.name_fit_params)):
		self.fit_params[2*i] 	= float(in_output_cbs[5+3*i])
		self.fit_params[2*i+1] 	= float(in_output_cbs[5+3*i+1])

	return

#---------------------------------------------------------------------------------------#
#		Calculate quantities of interest
#---------------------------------------------------------------------------------------#

def calculate_cbs_quantities(self,in_list,in_keyword):

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

	in_output_cbs 	= in_output_cbs.split()

	out_quantities 	= np.array([float(i) for i in in_output_cbs[2:]])

	return out_quantities

#---------------------------------------------------------------------------------------#
#		Write results to output file
#---------------------------------------------------------------------------------------#

def write_output(self):

	out_string  = '#############################\n'
	out_string += '#      Results CBSplot      #\n'
	out_string += '#           %i%s           #\n'% (self.A,self.nucl_name)
	out_string += '#    %s    #\n'% datetime.now().strftime('%d-%m-%Y %H:%M:%S')
	out_string += '#############################\n'
	out_string += '\n'

	for num_param,param in enumerate(self.name_fit_params):
		out_string += '%s\t%.4f +/- %.4f\n'% (param,self.fit_params[2*num_param],self.fit_params[2*num_param+1])

	out_file = open('%s/results_%i%s.txt'% (self.out_path,self.A,self.nucl_name),'w')
	out_file.write(out_string)
	out_file.close()

	return

#---------------------------------------------------------------------------------------#
#		Main CBS calculations
#---------------------------------------------------------------------------------------#

def main_cbs_calculations(self):

	cbs_energies,cbs_BE2,cbs_ME2,cbs_rho2E0 	= read_input(self)
	output_cbs_params 				= cbs_fit_data(self)

	extract_params(self,output_cbs_params)

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

	if self.write_output:
		 write_output(self)

	return


