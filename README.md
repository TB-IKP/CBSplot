# CBSplot

This [python](https://www.python.org/) library can be used to perform calculations 
in the framework of the Confined β-soft (CBS) Rotor Model [[1]](#Pie04a)
and provide levelschemes for the comparison to experimental data.
It is based on the program `cbsmodel` [[2]](#Ree16a) by M. Reese and
basically shares its syntax.

## Dependencies

* cbsmodel [[2]](#Ree16a)
* python (> 3.6)
* numpy
* matplotlib
* uncertainties

## Install

`CBSplot` can be obtained by cloning this repository to the local system and running

```
pip3 install CBSplot/
```

in the command line.

## Usage

An introduction to the syntax of `cbsmodel` is given in its manual [[2]](#Ree16a).
The library `CBSplot` requires the following three text files:

* `input_file` containing all `cbsmodel` commands,
* the CBS data file containing all levels and transitions the CBS is adapted to, and
* `exp_data_file` containing all levels and transitions to be plotted in the experimental level scheme.

The first two files are known from traditional calculations using `cbsmodel` 
and do not need to be rewritten for usage with `CBSplot`.
The last file uses the same syntax as the CBS data file.

In order to apply `CBSplot` to the nucleus <sup>154</sup>Sm, the following code can be used:

```
import CBSplot as cbs

cbs_154Sm = cbs.CBSplot(nucleus=['Sm',62,92],
			input_file=input_file.cbs,
			exp_data_file=exp_data_file.ET,
			out_path='~/my/CBS/calculations',
			write_output=True)
						
cbs_154Sm.run()
cbs_154Sm.plot()
```

The methods `run()` and `plot()` perform the CBS calculations and plot the results, respectively.
If `write_output` is `True`, the CBS parameters and all calculated quantities are stored in 
the output file `results_154Sm.txt` and stored in the directory specified by `out_path`.
If the output quantities have to be further processed, they can be obtained by

```
cbs_154Sm.cbs_energies
cbs_154Sm.cbs_BE2
cbs_154Sm.cbs_ME2
cbs_154Sm.cbs_rho2E0
```

Similarly, the experimental values, which are used for the creation of the levelscheme,
can be accessed via

```
cbs_154Sm.exp_energies
cbs_154Sm.exp_BE2
cbs_154Sm.exp_rho2E0
```

Finally, the set of CBS parameters (rb, Bbm2, bmax, etc.) 
and the reduced chisquare of the fit can be obtained from

```
cbs_154Sm.fit_params
cbs_154Sm.red_chi
```

A minimal example can be found in the [example](example) directory.

## References

<a name='Pie04a'>[1]</a> N. Pietralla and O.M. Gorbachenko, Phys. Rev. C **70**, 011304(R) (2004). [`doi:10.1103/PhysRevC.70.011304`](https://doi.org/10.1103/PhysRevC.70.011304).  
<a name='Ree16a'>[2]</a> M. Reese (2008), [`cbsmodel`](https://sourceforge.net/projects/cbsmodel/).  
